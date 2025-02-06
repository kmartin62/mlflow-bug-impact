from sqlalchemy import Column, Float, String
from ..db import Base

class VwImprovements(Base):
    __tablename__ = 'vw_improvements'

    title = Column(String, primary_key=True)
    percentage_change_accuracy = Column(Float)
    percentage_change_recall = Column(Float)
    percentage_change_precision = Column(Float)
    percentage_change_f1 = Column(Float)
    percentage_change_log_loss = Column(Float)