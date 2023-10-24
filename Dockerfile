# Use the official Airflow image as the base
FROM apache/airflow:latest

# Switch to airflow User
USER airflow

# Install the Docker, HTTP, and Airbyte providers for Airflow
RUN pip install apache-airflow-providers-docker \
  && pip install apache-airflow-providers-http \
  && pip install apache-airflow-providers-airbyte

# Switch back to root user
USER root