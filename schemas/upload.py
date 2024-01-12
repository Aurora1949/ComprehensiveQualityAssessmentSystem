from pydantic import BaseModel


class IUploadFileBase(BaseModel):
    filename: str
    hashed_filename: str


class IUploadFile(IUploadFileBase):
    path: str

    class Config:
        from_attribute: True


class IUploadFileResponse(IUploadFileBase):
    ...
