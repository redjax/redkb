---
title: "Alacritty"
date: 2024-10-09T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - util
  - alacritty
lastmod: "2026-04-13T04:44:39Z"
---

<!-- <p align="center">
    <img width="200" alt="Alacritty Logo" src="alacritty-term.svg">
</p> -->

![Alcritty logo](alacritty-term.svg#center-logo)

A modern terminal emulator with sensible defaults, configurable with a simple `alacritty.toml` file.

## Installation

Download & install Alacritty using one of the methods below. More info in the [Alacritty Github repository](https://github.com/alacritty/alacritty#installation).

- Download from the [homepage](https://alacritty.org) and install manually
- Download from the [Alacritty Github releases page](https://github.com/alacritty/alacritty/releases) and install manually.
- Download & install with a package manager
  - Windows: `winget install --id="Alacritty.Alacritty"`
  - Linux: `{apt,dnf,...} install alacritty`

## Configuration

Alacritty looks for a configuration file in the following locations, depending on OS; this file does not exist by default, you must create one if you want to configure Alacritty's defaults':

- Windows: `${env:APPDATA}\alacritty\alacritty.toml`
- Linux/Mac: `~/.config/alacritty/alacritty.toml` OR `~/alacritty.toml`

The Alacritty site has a [page dedicated to the available configuration options](https://alacritty.org/config-alacritty.html). Below are my personal configurations for Windows and Linux.

- 🔗 [Linux configuration](/docs/utilities/alacritty/linux/)
- 🔗 [Windows configuration](/docs/utilities/alacritty/windows/)

## Links

| Link                                                                   | Description                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [Homepage](https://alacritty.org)                                      | Project home                                                      |
| [Github](https://github.com/alacritty/alacritty)                       | Project source                                                    |
| [Configuration Reference](https://alacritty.org/config-alacritty.html) | `man`page-like documentation for the `alacritty.toml` config file |
