from datetime import datetime
from airflow import DAG
from docker.types import Mount

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator

# Replace this string with the ID generated from your Airbyte instance
CONN_ID = 'your_string_here'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2023, 10, 24),
    catchup=False,
)


# Need to change this to be an Airbyte DAG instead
t1 = AirbyteTriggerSyncOperator(
    task_id='airbyte_postgres_postgres',
    airbyte_conn_id='airbyte',
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag
)

t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh"
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    # Change this to your own paths
    mounts=[
        Mount(source='/Users/justinchau/Development/data-engineering-db/postgres_transformations',
              target='/dbt', type='bind'),
        Mount(source='/Users/justinchau/.dbt', target='/root', type='bind'),
    ],
    dag=dag
)

t1 >> t2
