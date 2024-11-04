# NGINX Proxy Manager

A GUI application for managing an NGINX reverse proxy server.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../backup_nginx-proxy-manager.sh
  ../fix_watchtower_permissions.sh
  ../safe_update.sh
```

## Container Files

### .env

```text title="nginx proxy manager .env" linenums="1"
## Default: ./data
NPM_DATA_DIR=
## Default: ./letsencrypt
NPM_LETSENCRYPT_DIR=

```

### .gitignore

```text title="nginx proxy manager .gitignore" linenums="1"
logs/
.env

```

### docker-compose.yml

```text title="nginx proxy manager docker-compose.yml" linenums="1"
---
services:

  app:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: npm_proxy
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ${NPM_DATA_DIR:-./data}:/data
      - ${NPM_LETSENCRYPT_DIR:-./letsencrypt}:/etc/letsencrypt
    labels:
      - "com.centurylinklabs.watchtower.enable=true"

  watchtower:
    image: containrrr/watchtower
    container_name: npm_proxy_watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
    environment:
      ## Remove old images after updating
      WATCHTOWER_CLEANUP: ${WATCHTOWER_CLEANUP:-"true"}
      ## Check for updates once every 24h
      WATCHTOWER_POLL_INTERVAL: ${WATCHTOWWER_POLL_INTERVAL:-86400}
    command: --label-enable

```

### backup_nginx-proxy-manager.sh

```shell title="backup_nginx-proxy-manager.sh" linenums="1"
#!/bin/bash

## Make a backup of the Nginx Proxy Manager directory.

timestamp() { date +"%Y-%m-%d_%H:%M"; }

BACKUP_DEST="${HOME}/backup/nginx_proxy_manager"
SRC_PATH="/home/${USER}/git/docker_templates/templates/docker_nginx-proxy-manager/new-version"
TAR_PATH="${BACKUP_DEST}/backup_${HOSTNAME}_nginx-proxy-manager_$(timestamp).tar.gz"

function make_backup() {
  echo "Backing up source path: ${SRC_PATH}"
  echo "  To destination: ${TAR_PATH}"

  sudo tar czvf "${TAR_PATH}" "${SRC_PATH}"

}

function fix_dest_dir_permissions() {
  sudo chown -R ${USER}:${USER} "${BACKUP_DEST}"
}

function main() {
  if [[ ! -d "${BACKUP_DEST}" ]]; then
    sudo mkdir -pv "${BACKUP_DEST}"
    fix_dest_dir_permissions
  fi

  make_backup

  echo "Fixing permissions on output file: ${TAR_PATH}"
  fix_dest_dir_permissions
}

main

```

### fix_watchtower_permissions.sh

```shell title="fix_watchtower_permissions.sh" linenums="1"
#!/bin/bash

##
# Allow watchtower container to interact with docker daemon
# to remove images and pull updates/restart containers.
##

USER=${USER}

echo "Granting watchtower container permissions to interact with the Docker daemon."

sudo setfacl --modify user:${USER}:rw /var/run/docker.sock

```

### safe_update.sh

```shell title="safe_update.sh" linenums="1"
#!/bin/bash

DATA_DIR="data"
DATA_BAK_DIR="data.bak"

function check_path_exists() {
  if [[ -d "${1}" ]]; then
    # echo "Path '${1}' exists"
    return 0
  else
    # echo "Path '${1}' does not exist"
    return 1
  fi
}

function main() {
  ## 0=exists, 1=not exists
  BAK_DIR_EXISTS=$(check_path_exists "${DATA_BAK_DIR}")

  if [[ $BAK_DIR_EXISTS -eq 0 ]]; then
    echo "$DATA_BAK_DIR exists"
  else
    echo "$DATA_BAK_DIR does not exist"
  fi
}

main

```

## Notes

## Links
