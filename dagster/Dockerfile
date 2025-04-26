FROM python:3.9-slim

WORKDIR /dagster

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]