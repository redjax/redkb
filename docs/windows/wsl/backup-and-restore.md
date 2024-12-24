---
tags:
  - windows
  - wsl
---

# Backup & Restore WSL distributions

WSL distributions can be backed up and restored using the `--export` and `--import` flags. This is useful for moving WSL distributions to new machines, creating backups before making modifications, and for restoring from "base" images.

The WSL backup files are in `.tar` format.

## Backup WSL

Backing up a WSL distribution involves compressing the entire virtual disk to a `.tar` file. The general command format is: `wsl --export <distribution-name> C:\path\to\<backup-name>.tar`.

```powershell title="Backup distribution named 'debian' to C:\wsl_backups"
wsl --export debian C:\wsl_backups\debian.tar
```

## Restore WSL

Restoring a WSL distribution involves decompressing an existing `.tar` file into a full clone of the source. The general command format is: `wsl --import <new-distribution-name> C:\path\to\new-distribution-name C:\path\to\<old-distribution-name>.tar`

```powershell title="Create distribution named debian-new from C:\wsl_backups\debian.tar"
wsl --import debian-new C:\wsl\debian-new C:\wsl_backups\debian.tar
```

## Clone existing WSL into new image

A useful practice is to create a "base" image that you can use to spawn off new WSL distributions as-needed. If you want a specific set of configurations, installed packages, etc, you can create a WSL distribution where you make all of these changes, then take a backup which you can repeatedly restore from for new distributions.

For example, say you have a WSL distribution named `deb-base`. In this distribution, you have modified the `/etc/wsl.conf` file, installed `git`, `docker`, and `neovim`. You've modified the `~/.config/nvim` directory, setting up a customized environment for the `neovim` app. You've also installed `tmux` and modified `~/.tmux.config`.

You do not want to repeat these steps each time you create a new WSL distribution. Pretend you now want to create a distribution named `deb-pydev`, where you will install [Astral's `uv` project manager](https://astral.sh/uv).

- First, create a backup of `deb-base`
    - `wsl --export deb-base C:\wsl_backups\deb-base.tar`
- Then, create a new distribution named `deb-pydev`, with the WSL VM's data stored in `C:\wsl\deb-pydev`
    - `wsl --import deb-pydev C:\wsl\deb-pydev C:\wsl_backup\deb-base.tar`
