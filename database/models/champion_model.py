from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from ..db import Base


class ChampionModel(Base):  
    __tablename__ = 'champion_model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(String, nullable=False)
    run_id = Column(String, ForeignKey('mlflow_metrics.run_id', ondelete="CASCADE"), unique=True, nullable=False)
    metric = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    selected_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)