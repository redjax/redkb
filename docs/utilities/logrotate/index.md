---
tags:
  - linux
  - logging
  - utilities
---

# Logrotate

[Logrotate](https://wiki.archlinux.org/title/Logrotate) is a Linux utility for rotating logs by reading policies defined in `/etc/logrotate.d/`. You can read more about setting up logrotate in [this RedHat blog entry](https://www.redhat.com/en/blog/setting-logrotate).

You can create a logrotate policy for pretty much any file you output logs to, but it is recommended to store your logs in `/var/log/` or a subdirectory in that path, i.e. `/var/log/program_name/some_logfile.log`.

Logrotate policies should be defined in files in the `/etc/logrotate.d/` directory.

!!! TIP

    When creating a logrotate policy file, choose a name that describes the log file it applies to,
    and create the file at the root of `/etc/logrotate.d/`, don't use subdirectories. There are ways
    to do that, but unless you have trouble maintaining your policies in a 'flat' structure, logrotate
    will not detect your nested policies.

    An example of a logrotate policy that rotates `/var/log/some_program/function.log` could be named
    `/etc/logrotate.d/some_program_function`.

    You do **not** need to put a file extension in the filename.

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

## Examples

### Backup home directory with logging

For this example, let's say you have a cron job that runs every 6 hours and creates a backup of your home directory. The job outputs its logs to `/var/log/home_backup/backup.log`. You want to rotate this file at 10MB, or every week (whichever occurs first), retaining 2 weeks worth of backups, and recreate the logfile once it's rotated.

You create logrotate policies in `/etc/logrotate.d/<logrotate_policy_name>`. The file can be named whatever you want, but it's advisable to make the name of the file descriptive of the log file it's rotating. You can omit a file extension from the file name.

Create a file at `/etc/logrotate.d/home_dir_backup`:

```plaintext
/var/log/home_backup.log {
    size 10M           # Rotate if log file reaches 10MB
    weekly             # Or rotate weekly, whichever happens first
    rotate 14          # Keep 14 rotated logs (2 weeks worth)
    compress           # Compress rotated logs with gzip
    delaycompress      # Delay compression until next rotation cycle
    missingok          # Don't issue error if log file is missing
    notifempty         # Skip rotation if log file is empty
    create 0640 root adm  # Recreate log file with correct permissions and ownership. You can also use $USER for the user and group
}

```

Now, if you schedule a cron job like this, the log file will automatically rotate:

```shell
0 */6 * * * cp -R /home/username /backup/homedir > /var/log/home_backup.log 2>&1  # this is the path you should use in the logrotate policy
```
