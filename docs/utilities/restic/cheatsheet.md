---
tags:
  - linux
  - windows
  - mac
  - utilities
  - backup
  - restic
  - cheatsheet
---

# Restic Cheatsheet

The cheat sheets below provide a quick guide for things you might already know but forget the commands/variable names.

## CLI Args

| Arg                                           | Notes                                                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `-r/--repo/--repository /path/to/repo`        | When running `restic` commands, sets the path to the repository.                                                         |
| `--repository-file /path/to/restic_repo_path` | Read the path to a restic repository. Same as passing the path with `-r`, but reads it from a file instead.              |
| `--password-file /path/to/restic_password`    | Read the password to a Restic repository from a file.                                                                    |
| `--password-command <command>`                | Shell command to obtain repository password (i.e. password manager CLI, read vault secret, etc).                         |
| `--key-hint <key>`                            | Key ID of a [Restic repository key](https://restic.readthedocs.io/en/latest/070_encryption.html#manage-repository-keys). |
| `--skip-if-unchanged` | When doing a `restic backup` operation, this will skip snapshotting path(s) that have not changed. |

## Commands

| Command                                                                                                                                                            | Explained                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `restic init --repo /path/to/repo`                                                                                                                                 | Initializes a restic repository at the given path. Note that the path must exist before you run the init command (`mkdir -p /path/to/repo`).                                                                                                               |
| `restic --repo /path/to/backup_repository --password-file ~/.restic/passwords/main backup /home/username --exclude-file ~/.restic/ignores/default --exclude *.jpg` | Creates a backup of `/home/repository` at the path in the `/path/to/backup_repository` path, provides the password in a file `restic` can read, provides a file defining patterns & paths to ignore, and explicitly excludes `.jpg` files from the backup. |
| `restic key add [--password-file path/to/current/password] [--new-password-file path/to/new/password]` | Generate a new key by inputting the master password, then a new password that can also unlock the database. Optionally add `--new-password-file` to output the new password to a file. |

## Environment Variables

| Environment Variable     | Example Value                   | Notes                                                                                                                    |
| ------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `RESTIC_REPOSITORY`      | `/opt/backups/restic/repo_name` | When running `restic` commands, provides the `--repo` value.                                                             |
| `RESTIC_REPOSITORY_FILE` | `/path/to/restic_repo_path`     | Read the path to a Restic repository from a file. You do not need to use `-r/--repo` when this is set.                   |
| `RESTIC_PASSWORD_FILE`   | `/path/to/restic_password`      | Read the password to a Restic repository from a file. Without this, you will be prompted for the repository's password.  |
| `RESTIC_KEY_HINT`        | `eb78040b`                      | Key ID of a [Restic repository key](https://restic.readthedocs.io/en/latest/070_encryption.html#manage-repository-keys). |
