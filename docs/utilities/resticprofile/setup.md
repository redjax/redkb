---
tags:
  - restic
  - resticprofile
---

# Setup

!!! info

    The steps in this section are the way I personally have managed my Restic/resticprofile configurations. For most of the file/directory paths in this guide, you could substitute whatever other paths you want, and change those paths in any of the commands listed in the guide.

    Also note that using a file to store your password is bad practice and security. This guide is meant to be a quick setup for home/personal use, where the master key file is deleted once a 'user access' key is created. In a production setup, you would want to use an environment variable, or the `--password-cmd` option (or [the `RESTIC_PASSWORD_COMMAND` env var for resticprofile](https://creativeprojects.github.io/resticprofile/reference/profile/index.html)) to retrieve the password from a vault.

## Initialize a new repository

- Create a directory `~/.restic/`
- Create another directory `~/.restic/password/`
    - Run the following commands to generate a 'main' and 'user' access key/password:
        - `resticprofile generate --random-key 4096 > ~/.restic/password/main`
            - This key is incredibly important, make sure you back it up somewhere like a password manager!
            - You can create and revoke keys as long as you still have this password.
            - Use it only when required, i.e. for creating new keys. Once you've setup the repository the first time and added your user access key, you should delete the file containing the master password (`rm ~/.restic/password/main`)
        - `resticprofile generate --random-key 4096 > ~/.restic/password/user_access`
        - (Optional) Generate any other passwords you want to use, just make sure you save all of them in a password manager/vault somewhere.
- Create a file `~/profiles.yaml` (read more about profiles on the [profiles.yaml page](profiles.md)).
    - We will start small with [a simple backup profile](#basic-profile), and other sections of this documentation will detail adding more profiles later.
- After creating your `profiles.yaml`, run `resticprofile -c ~/profiles.yaml --name <backup-profile-name> init`
- Next, add your `~/.restic/passwords/user_acces` key with `resticprofile -c ~/profiles.yaml --name <backup-profile-name> key add --new-password-file ~/.restic/passwords/user_access`
    - With the user access key added, edit your `~/profiles.yaml` and replace the `/home/user/.restic/passwords/main` line with `/home/user/.restic/passwords/user_access`.
    - The only time you will need your master key going forward is to add or revoke keys. Restic/resticprofile will prompt you for the master password when needed, and you can just paste it.
    - Otherwise, use your `user_access` key for everything after initializing the repository.
- (Optional) If you want to add ignore patterns to a backup profile, you can create a file, i.e. `~/.restic/ignores/default`, with patterns that should be ignored any time a backup profiles specifies `exclude-file: ~/.restic/ignores/default`.
    - Example rules:
        - `*.tmp`
        - `*.bak`
        - `*.log.*`
    - Read more in the [Excludes patterns section](excludes.md)

## Use resticprofile with an existing repository

If you already have a Restic repository, you can add it to your `profiles.yaml` and give it your password, and `resticprofile` will seamlessly take over the backup operations.

## Create backup profiles

`resticprofile` works off of profiles you define in YAML files. `resticprofile` looks for a file named `profiles.yaml` in the current directory, then in `~/profiles.yaml` in the user's `$HOME` directory.

You can provide the path to a configuration file with `resticprofile -c /path/to/your_profiles.yaml`.

The file can have any name, but if you use something other than `profiles.yaml`, you will have to provide it to `resticprofile` each time you run a command.

Navigate to the [profiles.yaml page] to read more about backup profiles.

### Basic profile

A simple starting point that backs up your `~/.bashrc`, `~/.profile`, and `~/.bash_aliases`.

```yaml
# yaml-language-server: $schema=https://creativeprojects.github.io/resticprofile/jsonschema/config.json

## The line above provides the profiles.yaml schema so editors like VSCode have syntax highlighting & completion.
---

## resticprofile configuration
version: "1"

## Set defaults that other profiles can inherit
default:
  repository: "local:/path/to/restic-repo"
  ## Change this to '~/.restic/passwords/user_access'
  #  after initializing the repository and adding the user_access key.
  password-file: "~/.restic/passwords/main"
  
## Create a profile to backup ~/.bash* dotfiles.
#  When you run resticprofile, call this profile with
#  `--name dot-bash-files
dot-bash-files:
  ## Inherit options defined in the default profile above. If an option
  #  is specified in default but not in this profile, the default setting
  #  will be used. Any options you define in this profile override the defaults.
  inherit: default

  ## Define the backup job
  backup:
    ## Enable verbose logging to see more output
    verbose: true
    ## Set the path(s) that should be backed up
    source:
      - "/home/user/.bashrc"
      - "/home/user/.profile"
      - "/home/user/.bash_aliases"
    
    ## Define 1 or more exclude patterns, and any path
    #  that matches during a backup will be skipped/excluded.
    #  These patterns would be irrelevant for this job since we're
    #  specifying the files explicitly. These excludes are merged
    #  with any defined in the default profile, or passsed with an
    #  exclude-file.
    exclude:
      - *.tmp
      - *.bak

    ## You can optionally pass the path(s) to 1 or more files
    #  that have ignore patterns for restic. The syntax
    #  is similar to .gitignores.
    #  Excludes are merged; anything defined in default, or
    #  passed as an explicit exclude: list (read above).
    exclude-file:
      - "/path/to/default_excludes_filename"
      - "/path/to/another_excludes_filename"

```

## Take your first backup

Now that your profiles are all set up, you can test your configuration with  `resticprofile -c ~/profiles.yaml --name <backup-profile-name> backup --dry-run`. Using `--dry-run` will show you any issues the backup might encounter, like permission errors or invalid syntax.

If you do not see any errors, run it again without `--dry-run` to take your first backup. You can see your backups with `resticprofile -c ~/profiles.yaml --name <backup-profile-name> snapshots`.
