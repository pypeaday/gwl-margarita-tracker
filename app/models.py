from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Margarita(Base):
    __tablename__ = "margaritas"

    id = Column(Integer, primary_key=True, index=True)
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow)
    price = Column(Float)
