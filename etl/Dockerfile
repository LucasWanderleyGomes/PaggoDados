FROM python:3.9-slim

WORKDIR /etl

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "etl.py"]