from typing import Union

from pydantic import BaseModel


class IToken(BaseModel):
    access_token: str
    token_type: str


class ITokenData(BaseModel):
    uid: Union[str, None]
