# Uptime Kuma

A simple but powerful uptime monitor.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

`...`

### .env

```text title="uptime kuma .env" linenums="1"
## Default: 3001
UPTIME_KUMA_PORT=
## Default: named volume "uptime_kuma_data"
UPTIME_KUMA_DATA_DIR=

```

### .gitignore

```text title="uptime kuma .gitignore" linenums="1"
**/data

```

### docker-compose.yml

```text title="uptime kuma docker-compose.yml" linenums="1"
---
volumes:
  uptime_kuma_data:

services:

  uptime-kuma:
    image: louislam/uptime-kuma
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - ${UPTIME_KUMA_PORT:-3001}:3001
    volumes:
      - ${UPTIME_KUMA_DATA_DIR:-uptime_kuma_data}:/app/data

```

## Notes

## Links
