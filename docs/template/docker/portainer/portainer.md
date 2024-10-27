---
tags:
    - docker
    - portainer
---

# Portainer

- [Portainer docs site](https://docs.portainer.io)
- [Portainer CE install](https://docs.portainer.io/start/install-ce/server)
  - [Portainer CE Linux - Docker Standalone](https://docs.portainer.io/start/install-ce/server/docker)

## Running Portainer Server

At least 1 Portainer server must be available for agents to connect to. Copy this script to a file, i.e. `run-portainer.sh`.

!!! note

    Don't forget to set `chmod +x run-portainer.sh`, or execute the script with `bash run-portainer.sh`.

```shell title="run-portainer.sh" linenums="1"
#!/bin/bash

WEBUI_PORT="9000"
## Defaults to 'portainer' if empty
CONTAINER_NAME=
## Defaults to a named volume, portainer_data.
#  Note: create this volume with $ docker volume create portainer_data
DATA_DIR=

echo ""
echo "Checking for new image"
echo ""

docker pull portainer/portainer-ce

echo ""
echo "Restarting Portainer"
echo ""

docker stop portainer && docker rm portainer

docker run -d \
    -p 8000:8000 \
    -p ${WEBUI_PORT:-9000}:9000 \
    --name=${CONTAINER_NAME:-portainer} \
    --restart=unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ${DATA_DIR:-portainer_data}:/data \
    portainer/portainer-ce

```

## Running Portainer Agent

Start a Portainer in agent mode to allow connection from a Portainer server. This setup is done in the Portainer server's webUI.

!!! warning

    It is probably easier to just download the agent script from the Portainer server when you are adding a connection. It offers a command you can run to simplify setup.

```shell title="run-portainer_agent.sh" linenums="1"
#!/bin/bash

echo ""
echo "Checking for new container image"
echo ""

docker pull portainer/agent

echo ""
echo "Restarting Portainer"
echo ""

docker stop portainer-agent && docker rm portainer-agent

docker run -d \
    -p 9001:9001 \
    --name=portainer-agent \
    --restart=unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:latest

```

## My Portainer backup script

Run this script to backup the Portainer `portainer_data` volume. Backup will be placed at `${CWD}/portainer_data_backup`

```shell title="backup_portainer.sh" linenums="1"
#!/bin/bash

# Name of container containing volume(s) to back up
CONTAINER_NAME=${1:-portainer}
THIS_DIR=${PWD}
BACKUP_DIR=$THIS_DIR"/portainer_data_backup"
# Directory to back up in container
CONTAINER_BACKUP_DIR=${2:-/data}
# Container image to use as temporary backup mount container
BACKUP_IMAGE=${3:-busybox}
BACKUP_METHOD=${4:-tar}
DATA_VOLUME_NAME=${5:-portainer-data}

if [[ ! -d $BACKUP_DIR ]]; then
  echo ""
  echo $BACKUP_DIR" does not exist. Creating."
  echo ""

  mkdir -pv $BACKUP_DIR
fi

function RUN_BACKUP () {

  sudo docker run --rm --volumes-from $1 -v $BACKUP_DIR:/backup $BACKUP_IMAGE $2 /backup/backup.tar $CONTAINER_BACKUP_DIR

}

function RESTORE_BACKUP () {

  echo ""
  echo "The restore function is experimental until this comment is removed."
  echo ""
  read -p "Do you want to continue? Y/N: " choice

  case $choice in
    [yY] | [YyEeSs])
      echo ""
      echo "Test print: "
      echo "sudo docker create -v $CONTAINER_BACKUP_DIR --name $DATA_VOLUME_NAME"2" $BACKUP_IMAGE true"
      echo ""
      echo "Test print: "
      echo "sudo docker run --rm --volumes-from $DATA_VOLUME_NAME"2" -v $BACKUP_DIR:/backup $BACKUP_IMAGE tar xvf /backup/backup.tar"
      echo ""

      echo ""
      echo "Compare to original container: "
      echo ""
      echo "Test print: "
      echo "sudo docker run --rm --volumes-from $CONTAINER_NAME -v $BACKUP_DIR:/backup $BACKUP_IMAGE ls /data"
    ;;
    [nN] | [NnOo])
      echo ""
      echo "Ok, nevermind."
      echo ""
    ;;
  esac

}

# Run a temporary container, mount volume to back up, create backup file
case $1 in
  "-b" | "--backup")
  case $BACKUP_METHOD in
    "tar")
      echo ""
      echo "Running "$BACKUP_METHOD" backup using image "$BACKUP_IMAGE
      echo ""

      RUN_BACKUP $CONTAINER_NAME "tar cvf"
    ;;
  esac
  ;;
  "-r" | "--restore")
  ;;
esac

```

## Run Portainer with Docker Compose

!!! note

    I do not use this method. I find it easier to run Portainer with a shell script.

```yaml title="Portainer docker-compose.yml" linenums="1"

version: "3"

services:

  portainer:
    image: portainer/portainer-ce:linux-amd64
    container_name: portainer
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ${PORTAINER_DATA:-./data}:/data

```
