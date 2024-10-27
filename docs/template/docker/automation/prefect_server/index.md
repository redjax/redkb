---
tags:
  - docker
  - templates
  - automation
  - python
  - data
---

# Prefect

[`prefect`](https://www.prefect.io) is a Python library for automating data workflows/pipelines. A lighter, more beginner-friendly analogue to [Apache `airflow`](https://airflow.apache.org).

This container is the server & database for `prefect`. You still need to write Python code to interact with the pipelines.

Visit the web UI at port `4200`. This is a dashboard where you can see pipelines/flows you've written and executed.

## Directory Structure

```text title="Container directory structure"
docker_prefect_server/
  ../postgres/
    ../pg_entrypoint/
      ../`pg_entrypoint.sh`
  ../prefect/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### docker-compose.yml

```yaml title="prefect docker-compose.yml" linenums="1"
---
networks:
  prefect_net:

services:
  prefect:
    image: prefecthq/prefect:2-python3.11
    restart: unless-stopped
    container_name: prefect-server
    env_file: .env
    entrypoint: ["prefect", "server", "start"]
    volumes:
      - ${PREFECT_DATA_DIR:-./prefect/data}:/root/.prefect
    ports:
      - ${PREFECT_WEBUI_PORT:-4200}:4200
    environment:
      PREFECT_SERVER_API_HOST: 0.0.0.0
      PREFECT_UI_URL: http://prefect:4200/api
      PREFECT_API_URL: http://prefect:4200/api
      PREFECT_API_DATABASE_CONNECTION_URL: ${PREFECT_DB_URL:-postgresql+asyncpg://postgres:postgres@prefect-db/prefect}
      PREFECT_API_DATABASE_ECHO: ${PREFECT_DB_ECHO:-false}
      PREFECT_API_DATABASE_MIGRATE_ON_START: ${PREFECT_MIGRATE_ON_START:-true}
    depends_on:
      - prefect-db
    networks:
      - prefect_net

  prefect-db:
    image: postgres:latest
    container_name: prefect-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DATABASE:-prefect}
      POSTGRES_HOST_AUTH_METHOD: ${POSTGRES_HOST_AUTH_METHOD}
    expose:
      - 5432
    ports:
      - ${POSTGRES_PORT:-5432}:5432
    volumes:
      - ${POSTGRES_DATA_DIR:-./postgres/data}:/var/lib/postgresql/data
      - ./postgres/pg_entrypoint:/docker-entrypoint-initdb.d
    networks:
      - prefect_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

```

### .env

```text title="prefect .env" linenums="1"
## Default: ./prefect/data
PREFECT_DATA_DIR=
## Default: 4200
PREFECT_WEBUI_PORT=
## postgresql+asyncpg://postgres:postgres@prefect-db/prefect
PREFECT_DB_URL=
## Default: false
PREFECT_DB_ECHO=
## Default: true
PREFECT_MIGRATE_ON_START=

## Default: postgres
POSTGRES_USER=
## Default: postgres
POSTGRES_PASSWORD=
## Default: ./postgres/data
POSTGRES_DATA_DIR=
## Default: 5432
POSTGRES_PORT=
## Default: empty/None
POSTGRES_HOST_AUTH_METHOD=
## Default: prefect
POSTGRES_DATABASE=

```

### .gitignore

```.gitignore title="prefect .gitignore" linenums="1"
prefect/data
postgres/data

```

### postgres/pg_entrypoint/pg_entrypoint.sh

```sh title="prefect pg_entrypoint.sh" linenums="1"
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$POSTGRES_DB" <<-EOSQL
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   CREATE EXTENSION IF NOT EXISTS "pg_trgm";
EOSQL

```

## Notes

## Links

- [Prefect Docs: Quickstart](https://docs.prefect.io/3.0/get-started/index)
- [Deploying Prefect with Docker Compose](https://htdocs.dev/posts/deploying-prefect-with-docker-compose-a-comprehensive-guide/)
