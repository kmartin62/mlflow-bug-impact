from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class DbService(ABC):
  @abstractmethod
  def get_all(self, db: Session):
    raise NotImplementedError("This feature is not implemented")
  
  @abstractmethod
  def get_by_id(self, db: Session, id):
    raise NotImplementedError("This feature is not implemented")
  
  @abstractmethod
  def insert(self, db: Session, model):
    raise NotImplementedError("This feature is not implemented")
  
  @abstractmethod
  def add(self, db: Session, model):
    raise NotImplementedError("This feature is not implemented")