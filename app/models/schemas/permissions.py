#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 11:39:48
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
from enum import IntFlag
from typing import Union


class Permissions(IntFlag):
    Fill: int = 0b0000_0001  # 填写
    Read: int = 0b0000_0010  # 参看
    ReadAll: int = 0b0000_0100  # 查看班级所有人
    EditUser: int = 0b0000_1000  # 编辑班级所有用户
    ReviewForm: int = 0b0001_0000  # 审核报表
    EditSemester: int = 0b0010_0000  # 编辑学期
    ReadAllClass: int = 0b0100_0000  # 查看所有班级的所有人
    EditAllUser: int = 0b1000_0000  # 查看所有班级的所有用户
    ReviewAllForm: int = 0b0001_0000_000  # 审核所有报表

    def __or__(self, other: 'Permissions'):
        return Permissions(self.value | other.value)

    def __and__(self, other: 'Permissions'):
        return Permissions(self.value & other.value)

    def __int__(self) -> int:
        return int(self.value())

    @staticmethod
    def has_permission(op: Union[int, "Permissions"], cp: "Permissions") -> bool:
        if isinstance(op, Permissions):
            return op.value & cp.value == cp.value
        elif isinstance(op, int):
            return op & cp.value() == cp.value

        raise TypeError(f"Type {type(op)} can not be compat with int or Permissions")

    @staticmethod
    def revoke_permission(op: Union[int, "Permissions"], cp: "Permissions") -> "Permissions":
        if isinstance(op, Permissions):
            return Permissions(op.value & ~cp.value)
        elif isinstance(op, int):
            return Permissions(op & ~cp.value)

        raise TypeError(f"Type {type(op)} can not be compat with int or Permissions")

    @staticmethod
    def add_permission(op: Union[int, "Permissions"], cp: "Permissions") -> "Permissions":
        if isinstance(op, Permissions):
            return Permissions(op.value | cp.value)
        elif isinstance(op, int):
            return Permissions(op | cp.value())

        raise TypeError(f"Type {type(op)} can not be compat with int or Permissions")

    @staticmethod
    def common_user() -> "Permissions":
        """
        普通用户权限
        :return:
        """
        return Permissions(Permissions.Fill | Permissions.Read)

    @staticmethod
    def class_admin_user(self) -> "Permissions":
        """
        班级管理员权限
        :return:
        """
        return Permissions(self.common_user | self.ReadAll | self.EditUser | self.ReviewForm)

    @staticmethod
    def reviewer(self) -> "Permissions":
        """
        审核员权限
        :return:
        """
        return Permissions(self.common_user | self.ReviewForm)

    @staticmethod
    def super_admin_user(self) -> "Permissions":
        """
        年级管理员类型权限
        :return:
        """
        return Permissions(self.class_admin_user | self.EditAllUser | self.ReadAllClass | self.ReviewAllForm)


if __name__ == "__main__":
    auth = Permissions.common_user()
    print("Common user can Read All", Permissions.has_permission(auth, Permissions.ReadAll))
    print("Now we add permissions to common user")
    auth = Permissions.add_permission(auth, Permissions.ReviewForm)
    print("Now user can review form", Permissions.has_permission(auth, Permissions.ReviewForm))
    print("We remove permissions from common user")
    auth = Permissions.revoke_permission(auth, Permissions.ReviewForm | Permissions.Fill)
    print("Now user can fill", Permissions.has_permission(auth, Permissions.Fill))
    print("Now user can review form", Permissions.has_permission(auth, Permissions.ReviewForm))
    print("Now user can read", Permissions.has_permission(auth, Permissions.Read))
