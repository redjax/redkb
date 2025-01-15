---
tags:
  - linux
  - debian
  - networking
---

# Debian Networking

...

## Set a static IP

### With the CLI

First, get your network interface name by running `ip a`. Look for a line that starts with `eno1`, `ens18`, `eth01`, etc. This interface should have an IP address on your subnet (i.e. for a `192.168.1.0/24` network, you might see an address like `192.168.1.102`). Note the interface name.

Create a backup of the `/etc/network/interfaces` file (`cp /etc/network/interfaces /etc/network/interfaces.orig`), then edit the file with `nano`, `(neo)vi(m)`, or some other terminal editor. Find your interface name in the file (referencing the interface you noted above) and change it to a `static` connection, with your desired IP address, gateway, and DNS nameservers. Replace any `xxx` values below with your own networking values.

```text title="Set static IP on Debian" linenums="1"
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug ens18
iface ens18 inet static
    address 192.168.1.xxx/24
    gateway 192.168.1.1
    nameservers 192.168.1.xxx,1.1.1.1,1.0.0.1
```

Restart your machine, or run one of the following (if you do not have systemd, use the 2nd method with `ifup` and `ifdown`):

- Restart systemd service: `sudo systemctl restart networking`
- Use the `ifup` and `ifdown` utility:
    - `sudo ifdown <eth0, eno1, ens18, ...>` (use your interface name, do not copy the `<angle brackets>`)
    - `sudo ifup <eth0, eno1, ens18>`

### With a GUI

...
