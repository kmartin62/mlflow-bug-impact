from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Text, ForeignKey
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

class CommitType(Base):  
    __tablename__ = "commit_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
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