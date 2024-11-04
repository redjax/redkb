# Adguard Home

An ad-blocking DNS manager.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
```

## Container Files

### .env

```text title="adguard-home .env" linenums="1"
## Default: ./adguardhome/work
ADGUARD_WORK_DIR=
## Default: ./adguardhome/config
ADGUARD_CONF_DIR=

```

### .gitignore

```text title="adguard-home .gitignore" linenums="1"
adguardhome/

```

### docker-compose.yml

```text title="adguard-home docker-compose.yml" linenums="1"
services:
  adguardhome:
    image: 'adguard/adguardhome:latest'
    container_name: 'adguard'
    hostname: 'adguard'
    restart: 'unless-stopped'
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ${ADGUARD_WORK_DIR:-./adguardhome/work}:/opt/adguardhome/work
      - ${ADGUARD_CONF_DIR:-./adguardhome/config}:/opt/adguardhome/conf
    ports:
      # Plain DNS
      - 53:53/tcp
      - 53:53/udp
      # AdGuard Home Admin Panel as well as DNS-over-HTTPS
      - 80:80/tcp
      - 443:443/tcp
      - 443:443/udp
      - 3000:3000/tcp
      # DNS-over-TLS
      - 853:853/tcp
      # DNS-over-QUIC
      - 784:784/udp
      - 853:853/udp
      - 8853:8853/udp
      # DNSCrypt
      - 5443:5443/tcp
      - 5443:5443/udp

```

## Notes

## Links

- [Docker Hub: Adguard Home](https://hub.docker.com/r/adguard/adguardhome)
