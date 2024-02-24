#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 11:52:57
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
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import UserInDB


class UserRepository(BaseRepository):
    async def get_user_by_account(self, *, account: str) -> UserInDB:
        user_row = await queries.get_user_by_account(self.connection, account=account)
        if user_row:
            user_row = dict(zip([
                'account',
                'hashed_password',
                'auth',
                'is_active',
                'name',
                'duties',
                'gender',
                'class_name'
            ],
                user_row))
            return UserInDB(**user_row)

        raise EntityDoesNotExist("user with account {0} does not exist".format(account))
