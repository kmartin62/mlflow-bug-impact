import os
from sqlalchemy.orm import Session
from database.models import SentimentModel

class SentimentModelService:
  def __init__(self):
    pass

  def get(self, db: Session):
    model = db.query(SentimentModel).filter_by(is_active=True).first()
    return model.sentiment_analysis_model if model else os.getenv("DEFAULT_SENTIMENT_MODEL")
