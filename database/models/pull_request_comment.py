from ..db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class PullRequestComment(Base):
    __tablename__ = 'pull_request_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pr_id = Column(Integer, ForeignKey('pull_request.id', ondelete='CASCADE'), nullable=False)
    comment = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    pull_request = relationship("PullRequest", back_populates="comments")