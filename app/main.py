from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime

app = FastAPI()


def get_db_fonte():
    conn = psycopg2.connect(
        database="fonte",
        user="postgres",
        password="postgres",
        host="db_fonte",
        port="5432"
    )
    return conn

class Data(BaseModel):
    timestamp: datetime
    wind_speed: float
    power: float
    ambient_temperature: float

from fastapi import Query

@app.get("/data/")
def read_data(start_date: datetime = Query(..., alias="start_date"), end_date: datetime = Query(..., alias="end_date"), variables: str = 'wind_speed,power'):
    ...
    conn = get_db_fonte()
    cur = conn.cursor()
    variables_list = variables.split(',')
    query = f"SELECT timestamp, {','.join(variables_list)} FROM data WHERE timestamp BETWEEN %s AND %s"
    cur.execute(query, (start_date, end_date))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({
            'timestamp': row[0],
            **{var: val for var, val in zip(variables_list, row[1:])}
        })
    conn.close()
    return data