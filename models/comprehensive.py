from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref


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
