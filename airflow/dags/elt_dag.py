from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def run_elt_script():
    script_path = "/opt/airflow/elt_script/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 26),
    catchup=False,
)

t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag,
)

# t2 = DockerOperator(
#     task_id='run_dbt',
#     image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
#     command=[
#         "run",
#         "--profiles-dir",
#         "/root",
#         "--project-dir",
#         "/dbt",
#         "--full-refresh"
#     ],
#     network_mode="elt_network",
#     mounts=[
#         Mount(source='/postgres_transformations', target='/dbt', type='bind'),
#         Mount(source='~/.dbt', target='/root', type='bind'),
#     ],
#     environment={
#         'DBT_PROFILE': 'default',
#         'DBT_TARGET': 'dev'
#     },
#     auto_remove=False,  # Optional: Remove the container when done
#     dag=dag
# )

t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    api_version='auto',
    auto_remove=True,
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt",
        "--full-refresh"
    ],
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source='/postgres_transformations', target='/dbt', type='bind'),
        Mount(source='~/.dbt', target='/root', type='bind'),
    ],
    dag=dag
)

# t2 = BashOperator(
#     task_id='run_dbt',
#     bash_command='dbt run --profiles-dir /root --project-dir /dbt',
#     dag=dag,
# )

t1 >> t2
