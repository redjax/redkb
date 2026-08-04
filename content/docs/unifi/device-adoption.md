---
title: "Device Adoption"
date: 2026-08-03T21:34:57-04:00
draft: false
weight: 10
toc: true
keywords: []
tags:
  - networking
  - unifi
  - ubiquiti
---

Adopting Unifi devices can be a challenge sometimes. When you first get a new Ubiquiti Unifi device, or something happens and your device and controller fall out of sync, it can be painful to re-adopt previous devices.

This section details my personal notes and situations I've encountered/resolved. If you don't find what you're looking for here, make sure to check the [Unifi device adoption documentation](https://help.ui.com/hc/en-us/articles/360012622613-UniFi-Device-Adoption).

## New Device Setup

Depending on your controller setup (I run mine in Docker), it may be as easy as pluggin your new device in and letting the controller find it. Adoption can be finicky sometimes; if your controller fails to adopt the device, try SSHing into it and running the `set-inform` command.

The default Unifi device credentials are:

| Username | Password |
| -------- | -------- |
| `ubnt`   | `ubnt`   |

If you configure a local admin user (Unifi has [documentation for this](https://help.ui.com/hc/en-us/articles/28692158912279-Adding-Admins-in-UniFi)), use that username/password instead.

The full command is: `set-inform http://<controller-ip-or-hostname>:8080/inform`. If you use a hostname, i.e. `unifi.example.com`, you could run `set-inform http://unifi.example.com:8080/inform`, otherwise use the device's IP address, i.e. `set-inform http://192.168.1.1:8080/inform`.

If you configured your Unifi controller to run on a port other than `:8080`, use that port instead.

To force device adoption, SSH into the remote machine and run the `set-inform` command:

```bash
$> ssh ubnt@192.168.1.102 # or whatever IP address the DHCP server assigned to the new device
Welcome to EdgeOS

By logging in, accessing, or using the Ubiquiti product, you
acknowledge that you have read and understood the Ubiquiti
License Agreement (available in the Web UI at, by default,
http://192.168.1.1) and agree to be bound by its terms.

ubnt@192.168.1.1's password: ubnt

## Run the set-inform command to tell the device where to request adoption
$> set-inform http://<controller-ip-or-hostname>:8080/inform
```

Then, in the Unifi controller webUI, you should see a new device pending adoption. You can complete the adoption there and Unifi will start managing the device.

## Forget & Re-Adopt Device

If you're having trouble with one of your devices, you can forget (or "Remove" in newer versions) the device from the controller webUI, then SSH into it and run the same commands you would for [new device setup](#new-device-setup).

This can sometimes fix configuration issues, or problems where a device continuously falls out of adoption, or is repeatedly rebooting.

## Gotchas

- [Unifi Flex Mini switches](https://store.ui.com/us/en/products/usw-flex-mini) do not have SSH capabilities, so the instructions above don't apply. You just have to hope really hard that it works.
  - Often, you just have to leave the switch plugged info until the controller notices it's connected. It will work as a "dumb" switch in the meantime.
