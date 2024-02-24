#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2024 by Jeffery Hsu
#  Email: me@cantyonion.site
#  Created on 2024/02/14
#  Last Modified on 2024/02/14 01:34:58
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

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Comprehensive(Base):
    __tablename__ = "comprehensive"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    title = Column(String, unique=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    semester = Column(String, nullable=False, unique=True)


class CurrentComprehensive(Base):
    __tablename__ = "current_comprehensive"
    id = Column(Integer, primary_key=True)
    # 使用 ForeignKey 来定义外键关系
    semester = Column(String, ForeignKey("comprehensive.semester"), unique=True)
    # 使用 relationship 来定义反向关系
    detail = relationship("Comprehensive", backref="current_comprehensive", uselist=False, lazy='selectin')


class ComprehensiveData(Base):
    __tablename__ = "c_data"
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey("comprehensive.semester"))
    uid = Column(String, ForeignKey("users.account"))
    codename = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    content = Column(String, nullable=False)
    upload = Column(String, ForeignKey("upload.hashed_filename"))


class ComprehensiveSubmitStatus(Base):
    __tablename__ = "c_submitstatus"
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey("comprehensive.semester"))
    uid = Column(String, ForeignKey("users.account"))
    status = Column(Boolean, nullable=False, default=False)


class ComprehensiveDistribute(Base):
    __tablename__ = "distribute"
    id = Column(Integer, primary_key=True)
    semester = Column(String, ForeignKey("comprehensive.semester"))
    admin_uid = Column(String, ForeignKey("users.account"))
    user_uid = Column(String, ForeignKey("users.account"))
    status = Column(Integer, nullable=False, default=0)
    distribute_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    complete_date = Column(DateTime, default=None)
