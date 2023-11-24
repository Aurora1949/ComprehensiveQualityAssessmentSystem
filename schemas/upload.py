from pydantic import BaseModel


class IUploadFile(BaseModel):
    filename: str
    path: str
    uid: str
