from ..db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# from .pull_request_comment_sentiment import PullRequestCommentSentiment

class SentimentModel(Base):
    __tablename__ = "sentiment_models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sentiment_analysis_model = Column(String, nullable=False)
    added_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    is_active = Column(Boolean, nullable=False, default=False)

    sentiments = relationship("PullRequestCommentSentiment", back_populates="model", cascade="all, delete")