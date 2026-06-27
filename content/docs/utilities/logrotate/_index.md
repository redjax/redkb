---
title: "Logrotate"
date: 2025-09-01T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - util
  - logrotate
  - linux
---

[Logrotate](https://wiki.archlinux.org/title/Logrotate) is a Linux utility for rotating logs by reading policies defined in `/etc/logrotate.d/`. You can read more about setting up logrotate in [this RedHat blog entry](https://www.redhat.com/en/blog/setting-logrotate).

You can create a logrotate policy for pretty much any file you output logs to, but it is recommended to store your logs in `/var/log/` or a subdirectory in that path, i.e. `/var/log/program_name/some_logfile.log`.

Logrotate policies should be defined in files in the `/etc/logrotate.d/` directory.

> [!TIP]
> When creating a logrotate policy file, choose a name that describes the log file it applies to,
> and create the file at the root of `/etc/logrotate.d/`, don't use subdirectories. There are ways
> to do that, but unless you have trouble maintaining your policies in a 'flat' structure, logrotate
> will not detect your nested policies.
>
> An example of a logrotate policy that rotates `/var/log/some_program/function.log` could be named
> `/etc/logrotate.d/some_program_function`.
>
> You do **not** need to put a file extension in the filename. The file must be owned by `root`.

## Policy file

A policy file defined at `/etc/logrotate.d/policy_filename` should start with the path to the file it applies to. For example, a policy that rotates a log at `/var/log/program_name/function.log` would start with:

```plaintext title="logrotate policy file path"
/var/log/program_name/function.log {}
```

You then add your configurations in the `{}` mapping.

For example, a logrotate policy that:

- rotates the file daily, keeping the last 14 rotated logs
- compresses each rotated file with `gzip`, but delays the most recently compressed logfile (for easy access of the most recently rotated log file)
- does not error if the log file is missing
- skips if the log file's contents are empty
- recreates the file after rotation with `chmod 0640` and `chown root:adm`

```plaintext title="Example logrotate policy" linenums="1"
/var/log/program_name/function.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
}
```

### Policy options

You can configure new `logrotate` policies by creating a file in `/etc/logrotate.d` as root. Each policy begins with the path to the log file, and has a set of policies in `{braces}`. These options control the actions `logrotate` takes when it runs its schedule.

Some commonly used options:

| Directive          | Example                       | Description                                                                               |
| ------------------ | ----------------------------- | ----------------------------------------------------------------------------------------- |
| `daily`            | `daily`                       | Rotate logs every day.                                                                    |
| `weekly`           | `weekly`                      | Rotate logs every week.                                                                   |
| `monthly`          | `monthly`                     | Rotate logs every month.                                                                  |
| `yearly`           | `yearly`                      | Rotate logs every year.                                                                   |
| `hourly`           | `hourly`                      | Rotate every hour (if logrotate runs hourly).                                             |
| `minutes N`        | `minutes 30`                  | Rotate every 30 minutes (supported in newer versions).                                    |
| `size`             | `size 10M`                    | Rotate when the log reaches 10 MB. Supports `k`, `M`, and `G` (e.g. `500k`, `10M`, `2G`). |
| `minsize`          | `minsize 5M`                  | Rotate on the scheduled interval only if the log is at least 5 MB.                        |
| `maxsize`          | `maxsize 100M`                | Rotate immediately if the log exceeds 100 MB, regardless of schedule.                     |
| `rotate`           | `rotate 7`                    | Keep the last 7 rotated logs.                                                             |
| `maxage`           | `maxage 30`                   | Delete rotated logs older than 30 days.                                                   |
| `minage`           | `minage 7`                    | Do not rotate logs newer than 7 days.                                                     |
| `compress`         | `compress`                    | Compress rotated logs (gzip by default).                                                  |
| `nocompress`       | `nocompress`                  | Disable compression.                                                                      |
| `compresscmd`      | `compresscmd /usr/bin/xz`     | Use a different compression program.                                                      |
| `uncompresscmd`    | `uncompresscmd /usr/bin/unxz` | Program used to decompress logs.                                                          |
| `compressext`      | `compressext .xz`             | Extension for compressed logs.                                                            |
| `compressoptions`  | `compressoptions -9`          | Pass options to the compression program.                                                  |
| `delaycompress`    | `delaycompress`               | Compress starting with the second rotation.                                               |
| `copy`             | `copy`                        | Copy the log without modifying the original.                                              |
| `copytruncate`     | `copytruncate`                | Copy the log, then truncate the original in place.                                        |
| `renamecopy`       | `renamecopy`                  | Rename, copy back, and remove the renamed file after rotation.                            |
| `nocopytruncate`   | `nocopytruncate`              | Disable copy-and-truncate behavior.                                                       |
| `create`           | `create 0644 alice alice`     | Create a new log file with the specified permissions and owner.                           |
| `nocreate`         | `nocreate`                    | Do not create a new log after rotation.                                                   |
| `olddir`           | `olddir /var/log/archive`     | Store rotated logs in another directory.                                                  |
| `noolddir`         | `noolddir`                    | Keep rotated logs beside the original log.                                                |
| `missingok`        | `missingok`                   | Ignore missing log files.                                                                 |
| `nomissingok`      | `nomissingok`                 | Treat a missing log as an error.                                                          |
| `notifempty`       | `notifempty`                  | Do not rotate empty log files.                                                            |
| `ifempty`          | `ifempty`                     | Rotate logs even if they are empty.                                                       |
| `dateext`          | `dateext`                     | Use date-based filenames (e.g. `app.log-20260627`).                                       |
| `nodateext`        | `nodateext`                   | Use numeric suffixes (`.1`, `.2`, etc.).                                                  |
| `dateformat`       | `dateformat -%Y%m%d`          | Customize the date suffix format.                                                         |
| `dateyesterday`    | `dateyesterday`               | Use yesterday's date in rotated filenames.                                                |
| `datehourago`      | `datehourago`                 | Use the previous hour in date-based filenames.                                            |
| `extension`        | `extension .log`              | Preserve the `.log` extension when rotating.                                              |
| `addextension`     | `addextension .bak`           | Append an extra extension to rotated logs.                                                |
| `start`            | `start 5`                     | Start numbering rotated logs at `.5`.                                                     |
| `mail`             | `mail admin@example.com`      | Email rotated logs.                                                                       |
| `nomail`           | `nomail`                      | Disable emailing logs.                                                                    |
| `mailfirst`        | `mailfirst`                   | Mail the newly rotated log.                                                               |
| `maillast`         | `maillast`                    | Mail the oldest log before it is deleted.                                                 |
| `sharedscripts`    | `sharedscripts`               | Run `prerotate`/`postrotate` only once for all logs in the block.                         |
| `nosharedscripts`  | `nosharedscripts`             | Run scripts once per log file.                                                            |
| `prerotate`        | `prerotate ... endscript`     | Run commands before rotation.                                                             |
| `firstaction`      | `firstaction ... endscript`   | Run commands once before any logs are rotated.                                            |
| `postrotate`       | `postrotate ... endscript`    | Run commands after rotation (e.g. reload a service).                                      |
| `lastaction`       | `lastaction ... endscript`    | Run commands once after all rotations complete.                                           |
| `preremove`        | `preremove ... endscript`     | Run commands before deleting an old log.                                                  |
| `su`               | `su alice alice`              | Rotate logs as the specified user and group.                                              |
| `tabooext`         | `tabooext + .rpmnew .bak`     | Ignore files with these extensions.                                                       |
| `taboopat`         | `taboopat + *.disabled`       | Ignore files matching these patterns.                                                     |
| `include`          | `include /etc/logrotate.d`    | Include additional configuration files.                                                   |
| `ignoreduplicates` | `ignoreduplicates`            | Ignore duplicate log file definitions.                                                    |
| `shred`            | `shred`                       | Securely overwrite logs before deletion.                                                  |
| `shredcycles`      | `shredcycles 3`               | Overwrite logs three times before deleting them.                                          |
| `allowhardlink`    | `allowhardlink`               | Allow rotation of logs with multiple hard links.                                          |
| `noallowhardlink`  | `noallowhardlink`             | Refuse to rotate logs with multiple hard links.                                           |
