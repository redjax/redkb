---
title: "DNS Management"
date: 2026-06-28T00:09:04-04:00
draft: true
weight: 10
toc: true
keywords: []
tags: []
---

By default, Fedora uses `NetworkManager` to manage network connections. DNS is typically handled through `systemd-resolved`, which receives DNS configuration from multiple sources:

- `NetworkManager` (per-connection settings)
- DHCP (router-provided DNS)
- VPNs (WireGuard, Tailscale, etc.)
- `/etc/systemd/resolved.conf` (global defaults)

DNS resolution is not strictly hierarchical, because multiple systems can provide DNS at the same time; it is more of a merged, per-interface system managed by `systemd-resolved`.

> [!WARNING] Inspect current DNS configuration
> Before making changes, always check what is currently active:
>
> ```shell
> resolvectl statusresolvectl dnsnmcli device show | grep DNS
> ```

## With NetworkManager (Recommended)

> [!NOTE] Connection name
> This guide uses the `Wired connection 1` as an example name throughout. This is the first wired connection interface found by NetworkManager.
>
> If you are targeting another interface, make sure to change `"Wired connection 1"` to your interface name in the commands below.

`NetworkManager` controls DNS on a per-interface basis. This is usually the most reliable way to ensure consistent DNS behavior.

View existing connections with:

```shell
sudo nmcli connection show
```

This will output a list of the interfaces detected by `NetworkManager`:

```shell
NAME               TYPE     DEVICE  
Wired connection 1 ethernet enp6s0  
tailscale0         tun      tailscale0
```

You should also set DNS manually and ignore DHCP DNS. This prevents your router or VPN from injecting unexpected DNS servers.

```shell
sudo nmcli connection modify "Wired connection 1" \
  ipv4.dns "192.168.1.5" \
  ipv4.ignore-auto-dns yes
```

You can also set multiple DNS addresses at once:

```shell
sudo nmcli connection modify "Wired connection 1" \
  ipv4.dns "192.168.1.5 192.168.1.1 1.1.1.1 1.0.0.1" \
  ipv4.ignore-auto-dns yes
```

Optional IPv6 equivalent:

```shell
sudo nmcli connection modify "Wired connection 1" \
  ipv6.dns "fd00::1" \
  ipv6.ignore-auto-dns yes
```

Restart the connection:

```shell
nmcli connection down "Wired connection 1"nmcli connection up "Wired connection 1"
```

A maintainable design is to use your router (`192.168.1.1`) as the single configured DNS resolver for clients, and configure all upstream resolvers (e.g. AdGuard, Cloudflare, fallback DNS) on the router itself. This centralizes DNS management and avoids per-device configuration differences. Note that many home routers do not strictly respect the order of DNS resolvers you configure; instead, they may round-robin, race upstreams, or fall back unpredictably. As a result, you may see occasional bypassing or “leakage” when using DNS-based filtering.

If you host your own DNS resolver, such as Pi-hole or AdGuard Home, a more common setup is to point all clients directly to the Pi-hole/AdGuard node and configure upstream resolvers (e.g. Cloudflare, ControlD/NextDNS, etc.) inside the DNS server itself. This avoids splitting DNS policy across multiple layers and reduces unexpected behavior from DHCP, VPNs, or per-interface DNS overrides.

## With systemd-resolved

`systemd-resolved` provides a global DNS layer that sits between applications and the actual DNS servers. On Fedora, it typically works together with `NetworkManager`, but it can also use its own configuration defined in `/etc/systemd/resolved.conf`.

Unlike traditional DNS setups, `systemd-resolved` does not strictly use a single ordered list of DNS servers. Instead, it maintains a pool of candidate DNS servers and selects between them dynamically based on interface availability, response time, and perceived reliability.

Edit `/etc/systemd/resolved.conf` and configure the `[Resolve]` section:

```conf
[Resolve]
# Primary DNS server(s)
# These are treated as a pool of candidates, not strict priority order
DNS=192.168.1.5
# Optional fallback DNS servers
# Only used if no other DNS servers are available or usable
FallbackDNS=192.168.1.1 1.1.1.1 1.0.0.1
# Route all domains through system DNS configuration
Domains=~.
```

After editing, restart the resolver:

```shell
sudo systemctl restart systemd-resolvedsudo resolvectl flush-caches
```

You can verify the active configuration with:

```shell
resolvectl status
resolvectl dns
```

And test resolution directly through the system resolver:

```shell
resolvectl query example.com
dig example.com
```

> [!NOTE] `dig`
> When using `systemd-resolved`, it is better to test resolution with `resolvectl`; `dig` queries the local stub resolver (`127.0.0.53`), which is managed by `systemd-resolved`. This means `dig` reflects the system’s actual DNS routing decisions, not necessarily a direct upstream query.

> [!IMPORTANT]  Multiple DNS sources
> If multiple DNS sources are configured (NetworkManager, VPNs, DHCP, and `resolved.conf`), `systemd-resolved` may select different DNS servers per interface. This can override global settings and cause unexpected resolution behavior.

## Troubleshooting DNS behavior

### Troubleshoot DNS resolution

If DNS resolution does not behave as expected, try the steps below to isolate the problem.

- Check which DNS servers are actually active:

```shell
resolvectl status
resolvectl dns
```

- Check whether multiple interfaces are providing DNS:

```shell
nmcli device show | grep DNS
```

- Flush caches after changes:

```shell
sudo resolvectl flush-caches
```
