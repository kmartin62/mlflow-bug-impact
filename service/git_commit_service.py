import logging
from .interface.db_service import DbService
from sqlalchemy.orm import Session
from database.models import GitCommit
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitCommitService(DbService):
  def __init__(self):
    pass

  def get_all(self, db: Session):
    return db.query(GitCommit).all()

  def get_by_id(self, db: Session, hash: str):
    return db.query(GitCommit).filter(GitCommit.hash == hash).first()

  def insert(self, db: Session, model: GitCommit):
    try:
        db.add(model)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"An error occured: {repr(e)}")
        db.rollback()
    finally:
        db.close()

  def add(self, db: Session, model: GitCommit):
    db.add(model)