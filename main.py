from datetime import timedelta
from typing import Any, Union

from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from database import crud
from database.crud import create_new_comprehensive, get_all_comprehensive, get_current_comprehensive, \
    set_current_comprehensive_db
from database.utils import get_db, init_db
from models.comprehensive import Comprehensive
from models.user import User
from schemas.auth import IToken
from schemas.comprehensive import IComprehensive, ICurrentComprehensive, IChangeComprehensive, \
    IComprehensiveFormTemplate
from schemas.user import IUserCreate, IUser
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, get_current_admin_user, \
    get_current_super_admin_user, SECRET_KEY, get_current_active_user
from utils.decorator import record_fatal_error
from utils.excel import get_student_from_upload_excel
from utils.functions import is_uid_valid, is_user_exists
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


@app.on_event("startup")
async def runtime_init_db():
    await init_db()


@app.get('/hello')
@record_fatal_error
def say_hello():
    a = None
    return "hello world"


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
async def create_user_by_excel(file: UploadFile, current_user: User = Depends(get_current_admin_user),
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
                    current_user: User = Depends(get_current_super_admin_user),
                    db: AsyncSession = Depends(get_db)):
    uid_list = uid.split(';')
    if set_type:
        return await crud.set_user_admin(db, uid_list, admin_type)
    return await crud.unset_user_admin(db, uid_list)


@app.get("/admin/get/userList", response_model=Page[IUser])
async def get_user_list(class_name: str = "", base_user_level: int = 0,
                        auth=Depends(get_current_super_admin_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_user_list_by_(db, class_name, base_user_level)


@app.get("/admin/user/resetPasswd")
async def reset_password(uid: str, auth=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.reset_passwd(db, uid)
    return {"msg": "密码重置成功"}


@app.post("/admin/user/modify")
async def modify_user_info(user: IUser, auth=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.update_user_info(db, user)
    return {"msg": "修改成功"}


@app.post("/admin/user/create")
async def create_user(user: IUser, auth=Depends(get_current_admin_user), db: AsyncSession = Depends(get_db)):
    await crud.create_user(db, user)
    return {"msg": "成功"}


@app.post("/admin/comprehensive/create")
async def create_comprehensive(comprehensive: IComprehensive, auth=Depends(get_current_super_admin_user),
                               db=Depends(get_db)):
    await create_new_comprehensive(db, comprehensive)
    return {"msg": "成功"}


@app.get("/admin/comprehensive/queryAll", response_model=list[IComprehensive])
async def query_all_comprehensive(auth=Depends(get_current_admin_user), db=Depends(get_db)):
    return await get_all_comprehensive(db)


@app.post("/admin/comprehensive/setCurrent")
async def set_current_comprehensive(semester: IChangeComprehensive, auth=Depends(get_current_admin_user),
                                    db=Depends(get_db)):
    await set_current_comprehensive_db(db, semester=semester.semester)


@app.get("/user/comprehensive/query", response_model=Union[ICurrentComprehensive, None])
async def query_current_comprehensive(db=Depends(get_db)):
    return await get_current_comprehensive(db)


@app.get("/user/comprehensive/getForm", response_model=list[IComprehensiveFormTemplate])
async def get_comprehensive_form(auth=Depends(get_current_active_user)):
    return parse_xml('./config/xlsx_format_xml.xml')


add_pagination(app)
