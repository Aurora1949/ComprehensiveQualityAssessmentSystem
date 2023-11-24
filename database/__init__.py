# see: https://fastapi.tiangolo.com/zh/tutorial/sql-databases/
# for async db see: https://juejin.cn/post/7084862618816479262 and
# https://stackoverflow.com/questions/66431083/using-asyncio-extension-with-sqlite-backend-broken-by-version-upgrade
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, as_declarative

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=AsyncSession)
Base = declarative_base()
