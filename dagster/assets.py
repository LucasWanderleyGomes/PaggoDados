from dagster import asset, ResourceDefinition, DailyPartitionsDefinition
import pandas as pd
from etl.etl import run_etl

@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-01-01")
)
def etl(context):
    start_date = context.partition_key
    run_etl(pd.to_datetime(start_date))