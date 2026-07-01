---
title: "UFW"
date: 2026-05-05T01:38:13-04:00
draft: false
weight: 10
toc: true
keywords: []
tags:
  - wireguard
  - vpn
  - networking
  - firewall
---

## Server

### Allow Wireguard UDP port

```shell
ufw allow 51820/udp
```

### Allow forwarding from VPN to LAN

```shell
ufw route allow in on wg0 out on eth0
```

### Enable forwarding in config

Edit `/etc/default/ufw`, set `DEFAULT_FORWARD_POLICY="ACCEPT"`. Add this value on a newline if it does not exist already.

### NAT (internet sharing)

Edit `/etc/ufw/before.rules`:

```rules
*nat
:POSTROUTING ACCEPT [0:0]

-A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE

COMMIT
```

### SSH access via VPN

```shell
ufw allow in on wg0 to any port 22 proto tcp
```

### HTTP/HTTPS via VPN

```shell
ufw allow in on wg0 to any port 80 proto tcp
ufw allow in on wg0 to any port 443 proto tcp
```

### Allow specific ports

```shell
ufw route allow in on wg0 to any port 22
ufw route allow in on wg0 to any port 443
```

### Deny inbound VPN traffic

```shell
ufw route deny in on wg0
```

## Client

### Allow all outgoing traffic

```shell
ufw default allow outgoing
```

### Allow WireGuard interface outbound explicitly

```shell
ufw allow out on wg0
```

### Deny all incoming

```shell
ufw default deny incoming
```

### Allow loopback

```shell
ufw allow in on lo
```
