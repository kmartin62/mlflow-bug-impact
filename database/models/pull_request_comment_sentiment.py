from sqlalchemy import Column, Integer, Text, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
# from .pull_request import PullRequest
from .sentiment_analysis import SentimentModel
from ..db import Base

class PullRequestCommentSentiment(Base):
    __tablename__ = "pull_request_comment_sentiment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pr_id = Column(Integer, ForeignKey("pull_request.id", ondelete="CASCADE"), unique=True, nullable=False)
    sentiment_label = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    analyzed_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    model_id = Column(Integer, ForeignKey("sentiment_models.id"), nullable=False)

    pull_request = relationship("PullRequest", back_populates="sentiments")
    model = relationship(SentimentModel, back_populates="sentiments")