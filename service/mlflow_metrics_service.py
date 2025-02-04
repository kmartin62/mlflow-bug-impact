import logging
from .interface.db_service import DbService
from sqlalchemy.orm import Session
from database.models import MlflowMetrics
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MlFlowMetricsService(DbService):
  def __init__(self):
    pass

  def get_all(self, db: Session):
    return db.query(MlflowMetrics).all()
  
  def get_by_id(self, db: Session, commit_hash):
    return db.query(MlflowMetrics).filter(MlflowMetrics.commit_hash == commit_hash).all()
  
  def insert(self, db: Session, model: MlflowMetrics):
    try:
      db.add(model)
      db.commit()
    except SQLAlchemyError as e:
      logger.error(f"An error occured: {repr(e)}")
      db.rollback()
    finally:
      db.close()

  def add(self, db: Session, model: MlflowMetrics):
    db.add(model)