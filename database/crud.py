import json
from typing import Optional

from fastapi_pagination.ext.sqlalchemy import paginate
from openpyxl.styles.builtins import total
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import query

from models.upload import Upload
from models.user import User, UserInfo
from schemas.upload import IUploadFile
from schemas.user import IUserCreate, IUserCreateByExcel, IUser
from utils.auth import verify_password, get_password_hash


async def get_user(db: AsyncSession, user_id: id):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar()


async def get_user_by_account(db: AsyncSession, account: str) -> Optional[User]:
    stmt = select(User).where(User.account == account)
    results = await db.execute(stmt)
    return results.scalar()


async def get_user_by_account_password(db: AsyncSession, account: str, password: str) -> Optional[User]:
    stmt = select(User).where(User.account == account)
    results = await db.execute(stmt)
    user = results.scalar()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User)
    results = await db.execute(stmt)
    return results.all()


async def create_user(db: AsyncSession, user: IUserCreate):
    hashed_password = get_password_hash(user.password)
    # db_user_info = UserInfo(name=user.name, gender=user.gender, account=user.account)
    auth = 0
    if user.account == 'root':
        auth = 2
    db_user = User(account=user.account, hashed_password=hashed_password, auth=auth)
    db.add(db_user)
    # db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_by_xlsx(db: AsyncSession, user: IUserCreateByExcel):
    hashed_password = get_password_hash(user.password)
    db_user = User(account=user.account, hashed_password=hashed_password)
    db_user_info = UserInfo(name=user.name, duties=user.duties, gender=user.gender, class_name=user.class_name,
                            uid=user.account)
    db.add(db_user)
    db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user)
    await db.refresh(db_user_info)


def record_upload_file(db: AsyncSession, uploadfile: IUploadFile):
    db_user = db.query(User).filter(User.account == uploadfile.uid).first()
    db_upload_file = Upload(path=uploadfile.path, filename=uploadfile.filename, uid=uploadfile.uid)
    db.add(db_upload_file)
    db.commit()
    db.refresh(db_upload_file)


async def set_user_admin(db: AsyncSession, uid_list: list[str], admin_type: int):
    stmt = update(User).where(User.account.in_(uid_list)).values(auth=admin_type)
    await db.execute(stmt)
    await db.commit()


async def unset_user_admin(db: AsyncSession, uid_list: list[str]):
    stmt = update(User).where(User.account.in_(uid_list)).values(auth=0)
    await db.execute(stmt)
    await db.commit()


async def get_user_list_by_(db: AsyncSession,
                            class_name: str,
                            base_user_level):
    stmt = (select(User)
            .join(UserInfo)
            .where(User.auth >= base_user_level)
            )
    if class_name:
        stmt = stmt.where(UserInfo.class_name.like(f"%{class_name}%"))

    return await paginate(db, stmt)


async def reset_passwd(db: AsyncSession, uid: str):
    stmt = update(User).where(User.account == uid).values(hashed_password=get_password_hash(uid))
    await db.execute(stmt)
    await db.commit()


async def update_user_info(db: AsyncSession, user: IUser):
    stmt = update(User).where(User.account == user.account).values(is_active=user.is_active, auth=user.auth)
    await db.execute(stmt)
    stmt = update(UserInfo).where(UserInfo.uid == user.account).values(name=user.extend.name, gender=user.extend.gender,
                                                                       duties=user.extend.duties,
                                                                       class_name=user.extend.class_name)
    await db.execute(stmt)
    await db.commit()


async def create_user(db: AsyncSession, user: IUser):
    hashed_password = get_password_hash(user.account)
    db_user = User(account=user.account, hashed_password=hashed_password)
    db_user_info = UserInfo(name=user.extend.name, duties=user.extend.duties, gender=user.extend.gender,
                            class_name=user.extend.class_name,
                            uid=user.account)
    db.add(db_user)
    db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user)
    await db.refresh(db_user_info)
