docker compose up init-airflow

sleep 5

docker compose up -d

sleep 5

cd airbyte

docker compose up -d
