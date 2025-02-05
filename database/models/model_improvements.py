from sqlalchemy import Column, Integer, ForeignKey, Float, TIMESTAMP, Text
from sqlalchemy.sql import func
from ..db import Base


class ModelImprovements(Base):  
  __tablename__ = "model_improvements"

  id = Column(Integer, primary_key=True, autoincrement=True)
  commit_hash = Column(Text, ForeignKey("git_commit.hash", ondelete="CASCADE"), nullable=False)
  experiment_id = Column(Text, nullable=False)
  run_id = Column(Text, ForeignKey("mlflow_metrics.run_id", ondelete="CASCADE"), unique=True, nullable=False)

  percentage_change_accuracy = Column(Float)
  percentage_change_recall = Column(Float)
  percentage_change_precision = Column(Float)
  percentage_change_f1 = Column(Float)
  percentage_change_log_loss = Column(Float)

  created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())