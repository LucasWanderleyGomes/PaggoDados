# alvo_db/create_alvo.py
from sqlalchemy import create_engine
from models import Base
from models import Signal

engine = create_engine('postgresql://postgres:postgres@localhost:5433/alvo')
Base.metadata.create_all(engine)

# Inserir nomes dos sinais
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
for name in ['wind_speed', 'power']:
    session.add(Signal(name=name))
session.commit()