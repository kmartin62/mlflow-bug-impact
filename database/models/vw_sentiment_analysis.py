from sqlalchemy import Column, Integer, String
from ..db import Base

class VwSentimentAnalysis(Base):
    __tablename__ = 'vw_sentiment_analysis'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    comments_count = Column(Integer)
    sentiment_label = Column(String)