# InfluxDB

Dockerized InfluxDB database server. InfluxDB is a special purpose time-series database.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../grafana
    ../datasource.yml
    ../grafana.ini
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="influxdb .env" linenums="1"
## Default: influxdb
INFLUXDB_CONTAINER_NAME=
## Default: 8086
INFLUXDB_HTTP_PORT=
## Default: setup
INFLUXDB_INIT_MODE=
## Default: admin
INFLUXDB_INIT_USERNAME=
## Default: influxAdmin
INFLUXDB_INIT_PASSWORD=
## Default: influxDefault
INFLUXDB_INIT_ORG=
## Default: influxDefaultBucket
INFLUXDB_INIT_BUCKET=
## Default: ./data
INFLUXDB_DATA_DIR=
## Default: ./config
INFLUXDB_CONFIG_DIR=

## Default: grafana
GRAFANA_CONTAINER_NAME=
## Default: 3000
GRAFANA_HTTP_PORT=
## Default: ./grafana/data
GRAFANA_DATA_DIR=

```

### .gitignore

```text title="influxdb .gitignore" linenums="1"
grafana/*

!**/*.example
!**/*.example.*
!**/.*.example
!**/.*.example.*

data/*

```

### docker-compose.yml

```text title="influxdb docker-compose.yml" linenums="1"
---
networks:
  influx-net:
    external: true

volumes:
  grafana_data:

services:
  influxdb:
    image: influxdb:2
    container_name: ${INFLUXDB_CONTAINER_NAME:-influxdb}
    restart: unless-stopped
    ports:
      - ${INFLUXDB_HTTP_PORT:-8086}:8086
    environment:
      DOCKER_INFLUXDB_INIT_MODE: ${INFLUXDB_INIT_MODE:-setup}
      DOCKER_INFLUXDB_INIT_USERNAME: ${INFLUXDB_INIT_USERNAME:-admin}
      DOCKER_INFLUXDB_INIT_PASSWORD: ${INFLUXDB_INIT_PASSWORD:-influxAdmin}
      DOCKER_INFLUXDB_INIT_ORG: ${INFLUXDB_INIT_ORG:-influxDefault}
      DOCKER_INFLUXDB_INIT_BUCKET: ${INFLUXDB_INIT_BUCKET:-influxDefaultBucket}
    volumes:
      - ${INFLUXDB_DATA_DIR:-./data}:/var/lib/influxdb2
      - ${INFLUXDB_CONFIG_DIR:-./config}:/etc/influxdb2
    networks:
      - influx-net

  grafana:
    image: grafana/grafana
    container_name: ${GRAFANA_CONTAINER_NAME:-grafana}
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASS:-grafana}
      - GF_USERS_ALLOW_SIGN_UP=${GRAFANA_ALLOW_USER_SIGNUP:-false}
    ports:
      - "${GRAFANA_HTTP_PORT:-3000}:3000"
    depends_on:
      - influxdb
    volumes:
      - ${GRAFANA_DATA_DIR:-./grafana/data}:/var/lib/grafana
      - ${GRAFANA_CONF_FILE:-./grafana/grafana.ini}:/etc/grafana/grafana.ini
      - ${GRAFANA_DATASOURCE_FILE:-./grafana/datasource.yml}:/etc/grafana/provisioning/datasources/datasource.yml
    networks:
      - influx-net

```

### grafana/datasource.yml

```yaml title="influxdb grafana/datasource.yml" linenums="1"
apiVersion: 1

datasources:

- name: InfluxDB
  type: influxdb
  access: proxy
  url: http://influxdb:8086
  isDefault: true
  editable: true
  user: admin
  jsonData:
    version: Flux
    organization: null
    dbName: null
    tlsSkipVerify: true
    insecureGrpc: true
  secureJsonData:
    token: null

```

### grafana/grafana.ini

```ini title="influxdb grafana/grafana.ini" linenums="1"
[paths]
provisioning = /etc/grafana/provisioning

[server]
enable_gzip = true
# To add HTTPS support:	
#protocol = https	
#;http_addr =	
#http_port = 3000	
#domain = localhost	
#enforce_domain = false	
#root_url = https://localhost:3000	
#router_logging = false	
#static_root_path = public	
#cert_file = /etc/certs/cert.pem	
#cert_key = /etc/certs/cert-key.pem

[security]
# If you want to embed grafana into an iframe for example
allow_embedding = true

[users]
default_theme = dark

```

## Notes

`...`

## Links

- [link1](#)
