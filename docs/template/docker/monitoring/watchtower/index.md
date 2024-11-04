# Watchtower

A container to watch other containers and automate performing image pulls & updates.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="watchtower .env" linenums="1"
# Default: true
WATCHTOWER_MONITOR_ONLY=
# Add the following label to containers if below is "true" (default)
#   com.centurylinklabs.watchtower.enable="true"
WATCHTOWER_LABEL_ENABLE=
# Default: false
WATCHTOWER_CLEANUP=true
# Default: false
WATCHTOWER_INCLUDE_RESTARTING=
# Default: false
WATCHTOWER_INCLUDE_STOPPED=
# Default: false
WATCHTOWER_REVIVE_STOPPED=

## Notification settings

# Options: (default) email, msteams, slack, gotify, shoutrrr
WATCHTOWER_NOTIFICATION_TYPE=
WATCHTOWER_FROM_ADDR=
WATCHTOWER_TO_ADDR=
# Default: smtp.gmail.com
WATCHTOWER_EMAIL_SERVER=
WATCHTOWER_NOTIFICATION_DELAY=
WATCHTOWER_NOTIFICATION_PASSWORD=
WATCHTOWER_EMAIL_SUBJECT=
# Default: 587
WATCHTOWER_NOTIFICATION_EMAIL_PORT=

```

### .gitignore

```text title="watchtower .gitignore" linenums="1"
# Ignore .env file
.env

# Don't ignore specific files
!**/*.example

```

### docker-compose.yml

```text title="watchtower docker-compose.yml" linenums="1"
---
networks:
  watchtower:
    external: true
    
services:

  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    environment:
      WATCHTOWER_MONITOR_ONLY: ${WATCHTOWER_MONITOR_ONLY:-true}
      WATCHTOWER_CLEANUP: ${WATCHTOWER_CLEANUP:-false}
      WATCHTOWER_LABEL_ENABLE: ${WATCHTOWER_LABEL_ENABLE:-true}
      WATCHTOWER_INCLUDE_RESTARTING: ${WATCHTOWER_INCLUDE_RESTARTING:-false}
      WATCHTOWER_INCLUDE_STOPPED: ${WATCHTOWER_INCLUDE_STOPPED:-false}
      WATCHTOWER_REVIVE_STOPPED: ${WATCHTOWER_REVIVE_STOPPED:-false}
      ## Notification settings below. Comment section until "volumes" to disable notifications
      WATCHTOWER_NOTIFICATIONS: ${WATCHTOWER_NOTIFICATION_TYPE:-email}
      WATCHTOWER_NOTIFICATION_EMAIL_FROM: ${WATCHTOWER_FROM_ADDR}
      WATCHTOWER_NOTIFICATION_EMAIL_TO: ${WATCHTOWER_TO_ADDR}
      # you have to use a network alias here, if you use your own certificate
      WATCHTOWER_NOTIFICATION_EMAIL_SERVER: ${WATCHTOWER_EMAIL_SERVER:-smtp.gmail.com}
      WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PORT: ${WATCHTOWER_EMAIL_PORT:-587}
      WATCHTOWER_NOTIFICATION_EMAIL_DELAY: ${WATCHTOWER_NOTIFICATION_DELAY:-2}
      WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PASSWORD: ${WATCHTOWER_NOTIFICATION_PASSWORD}
      WATCHTOWER_NOTIFICATION_EMAIL_SUBJECTTAG: ${WATCHTOWER_EMAIL_SUBJECT}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - watchtower

```

## Notes

- You must create a Docker network on the host (i.e. not just in the `docker-compose.yml` file), named `watchtower`, for this to function.
- This container assumes you are installing watchtower on the host and want it to watch any container on the `watchtower` network with the watchtower label applied.

## Links

- [Watchtower container args](https://containrrr.dev/watchtower/arguments/)
