from typing import Optional

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.comprehensive import Comprehensive, CurrentComprehensive, ComprehensiveData, ComprehensiveSubmitStatus
from models.upload import Upload
from models.user import User, UserInfo
from schemas.comprehensive import IComprehensive, IComprehensiveSaveData
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


async def create_new_comprehensive(db: AsyncSession, comprehensive: IComprehensive):
    db_comprehensive = Comprehensive(
        title=comprehensive.title,
        start_date=comprehensive.start_date,
        end_date=comprehensive.end_date,
        semester=comprehensive.semester
    )
    db.add(db_comprehensive)
    await db.commit()
    await db.refresh(db_comprehensive)
    return True


async def set_current_comprehensive_db(db: AsyncSession, semester: str):
    stmt = update(CurrentComprehensive).where(CurrentComprehensive.id == 1).values(semester=semester)
    await db.execute(stmt)
    await db.commit()


async def get_all_comprehensive(db: AsyncSession) -> list[Comprehensive]:
    stmt = select(Comprehensive)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_current_comprehensive(db: AsyncSession):
    stmt = select(CurrentComprehensive)
    result = await db.execute(stmt)
    return result.scalar()


async def save_comprehensive_data(db: AsyncSession, semester: str, uid: str, data: IComprehensiveSaveData):
    comprehensive_data = data.data
    stmt = select(ComprehensiveData).where(ComprehensiveData.semester == semester, ComprehensiveData.uid == uid)
    exist_records = await db.execute(stmt)
    exist_records = exist_records.scalars().all()
    exist_codenames_list = [record.codename for record in exist_records]
    exist_codenames = set(exist_codenames_list)
    exist_mult_codenames = {codename for codename in exist_codenames_list if exist_codenames_list.count(codename) > 1}
    data_codenames = [item.codename for item in comprehensive_data]
    data_mult_codenames = {codename for codename in data_codenames if data_codenames.count(codename) > 1}

    for codename in exist_codenames:
        if not (codename not in data_codenames or (codename in exist_mult_codenames and codename in data_codenames) or (codename in data_mult_codenames)):
            continue
        stmt = delete(ComprehensiveData).where(
            ComprehensiveData.codename == codename,
            ComprehensiveData.uid == uid,
            ComprehensiveData.semester == semester
        )
        await db.execute(stmt)

    for data_item in comprehensive_data:
        stmt = select(ComprehensiveData).where(
            ComprehensiveData.codename == data_item.codename,
            ComprehensiveData.uid == uid,
            ComprehensiveData.semester == semester
        )
        record = await db.execute(stmt)
        record = record.scalars().first()
        if record:
            record.content = data_item.content
            record.score = data_item.score
        else:
            new_record = ComprehensiveData(
                semester=semester,
                uid=uid,
                content=data_item.content,
                score=data_item.score,
                codename=data_item.codename
            )
            db.add(new_record)

    await db.commit()


async def get_comprehensive_data(db: AsyncSession, semester: str, uid: str) -> list[ComprehensiveData]:
    stmt = select(ComprehensiveData).where(ComprehensiveData.semester == semester, ComprehensiveData.uid == uid)
    result = await db.execute(stmt)
    return result.scalars().all()


async def change_user_comprehensive_status(db: AsyncSession, uid: str, semester: str, status: bool) -> None:
    stmt = select(ComprehensiveSubmitStatus).where(ComprehensiveSubmitStatus.uid == uid, ComprehensiveSubmitStatus.semester==semester)
    result = await db.execute(stmt)
    result = result.scalars().first()
    if result:
        result.status = status
    else:
        new_record = ComprehensiveSubmitStatus(
            uid=uid,
            semester=semester,
            status=status
        )
        db.add(new_record)
    await db.commit()


async def get_user_comprehensive_status(db:AsyncSession, uid: str, semester: str) -> bool:
    stmt = select(ComprehensiveSubmitStatus).where(ComprehensiveSubmitStatus.uid == uid, ComprehensiveSubmitStatus.semester==semester)
    result = await db.execute(stmt)
    result = result.scalars().first()
    if not result:
        return True
    return not result.status
