---
tags:
  - restic
  - resticprofile
---

# profiles.yaml

`resticprofile` operates off of YAML files that define backup "profiles" for Restic. [Read more about profile configuration in the `resticprofile` Getting Started docs](https://creativeprojects.github.io/resticprofile/configuration/getting_started/index.html).

## Schedules

You can add schedules & retention policies to your backups using a [schedule configuration](https://creativeprojects.github.io/resticprofile/schedules/configuration/index.html). Using options like `schedule:`, `schedule-permission:`, `schedule-priority:`, and more, you can set specific backup profiles to run at a given interval, or to run cleanup operations occasionally & automatically.

!!! tip
    
    [Read more about scheduling in the `resticprofile` docs](https://creativeprojects.github.io/resticprofile/schedules/configuration/index.html#schedule).

### Example schedule

The example below defines a backup, and schedules for cleanup & caching. The schedules are:

- Retains the 2 most recent backups
- Retains 24 hourly snapshots for jobs that run hourly
- Retains 7 daily snapshots for jobs that run daily
- Retains 4 weekly snapshots for jobs that run weekly
- Skips deleting snapshots that would be deleted by one of the conditions above, if it has a tag `forever`
- Runs a prune operation when the scheduled cleanup runs
  - Prunes weekly by default
- Checks the backups once a week

```yaml
---
version: "1"

global:
  ## Set scheduler options globally. You can still override in individual backup profiles
  scheduler: auto
  schedule-defaults:
    permission: auto

default:
  repository: "local:/path/to/restic-repo"
  password-file: "/path/to/restic/password"

  backup:
    skip-if-unchanged: true
    group-by: "tags,host,paths"

  ## Define backup retention policy
  #  https://creativeprojects.github.io/resticprofile/schedules/index.html
  forget:
    keep-last: 2
    keep-hourly: 24
    keep-daily: 7
    keep-weekly: 4
    keep-tag:
      - forever
    prune: true

  ## Define pruning policy
  #  https://creativeprojects.github.io/resticprofile/reference/profile/prune/index.html
  prune:
    schedule: "weekly"
    schedule-permission: "auto"

  ## Checks the repository for errors
  #  https://creativeprojects.github.io/resticprofile/reference/profile/check/index.html
  check:
    schedule: "weekly"
    schedule-after-network-online: false
    schedule-ignore-on-battery: false
    schedule-ignore-on-battery-less-than: 20
    read-data: true
    with-cache: false

```

## Example Windows profile

In your `$env:USERPROFILE` path, create a file `profiles.yaml`. This will be where you define your backups. You can create multiple profile files, but it's easy to start by just keeping them all in 1 place.

This is an example of a `profiles.yaml` for a Windows machine, defining defaults for all jobs that can be overridden, and a number of paths to back up:

```yaml
# yaml-language-server: $schema=https://creativeprojects.github.io/resticprofile/jsonschema/config.json
---

## resticprofile configuration
version: "1"

global:
  default-command: ls latest
  initialize: true
  priority: low
  ## Restic won't start a profile if there's less than 100MB of RAM available
  min-memory: 100
  scheduler: auto
  schedule-defaults:
    permission: auto

groups:
  basic:
    - home

  full-backup:
    - c_scripts
    - home

## Set defaults that profiles can inherit
default:
  repository: "local:X:\\path\\to\\restic-repo"
  password-file: "C:\\Users\\username\\.restic\\passwords\\user_access.txt"

  ## Backup operation defaults
  #  https://creativeprojects.github.io/resticprofile/reference/profile/backup/index.html
  backup:
    verbose: false
    one-file-system: false
    read-concurrency: 4
    skip-if-unchanged: true
    group-by: "tags,host,paths"
    exclude:
      - *.tmp
      - *.log
      - *.log.*
      - "Temp"
      - "$RECYCLE.BIN"
      - "\temp"
      - "\tmp"
      - "\Users\*\AppData\Local\Temp\"
      - "\Users\*\AppData\Local\Package Cache"
      - "\Users\*\AppData\Roaming\*\cache\"
      - "\Users\*\Local\Temp"
      - "\Users\*\Local\Microsoft\Windows\INetCache"
    exclude-file: "C:\\Users\\username\\.restic\\ignores\\default"
    ## Exclude files like OneDrive On-Demand Files
    exclude-cloud-files: true

  ## Define backup retention policy
  #  https://creativeprojects.github.io/resticprofile/reference/profile/retention/index.html
  forget:
    keep-last: 2
    keep-hourly: 24
    keep-daily: 7
    keep-weekly: 4
    keep-tag:
      - forever
    prune: true

  ## Define pruning policy
  #  https://creativeprojects.github.io/resticprofile/reference/profile/prune/index.html
  prune:
    schedule: "weekly"
    schedule-permission: "auto"

  ## Checks the repository for errors
  #  https://creativeprojects.github.io/resticprofile/reference/profile/check/index.html
  check:
    schedule: "weekly"
    schedule-after-network-online: false
    schedule-ignore-on-battery: false
    schedule-ignore-on-battery-less-than: 20
    read-data: true
    with-cache: false

  ## Cache settings
  #  https://creativeprojects.github.io/resticprofile/reference/profile/cache/index.html
  cache:
    cleanup: true
    max-age: 30
    no-size: false

  ## ignore restic warnings when files cannot be read
  no-error-on-warning: true

home:
  inherit: default

  backup:
    verbose: true
    source:
      - "C:\\Users\\username"

    ## Add more ignore files. They will be merged with the default
    #  ignore defined in the default: profile
    exclude-file:
      - "C:\\Users\\username\\.restic\\ignores\\home"
      - "C:\\Users\\username\\.restic\\ignores\\gitdir"
      - "C:\\Users\\username\\.restic\\ignores\\desktop"
    ## Run backup twice a day
    schedule: "*/12:*"
    schedule-permission: "user"
    schedule-priority: "standard"
    schedule-lock-mode: default
    schedule-lock-wait: 15m30s

  tags:
    - home
    - userland

  check:
    schedule: "*-*-01 03:00"

c_scripts:
  inherit: default

  backup:
    verbose: true
    source:
      - "C:\\scripts"
    exclude-file:
      - "C:\\Users\\username\\.restic\\ignores\\gitdir"
    ## Run backup daily
    schedule: "daily"
    schedule-permission: "user"
    schedule-priority: "standard"
    schedule-lock-mode: default
    schedule-lock-wait: 15m30s

  tags:
    - scripts

  check:
    schedule: "*-*-01 03:00"

```

After configuring the `profiles.yaml`, you can use `resticprofile -c path\to\profiles.yaml` to run the default backups. You can also run one of the backup "groups" with `resticprofile -c path\to\profiles.yaml --name <group_name>`

## Example Linux profile

```yaml
# yaml-language-server: $schema=https://creativeprojects.github.io/resticprofile/jsonschema/config.json
---
version: "1"

###
# This is a basic default profile I use that's kind of a
# bare-minimum for all of my machines, and the starting point for
# other profiles.
#
# To use this profile as-is, copy it to /home/user/profiles.yaml,
# or pass it with `resticprofile -c /path/to/default.yaml`
###

global:
  default-command: backup
  initialize: true
  priority: low
  min-memory: 100

groups:
  full-backup:
    - home

  userland:
    - home

default:
  ## Path must exist. If you don't want to run resticprofile as root,
  #  make sure it's owned by the user running resticprofile, i.e.
  #  chmod 700 /opt/restic  (if repository is /opt/restic/repo)
  repository: "local:/opt/restic/repo"
  ## Create a password with:
  #    $> resticprofile generate --random-key $KEY_LENGTH > /path/to/restic.key
  password-file: ""
  default-command: snapshots
  initialize: false
  priority: low
  min-memory: 100

  ## Define backup retention policy
  #  https://creativeprojects.github.io/resticprofile/schedules/index.html
  forget:
    keep-last: 2
    keep-hourly: 24
    keep-daily: 7
    keep-weekly: 4
    keep-tag:
      - forever
    prune: true

  ## Define pruning policy
  #  https://creativeprojects.github.io/resticprofile/reference/profile/prune/index.html
  prune:
    schedule: "weekly"
    schedule-permission: "auto"

  ## Backup operation defaults
  #  https://creativeprojects.github.io/resticprofile/reference/profile/backup/index.html
  backup:
    verbose: false
    one-file-system: false
    read-concurrency: 4
    skip-if-unchanged: true
    exclude:
      - ".tmp/"
      - ".cache/"
    exclude-file:
      - "/home/user/.restic/ignores/default"
    exclude-cloud-files: true
    group-by: "tags,host,paths"

  ## Checks the repository for errors
  #  https://creativeprojects.github.io/resticprofile/reference/profile/check/index.html
  check:
    schedule: "weekly"
    schedule-after-network-online: false
    schedule-ignore-on-battery: false
    schedule-ignore-on-battery-less-than: 20
    read-data: true
    with-cache: false

  ## Cache settings
  #  https://creativeprojects.github.io/resticprofile/reference/profile/cache/index.html
  cache:
    cleanup: false
    max-age: 30
    no-size: false

  no-error-on-warning: true

## Backup home dir
home:
  inherit: default
  default-command: backup

  backup:
    verbose: true
    source: "/home/user"
    read-concurrency: 4
    skip-if-unchanged: true
    exclude:
      - ".tmp/"
      - ".cache/"
    exclude-file:
      - "/home/user/.restic/ignores/default"
      - "/home/user/.restic/ignores/home"
    exclude-cloud-files: true
    group-by: "tags,host,paths"
    schedule: "*/12:*"
    schedule-permission: "user"
    schedule-priority: "standard"
    schedule-lock-mode: default
    schedule-lock-wait: 15m30s

  tags:
    - home
    - userland

```
