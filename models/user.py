from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    auth = Column(Integer, default=0)  # 0 普通用户， 1 管理员， 2 超级管理员
    is_active = Column(Boolean, default=True)
    extend = relationship("UserInfo", backref="users", uselist=False, cascade="delete", lazy='selectin')


class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    duties = Column(String, default=None)
    gender = Column(Integer, index=True)  # 0 女 1 男
    class_name = Column(String, index=True)
    uid = Column(String, ForeignKey("users.account"))
