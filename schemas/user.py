from typing import Optional, Union

from pydantic import BaseModel


class IUserBase(BaseModel):
    account: str


class IUserInfo(BaseModel):
    id: int
    name: str
    duties: Optional[str]
    gender: int
    class_name: str

    class Config:
        from_attributes = True


class IUserCreate(IUserBase):
    password: str
    name: str
    gender: int


class IUserCreateByExcel(IUserBase):
    password: str
    name: str
    gender: int
    duties: Optional[str]
    class_name: str

    def __str__(self):
        return f"IUserCreateByExcel<name='{self.name},gender='{self.gender}',duties='{self.duties}',class='{self.class_name}'>"


class IUserLogin(IUserBase):
    password: str


class IUserExtend(BaseModel):
    name: str
    duties: Optional[str]
    gender: int
    class_name: str
    uid: str

    class Config:
        from_attributes = True


class IUser(IUserBase):
    account: str
    auth: int
    is_active: bool
    extend: Union[IUserExtend, None]

    class Config:
        from_attributes = True
