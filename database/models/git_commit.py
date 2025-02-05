from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.sql import func
from .commit_type import CommitType
from ..db import Base

    
class GitCommit(Base):
    __tablename__ = "git_commit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(Text, nullable=False, unique=True)
    pr_id = Column(Integer, ForeignKey("pull_request.id", ondelete="CASCADE"), nullable=True)
    author = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    lines_added = Column(Integer, nullable=False, default=0)
    lines_deleted = Column(Integer, nullable=False, default=0)
    affected_files_count = Column(Integer, nullable=False, default=0)
    commit_type_id = Column(Integer, ForeignKey("commit_type.id"))