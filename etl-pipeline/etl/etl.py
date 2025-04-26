import httpx
import pandas as pd
from sqlalchemy import create_engine
import datetime

API_URL = "http://localhost:8000/data"
DB_URL = "postgresql://postgres:postgres@localhost:5433/alvo"

def main(data_input):
    start = pd.Timestamp(data_input)
    end = start + pd.Timedelta(days=1)
    params = {
        "start": str(start),
        "end": str(end),
        "variables": ["wind_speed", "power"],
    }
    with httpx.Client() as client:
        r = client.get(API_URL, params=params)
    df = pd.DataFrame(r.json())
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index)

    agg = df.resample('10min').agg(['mean', 'min', 'max', 'std'])
    rows = []
    for var in ['wind_speed', 'power']:
        sign_id = 1 if var == 'wind_speed' else 2
        part = agg[var].reset_index()
        part['signal_id'] = sign_id
        part.rename(columns={'mean':'value', 'min':'min_value', 'max':'max_value', 'std':'std_value', 'timestamp':'timestamp'}, inplace=True)
        rows.append(part[['timestamp', 'signal_id', 'value', 'min_value', 'max_value', 'std_value']])
    result = pd.concat(rows)
    
    
    engine = create_engine(DB_URL)
    result.to_sql('signal_data', engine, if_exists='append', index=False)

if __name__ == "__main__":
    main("2023-01-02")