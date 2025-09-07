---
tags:
  - restic
  - resticprofile
---

# pcloud

[pCloud](https://pcloud.com) remote for `resticprofile` via [`rclone`](https://rclone.org/).

## Requirements

`resticprofile` does not support `pCloud` as a destination by default, but you can pass a pre-configured `rclone` destination to the backup profile to connect to a Restic repository stored in pCloud.

[Install Rclone](https://rclone.org/install/) to get started.

!!! tip

    On Linux, you can install Rclone with `sudo -v ; curl https://rclone.org/install.sh | sudo bash`.

    On Mac, you can install Rclone with [Homebrew](https://brew.sh) using `brew install rclone`, or with [macports](https://www.macports.org) using `sudo port install rclone`.

    On Linux, you can install Rclone with [Winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) using `winget install Rclone.Rclone`, with [Chocolatey](https://chocolatey.org/install) using `choco install rclone`, or with [scoop](https://scoop.sh) using `scoop install rclone`.

## Get your pCloud token

!!! note

    The commands below do not work in a headless/CLI environment. It is assumed you have access to a machine with a GUI and `rclone` installed, where you can pre-authorize `resticprofile` by signing in and obtaining a JSON token to pass to your backup profile.

Install `rclone` on a machine with a GUI where you can open a web browser and run this command:

```shell
rclone authorize "pcloud"
```

This will open a browser and prompt you to login to pCloud, and the terminal where you ran the authorize command will show you a JSON token. Save this to a password manager.

## Add pCloud to Rclone configuration

On the machine where your `resticprofile` backup profile wants to use the pCloud remote, run `rclone config`. Enter `n` to set up a new remote, and give it a name, i.e. `pcloud`.

When you are presented with a list of remotes, type `pcloud` and hit enter. Leave the `client_id` and `client_secret` by pressing Enter when prompted for them, then type `n` when prompted to edit advanced config.

Answer `N` when you are asked if you want to use a web browser to automatically authenticate rclone with the remote.

This will walk you through choosing a new remote, then `pcloud`, and you should answer `n` at the prompt to autoconfig. You will then be prompted to input your `config_token`; paste [the JSON you copied from authenticating earlier](#get-your-pcloud-token) and hit enter, then finish setting up your new remote.

When you are finished setting up the pCloud remote, you will have a new line in your `~/.config/rclone/rclone.conf`.

## Setup pCloud remote in your profiles.yaml

Create a profile like this in your `profiles.yaml` for resticprofile:

```yaml
## ...
#  other options, like global, default, groups, etc

## Backup to pCloud via rclone
remote_pcloud:
  inherit: default

  ## Use rclone:<remote-name>: to tell resticprofile to use the rclone pcloud backend you configured.
  repository: "rclone:pcloud:path/in/pcloud/to/restic-repo"
  password-file: "/path/to/remote_pcloud_main"
	
  env:
    ## so 'sudo resticprofile' commands work
    RCLONE_CONFIG: "/home/user/.config/rclone/rclone.conf"

  backup:
    source:
      - "/path/to/backup"
    read-concurrency: 4
    skip-if-unchanged: true
    verbose: true
    exclude:
      - ".tmp/"
      - ".cache/"
    exclude-cloud-files: true
    group-by: "tags,host,paths"
    schedule: "daily"
    schedule-permission: "system"
    schedule-priority: "standard"
    schedule-lock-mode: default
    schedule-lock-wait: 15m30s

  forget:
    keep-daily: 21
    keep-weekly: 12
    keep-monthly: 36
    prune: true

  check:
    schedule: "03:00"
    schedule-lock-wait: 30m

  tags:
    - remote
    - remote_pcloud
    - privileged
```

Now when you run `resticprofile -c ~/profiles.yaml --name remote_pcloud backup`, Restic will connect to pCloud and backup to the repository stored at the path you specified.
