from ..db import Base
from .pull_request_comment import PullRequestComment
from .pull_request_comment_sentiment import PullRequestCommentSentiment
from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class PullRequest(Base):
    __tablename__ = "pull_request"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20), unique=True, nullable=False)
    author = Column(String(20), unique=True, nullable=False)
    state = Column(Enum("open", "closed", "merged", name="state"), nullable=False)
    comments_count = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    merged_at = Column(TIMESTAMP, nullable=True)

    comments = relationship(PullRequestComment, back_populates="pull_request", cascade="all, delete-orphan")
    sentiments = relationship(PullRequestCommentSentiment, back_populates="pull_request", cascade="all, delete")

    def __str__(self):
        return f"PullRequest(id={self.id}, title='{self.title}', author='{self.author}', state='{self.state}', comments_count={self.comments_count}, created_at={self.created_at}, merged_at={self.merged_at})"