#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/02/15
#  Last Modified on 2024/02/15 12:56:39
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


class IComprehensiveDistribute(BaseModel):
    semester: str
    admin_id: str
    user_id_list: list[str]


class IComprehensiveJob(BaseModel):
    name: str
    class_name: str
    account: str
    submit_status: Optional[bool]
    distribute_status: int
