from dagster import job, schedule
from .assets import etl

@job
def etl_job():
    etl()

@schedule(cron_schedule="0 0 * * *", job=etl_job, execution_timezone="UTC")
def daily_etl_schedule(_context):
    run_config = {}
    return run_config