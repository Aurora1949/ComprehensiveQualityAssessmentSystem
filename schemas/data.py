from typing import Union

from pydantic import BaseModel


class IEvidence(BaseModel):
    picture: str
    description: str


class IProjectData(BaseModel):
    codename: str
    value: Union[int | float]
    evidence: IEvidence


class IProject(BaseModel):
    project: str
    add: list[IProjectData]
    subtract: list[IProjectData]


class IAssessmentTable(BaseModel):
    xh: str
    semester: str
    data: list[IProject]
