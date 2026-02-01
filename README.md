# Football Data Pipline (initial Setup)

## Overview
This project sets up the foundational infrastructure for a football data pipline.
The current stage focuses on local infrastructure, database initialization, and environment validation. No data ingestion or orchestration logic has been implemented yet.

## Current Status

### Implemented
- Dockerized PostgreSQL database
- Database schema separation (raw, staging, mart)
- Python environment setup with SQLAlchemy
- Connectivity validation between Python and PostgreSQL

### Not Implemented Yet
- Data ingestion pipelines
- Airflow DAGs
- Data transformations
- OCR or search components

## Project Structure
football-pipeline/
├─ .venv/                # Project-level Python virtual environment
├─ infra/
│  └─ db/
│     └─ docker-compose.yml
├─ scripts/
│  └─ db_smoke_test.py
└─ README.md

## Infrastructure
### Database
- PostgreSQL running in Docker
- Persistent volume for data storage
- Schemas created:
    - raw - source data
    - staging = cleaned/intermediate data
    - mart - analytics-ready tables
### Tools
- Docker
- PostgreSQL
- Python
- SQLAlchemy
- psycoqg2
- DBeaver (for inspection and validation)

## ENVIRONMENT SETUP:
- Create a project folder
```bash
mkdir football-pipeline
cd football-pipeline
mkdir infra
mkdir infra\db
mkdir scripts
```
- Create infra/db/docker-compose.yml
- Start Postgres (from docker-compose.yml)
```bash
docker compose -f infra/db/docker-compose.yml up -d
docker ps
```
- Create DB schemas (raw/staging/mart)
```bash
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS raw;"
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS staging;"
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS mart;"
```
- Verify connection using DBeaver
    + Host: localhost
    + Port: 5432
    + Database: football_dw
    + Username: football_user
    + Password: football_pass
* Test the connection with this SQL in DBeaver
```SQL
SELECT current_database(), current_user;
SELECT schema_name FROM information_schema.schemata
WHERE schema_name IN ('raw','staging','mart');
```
- Python environment (minimal)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install pandas sqlalchemy psycopg2-binary
```
- Python connection test (1 file): This is a smoke test, not application logic.

## STRUCTURED DATA PIPLINE(FOOTBALL DATA FIRST)
## AIRFLOW ORCHESTRATION (BASIC)
## UNSTRUCTURED DOCUMENTS
## SEARCH LAYER