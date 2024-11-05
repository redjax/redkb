# RabbitMQ

RabbitMQ is a messaging/event queue broker, useful for asynchronous processing and PUB/SUB architecture.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../provision/
    ../rabbitmq.config
    ../rabbitmq.enabled_plugins
```

## Container Files

### .env

```text title="rabbitmq .env" linenums="1"
## Default: rabbitmq
RABBITMQ_CONTAINER_NAME=
## Default: rabbitmq
RABBITMQ_USER=
## Default: rabbitmq
RABBITMQ_PASS=
## Default: 5672
RABBITMQ_AMPQ_PORT=
## Default: 15672
RABBITMQ_HTTP_PORT=
## Default: ./data/rabbitmq
RABBITMQ_DATA_DIR=
## Default: ./logs/rabbitmq
RABBITMQ_LOGS_DIR=
## Default: ./provision/rabbitmq.config
RABBITMQ_CONFIG_FILE=
## Default: ./provision/rabbitmq.enabled_plugins
RABBITMQ_ENABLED_PLUGINS_FILE=

```

### .gitignore

```text title="rabbitmq .gitignore" linenums="1"
provision/*

!*.example
!*.example.*
!example.*
!.example.*
!example.*
!example.*.*

```

### docker-compose.yml

```text title="rabbitmq docker-compose.yml" linenums="1"
---
services:
  rabbitmq:
    image: rabbitmq:management
    container_name: ${RABBITMQ_CONTAINER_NAME:-rabbitmq}
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-rabbitmq}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS:-rabbitmq}
      # RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_VHOST:-rabbitmq}
      # RABBITMQ_ENABLED_PLUGINS_FILE: /etc/rabbitmq/enabled_plugins
    ports:
      ## AMQP protocol
      - ${RABBITMQ_AMPQ_PORT:-5672}:5672
      - ${RABBITMQ_HTTP_PORT:-15672}:15672
    volumes:
      - ${RABBITMQ_DATA_DIR:-./data/rabbitmq}:/var/lib/rabbitmq
      - ${RABBITMQ_LOGS_DIR:-./logs/rabbitmq}:/var/log/rabbitmq
      - ${RABBITMQ_CONFIG_FILE:-./provision/rabbitmq.config}:/etc/rabbitmq/rabbitmq.config
      - ${RABBITMQ_ENABLED_PLUGINS_FILE:-./provision/rabbitmq.enabled_plugins}:/etc/rabbitmq/enabled_plugins
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 30s
      retries: 3

```

### provision/rabbitmq.config

```text title="rabbitmq.config" linenums="1"
[
  {rabbit, [
    {queue_index_max_journal_entries, 10000},
    {vm_memory_high_watermark, 0.4},
    {disk_free_limit, {mem_relative, 0.1}}
  ]}
].
```

### provision/rabbitmq.enabled_plugins

```text title="rabbitmq.enabled_plugins" linenums="1"
[rabbitmq_management,rabbitmq_prometheus].
```

## Notes

- The `rabbitmq.config` and `rabbitmq.enabled_plugins` files are not required.
    - These files allow you to modify RabbitMQ's container runtime, installing plugins like `rabbitmq_management` (for a webUI), or modifying RabbitMQ's parameters on free disk space & memory usage.
    - If you do *not* create these files, RabbitMQ will run with its predefined defaults.

## Links
