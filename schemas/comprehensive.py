import datetime
from typing import Optional, Union

from pydantic import BaseModel


class IComprehensive(BaseModel):
    title: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    semester: str

    class Config:
        from_attributes = True


class ICurrentComprehensive(BaseModel):
    semester: str
    detail: IComprehensive


class IChangeComprehensive(BaseModel):
    semester: str


class IConductScorecard(BaseModel):
    serial_number: Optional[str]
    title: str
    codename: Optional[str]
    standard: Optional[list[Union[int, float]]]
    at: Optional[str]
    sub: Optional[list["IConductScorecard"]]
    no_evidence: bool
    single: bool
    multiple: bool
    per_time: Optional[int]


class IComprehensiveFormTemplate(BaseModel):
    subject: str
    add: list[IConductScorecard]
    subtract: list[IConductScorecard]


class IComprehensiveDataItem(BaseModel):
    codename: str
    score: Union[int, float]
    content: str
    upload: Optional[str]


class IComprehensiveSaveData(BaseModel):
    data: list[IComprehensiveDataItem]
    draft: bool
    semester: str
