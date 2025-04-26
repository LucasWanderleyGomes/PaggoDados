import httpx
import pandas as pd
from sqlalchemy import create_engine
import logging


logging.basicConfig(level=logging.INFO)

def extract(start_date):
    response = httpx.get(f'http://app:8000/data/?start_date={start_date}&end_date={start_date + pd.Timedelta(days=1)}&variables=wind_speed,power')
    return response.json()

def transform(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    aggregated = df.resample('10T').agg(['mean', 'min', 'max', 'std'])
    return aggregated

def load(data):
    engine = create_engine('postgresql://postgres:postgres@db_alvo:5432/alvo')
    data.to_sql('signal_data', engine, if_exists='append', index=True)

def run_etl(start_date):
    try:
        data = extract(start_date)
        aggregated_data = transform(data)
        load(aggregated_data)
        logging.info('ETL process completed successfully')
    except Exception as e:
        logging.error(f'ETL process failed with error: {e}')
if __name__ == "__main__":
    run_etl(pd.to_datetime('2023-01-01'))