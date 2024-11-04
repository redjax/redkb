# Minio S3 Storage

Minio is an implementation of the S3 storage type. You can self host your own S3 storage!

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../data/
    ../alert.rules
    ../prometheus.yml
```

## Container Files

### .env

```text title="minio s3 storage .env" linenums="1"
## Default: admin
MINIO_ROOT_USER=
## Default: minio-devAdmin
MINIO_ROOT_PASSWORD=
## Default: 9000
MINIO_COMM_PORT=
## Default: 9001
MINIO_WEBUI_PORT=
## Default: ./data/minio
MINIO_DATA_DIR=

## Default: ./data/prometheus/prometheus.yml
PROMETHEUS_CONFIG_FILE=
## Default: ./data/prometheus/alert.rules
PROMETHEUS_ALERTMANAGER_RULES_FILE=

```

### .gitignore

```text title="minio s3 storage .gitignore" linenums="1"
data/*
data/prometheus/*

!data/prometheus/

!data/prometheus/example.*
!data/prometheus/example.*.*

!example.*
!example.*.*
!*.example
!*.example.*
!.*.example
!.*.example.*

```

### docker-compose.yml

```text title="minio s3 storage docker-compose.yml" linenums="1"
---
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: minio-prometheus
    volumes:
      - ${PROMETHEUS_CONFIG_FILE:-./data/prometheus/prometheus.yml}:/etc/prometheus/prometheus.yml
      - ${PROMETHEUS_ALERTMANAGER_RULES_FILE:-./data/prometheus/alert.rules}:/alertmanager/alert.rules
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
    ports:
      - "9090:9090"

  minio:
    image: quay.io/minio/minio:latest
    container_name: minio
    command: server /data --console-address ":9001"
    restart: unless-stopped
    environment:
      - MINIO_ROOT_USER=${MINIO_ROOT_USER:-admin}
      - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD:-minio-devAdmin}
      ## Should only be enabled for a local minio instance. Use bearer tokens in prod
      - MINIO_PROMETHEUS_AUTH_TYPE="public"
      - MINIO_PROMETHUS_URL="prometheus:9090"
    ports:
      - ${MINIO_COMM_PORT:-9000}:9000
      - ${MINIO_WEBUI_PORT:-9001}:9001
    volumes:
      - ${MINIO_DATA_DIR:-./data/minio}:/data

  watchtower:
    image: containrrr/watchtower
    container_name: minio-watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

```

### data/prometheus/alert.rules

```text title="alert.rules" linenums="1"
groups:
- name: example
  rules:

  ## Alert for any instance unreachable for >5 mins
  - alert: InstanceDown
    expr: up == 0
    for: 5m

```

### data/prometheus/prometheus.yml

```yaml title="prometheus.yml" linenums="1"
global:
  scrape_interval: 15s

rule_files:
- "/alertmanager/alert.rules"

scrape_configs:
  - job_name: "minio-cluster"
    ## This can be omitted if MinIO has env variable:
    #    MINIO_PROMETHEUS_AUTH_TYPE="public"
    # bearer_token: TOKEN
    metrics_path: /minio/v2/metrics/cluster
    scheme: https
    static_configs:
    - targets: ["minio:9001"]

  - job_name: "minio-nodes"
    ## This can be omitted if MinIO has env variable:
    #    MINIO_PROMETHEUS_AUTH_TYPE="public"
    # bearer_token: TOKEN
    metrics_path: /minio/v2/metrics/node
    scheme: https
    static_configs:
    - targets: ["minio:9001"]

  - job_name: "minio-bucket"
    ## This can be omitted if MinIO has env variable:
    #    MINIO_PROMETHEUS_AUTH_TYPE="public"
    # bearer_token: TOKEN
    metrics_path: /minio/v2/metrics/bucket
    scheme: https
    static_configs:
    - targets: ["minio:9001"]

  - job_name: "minio-resource"
    ## This can be omitted if MinIO has env variable:
    #    MINIO_PROMETHEUS_AUTH_TYPE="public"
    # bearer_token: TOKEN
    metrics_path: /minio/v2/metrics/resource
    scheme: https
    static_configs:
    - targets: ["minio:9001"]

```

## Notes

This container includes `prometheus` for monitoring/logging. If you use the `prometheus` container, you *must* create the `data/prometheus/` directory and manually create an `alert.rules` and `prometheus.yml` within.

## Links
