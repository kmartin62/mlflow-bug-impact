from sqlalchemy import Column, Integer, TIMESTAMP, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db import Base
from .git_commit import GitCommit

class MlflowMetrics(Base):
    __tablename__ = 'mlflow_metrics'

    id = Column(Integer, primary_key=True)
    experiment_id = Column(String, nullable=False)
    run_id = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    model = Column(String, nullable=False)
    accuracy = Column(Float)
    recall = Column(Float)
    precision = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    log_loss = Column(Float)
    commit_hash = Column(String, ForeignKey('git_commit.hash', ondelete='CASCADE'), nullable=False)

    git_commit = relationship(GitCommit, backref='mlflow_metrics')