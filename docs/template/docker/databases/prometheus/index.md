# Prometheus

Prometheus is equal parts database, logging server, and monitoring/alerting. It's a very useful tool for many use cases, for example as a backend for Grafana.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../data/prometheus
    ../alert.rules
    ../prometheus.yml
```

## Container Files

### .env

```text title="prometheus .env" linenums="1"
## Default: 9090
PROMETHEUS_WEBUI_PORT=
## Default: ./data/prometheus/prometheus.yml
PROMETHEUS_CONFIG_FILE=
## Default: ./data/prometheus/alert.rules
PROMETHEUS_ALERTMANAGER_RULES_FILE=

```

### .gitignore

```text title="prometheus .gitignore" linenums="1"
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

```text title="prometheus docker-compose.yml" linenums="1"
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
      - ${PROMETHEUS_WEBUI_PORT:-9090}:9090

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

- The `data/prometheus/` directory (and the files within, `alert.rules` and `prometheus.yml`) do not exist by default, you must create them before starting the container.

## Links
