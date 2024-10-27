# MariaDB

Dockerized MariaDB database server.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="mariadb .env" linenums="1"
## Default: mysql
MYSQL_ROOT_PASSWORD=
## Default: mysql
MYSQL_DATABASE=
## Default: mysql
MYSQL_USER=
## Default: mysql
MYSQL_PASSWORD=
## Default: ./data/db
MYSQL_DATA_DIR=
## Default: ./data/docker-entrypoint
MYSQL_SCRIPT_INIT_DIR=
## Default: 3306
MYSQL_DB_PORT=

```

### .gitignoree

```text title="mariadb .gitignore" linenums="1"
backup/
backup/*
backup/**
backup/**/
backup/**/*
backup/**/**

```

### docker-compose.yml

```text title="mariadb docker-compose.yml" linenums="1"
---
services:
  mariadb:
    image: mariadb
    container_name: medcab_db-practice
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-mysql}
      MYSQL_DATABASE: ${MYSQL_DATABASE:-mysql}
      MYSQL_USER: ${MYSQL_USER:-mysql}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-mysql}
    volumes:
      - ${MYSQL_DATA_DIR:-./data/db}:/var/lib/mysql
      ## Add SQL scripts to this directory to automatically execute them when the container starts
      - ${MYSQL_SCRIPT_INIT_DIR:-./data/docker-entrypoint}:/docker-entrypoint-initdb.d
    ports:
      - "${MYSQL_DB_PORT:-3306}:3306"

```

## Notes

## Links
