from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signal'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    
class SignalData(Base):
    __tablename__ = 'signal_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    signal_id = Column(Integer, ForeignKey('signal.id'))
    timestamp = Column(DateTime, index=True)
    value = Column(Float)
    min_value = Column(Float)
    max_value = Column(Float)
    std_value = Column(Float)