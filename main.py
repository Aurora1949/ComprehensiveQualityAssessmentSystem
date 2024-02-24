#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/02/15
#  Last Modified on 2024/02/15 07:53:13
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
from datetime import timedelta
from typing import Union, Optional

import aiofile
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, add_pagination
from school_api import SchoolClient
from school_api.client.utils import LoginFail
from school_api.exceptions import ScoreException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import StreamingResponse

from database import crud
from database.crud import create_new_comprehensive, get_all_comprehensive, get_current_comprehensive, \
    set_current_comprehensive_db
from database.utils import get_db, init_db
from models.user import User
from schemas.auth import IToken
from schemas.comprehensive import IComprehensive, ICurrentComprehensive, IChangeComprehensive, \
    IComprehensiveFormTemplate, IComprehensiveSaveData, IComprehensiveDataItem, IComprehensiveDistribute, \
    IComprehensiveJob
from schemas.upload import IUploadFile, IUploadFileResponse
from schemas.user import IUserCreate, IUser, IJWXTAccount, IJWXTUserResponse, CourseData, \
    IUserComprehensiveStatusWithClassName
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_admin_user, \
    get_current_super_admin_user, SECRET_KEY, get_current_active_user
from utils.decorator import record_fatal_error
from utils.excel import get_student_from_upload_excel
from utils.functions import is_uid_valid, is_user_exists, hashed_string, write_file_to_disk, get_file_md5, \
    get_media_type, guess_extension
from utils.uxml import parse_xml

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
)

school = SchoolClient("http://jwxt2.jit.edu.cn/")


@app.on_event("startup")
async def runtime_init_db():
    await init_db()


@app.post('/register')
@record_fatal_error
async def register_new_user(user: IUserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)


@app.post("/token", response_model=IToken)
@record_fatal_error
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_account_password(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户名或密码",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.account}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/admin/create_user/excel")
@record_fatal_error
async def create_user_by_excel(file: UploadFile, _: User = Depends(get_current_admin_user),
                               db: AsyncSession = Depends(get_db)):
    error_list = []
    for user in get_student_from_upload_excel(file):
        if not is_uid_valid(user.account):
            error_list.append({
                "name": user.name,
                "detail": f"uid {user.account} not match pattern."
            })
            continue

        if await is_user_exists(user.account, db):
            error_list.append({
                "name": user.name,
                "detail": f"uid {user.account} has already exist."
            })
            continue

        await crud.create_user_by_xlsx(db, user)
    return {
        "msg": "success",
        "err": {
            "num": len(error_list),
            "data": error_list
        }
    }


