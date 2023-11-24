from pydantic import BaseModel

from schemas.user import IUser


class IResponse(BaseModel):
    ...


class IUserListResponse(IResponse):
    total: int
    page: int
    data: list[IUser]
