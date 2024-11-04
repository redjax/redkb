# Unifi Controller

Dockerized version of the Unifi Controller software (alternative to using their CloudKey).

!!! warning

    The [LinuxServer container I have been using is no longer supported](https://github.com/linuxserver/docker-unifi-controller).

    Please do not use the template on this page until this message is removed, indicating I have updated my template to use [the new container from LinuxServer](https://github.com/linuxserver/docker-unifi-network-application).

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../update-controller-container.sh
```

## Container Files

### .env

```text title="unifi controller .env" linenums="1"
UNIFI_CONF_DIR=
UNIFI_INFORM_DIR=
UNIFI_WEB_PORT=443
UNIFI_GUEST_HTTP_PORT=
UNIFI_GUEST_HTTPS_PORT=

```

### .gitignore

```text title="unifi controller .gitignore" linenums="1"
config/

```

### docker-compose.yml

```text title="unifi controller docker-compose.yml" linenums="1"
---
# networks:
#   watchtower:
#     external: true

services:

  unifi-controller:
    image: ghcr.io/linuxserver/unifi-controller
    # image: ghcr.io/linuxserver/unifi-controller:7.1.65
    container_name: unifi-controller
    restart: always
    environment:
      - PUID=1000
      - PGID=1000
      # - MEM_LIMIT=768M #optional
    volumes:
      # - ./unifi-controller/config:/config
      - ${UNIFI_CONF_DIR:-./config}:/config
    ports:
      - 3478:3478/udp # STUN
      - 10001:10001/udp # AP discovery
      - ${UNIFI_INFORM_PORT:-8080}:8080 # Device comm., i.e. set-inform
      - ${UNIFI_WEB_PORT:-8443}:8443  # web admin
      - 1900:1900/udp # optional, "make controller discoverable on L2 network
      - ${UNIFI_GUEST_HTTP_PORT:-8843}:8843 # optional, guest portal HTTPS redirect
      - ${UNIFI_GUEST_HTTPS_PORT:-8880}:8880 # optional, guest portal HTTP redirect
      - 6789:6789 # optional, mobile throughput test
      - 5514:5514/udp #optional, remote syslog
    # labels:
    #   - com.centurylinklabs.watchtower.enable="true"
    # networks:
    #   - watchtower

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ## 259200s = 3 days
    command: --interval 259200

```

### update-controller-container.sh

```shell title="Update Unifi Controller container" linenums="1"
#!/bin/bash

# Update the unifi controller container

# Pull latest image
docker compose pull unifi-controller

# Run commands to remove existing container, just in case
docker stop unifi-controller
docker rm unifi-controller

# Recreate container from new image
docker compose up -d

```

## Notes

## Links

- [link1](#)
