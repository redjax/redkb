---
tags:
    - utilities
    - terminal

---

# Alacritty

<p align="center">
    <img width="200" alt="Alacritty Logo" src="https://raw.githubusercontent.com/alacritty/alacritty/master/extra/logo/compat/alacritty-term.svg">
</p>

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

- 🔗 [Linux configuration](./linux.md)
- 🔗 [Windows configuration](./windows.md)

## Links

| Link                                                                   | Description                                                       |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [Homepage](https://alacritty.org)                                      | Project home                                                      |
| [Github](https://github.com/alacritty/alacritty)                       | Project source                                                    |
| [Configuration Reference](https://alacritty.org/config-alacritty.html) | `man`page-like documentation for the `alacritty.toml` config file |
