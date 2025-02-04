from sqlalchemy import Column, Integer, String, Text
from ..db import Base
# TODO: clear code later


class CommitType(Base):  
    __tablename__ = "commit_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)