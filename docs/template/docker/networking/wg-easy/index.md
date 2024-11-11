# WireGuard Easy

Utilities for simplifying deployment & management of a WireGuard VPN.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../generate_wg_password_hash.sh
```

## Container Files

### .env

```text title="wireguard easy .env" linenums="1"
## Default: (unset) encrypt your password using
#  the generate_wg_password_hash.sh script, paste
#  encrypted password here, replacing any $ characters
#  with $$.
WG_EASY_ADMIN_PASSWORD_HASH=

## Default: latest
#  Find most recent release at: https://github.com/wg-easy/wg-easy/releases
WG_EASY_IMG_VER=
## Default: en
WG_EASY_LANG=
## Default: 127.0.0.1
WG_EASY_HOST=
## Default: 1.1.1.1
WG_EASY_DEFAULT_DNS=
## Default: 1420
WG_EASY_MTU=
## Default: 25
WG_EASY_KEEPALIVE=
## Default: true
WG_EASY_ENABLE_TRAFFIC_STATS=
## Default: true
WG_EASY_ENABLE_ONETIME_LINKS=
## Default: true
WG_EASY_ENABLE_UI_CLIENT_SORT=
## Default: (named volume) wg-easy_etc
WG_EASY_DATA_DIR=
## Default: 51820
WG_EASY_LISTEN_PORT=
## Default: 51821
WG_EASY_WEBUI_PORT=

```

### .gitignore

```text title="wireguard easy .gitignore" linenums="1"
wg-easy/data

```

### docker-compose.yml

```text title="wireguard easy docker-compose.yml" linenums="1"
---
volumes:
  wg-easy_etc: {}

services:
  wg-easy:
    image: ghcr.io/wg-easy/wg-easy:${WG_EASY_IMG_VER:-latest}
    container_name: wg-easy
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
      # - NET_RAW # ⚠️ Uncomment if using Podman
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.conf.all.src_valid_mark=1
    environment:
      # Change Language:
      # (Supports: en, ua, ru, tr, no, pl, fr, de, ca, es, ko, vi, nl, is, pt, chs, cht, it, th, hi, ja, si)
      - LANG=${WG_EASY_LANG:-en}
      # ⚠️ Required:
      # Change this to your host's public address
      - WG_HOST=${WG_EASY_HOST:-127.0.0.1}

      # Optional:
      - PASSWORD_HASH=${WG_EASY_ADMIN_PASSWORD_HASH}
      # - PORT=51821
      # - WG_PORT=51820
      # - WG_CONFIG_PORT=92820
      # - WG_DEFAULT_ADDRESS=10.8.0.x
      - WG_DEFAULT_DNS=${WG_EASY_DEFAULT_DNS:-1.1.1.1}
      - WG_MTU=${WG_EASY_MTU:-1420}
      # - WG_ALLOWED_IPS=192.168.15.0/24, 10.0.1.0/24
      ## Second(s) to keep connection alive. 0=don't keep connection alive
      - WG_PERSISTENT_KEEPALIVE=${WG_EASY_KEEPALIVE:-25}
      # - WG_PRE_UP=echo "Pre Up" > /etc/wireguard/pre-up.txt
      # - WG_POST_UP=echo "Post Up" > /etc/wireguard/post-up.txt
      # - WG_PRE_DOWN=echo "Pre Down" > /etc/wireguard/pre-down.txt
      # - WG_POST_DOWN=echo "Post Down" > /etc/wireguard/post-down.txt
      ## Enable detailed RX/TX client stats in webUI
      - UI_TRAFFIC_STATS=${WG_EASY_ENABLE_TRAFFIC_STATS:-true}
      ## 0=Charts disabled, 1=Line chart, 2=Area chart, 3=Bar chart)
      # - UI_CHART_TYPE=0 
      - WG_ENABLE_ONE_TIME_LINKS=${WG_EASY_ENABLE_ONETIME_LINKS:-true}
      ## Sort clients in webUI by name
      - UI_ENABLE_SORT_CLIENTS=${WG_EASY_ENABLE_UI_CLIENT_SORT:-true}
      ## Enable client expiration
      # - WG_ENABLE_EXPIRES_TIME=true
      # - ENABLE_PROMETHEUS_METRICS=false
      # - PROMETHEUS_METRICS_PASSWORD=$$2a$$12$$vkvKpeEAHD78gasyawIod.1leBMKg8sBwKW.pQyNsq78bXV3INf2G # (needs double $$, hash of 'prometheus_password'; see "How_to_generate_an_bcrypt_hash.md" for generate the hash)
    volumes:
      - ${WG_EASY_DATA_DIR:-wg-easy_etc}:/etc/wireguard
    ports:
      - ${WG_EASY_LISTEN_PORT:-51820}:51820/udp
      - ${WG_EASY_WEBUI_PORT:-51821}:51821/tcp

```

### generate_wg_password_hash.sh

This script prompts the user for a password for the `wg-easy` webUI admin, then returns the password as a bcrypt string. This password hash should be pasted in the `.env` file's `WG_EASY_ADMIN_PASSWORD_HASH` env variable, replacing any `$` characters with `$$`.

```shell title="generate_wg_easy_password_hash.sh" linenums="1"
#!/bin/bash

## Get user password before running container.
#  Hide password input with -s
read -s -p "Password to encrypt: " USER_PASSWORD

echo "Hashing password with wg-easy container"
docker run -it ghcr.io/wg-easy/wg-easy wgpw "${USER_PASSWORD}"

echo "Paste the password above into your .env file's 'WG_EASY_ADMIN_PASSWORD_HASH' variable. Make sure to change any '$' symbols to '\$\$'!"

```

## Notes

### Usage

- Copy `.env.example` -> `.env`
- Generate your admin password by running the [`generate_wg_password_hash.sh`](./generate_wg_password_hash.sh) script.
    - Copy the generated password into the `WG_EASY_ADMIN_PASSWORD_HASH` env variable in `.env`.
    - **NOTE**: You must replace any `$` characters with `$$`.
- Set your machine's hostname/address in `WG_EASY_HOST`
    - This can be an IP address or FQDN (i.e. `wg.your-domain.com`), but FQDN is preferred.
- Allow the following ports through your firewall:
    - `51820/udp` (WireGuard's communication port)
    - `51821/tcp` (WireGuard's webUI port)
- Run the stack with `docker compose up -d`
- Access the web UI at `http://<your-wireguard-hostname>:51821`

## Links

- [Github: wg-easy](https://github.com/wg-easy/wg-easy)
    - [Run WireGuard Easy](https://github.com/wg-easy/wg-easy?tab=readme-ov-file#2-run-wireguard-easy)
    - [WireGuard Docker env variables](https://github.com/wg-easy/wg-easy?tab=readme-ov-file#options)
    - [Using WireGuard Easy with NGINX SSL](https://github.com/wg-easy/wg-easy/wiki/Using-WireGuard-Easy-with-nginx-SSL)
