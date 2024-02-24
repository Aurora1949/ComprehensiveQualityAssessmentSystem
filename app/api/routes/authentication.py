#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 11:56:10
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
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UserRepository
from app.models.schemas.users import UserInResponse, UserInLogin, UserWithToken
from app.resources import lang
from app.services import jwt

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
        user_login: UserInLogin = Body(..., embed=True, alias="users"),
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
        settings: AppSettings = Depends(get_app_settings)
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=lang.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await users_repo.get_user_by_account(account=user_login.account)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            account=user.account,
            gender=user.gender,
            auth=user.auth,
            is_active=user.is_active,
            name=user.name,
            class_name=user.class_name,
            duties=user.duties,
            token=token
        ),
    )
