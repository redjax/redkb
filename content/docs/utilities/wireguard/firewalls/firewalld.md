---
title: "Firewalld"
date: 2026-05-05T01:38:13-04:00
draft: true
weight: 30
toc: true
keywords: []
tags:
  - wireguard
  - vpn
  - networking
  - firewall
---

## Server

### Create dedicated zone

```shell
firewall-cmd --permanent --new-zone=wireguard
```

### Assign interface

```shell
firewall-cmd --permanent --zone=wireguard --add-interface=wg0
```

### Allow WireGuard port

```shell
firewall-cmd --permanent --add-port=51820/udp
```

### Allow all traffic from VPN zone

```shell
firewall-cmd --permanent --zone=wireguard --set-target=ACCEPT
```

### NAT (internet sharing)

```shell
firewall-cmd --permanent --add-masquerade
```

### Enable forwarding

```shell
firewall-cmd --permanent --zone=wireguard --add-forward
```

### Allow only SSH from VPN

```shell
firewall-cmd --permanent --zone=wireguard --add-service=ssh
```

### Allow HTTP/HTTPS

```shell
firewall-cmd --permanent --zone=wireguard --add-service=http
firewall-cmd --permanent --zone=wireguard --add-service=https
```

### Drop connections that aren't explicitly allowed

```shell
firewall-cmd --permanent --zone=wireguard --set-target=DROP
```

## Client

### Trust WireGuard interface

```shell
firewall-cmd --permanent --zone=trusted --add-interface=wg0
```

### Set default zone to drop

```shell
firewall-cmd --set-default-zone=drop
```

### Allow loopback implicitly

```shell
firewall-cmd --permanent --zone=trusted --add-interface=lo
```
