import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import crud


def is_uid_valid(uid: str) -> bool:
    return bool(re.match("^[12][0-9]{9}$", uid))


async def is_user_exists(uid: str, db: AsyncSession):
    return bool(await crud.get_user_by_account(db, uid))
