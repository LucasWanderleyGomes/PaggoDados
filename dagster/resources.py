from dagster import resource
from sqlalchemy import create_engine

@resource(
    config_schema={
        "host": str,
        "port": int,
        "database": str,
        "username": str,
        "password": str,
    }
)
def postgres_resource(context):
    host = context.resource_config["host"]
    port = context.resource_config["port"]
    database = context.resource_config["database"]
    username = context.resource_config["username"]
    password = context.resource_config["password"]

    engine = create_engine(f"postgresql://{password}:{username}@{host}:{port}/{database}")

    return engine