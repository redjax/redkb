# OpenVSCode Server

Dockerized [`openvscode-server`](https://github.com/gitpod-io/openvscode-server)

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../server.Dockerfile
  ../vscode-extensions.list
  ../nginx/
    ../nginx.conf
```

### Setup

- Copy `.env.example` -> `.env`
  - Edit environment variables, like the NGINX port and container storage.
- Create SSL certificate with [`generate_ssl_certificates.ssh`](./generate_ssl_certificates.sh)
- (Optional) edit the [`vscode-extensions.list`](./vscode-extensions.list) file, adding/removing any extensions you want installed by default in the container.
- Run `docker compose up -d`

## Container Files

### .env

```text title="openvscode server .env" linenums="1"
## Default: 0.4.27
UV_IMG_VERSION=
## Default: Etc/UTC
TZ=

## Default: (named volume) openvscode-config
CODE_SERVER_CONF_DIR=
## Default: 3000
CODE_HTTP_PORT=

## Default: 80
NGINX_HTTP_PORT=
## Default: 443
NGINX_HTTPS_PORT=

## Default: 1000
PUID=
## Default: 1000
PGID=
## Default: Unset/empty
CODE_CONNECTION_TOKEN=
## Default: Unset/empty
CODE_CONNECTION_SECRET=
## Default: password
CODE_SUDO_PASSWORD=
## Default: Unset/empty
CODE_SUDO_PASSWORD_HASH=
## Default: (named volume) openvscode-config
CODE_SERVER_CONF_DIR=
## Default: latest
CODE_SERVER_BASE=

```

### .gitignore

```text title="openvscode server .gitignore" linenums="1"
nginx/.certs/
code/data/

## Ignore all SSL certificate & key files
.crt
.key

## Allow Environment patterns
!*example*
!*example*.*
!*.*example*
!*.*example*.*
!*.*.*example*
!*.*.*example*.*

```

### docker-compose.yml

```text title="openvscode server docker-compose.yml" linenums="1"
---
volumes:
  openvscode-config: {}

networks:
  code-net: {}

services:

  openvscode-server:
    build:
      dockerfile: server.Dockerfile
      args:
        UV_BASE: ${UV_IMG_VERSION:-0.4.27}
        OPENVSCODE_SERVER_BASE: ${CODE_SERVER_BASE:-latest}
    container_name: openvscode-server
    restart: unless-stopped
    environment:
      - PUID=${PUID:-1000}
      - PGID=${PGID:-1000}
      - TZ=${TZ:-Etc/UTC}
      ## Optional
      - CONNECTION_TOKEN=${CODE_CONNECTION_TOKEN}
      ## Optional
      - CONNECTION_SECRET=${CODE_CONNECTION_SECRET}
      ## Optional
      - SUDO_PASSWORD=${CODE_SUDO_PASSWORD:-password}
      ## Optional
      - SUDO_PASSWORD_HASH=${CODE_SUDO_PASSWORD_HASH:-}
    volumes:
      - ${CODE_SERVER_CONF_DIR:-openvscode-config}:/config
      - ${PWD}/code:/home/workspace/redkb:cached
    expose:
      - 3000
    networks:
      - code-net

  nginx:
    image: nginx:latest
    container_name: openvscode-server-proxy
    restart: unless-stopped
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/.certs/nginx:/etc/nginx/ssl
    ports:
      - ${NGINX_HTTP_PORT:-80}:80
      - ${NGINX_HTTPS_PORT:-443}:443
    networks:
      - code-net

```

### server.Dockerfile

```Dockerfile title="OpenVSCode-Server Dockerfile" linenums="1"
ARG UV_BASE=${UV_IMG_VER:-0.4.27}
ARG OPENVSCODE_SERVER_BASE=${OPENVSCODE_SERVER_BASE:-latest}

FROM ghcr.io/astral-sh/uv:$UV_BASE AS uv
FROM gitpod/openvscode-server:$OPENVSCODE_SERVER_BASE AS base

## Add Astral uv to the container
COPY --from=uv /uv /bin/uv

ENV OPENVSCODE_SERVER_ROOT="/home/.openvscode-server"
ENV OPENVSCODE="${OPENVSCODE_SERVER_ROOT}/bin/openvscode-server"

## Switch to root to install apt packages
USER root
RUN apt-get update -y && apt-get install -y openssh-server

## Switch back to runtime user
USER openvscode-server

FROM base AS runtime

COPY ./vscode-extensions.list ./

SHELL ["/bin/bash", "-c"]

RUN cat vscode-extensions.list | xargs -L 1 ${OPENVSCODE} --install-extension

```

### vscode-extensions.list
```txt title="vscode-extensions.list" linenums="1"
## https://marketplace.visualstudio.com/items?itemName=AdamViola.parquet-explorer
adamviola.parquet-explorer
## https://marketplace.visualstudio.com/items?itemName=almenon.arepl
almenon.arepl
## https://marketplace.visualstudio.com/items?itemName=bradgashler.htmltagwrap
bradgashler.htmltagwrap
## https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff
charliermarsh.ruff
## https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager
donjayamanne.python-environment-manager
## https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack
donjayamanne.python-extension-pack
## https://marketplace.visualstudio.com/items?itemName=ecmel.vscode-html-css
ecmel.vscode-html-css
## https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig
editorconfig.editorconfig
## https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode
esbenp.prettier-vscode
## https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag
formulahendry.auto-close-tag
##  https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-complete-tag
formulahendry.auto-complete-tag
##  https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag
formulahendry.auto-rename-tag
##  https://marketplace.visualstudio.com/items?itemName=foxundermoon.shell-format
foxundermoon.shell-format
##  https://marketplace.visualstudio.com/items?itemName=grapecity.gc-excelviewer
grapecity.gc-excelviewer
##  https://marketplace.visualstudio.com/items?itemName=hashicorp.hcl
hashicorp.hcl
##  https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio
hediet.vscode-drawio
##  https://marketplace.visualstudio.com/items?itemName=hyesun.py-paste-indent
hyesun.py-paste-indent
##  https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv
janisdd.vscode-edit-csv
##  https://marketplace.visualstudio.com/items?itemName=jomeinaster.bracket-peek
jomeinaster.bracket-peek
##  https://marketplace.visualstudio.com/items?itemName=kaih2o.python-resource-monitor
kaih2o.python-resource-monitor
##  https://marketplace.visualstudio.com/items?itemName=kevinrose.vsc-python-indent
kevinrose.vsc-python-indent
##  https://marketplace.visualstudio.com/items?itemName=mads-hartmann.bash-ide-vscode
mads-hartmann.bash-ide-vscode
##  https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph
mhutchie.git-graph
##  https://marketplace.visualstudio.com/items?itemName=mohsen1.prettify-json
mohsen1.prettify-json
##  https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy
ms-python.debugpy
##  https://marketplace.visualstudio.com/items?itemName=ms-python.python
ms-python.python
##  https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance
ms-python.vscode-pylance
##  https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter
ms-toolsai.jupyter
##  https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter-keymap
ms-toolsai.jupyter-keymap
##  https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter-renderers
ms-toolsai.jupyter-renderers
##  https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-jupyter-cell-tags
ms-toolsai.vscode-jupyter-cell-tags
##  https://marketplace.visualstudio.com/items?itemName=ms-vscode.powershell
ms-vscode.powershell
##  https://marketplace.visualstudio.com/items?itemName=mutantdino.resourcemonitor
mutantdino.resourcemonitor
##  https://marketplace.visualstudio.com/items?itemName=njqdev.vscode-python-typehint
njqdev.vscode-python-typehint
##  https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow
oderwat.indent-rainbow
##  https://marketplace.visualstudio.com/items?itemName=pflannery.vscode-versionlens
pflannery.vscode-versionlens
##  https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer
qwtel.sqlite-viewer
##  https://marketplace.visualstudio.com/items?itemName=redhat.ansible
redhat.ansible
##  https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml
redhat.vscode-xml
##  https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml
redhat.vscode-yaml
##  https://marketplace.visualstudio.com/items?itemName=rogalmic.bash-debug
rogalmic.bash-debug
##  https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml
samuelcolvin.jinjahtml
##  https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker
streetsidesoftware.code-spell-checker
##  https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml
tamasfe.even-better-toml
##  https://marketplace.visualstudio.com/items?itemName=teticio.python-envy
teticio.python-envy
##  https://marketplace.visualstudio.com/items?itemName=vincaslt.highlight-matching-tag
vincaslt.highlight-matching-tag
##  https://marketplace.visualstudio.com/items?itemName=visualstudioexptteam.intellicode-api-usage-examples
visualstudioexptteam.intellicode-api-usage-examples
##  https://marketplace.visualstudio.com/items?itemName=visualstudioexptteam.vscodeintellicode
visualstudioexptteam.vscodeintellicode
##  https://marketplace.visualstudio.com/items?itemName=visualstudioexptteam.vscodeintellicode-completions
visualstudioexptteam.vscodeintellicode-completions
##  https://marketplace.visualstudio.com/items?itemName=wattenberger.footsteps
wattenberger.footsteps
##  https://marketplace.visualstudio.com/items?itemName=wholroyd.jinja
wholroyd.jinja
##  https://marketplace.visualstudio.com/items?itemName=# william-voyek.vscode-nginx
# william-voyek.vscode-nginx
##  https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one
yzhang.markdown-all-in-one

```

### generate_ssl_certificates.sh

Note: This is a Bash script and will only run on Linux. You can use WSL if you are on Windows.

```shell title="generate_ssl_certificates.sh" linenums="1"
#!/bin/bash

CONTAINER_CERT_DIR="./nginx/.certs/nginx"

if [[ ! -d "${CONTAINER_CERT_DIR}" ]]; then
  echo "SSL certificate directory '${CONTAINER_CERT_DIR}' does not exist. Creating."
  mkdir -pv "${CONTAINER_CERT_DIR}"
fi

read -p "What is your domain (i.e. hostname.home, localhost.home, etc): " DOMAIN

echo "Generating SSL certificate for edit.* domains"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${CONTAINER_CERT_DIR}/edit_key.key -out ${CONTAINER_CERT_DIR}/edit_cert.crt -subj "/CN=edit.${DOMAIN}"

echo "Generating SSL certificate for docs.* domains"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${CONTAINER_CERT_DIR}/docs_key.key -out ${CONTAINER_CERT_DIR}/docs_cert.crt -subj "/CN=docs.${DOMAIN}"

```

### nginx.conf

This configuration enables HTTPS reverse proxying on your LAN using a self signed certificate. You will get an HTTPS error that you will need to proceed past, but this enables functionality in OpenVSCode Server like previewing Markdown files.

```conf title="nginx.conf" linenums="1"
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Enable logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Generic server block for edit.* subdomains
    server {
        listen 443 ssl;
        server_name edit.*;

        ssl_certificate /etc/nginx/ssl/edit_cert.crt;  # Path to your SSL certificate
        ssl_certificate_key /etc/nginx/ssl/edit_key.key;  # Path to your SSL key

        location / {
            proxy_pass http://openvscode-server:3000;  # Adjust the proxy_pass to your service
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            ## Add these lines to fix the error:
            #  The workbench failed to connect to the server (Error: WebSocket close with status code 1006)
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection upgrade;
            proxy_set_header Accept-Encoding gzip;
        }
    }

}

```

## Notes


## Links
