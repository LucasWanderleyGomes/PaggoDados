# fonte_db/load_fonte.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

start = pd.Timestamp('2023-01-01 00:00:00')
end   = start + pd.Timedelta(days=10)
idx = pd.date_range(start, end, freq='1min')[:-1]

df = pd.DataFrame({
    'timestamp': idx,
    'wind_speed': np.random.uniform(0, 25, size=len(idx)),
    'power': np.random.uniform(0, 1000, size=len(idx)),
    'ambient_temperature': np.random.uniform(-10, 40, size=len(idx)),
})

engine = create_engine('postgresql://postgres:postgres@localhost:5433/fonte')
df.to_sql('data', engine, if_exists='append', index=False)