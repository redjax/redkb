# Mosquitto

An open source message broker like RabbitMQ. Mosquitto is simpler and more lightweight than RabbitMQ and better suited for devices like a Raspberry Pi.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../mosquitto-host-setup.sh
  ../config/mosquitto
    ../ mosquitto.conf
```

## Container Files

### .env

```text title="mosquitto .env" linenums="1"
## Default: mosquitto
MQTT_CONTAINER_NAME=
## Default: 1883
MQTT_PORT=
## Default: 9001
MQTT_HTTP_PORT=
## Default: ./config/mosquitto
MQTT_CONFIG_DIR=
## Default: ./data/mosquitto
MQTT_DATA_DIR=
## Default: ./logs/mosquitto
MQTT_LOGS_DIR=
## Default: America/New_York
TZ=
## Default: 1883
PUID=
## Default: 1883
PGID=

```

### .gitignore

```text title="mosquitto .gitignore" linenums="1"
data/*
config/*

!*.example
!*.example.*
!.*.example
!.*.example.*

```

### docker-compose.yml

```text title="mosquitto docker-compose.yml" linenums="1"
---
networks:
  default:
    name: mqtt-network

services:
  mosquitto:
    image: eclipse-mosquitto
    container_name: ${MQTT_CONTAINER_NAME:-mosquitto}
    restart: unless-stopped
    env_file: ./.env
    stdin_open: true
    tty: true
    # network_mode: "host"
    ports:
      - ${MQTT_PORT:-1883}:1883
      - ${MQTT_HTTP_PORT:-9001}:9001
    volumes:
      - ${MQTT_CONFIG_DIR:-./config/mosquitto}:/mosquitto/config:rw
      - ${MQTT_DATA_DIR:-./data/mosquitto}:/mosquitto/data:rw
      - ${MQTT_LOGS_DIR:-./logs/mosquitto}:/mosquitto/log:rw
    environment:
      TZ: ${TZ:-America/New_York}
    user: "${PUID:-1883}:${PGID:-1883}"

```

### mosquitto-host-setup.sh

```shell title="mosquitto-host-setup.sh" linenums="1"
#!/bin/bash

## https://pimylifeup.com/home-assistant-docker-compose/#creating-a-user-for-the-mosquitto-docker-container

if [[ ! $(getent passwd "mosquitto" 2>&1) ]]; then

    echo "Creating mosquitto user"
    sudo useradd -u 1883 -g 1883 mosquitto

fi

if [[ ! $(getent group mosquitto /dev/null 2>&1) ]]; then
    echo "Creating mosquitto group"
    sudo groupadd -g 1883 mosquitto
fi

if [[ ! -d ./config/mosquitto ]]; then
    echo "Creating config dir"
    mkdir -pv ./config/mosquitto
fi

if [[ ! -d ./data/mosquitto ]]; then
    echo "Creating mosquitto data dir"
    mkdir -pv ./data/mosquitto
fi

if [[ ! -d ./logs/mosquitto ]]; then
    echo "Creating mosquitto logs directory"
    mkdir -pv ./logs/mosquitto
fi

if [[ ! -f ./logs/mosquitto/mosquitto.log ]]; then
    echo "Creating empty mosquitto log file."
    touch ./logs/mosquitto/mosquitto.log
fi

if [[ ! -f ./config/mosquitto/mosquitto.conf ]]; then
    echo "Creating config file"

    ## Create mosquitto conf file & echo config into it
    cat <<EOF >./config/mosquitto/mosquitto.conf
allow_anonymous true
# password_file /mosquitto/config/pwfile
listener        1883 0.0.0.0
listener        9001 0.0.0.0
protocol websockets
persistence     true
persistence_file mosquitto.db
persistence_location /mosquitto/data/
log_type subscribe
log_type unsubscribe
log_type websockets
log_type error
log_type warning
log_type notice
log_type information
log_dest        file /mosquitto/log/mosquitto.log
EOF

    # sudo chmod 0700 ./config/mosquitto/mosquitto.conf

fi

if [[ ! -f ./data/mosquitto/mosquitto.db ]]; then
    echo "Creating empty mosquitto.db database file for container"
    touch ./data/mosquitto/mosquitto.db

    # sudo chown 1883:1883 mosquitto.db
    sudo chmod 0700 ./data/mosquitto/mosquitto.db
fi

echo "Setting owner of ./data, ./logs, ./config to 1883:1883"
declare -a chmod_dirs=(./data ./logs ./config)
for d in "${chmod_dirs[@]}"; do
    sudo chmod o+w ./logs/mosquitto/mosquitto.log
    sudo chown -R 1883:1883 "${d}"
done

```

### config/mosquitto/mosquitto.conf

```conf title="mosquitto.conf" linenums="1"
 allow_anonymous  true
# password_file /mosquitto/config/pwfile
 listener         1883 0.0.0.0
 listener         9001 0.0.0.0
 protocol         websockets
 persistence      true
 persistence_file mosquitto.db
persistence_location /mosquitto/data/
 log_type         subscribe
 log_type         unsubscribe
 log_type         websockets
 log_type         error
 log_type         warning
 log_type         notice
 log_type         information
 log_dest         file /mosquitto/log/mosquitto.log

```

## Notes

## Links
