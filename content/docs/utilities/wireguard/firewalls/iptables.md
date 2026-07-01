---
title: "Iptables"
date: 2026-05-05T01:38:13-04:00
draft: true
weight: 20
toc: true
keywords: []
tags:
  - wireguard
  - vpn
  - networking
  - firewall
---

## Server

### Basic WireGuard access

Allow WireGuard UDP port:

```shell
iptables -A INPUT -p udp --dport 51820 -j ACCEPT
```

Allow established traffic back in

```shell
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### Enable VPN forwarding (core VPN function)

Allow VPN -> LAN forwarding:

```shell
iptables -A FORWARD -i wg0 -o eth0 -j ACCEPT
```

Allow return traffic:

```shell
iptables -A FORWARD -i eth0 -o wg0 -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### NAT (internet sharing via VPN)

Masquerade VPN subnet to WAN:

```shell
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE
```

### Restrict VPN access

> [!WARNING]
> These commands will cut your regular Internet access. Only run them if you know what you're doing
> and intend to allow traffic *only* over the VPN.

Allow only SSH from VPN

```shell
iptables -A INPUT -i wg0 -p tcp --dport 22 -j ACCEPT
```

Drop everything else from VPN interface

```shell
iptables -A INPUT -i wg0 -j DROP
```

## Client

### Basic VPN interface rules

Allow outbound VPN traffic

```shell
iptables -A OUTPUT -o wg0 -j ACCEPT
```

Allow responses from VPN

```shell
iptables -A INPUT -i wg0 -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### Strict lockdown

> [!WARNING]
> This command will isolate the machine from non-wireguard networks. Only run if if you know what you're doing
> and intend to allow traffic *only* over the VPN.

Block all non-loopback inbound traffic

```shell
iptables -A INPUT ! -i lo -j DROP
```
