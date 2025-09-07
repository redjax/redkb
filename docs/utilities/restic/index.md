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

## Tips & Tricks

### 'Permission Denied' Errors

If you get a permission error when creating backups, you should use `sudo` to perform the backup. This also means the owner of the backup in restic's repository will be owned by root; any time you run a command that interacts with the repository, i.e. `restic snapshots`, you will get permission errors when restic tries to interact with that path.

You can safely change the ownership of your restic repository path, without affecting the ownership in the repository itself. When restoring a backup, run with `sudo` or as the root user; this will restore paths with their original ownership, i.e. paths owned by root will be restored with root ownership, and paths owned by `$USER` will have ownership restored to the user.

If you restore a restic backup as a regular, non-root user after changing ownership in the restic repository path, you will get a permisssion error.

!!! warning

    When changing ownership in your restic repository path, you will not damage the backup, but you do still need to be mindful of ACLs. You should create a group, i.e. `resticusers`, and set group ownership on your restic repository path.

    If you are running restic on a single-user home machine and are ok with the security risks of your user owning the files in the restic repository, you can safely set ownership with `chmod -R $USER:$USER /path/to/restic-repo` without harming the backups.

## Links

- [Restic home](https://restic.net)
- [Restic Github](https://github.com/restic/restic)
- [Restic docs](https://restic.readthedocs.io)
    - [Restic install docs](https://restic.readthedocs.io/en/latest/020_installation.html)
    - [Restic prepare new repo docs](https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html)
