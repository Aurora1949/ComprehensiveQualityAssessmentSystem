from sqlalchemy import Column, Integer, ForeignKey, String

from database import Base


class Upload(Base):
    __tablename__ = "upload"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    filename = Column(String, index=True)
    hashed_filename = Column(String, index=True)
    uid = Column(String, ForeignKey("users.account"))