@app.get("/user/me", response_model=IUser)
async def read_user_info(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    """
    bug fix see: https://stackoverflow.com/questions/74252768/missinggreenlet-greenlet-spawn-has-not-been-called
    :param current_user:
    :param db:
    :return:
    """
    return await crud.get_user_by_account(db, current_user.account)


@app.post("/admin/set_admin")
async def set_admin(uid: str,
                    set_type: bool,
                    admin_type: int = 1,
                    _: User = Depends(get_current_super_admin_user),
                    db: AsyncSession = Depends(get_db)):
    uid_list = uid.split(';')
    if set_type:
        return await crud.set_user_admin(db, uid_list, admin_type)
    return await crud.unset_user_admin(db, uid_list)


@app.get("/admin/get/userList", response_model=Page[IUser])
async def get_user_list(class_name: str = "", base_user_level: int = 0,
                        _=Depends(get_current_super_admin_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_user_list_by_(db, class_name, base_user_level)


@app.get("/admin/user/resetPasswd")
async def reset_password(uid: str, _=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.reset_passwd(db, uid)
    return {"msg": "密码重置成功"}


@app.post("/admin/user/modify")
async def modify_user_info(user: IUser, _=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.update_user_info(db, user)
    return {"msg": "修改成功"}


@app.post("/admin/user/create")
async def create_user(user: IUser, _=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.create_user(db, user)
    return {"msg": "成功"}


@app.post("/admin/comprehensive/create")
async def create_comprehensive(comprehensive: IComprehensive, _=Depends(get_current_super_admin_user),
                               db=Depends(get_db)):
    await create_new_comprehensive(db, comprehensive)
    return {"msg": "成功"}


@app.get("/admin/comprehensive/queryAll", response_model=list[IComprehensive])
async def query_all_comprehensive(_=Depends(get_current_admin_user), db=Depends(get_db)):
    return await get_all_comprehensive(db)


@app.post("/admin/comprehensive/setCurrent")
async def set_current_comprehensive(semester: IChangeComprehensive, _=Depends(get_current_admin_user),
                                    db=Depends(get_db)):
    await set_current_comprehensive_db(db, semester=semester.semester)


@app.get("/user/comprehensive/query", response_model=Union[ICurrentComprehensive, None])
async def query_current_comprehensive(db=Depends(get_db)):
    return await get_current_comprehensive(db)


@app.get("/user/comprehensive/getForm", response_model=list[IComprehensiveFormTemplate])
async def get_comprehensive_form(_=Depends(get_current_active_user)):
    return parse_xml('./config/xlsx_format_xml.xml')


@app.post("/user/comprehensive/save")
async def save_comprehensive(data: IComprehensiveSaveData, auth: User = Depends(get_current_active_user),
                             db: AsyncSession = Depends(get_db)):
    if not auth.extend.uid:
        raise HTTPException(status_code=400, detail="此用户不支持该操作")
    uid = auth.account
    semester = data.semester
    is_save = await crud.get_user_comprehensive_status(db, uid, semester)
    if is_save:
        raise HTTPException(status_code=400, detail="已填报，不可修改")
    await crud.save_comprehensive_data(db, semester, uid, data)
    if not data.draft:
        await crud.change_user_comprehensive_status(db, uid, data.semester, True)


@app.get("/user/comprehensive/getData", response_model=list[IComprehensiveDataItem])
async def get_comprehensive_data(semester: str, uid: str = None, current_user: User = Depends(get_current_active_user),
                                 db: AsyncSession = Depends(get_db)):
    if uid and uid != current_user.account:
        if current_user.auth <= 1:
            raise HTTPException(status_code=403, detail="无权限")
        return await crud.get_comprehensive_data(db, semester, uid)
    return await crud.get_comprehensive_data(db, semester, current_user.account)


@app.get("/user/comprehensive/available", response_model=bool)
async def get_comprehensive_data_available(semester: str, user: User = Depends(get_current_active_user),
                                           db: AsyncSession = Depends(get_db)):
    return await crud.get_user_comprehensive_status(db, uid=user.account, semester=semester)


@app.post("/upload", response_model=IUploadFileResponse)
async def upload_file(file: UploadFile, user: User = Depends(get_current_active_user),
                      db: AsyncSession = Depends(get_db)):
    filename = file.filename
    hashed_filename = await get_file_md5(file)
    hashed_filename = hashed_string(hashed_filename + user.account)
    extension_name = guess_extension(file)
    folder_name = hashed_filename[:2]
    file_path = os.path.join("uploads", folder_name)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path = os.path.join(file_path, hashed_filename + "." + extension_name)

    await write_file_to_disk(file_path, file)
    return await crud.record_upload_file(db, uid=user.account, file_path=file_path, filename=filename,
                                         hashed_filename=hashed_filename)


@app.get("/files/{hashed_filename}")
async def read_uploaded_file(hashed_filename: str, db: AsyncSession = Depends(get_db)):
    try:
        db_file: IUploadFile = await crud.get_record_files(db, hashed_filename)
        if db_file is None:
            raise HTTPException(status_code=404, detail="Not Found")

        return StreamingResponse(await aiofile.async_open(db_file.path, 'rb'), media_type=get_media_type(db_file.path))
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Found, But not on disk.")


@app.post("/user/bind", response_model=IJWXTUserResponse)
async def bind_user(jwxt_account: IJWXTAccount, db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_active_user)):
    if jwxt_account.username != user.account:
        raise HTTPException(status_code=403, detail="不允许绑定不同学号的账户")
    if not jwxt_account.password:
        raise HTTPException(status_code=400, detail="密码为空")

    stu = school.user_login(jwxt_account.username, jwxt_account.password, use_cookie_login=False)
    if isinstance(stu, LoginFail):
        raise HTTPException(status_code=403, detail=stu.tip)

    result = await crud.create_user_jwxt_bind(db, jwxt_account.username, jwxt_account.password, **stu.get_info())
    if result:
        return result
    raise HTTPException(status_code=400, detail="已绑定，不可重复绑定")


@app.get("/user/bind/info", response_model=Optional[IJWXTUserResponse])
async def get_bound_user_info(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_active_user)):
    return await crud.get_user_jwxt_info(db, user.account)


@app.delete("/user/bind")
async def delete_bound_user_info(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_active_user)):
    return await crud.delete_user_jwxt_info(db, user.account)


@app.get("/user/bind/score", response_model=Optional[CourseData])
async def get_bound_user_score(semester: str, db: AsyncSession = Depends(get_db),
                               user: User = Depends(get_current_active_user)):
    info = await crud.get_user_jwxt_info(db, user.account)
    if info is None:
        raise HTTPException(status_code=400, detail="未绑定教务系统")

    stu = school.user_login(info.uid, info.password)

    if isinstance(stu, LoginFail):
        raise HTTPException(status_code=403, detail=f"{stu.tip}，如一直出错请尝试重新绑定教务系统。")
    semester = semester[:-2]
    try:
        return stu.get_score(score_year=semester)
    except ScoreException:
        return None


@app.get("/admin/job/my", response_model=list[IComprehensiveJob])
async def get_admin_job(semester: str, db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_admin_user)):
    return await crud.get_my_job(db, semester, user.account)


@app.post("/admin/job/distribute")
async def distribute_job(data: IComprehensiveDistribute, db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_admin_user)):
    e_list = await crud.set_distribute_job(db=db, data=data)
    if e_list:
        raise HTTPException(status_code=400, detail="学号为{}已被分配，无法再分配".format("、".join(e_list)))


@app.get("/admin/job/distribute", response_model=Page[IUserComprehensiveStatusWithClassName])
async def get_distribute_job(semester: str, db: AsyncSession = Depends(get_db),
                             _: User = Depends(get_current_super_admin_user)):
    return await crud.get_users_comprehensive_list(db, semester)


@app.get("/admin/query/admin", response_model=list[str])
async def get_admins_id(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_super_admin_user)):
    admin_list = await crud.get_user_by_auth(db, 1)
    return [user.account for user in admin_list]


add_pagination(app)
