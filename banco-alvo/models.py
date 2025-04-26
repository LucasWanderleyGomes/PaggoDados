from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgresql://postgres:postgres@db_alvo:5432/alvo')
Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signal'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = relationship("SignalData", backref="signal")

class SignalData(Base):
    __tablename__ = 'signal_data'
    id = Column(Integer, primary_key=True)
    signal_id = Column(Integer, ForeignKey('signal.id'))
    timestamp = Column(DateTime)
    value = Column(Float)

Base.metadata.create_all(engine)