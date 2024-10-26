# n8n

[`n8n`](https://n8n.io) is a workflow automation tool. Similar to Zapier, `n8n` can integrate with many sources and provide a no/low code (javascript) interface for building your own automations.

Automate your home by using `n8n` with [`homeassistant`](https://www.home-assistant.io), make automated HTTP requests to REST APIs and do something with the response (i.e. send the daily weather forcast via Telegram), and more.

## Directory Structure

```title="Container directory structure"
docker_n8n/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../generate_encryption_key.sh
```

## Container Files

### .env

```text title="n8n .env" linenums="1"
## Default: Etc/UTC
TZ=

## Default: 5678
N8N_PORT=
## Default: named volume 'n8n_conf'
N8N_DATA_DIR=

## Default: true
N8N_BASIC_AUTH=
## Default: n8n
N8N_BASIC_AUTH_USER=
## Default: n8nadmin
N8N_BASIC_AUTH_PASSWORD=

## Default: false
N8N_SMTP_SSL=

## Default: unset
N8N_HOST=
## Default: https
N8N_PROTOCOL=
## Default: production
N8N_NODE_ENV=

## Default: unset
N8N_WEBHOOK_URL=

## Default: unset
N8N_ENCRYPTION_KEY=<generate by running ./generate_encryption_key.sh>

```

### docker-compose.yml

```yaml title="docker-compose.yml" linenums="1"
version: "3"

volumes:
  n8n_conf:
  n8n_files:

services:

  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - ${N8N_PORT:-5678}:5678
    volumes:
      - ${N8N_DATA_DIR:-n8n_conf}:/home/node/.n8n
      - ${N8N_WORKFLOW_FILES_DIR:-n8n_files}:/files
    environment:
      - TZ=${TZ:-America/New_York}
      - GENERIC_TIMEZONE=${TZ:-America/New_York}
      - N8N_BASIC_AUTH_ACTIVE=${N8N_BASIC_AUTH:-true}
      - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER:-n8n}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD:-n8nadmin}
      # If accessing outside the local network, uncomment below
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=${N8N_PORT:-5678}
      - N8N_PROTOCOL=${N8N_PROTOCOL:-https}
      - N8N_NODE_ENV=${N8N_NODE_ENV:-production}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - WEBHOOK_URL=${N8N_WEBHOOK_URL}
      - N8N_SMTP_SSL=${N8N_SMTP_SSL:-false}

```

### generate_encryption_key.sh

```sh title="generate_encryption_key.sh" linenums="1"
#!/bin/bash

key=$(openssl rand -hex 32)

echo "Encryption key:"
echo "$key"

```

## Notes

## Links
