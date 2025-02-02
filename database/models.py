from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from sqlalchemy.sql import func
from .db import Base

class PullRequest(Base):
    __tablename__ = "pull_request"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20), unique=True, nullable=False)
    author = Column(String(20), unique=True, nullable=False)
    state = Column(Enum("open", "closed", "merged", name="state"), nullable=False)
    comments_count = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    merged_at = Column(TIMESTAMP, nullable=True)