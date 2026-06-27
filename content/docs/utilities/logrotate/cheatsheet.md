---
title: "Cheatsheet"
date: 2026-06-27T00:56:48-04:00
draft: true
weight: 10
toc: true
keywords: []
tags:
  - "logrotate"
  - "logs"
  - "linux"
  - "util"
---

## Logrotate Cheatsheet

| Command                                              | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- |
| `sudo logrotate -d /etc/logrotate.conf`              | Validate config without making changes               |
| `sudo logrotate -d /etc/logrotate.d/config-filename` | Validate a single policy file without making changes |
| `sudo logrotate -v /etc/logrotate.conf`              | Enable verbose output                                |
| `sudo logrotate -f /etc/logrotate.conf`              | Force every log to rotate immediately                |
| `sudo logrotate -f /etc/logrotate.d/config-filename` | Force only 1 policy                                  |
| `sudo systemctl status logrotate.timer`              | Check if `logrotate` is running on a timer           |

## Example policy files

### General purpose config

This is a good generic policy for most types of log files. The rules for this policy are:

- Rotates logs at 50MB
- Rotates logs weekly
- Keeps 3 months of rotated logs
- Compresses rotated logs
  - Waits 1 rotation before compressing the most recently compressed log
- Skips missing target files and empty logs
- Creates/initializes log file when it runs and sets ownership
  
```plaintext
/var/log/myapp.log {
    size 50M
    weekly
    maxage 90

    rotate 12

    compress
    delaycompress

    missingok
    notifempty

    #################################
    # Choose 1 of the options below #
    #################################
    
    ## Create log file & assign permissions if it doesn't exist
    create 0644 username groupname
}
```

### Log in user's $HOME

Rotate a file in a user `alice`'s home directory when it reaches 10MB or every month, whichever comes first:

```plaintext
/home/alice/.logs/some-logfile.log {
    size 10M
    monthly
    maxage 30

    rotate 4

    compress
    delaycompress

    missingok
    notifempty

    copytruncate
}
```

### Daily rotate a busy app's logs

Rotate logs for a busy app daily, but only if there's at least 50MB of data in the log:

```plaintext
/var/log/myapp.log {
    daily
    minsize 50M

    rotate 14

    compress
    delaycompress

    missingok
    notifempty

    create 0640 myapp myapp
}
```

### Rotate webserver logs when they reach 500MB

```plaintext
/var/log/nginx/access.log {
    maxsize 500M

    rotate 30

    compress

    create 0640 www-data adm

    postrotate
        systemctl reload nginx
    endscript
}
```

### Create log archives

Archive logs weekly, keeping 3 months of weekly logs with date-based filenames. Produces log files like:

- `archive.log`
- `archive.log-2026-06-20.gz`
- `archive.log-2026-06-13.gz`

```plaintext
/var/log/archive.log {
    weekly

    rotate 12

    dateext
    dateformat -%Y-%m-%d

    compress

    create 0644 root root
}
```

### Move old logs to another directory on rotate

```plaintext
/var/log/myapp.log {
    weekly

    rotate 8

    olddir /var/log/archive

    compress

    create 0644 myapp myapp
}
```

### Apply policy to any .log file in /var/log

```plaintext
/var/log/myapp/*.log {
    daily

    rotate 7

    compress

    sharedscripts

    postrotate
        systemctl reload myapp
    endscript
}
```

### Keep 1 year of monthly logs

```plaintext
/var/log/audit.log {
    monthly

    rotate 12

    compress

    create 0600 root root
}
```

### Delete old logs after 90 days

```plaintext
/var/log/events.log {
    weekly

    rotate 100

    maxage 90

    compress
}
```

### Rotate logs by time, regardless of size

```plaintext
/var/log/cron.log {
    daily

    rotate 30

    compress

    missingok
    notifempty

    create 0644 root root
}
```

### Rotate a large log at 2GB and archive with `xz` compression

```logrotate
/var/log/debug.log {
    size 2G

    rotate 10

    compress
    compresscmd /usr/bin/xz
    uncompresscmd /usr/bin/unxz
    compressext .xz
    compressoptions -9

    create 0644 root root
}
```

### Perform an action after rotating

```shell
/var/log/mydaemon.log {
    weekly

    rotate 8

    compress

    create 0640 mydaemon mydaemon

    postrotate
        kill -HUP $(cat /run/mydaemon.pid)
    endscript
}
```
