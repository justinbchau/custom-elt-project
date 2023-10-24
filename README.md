# Custom ELT Project

This repository contains a custom Extract, Load, Transform (ELT) project that utilizes Docker, Airbyte, Airflow, dbt, and PostgreSQL to demonstrate a simple ELT process.

## Repository Structure

1. **docker-compose.yaml**: This file contains the configuration for Docker Compose, which is used to orchestrate multiple Docker containers. It defines multiple services:
   - `source_postgres`: The source PostgreSQL database running on port 5433.
   - `destination_postgres`: The destination PostgreSQL database running on port 5434.
   - `postgres`: The postgres database used to store metadata from Airflow.
   - `webserver`: The Web UI for Airflow.
   - `scheduler`: Airflow's scheduler to orchestrate your tasks.

2. **airflow**: This folder contains the Airflow project including the dags to orchestrate both Airbyte and dbt to complete the ELT workflow

3. **postgres_transformations**: This folder contains the dbt project including all of the custom models we will be writing into the destination database

4. **source_db_init/init.sql**: This SQL script initializes the source database with sample data. It creates tables for users, films, film categories, actors, and film actors, and inserts sample data into these tables.

## How It Works

1. **Docker Compose**: Using the `docker-compose.yaml` file, a couple Docker containers are spun up:
   - A source PostgreSQL database with sample data.
   - A destination PostgreSQL database.
   - A Postgres database to store Airflow metadata
   - The webserver to access Airflow throught the UI
   - Airflow's Scheduler

2. **ELT Process**: Within Airbyte, you will input the information for both the source and destination databases to create a connection. From there, you'll take the connection ID from the Airbyte UI, plug it into the `elt_dag.py` file so that when you run Airflow, it can run the sync for you. After the sync is complete, Airflow will run dbt to run the transformations on top of the destination database. 

3. **Database Initialization**: The `init.sql` script initializes the source database with sample data. It creates several tables and populates them with sample data.

## Getting Started

1. Ensure you have Docker and Docker Compose installed on your machine.
2. Clone this repository.
3. Navigate to the repository directory and run `./start.sh`.
4. Once all containers are up and running, you can access the Airbyte UI at `http://localhost:8000` and the Airflow UI at `http://localhost:8080`
5. Within Airbyte, you'll input the information for both the source and destination databases. (Information can be found in the `docker-compose.yaml` file in the root directory)
6. Take the Connection ID once you have created the connection and paste the string into the `CONN_ID` variable found in the `elt_dag.py` file. That will be located in the `airflow directory`
   1. *NOTE*: You may need to restart the set of Docker containers that have Airflow and dbt in order for the new Connection ID to propogate in the services
7. Once that is all setup, you can head into Airflow, run the DAG and watch as the ELT process is orchestrated for you!
