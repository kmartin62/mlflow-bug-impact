import logging
from .interface.db_service import DbService
from sqlalchemy.orm import Session
from database.models import PullRequestComment
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PullRequestCommentsService(DbService):
  def __init__(self):
    pass

  def get_all(self, db: Session):
    return db.query(PullRequestComment).all()
  
  def get_by_id(self, db: Session, id):
    return db.query(PullRequestComment).filter(PullRequestComment.pr_id == id).all()
  
  def insert(self, db: Session, model: PullRequestComment):
    try:
      db.add(model)
      db.commit()
    except SQLAlchemyError as e:
      logger.error(f"An error occured: {repr(e)}")
      db.rollback()
    finally:
      db.close()

  def add(self, db: Session, model: PullRequestComment):
    db.add(model)