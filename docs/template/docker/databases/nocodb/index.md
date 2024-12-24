---
tags:
  - docker
  - templates
  - database
  - nocodb
  - nocode
---

# NocoDB

A free, open-source, self-hostable alternative to [Airtable](https://airtable.com)

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="nocodb .env" linenums="1"
## Default: 8080
NOCODB_HTTP_PORT=
## Default: (named volume) nocodb_data
NOCODB_DATA_DIR=

## Default: postgres
POSTGRES_USER=
## Default: password
POSTGRES_PASSWORD=
## Default: root_db
POSTGRES_DATABASE=
## Default: (named volume) nocodb_db_data
POSTGRES_DATA_DIR=

```

### .gitignore

```text title="nocodb .gitignore"
nocodb/data/

```

### docker-compose.yml

```text title="nocodb docker-compose.yml" linenums="1"
---
volumes: 
  nocodb_db_data: {}
  nocodb_data: {}

networks:
  nocodb_net: {}

services: 
  nocodb:
    image: "nocodb/nocodb:latest"
    container_name: nocodb
    restart: unless-stopped
    depends_on: 
      postgres: 
        condition: service_healthy
    environment: 
      NC_DB: "pg://${POSTGRES_USER:-postgres}:5432?u=${POSTGRES_USER:-postgres}&p=${POSTGRES_PASSWORD:-password}&d=${POSTGRES_DATABASE:-root_db}"
    ports: 
      - ${NOCODB_HTTP_PORT:-8080}:8080
    volumes: 
      - ${NOCODB_DATA_DIR:-nocodb_data}:/usr/app/data"
    networks:
      - nocodb_net

  postgres:
    image: postgres
    container_name: nocodb_db
    restart: unless-stopped
    environment: 
      POSTGRES_USER: ${POSTGRES_USERNAME:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DATABASE:-root_db}
    healthcheck: 
      interval: 10s
      retries: 10
      test: "pg_isready -U \"$$POSTGRES_USER\" -d \"$$POSTGRES_DATABASE\""
      timeout: 2s
    volumes: 
      - ${POSTGRES_DATA_DIR:-nocodb_db_data}:/var/lib/postgresql/data
    networks:
      - nocodb_net

```

## Notes

### Usage

- Create your `docker-compose.yml`, `.env`, and `.gitignore` files.
- Edit the `.env` and set a new password for the Postgres database (in the `POSTGRES_PASSWORD` variable).
- Run `docker compose up -d`
- Navigate to `http://your-ip:nocodb-port` to open the admin setup page

## Links

- [NocoDB Github](https://github.com/nocodb/nocodb)
- [NocoDB Website](https://nocodb.com)
- [NocoDB Documentation](https://docs.nocodb.com)
