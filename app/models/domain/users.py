#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 11:46:16
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

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security


class User(RWModel):
    account: str
    auth: int
    is_active: bool
    name: str
    duties: str
    gender: int
    class_name: str


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.hashed_password = security.get_password_hash(password)
