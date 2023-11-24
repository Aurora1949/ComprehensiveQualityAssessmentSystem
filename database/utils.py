from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine


async def init_db() -> None:
    """
    see: https://stackoverflow.com/questions/68230481/sqlalchemy-attributeerror-asyncengine-object-has-no-attribute-run-ddl-visit
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> Generator[AsyncSession, None, None]:
    """

    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
