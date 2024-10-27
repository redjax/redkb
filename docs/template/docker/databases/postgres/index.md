---
tags:
    - docker
    - templates
    - database
    - postgres
---

# Postgresql

Dockerized PostgreSQL database server.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../pg_entrypoint
    ../pg_entrypoint.sh
  ../.env
  ../.gitignore
  ../docker-compose.yml

```

## Container Files

### .env

```text title="postgresql .env" linenums="1"
container_dir/
############
# POSTGRES #
############

# Default: "bullseye". Tag for docker image (i.e. <image>:<tag>).
#   https://hub.docker.com/_/postgres/?tab=tags
POSTGRES_IMAGE_TAG=

# Default: postgres
POSTGRES_CONTAINER_NAME=

# Default: postgres
POSTGRES_USER=
# Default: postgres
POSTGRES_PASSWORD=

# Default: named volume "postgres_data"
POSTGRES_DATA_DIR=

# Default: 5432
POSTGRES_PORT=

# Default: unset
# Read section on this variable in docker docs before setting:
#   https://hub.docker.com/_/postgres/
POSTGRES_HOST_AUTH_METHOD=

###########
# PGADMIN #
###########

# Default: latest
#   https://hub.docker.com/r/dpage/pgadmin4/tags
PGADMIN_IMAGE_TAG=

# Default: pgadmin
PGADMIN_CONTAINER_NAME=

# Default: admin@example.com
PGADMIN_DEFAULT_EMAIL=

# Default: pgadmin
PGADMIN_DEFAULT_PASSWORD=

# Default: 80
PGADMIN_LISTEN_PORT=

# Default: 15432
PGADMIN_PORT=

# Default: named volume "pgadmin_data"
PGADMIN_DATA_DIR=

```

### docker-compose.yml

```text title="postgresql docker-compose.yml
---
volumes:
  postgres_data:
  pgadmin_data:

networks:
  pg_net:

services:

  postgres:
    image: postgres:${POSTGRES_IMAGE_TAG:-bullseye}
    container_name: ${POSTGRES_CONTAINER_NAME:-postgres}
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      # Read section on this variable in docker docs before setting:
      #   https://hub.docker.com/_/postgres/
      POSTGRES_HOST_AUTH_METHOD: ${POSTGRES_HOST_AUTH_METHOD}
    expose:
      - 5432
    ports:
      - ${POSTGRES_PORT:-5432}:5432
    volumes:
      - ${POSTGRES_DATA_DIR:-postgres_data}:/var/lib/postgresql/data
      # Mount directory with init scripts for docker, i.e. install UUID extension
      - ./pg_entrypoint:/docker-entrypoint-initdb.d/
      # Mount directory to store SQL scripts
      - ${POSTGRES_SCRIPTS_DIR:-./pgsql_scripts}:/scripts
      # Uncomment line below to restore a database backup.
      # - ${POSTGRES_DB_BACKUP}:/path/here
    networks:
      - pg_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 1s
      timeout: 5s
      retries: 10

  pgadmin:
    image: dpage/pgadmin4:${PGADMIN_IMAGE_TAG:-latest}
    container_name: ${PGADMIN_CONTAINER_NAME:-pgadmin}
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-pgadmin}
      PGADMIN_LISTEN_PORT: ${PGADMIN_LISTEN_PORT:-80}
    ports:
      - ${PGADMIN_PORT:-15432}:80
    volumes:
      - ${PGADMIN_DATA_DIR:-pgadmin_data}:/var/lib/pgadmin
    depends_on:
      - postgres
    networks:
      - pg_net


```

### pg_entrypoint/pg_entrypoint.sh

```text title="pg_entrypoint.sh" linenums="1"
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$POSTGRES_DB" <<-EOSQL
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL

```

## Notes

## Links

- [How to backup/restore (migrate) docker named volumes](https://www.youtube.com/watch?v=ZEy8iFbgbPA)
- [Helpful docker command cheat sheet](https://github.com/xcad2k/cheat-sheets/blob/main/infrastructure/docker/docker-cli.md)
