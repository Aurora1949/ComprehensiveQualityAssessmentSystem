from typing import Optional

from fastapi_pagination import Page
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


async def get_user_by_account(db: AsyncSession, account: str) -> Optional[User]:
    """
    根据用户账户查找账户
    :param db:
    :param account:
    :return: ``Optional[User]``
    """
    stmt = select(User).where(User.account == account)
    results = await db.execute(stmt)
    return results.scalar()


async def get_user_by_account_password(db: AsyncSession, account: str, password: str) -> Optional[User]:
    """
    根据给定的用户账户与密码查找账户
    :param db:
    :param account:
    :param password:
    :return: ``Optional[User]``
    """
    stmt = select(User).where(User.account == account)
    results = await db.execute(stmt)
    user = results.scalar()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(db: AsyncSession, user: IUserCreate):
    """

    :param db:
    :param user:
    :return:
    """
    hashed_password = get_password_hash(user.password)
    auth = 0
    if user.account == 'root':
        auth = 2
    db_user = User(account=user.account, hashed_password=hashed_password, auth=auth)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_by_xlsx(db: AsyncSession, user: IUserCreateByExcel):
    """

    :param db:
    :param user:
    :return:
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(account=user.account, hashed_password=hashed_password)
    db_user_info = UserInfo(name=user.name, duties=user.duties, gender=user.gender, class_name=user.class_name,
                            uid=user.account)
    db.add(db_user)
    db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user)
    await db.refresh(db_user_info)


async def record_upload_file(db: AsyncSession, uid: str, file_path: str, filename: str, hashed_filename: str) -> IUploadFile:
    stmt = select(Upload).where(Upload.hashed_filename == hashed_filename)
    result = await db.execute(stmt)
    result = result.scalars().first()

    if result:
        return result

    new_record = Upload(hashed_filename=hashed_filename, uid=uid, path=file_path, filename=filename)
    db.add(new_record)

    await db.commit()
    await db.refresh(new_record)
    return new_record


async def get_record_files(db: AsyncSession, hashed_filename: str) -> IUploadFile:
    stmt = select(Upload).where(Upload.hashed_filename == hashed_filename)
    result = await db.execute(stmt)
    return result.scalars().first()


async def set_user_admin(db: AsyncSession, uid_list: list[str], admin_type: int):
    stmt = update(User).where(User.account.in_(uid_list)).values(auth=admin_type)
    await db.execute(stmt)
    await db.commit()


async def unset_user_admin(db: AsyncSession, uid_list: list[str]):
    """

    :param db:
    :param uid_list:
    :return:
    """
    stmt = update(User).where(User.account.in_(uid_list)).values(auth=0)
    await db.execute(stmt)
    await db.commit()


async def get_user_list_by_(db: AsyncSession, class_name: str, base_user_level: int) -> Page[IUser]:
    """
    根据班级名和给定的基准权限查找用户，并返回分页结果
    :param db:
    :param class_name: 班级名称
    :param base_user_level: 基准用户权限
    :return: ``Page[IUser]``
    """
    stmt = select(User).join(UserInfo).where(User.auth >= base_user_level)
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


async def create_new_comprehensive(db: AsyncSession, comprehensive: IComprehensive) -> bool:
    """
    创建新的综测信息
    :param db: ``AsyncSession`` 异步数据库
    :param comprehensive:
    :return: ``bool``
    """
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


async def set_current_comprehensive_db(db: AsyncSession, semester: str) -> None:
    """
    设置当前综测
    :param db: ``AsyncSession`` 异步数据库
    :param semester: 学期代号
    :return: ``None``
    """
    stmt = update(CurrentComprehensive).where(CurrentComprehensive.id == 1).values(semester=semester)
    await db.execute(stmt)
    await db.commit()


async def get_all_comprehensive(db: AsyncSession) -> list[Comprehensive]:
    """
    获取所有综测信息
    :param db: ``AsyncSession`` 异步数据库
    :return: ``list[Comprehensive]``
    """
    stmt = select(Comprehensive)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_current_comprehensive(db: AsyncSession) -> CurrentComprehensive | None:
    """
    获取当前期综测信息
    :param db: ``AyncSession`` 异步数据库
    :return: ``Optional[CurrentComprehensive]``
    """
    stmt = select(CurrentComprehensive)
    result = await db.execute(stmt)
    return result.scalar()


async def save_comprehensive_data(db: AsyncSession, semester: str, uid: str, data: IComprehensiveSaveData) -> None:
    """
    将信息保存至数据库中
    :param db: ``AsyncSession`` 异步数据库
    :param semester: 学期代号
    :param uid: 用户的账户
    :param data: 从前端收到的信息
    :return: ``None``
    """
    comprehensive_data = data.data
    stmt = select(ComprehensiveData).where(ComprehensiveData.semester == semester, ComprehensiveData.uid == uid)
    exist_records = await db.execute(stmt)
    # 在数据库中的所有记录
    exist_records = exist_records.scalars().all()
    # 在记录中的所有 codename
    exist_codenames_list = [record.codename for record in exist_records]
    # 剔除记录中重复的 codename
    exist_codenames = set(exist_codenames_list)
    # 记录中重复的 codename
    exist_mult_codenames = {codename for codename in exist_codenames_list if exist_codenames_list.count(codename) > 1}
    # 数据中所有的 codename
    data_codenames = [item.codename for item in comprehensive_data]
    # 数据中重复的 codename
    data_mult_codenames = {codename for codename in data_codenames if data_codenames.count(codename) > 1}

    # 查找并删除不需要的记录
    for codename in exist_codenames:
        # 当 codename 不在数据中时，或者 codename 在记录中重复又存在数据中，或者 codename 存在于在数据中重复，我们则删除这条记录
        if not (codename not in data_codenames or (codename in exist_mult_codenames and codename in data_codenames) or (codename in data_mult_codenames)):
            continue
        stmt = delete(ComprehensiveData).where(
            ComprehensiveData.codename == codename,
            ComprehensiveData.uid == uid,
            ComprehensiveData.semester == semester
        )
        await db.execute(stmt)

    # 修改已有或添加新的记录
    for data_item in comprehensive_data:
        stmt = select(ComprehensiveData).where(
            ComprehensiveData.codename == data_item.codename,
            ComprehensiveData.uid == uid,
            ComprehensiveData.semester == semester
        )
        record = await db.execute(stmt)
        record = record.scalars().first()
        if record:
            # 存在并修改
            record.content = data_item.content
            record.score = data_item.score
            record.upload = data_item.upload
        else:
            # 不存在则新增
            new_record = ComprehensiveData(
                semester=semester,
                uid=uid,
                content=data_item.content,
                score=data_item.score,
                codename=data_item.codename,
                upload=data_item.upload
            )
            db.add(new_record)

    await db.commit()


async def get_comprehensive_data(db: AsyncSession, semester: str, uid: str) -> list[ComprehensiveData]:
    """
    从数据库中返回填报的信息
    :param db: ``AsyncSession`` 异步数据库
    :param semester: 学期代号
    :param uid: 用户的账户
    :return: ``list[ComprehensiveData]``
    """
    stmt = select(ComprehensiveData).where(ComprehensiveData.semester == semester, ComprehensiveData.uid == uid)
    result = await db.execute(stmt)
    return result.scalars().all()


async def change_user_comprehensive_status(db: AsyncSession, uid: str, semester: str, status: bool) -> None:
    """
    更改用户填报的状态
    :param db: ``AsyncSession`` 异步数据库
    :param uid: 用户的账户
    :param semester: 学期代号
    :param status: 要修改的状态， ``True`` 为已提交, ``False`` 为未提交
    :return: ``None``
    """
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


async def get_user_comprehensive_status(db: AsyncSession, uid: str, semester: str) -> bool:
    """
    获取用户是否已经填报完成, ``True`` 表示已提交，``False`` 表示提交
    :param db: ``AsyncSession`` 异步数据库
    :param uid: 用户的账户
    :param semester: 学期代号
    :return: ``bool``
    """
    stmt = select(ComprehensiveSubmitStatus).where(ComprehensiveSubmitStatus.uid == uid, ComprehensiveSubmitStatus.semester==semester)
    result = await db.execute(stmt)
    result = result.scalars().first()
    if result is None:
        return False
    return result.status
