#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/02/14
#  Last Modified on 2024/02/14 02:49:58
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

from typing import Optional, Union

from pydantic import BaseModel, RootModel


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


class IUserOnlyID(BaseModel):
    account: str


class IUserComprehensiveStatusWithClassName(BaseModel):
    account: str
    name: Optional[str]
    status: Optional[bool]
    class_name: Optional[str]


class IJWXTAccount(BaseModel):
    username: str
    password: str


class IJWXTUserResponse(BaseModel):
    uid: str
    faculty: str
    specialty: str
    education_level: str
    eductional_systme: str


class Course(BaseModel):
    credit: float
    score: Union[float, str]  # 成绩可能是数字或字符串
    lesson_name: str
    point: float
    bkcj: Union[str, None] = None  # 补考成绩，可选字段
    cxcj: Union[str, None] = None  # 重修成绩，可选字段


class CourseData(RootModel):
    root: dict[str, list[Course]]  # 使用字典来表示不同的学年
