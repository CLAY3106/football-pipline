# Football Data Pipeline (Foundation)

## Overview
This project sets up the foundational infrastructure for a football data pipline.
The current stage focuses on local infrastructure, database initialization, and environment validation. No data ingestion or orchestration logic has been implemented yet.

## Current Status
This repository contains the initial foundation of a football data pipeline.
The focus so far is on **data ingestion setup** and **raw-layer schema generation**.

### Implemented
- Dockerized PostgreSQL database
- Database schema separation (raw, staging, mart)
- Python environment setup with SQLAlchemy
- Connectivity validation between Python and PostgreSQL
- Downloading football datasets from Kaggle
- Inspecting CSV schemas
- Automatically generating PostgreSQL `raw` tables from CSV headers
- Handling non-UTF8 encodings safely (latin1 → UTF-8 in Postgres)
- Reproducible SQL initialization scripts

## Project Structure
```
football-pipeline/
├─ data/
│  └─ raw/ # Kaggle CSV datasets
├─ infra/
│  └─ db/
│     └─ docker-compose.yml
|  └─ init/ #SQL init scripts (schemas, raw tables)
├─ scripts/
│  └─ db_smoke_test.py
│  └─ show_columns.py # Inspect CSV headers
│  └─ generate_raw_sql_all.py # Generate raw-layer SQL automatically
├─ requirements.txt
└─ README.md
```

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
### 1. Project scaffolding
- Create a project folder
```bash
mkdir football-pipeline
cd football-pipeline
mkdir infra
mkdir infra\db
mkdir scripts
```
### 2. Start PostgreSQL
- Create infra/db/docker-compose.yml
- Start Postgres (from docker-compose.yml)
```bash
docker compose -f infra/db/docker-compose.yml up -d
docker ps
```
### 3. Create database schemas
- Create DB schemas (raw/staging/mart)
```bash
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS raw;"
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS staging;"
docker exec -it football_pg psql -U football_user -d football_dw -c "CREATE SCHEMA IF NOT EXISTS mart;"
```
### 4. Verify connection (DBeaver)
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
### 5. Python environment
- Python environment (minimal)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install pandas sqlalchemy psycopg2-binary
```
### 6. Python connectivity test
- Python connection test (1 file): This is a smoke test, not application logic.

### 7. Raw layer design
- One raw table per CSV file
- Column names are normalized automatically
- All columns are stored as `TEXT`
- No transformations are applied at this stage

### 8. Dataset
Downloaded using Kaggle API (not committed):
- Football datasets (CSV format)

## STRUCTURED DATA PIPLINE(FOOTBALL DATA FIRST)
## AIRFLOW ORCHESTRATION (BASIC)
## UNSTRUCTURED DOCUMENTS
## SEARCH LAYER
