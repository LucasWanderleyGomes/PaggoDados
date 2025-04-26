from fastapi import FastAPI, Query
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List, Optional

app = FastAPI()
engine = create_engine('postgresql://postgres:postgres@localhost:5433/fonte')

@app.get("/data")
def get_data(start: str, end: str, variables: Optional[List[str]] = Query(...)):
    cols = ", ".join(['timestamp'] + variables)
    query = text(f"SELECT {cols} FROM data WHERE timestamp >= :start AND timestamp < :end")
    df = pd.read_sql(query, params={'start': start, 'end': end}, con=engine)
    return df.to_dict(orient="records")