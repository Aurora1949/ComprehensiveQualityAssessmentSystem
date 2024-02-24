#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/01/31
#  Last Modified on 2024/01/31 12:02:39
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
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.resources import lang
from app.services import jwt

HEADER_KEY = "Authorization"


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
            self,
            request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=lang.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
        *,
        required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
        api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
        settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lang.WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lang.WRONG_TOKEN_PREFIX,
        )

    return token


def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
        settings: AppSettings = Depends(get_app_settings),
) -> str:
    if authorization:
        return _get_authorization_header(authorization, settings)

    return ""


async def _get_current_user(
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
        token: str = Depends(_get_authorization_header_retriever()),
        settings: AppSettings = Depends(get_app_settings),
) -> User:
    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lang.MALFORMED_PAYLOAD,
        )

    try:
        return await users_repo.get_user_by_account(account=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=lang.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
        repo: UsersRepository = Depends(get_repository(UsersRepository)),
        token: str = Depends(_get_authorization_header_retriever(required=False)),
        settings: AppSettings = Depends(get_app_settings),
) -> Optional[User]:
    if token:
        return await _get_current_user(repo, token, settings)

    return None
