---
tags:
  - linux
  - utilities
  - bash
---

# Rsync

[`rsync`](https://www.man7.org/linux/man-pages/man1/rsync.1.html) is a useful utility for synchronizing files. It can synch between hosts with SSH, locally between 2 directories, and more. A hosted version exists at [`rsync.net`](https://rsync.net), offering a reliable, flexible solution for synchronizing files to a trusted remote.

This page focuses on the `rsync` CLI utility for Linux.

## Installation

Installing `rsync` on Linux is easy, the package exists in most repositories:

```bash title="Install rsync"
## Debian/Ubuntu
sudo apt install -y rsync

## RedHat/Fedora/OpenSuSE
sudo dnf install -y rsync

## Alpine
sudo apk add rsync

```

## Usage

Check `rsync`'s version with `rsync --version`. The commands in this documentation do not cover the full functionality of `rsync`. Rather, they're a reflection of how I've used the tool.

### Rsync Args

!!! note

    This list is not exhaustive. It's a cheat sheet I've made for myself. If I haven't used an arg, it will not be listed below.

    See a [full list of `rsync` args](https://ss64.com/bash/rsync_options.html), or check out an [`rsync` cheat-sheet](https://devhints.io/rsync).

| arg | description                               |
| --- | ----------------------------------------- |
| -r  | Recursive copy (unnecessary with -a)      |
| -a  | Archive mode, includes recursive transfer |
| -z  | Compress the data                         |
| -v  | Verbose/detailed info during transfer     |
| -h  | Human readable output                     |

### Replace cp command with rsync for faster transfers

Edit your `~/.bash_aliases` file:

```text title="~/.bash_aliases" linenums="1"
## other aliases

## Replace cp with rsync if rsync is installed
if [ -x /usr/bin/rsync ]; then
  alias cp="rsync --progress -auHxvz "
fi

```

## Examples

### Sync local path to remote

```bash title="rsync local path to remote" linenums="1"
## Show a progress bar, archive & compress data during transfer, show verbose & human-readable output
rsync -avzh --progress /local/path user@remote:/remote/path/
```

### Sync remote path to local

```bash title="rsync remote path to local" linenums="1"
## Show a progress bar, archive & compress data during transfer, show verbose & human-readable output
rsync -avzh --progress user@remote:/remote/path/ /local/path
```
