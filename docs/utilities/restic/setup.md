---
tags:
  - linux
  - windows
  - mac
  - restic
  - utilities
  - backup
---

# Restic Setup

!!! WARNING

    This documentation is the system I've settled on for my own Restic backups.
    I will explain it in detail and if it sounds like something you'd like to replicate,
    it should work the same on your machine.

    Your needs may differ from mine, but hopefully you can adapt some of the work here for
    your own needs.

    Restic provides a [quickstart guide](https://restic.readthedocs.io/en/latest/010_introduction.html),
    which you should run through at least once to learn the steps.

While you can pass [many options as CLI args to `restic`](https://restic.readthedocs.io/en/latest/manual_rest.html), the setup below sets up a pipeline of sorts for providing `restic` commands with the values it needs.

## .restic dir

Create a directory at `~/.restic`. This is where you will store your Restic configurations.

Create the following directories in `~/.restic`:

- `~/.restic/ignores/`: This directory will store "restic ignore" files, which you can pass with `restic src/ --exclude-file ~/.restic/ignores/ignore_filename`
    - Read more in the [ignore/exclude docs](exclude.md)
- `~/.restic/passwords/`: 
    - Storing a repository password in a file is not the most secure, but can be used for smaller/non-sensitive backups, or while you're still learning Restic.
    - When creating a repository, you're prompted for a password. Paste the password you used into a file in `~/.restic/passwords/password_filename` (you can use any filename).
    - You can then set the env var (either in `~/.bashrc` or in a script before executing a `restic` command) `RESTIC_PASSWORD_FILE="~/.restic/passwords/password_filename`
    - Read more in the [handling repository passwords docs](passwords.md)
- `~/.restic/repo/`: (optional) You can create a symlink to your backup directory if you want, so you can use `restic -r ~/.restic/repo`:
    - `ln -s /path/to/restic_repo /home/$USER/.restic/repo`

## .resticrc file

In your `~/.restic` directory, you should also create a `.resticrc` file. This file can be used to provide Restic's env vars to the shell.

```shell title="~/.restic/.resticrc" linenums="1"
## Export path to the file with your repository file
export RESTIC_PASSWORD_FILE="/home/username/.restic/passwords/password_filename"
## Export path to file containing the path to the repository that the password unlocks
export RESTIC_REPOSITORY_FILE="/home/username/.restic/repo_path"

```

After creating your `.resticrc` file, you can source it in your profile, i.e. by adding this to `~/.bashrc`:

```shell title="~/.basrc" linenums="1"
## Other .bashrc entries above

## Source ~/.restic/.resticrc if it exists
if [[ -f "$HOME/.restic/.resticrc" ]]; then
  . "$HOME/.restic/.resticrc"
fi

```

This step is optional, but will let you run `restic` commands directly without needing to provide a `-r/--repository` or `--password-file` parameter.

You can also source this file in a shell script to add the `RESTIC_PASSWORD_FILE` and `RESTIC_REPOSITORY_FILE` to the script's environment.
