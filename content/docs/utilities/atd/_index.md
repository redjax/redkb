---
title: "Atd"
date: 2026-11-24T20:31:34-05:00
draft: false
weight: 2
toc: true
keywords: []
tags:
  - linux
  - cli
  - systemd
  - atd
---

`atd` is a job scheduler daemon that runs jobs scheduled for later execution. Like cron, but when you only need to run a script on a schedule a single time.

## Installation

- Debian/Ubuntu:

  ```shell
  sudo apt update -y
  sudo apt install -y at
  sudo systemctl enable --now atd
  ```

- RedHat/Fedora/CentOS/AlmaLinux/RockyLinux:

  ```shell
  # DNF
  sudo dnf install -y at
  sudo systemctl enable --now atd

  # YUM
  sudo yum install at
  sudo systemctl enable --now atd
  ```

- openSUSE:

  ```shell
  sudo zypper install at
  sudo systemctl enable --now atd
  ```

- Arch Linux:

  ```shell
  sudo pacman -S at
  sudo systemctl enable --now atd
  ```

## Usage

After [installing `atd`](#installation), start the systemd service with `sudo systemctl enable --now atd`.

```shell
at [-V] [-q QUEUE] [-f FILE] [-mMlv] TIMESPEC...
at [-V] [-q QUEUE] [-f FILE] [-mMkv] -t [[CC]YY]MMDDhhmm[.ss]
```

`at` reads commands from standard input, or from a file with `-f`, and runs them with `/bin/sh`. Press `Ctrl+D` to finish entering commands at the `at>` prompt.

```shell
## Interactive
at 14:30
at> /home/user/backup.sh
at> 

## From a pipe
echo "/home/user/backup.sh" | at now + 10 minutes

## From a file
at -f ./backup.sh 02:00 tomorrow
```

### Time specifications

`TIMESPEC` accepts several forms:

- Time of day: `HH:MM`, `HHMM`, or a 12-hour form such as `3:00 PM`. If the time has already passed today, `at` assumes tomorrow.
- Keywords: `now`, `midnight`, `noon`, `teatime` (4 PM).
- Dates: `month-name day [year]`, `MMDDYY`, `MM/DD/YY`, `DD.MM.YY`, `YYYY-MM-DD`. The date must come after the time of day.
- Relative: `now + 30 minutes`, `now + 1 day`, `4pm + 3 days`.

### Options

| Option     | Description                                                              |
| ---------- | ------------------------------------------------------------------------ |
| `-q QUEUE` | Use the named queue (a single letter).                                   |
| `-f FILE`  | Read commands from `FILE` instead of stdin.                              |
| `-m`       | Send mail to the user when the job finishes, even if there is no output. |
| `-M`       | Never send mail.                                                         |
| `-l`       | List pending jobs. Same as `atq`.                                        |
| `-d`       | Delete a job. Same as `atrm`.                                            |
| `-c JOB`   | Print the job's contents to stdout.                                      |
| `-b`       | Run as `batch`.                                                          |
| `-t TIME`  | Schedule using the `[[CC]YY]MMDDhhmm[.ss]` format [10].                  |
| `-v`       | Show the job's execution time.                                           |
| `-V`       | Print the version.                                                       |

### Managing jobs

```shell
atq          # list pending jobs (same as at -l)
at -c 3      # show the contents of job 3
atrm 3       # remove job 3 (same as at -d 3)
batch        # run when system load is low
```

> [!NOTE]
> `atq` lists only your own jobs, unless you're root, in which case it lists everyone's. Its output has the job number, date, hour, queue, and user.

### Running with sudo

Use `sudo at` to queue the job as root. The job then runs with root privileges, so the commands inside it don't need `sudo`.

```shell
## Pipe a single command
echo "systemctl restart nginx" | sudo at 03:00 tomorrow

## Run a script file as root
sudo at -f /usr/local/bin/maintenance.sh 01:30

## Multiple commands with a heredoc
sudo at now + 1 hour <<'EOF'
apt update -y
apt upgrade -y
EOF

## View pending root jobs
sudo atq
```

If you queue the job as a normal user and call `sudo` inside it, `sudo` needs a password but the job has no terminal. Use `sudo at` as above, or configure passwordless sudo for that command.

### Logging output to a file

To redirect output to a logfile, put the redirect inside the job, before `at`. A redirect after `at` only captures `at`'s own `"job N at ..."` message. Use `>>` to append and `2>&1` to include errors.

```shell
## Log a single command (as your user)
echo "~/scripts/job.sh >> ~/job.log 2>&1" | at now + 5 minutes

## Log a script file's output
at -f ~/scripts/backup.sh 02:00 tomorrow
## (inside backup.sh: ./do-backup >> ~/backup.log 2>&1)

## Log several commands with timestamps
at 23:00 <<'EOF'
{
  echo "Started: $(date)"
  /usr/local/bin/sync.sh
  echo "Finished: $(date)"
} >> ~/sync.log 2>&1
EOF

## Check the log
tail ~/sync.log
```

Quote the heredoc delimiter (`'EOF'`) so `$(date)` runs when the job runs. If you don't redirect, `at` mails any output to the user, and that only works if a mail system is set up.

### Examples

- Run a command 10 minutes from now:

  ```shell
  echo "/usr/local/bin/backup.sh" | at now + 10 minutes
  ```

- Run a script at 2:30 PM today (or tomorrow, if that time has passed):

  ```shell
  at -f ~/scripts/cleanup.sh 14:30
  ```

- Run a command tomorrow at a specific time:

  ```shell
  echo "systemctl restart nginx" | sudo at 03:00 tomorrow
  ```

- Run on a specific date, and mail the output when it finishes:

  ```shell
  at -m 09:00 2026-12-15
  at> /home/user/report.sh
  at> <Ctrl+D>
  ```

- Run a job at 4 PM three days from now, using a heredoc for multiple commands:

  ```shell
  at 4pm + 3 days <<EOF
  cd /var/www/site
  git pull
  systemctl reload nginx
  EOF
  ```

- List and remove pending jobs:

  ```shell
  atq        # list pending jobs
  at -c 5    # view the contents of job 5
  atrm 5     # delete job 5
  ```

- Run a command as root and pipe output to a file `/var/log/backup-at.log`:

  ```shell
  echo "/usr/local/bin/backup.sh >> /var/log/backup-at.log 2>&1" | sudo at 02:00 tomorrow
  ```
