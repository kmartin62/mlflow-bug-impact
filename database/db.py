from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
  pass

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()