---
tags:
  - docker
  - templates
  - monitoring
  - beszel
---


# Beszel

A simple, no-frills monitoring server.

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

```text title="beszel .env" linenums="1"
## Default: 8090
BESZEL_WEBUI_PORT=
## Default: ./beszel/data
BESZEL_DATA_DIR=

```

### .gitignore

```text title="beszel .gitignore" linenums="1"
beszel/data

```

### docker-compose.yml

```text title="beszel docker-compose.yml" linenums="1"
---
services:
  beszel:
    image: 'henrygd/beszel'
    container_name: 'beszel'
    restart: unless-stopped
    ports:
      - ${BESZEL_WEBUI_PORT:-8090}:8090
    volumes:
      - ${BESZEL_DATA_DIR:-./beszel/data}:/beszel_data

```

## Notes

- After setting up a Beszel server, log into the web UI and add servers using the `+` button in the top right.
    - When you add a new server, you will be given an option to copy a `docker-compose.yml` or shell command for installing the agent.
    - If you're able to use Docker, that's the simplest way to add a new server.
    - Create the new client, save it, then paste the shell script or `docker-compose.yml` on the target you want to monitor.
        - The client will automatically connect back to the Beszel server using a preshared SSH key.

## Links
