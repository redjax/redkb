# Redis

Dockerized Redis database server. Redis is a key/value store that can act as a powerful cache or in-memory database.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="redis .env" linenums="1"
## Default: redis
REDIS_CONTAINER_NAME=
## Default: ./data/redis
REDIS_CACHE_DIR=
## Default: 6379
REDIS_PORT=

## Default: redis-commander
REDIS_COMMANDER_CONTAINER_NAME=
## Default: 8081
REDIS_COMMANDER_PORT=

```

### .gitignore

```text title="redis .gitignore" linenums="1"
data/*

```

### docker-compose.yml

```text title="redis docker-compose.yml" linenums="1"
---
services:
  redis:
    ## Fix "overcommit memory" warning
    #  https://ourcodeworld.com/articles/read/2083/how-to-remove-redis-warning-on-docker-memory-overcommit-must-be-enabled
    #  https://r-future.github.io/post/how-to-fix-redis-warnings-with-docker/
    image: redis
    container_name: ${REDIS_CONTAINER_NAME:-redis}
    restart: unless-stopped
    command: redis-server --save 20 1 --loglevel verbose
    volumes:
      - ${REDIS_CACHE_DIR:-./data/redis}:/data
    expose:
      - 6379
    ports:
      - ${REDIS_PORT:-6379}:6379
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
      interval: 1s
      timeout: 3s
      retries: 5

  # redis-commander:
  #   image: rediscommander/redis-commander:latest
  #   container_name: ${REDIS_COMMANDER_CONTAINER_NAME:-redis-commander}
  #   hostname: redis-commander
  #   restart: unless-stopped
  #   environment:
  #     - REDIS_HOSTS=local:redis:${REDIS_PORT:-6379}
  #   ports:
  #     - ${REDIS_COMMANDER_PORT:-8081}:8081

```

## Notes

`...`

## Links

- [link1](#)
