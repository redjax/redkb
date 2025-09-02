---
tags:
  - linux
  - windows
  - mac
  - utilities
  - bash
  - backup
---

# Restic

[Restic](https://restic.net) is a backup utility written in Go. The tool is fast & relatively simple to setup & script, making it useful for per-machine backups.

Restic works by creating a repository (or multiple repositories) to store backup files in, and does differential snapshot backups on subsequent runs, backing up only what has changed and de-duplicating data in the process.

The repository itself can live on your machine, network, or in cloud storage (Amazon S3, Backblaze B2, an SFTP directory, etc).

Learn more about:

- [Restic setup](setup.md)
- [Excluding files/paths from backups](exclude.md)
- [Handling Restic repository passwords](passwords.md)
- [Scripting `restic` commands](scripting.md)

## Links

- [Restic home](https://restic.net)
- [Restic Github](https://github.com/restic/restic)
- [Restic docs](https://restic.readthedocs.io)
    - [Restic install docs](https://restic.readthedocs.io/en/latest/020_installation.html)
    - [Restic prepare new repo docs](https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html)
