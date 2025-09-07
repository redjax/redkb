---
tags:
  - restic
  - resticprofile
---

# SSH/SFTP

SSH/SFTP remote connects to a repository on a remote machine via SSH.

## Setup

### SSH key setup

Create an SSH key to connect to the remote with using:

```shell title="Create SSH keypair"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/resticprofile_id_rsa -N ""
```

Create/edit `~/.ssh/config` and add an entry for your remote host:

```plaintext title="SSH config file" linenums="1"
Host your-remote
  HostName <IP or FQDN of remote host>
  User <remote username>
  # Port 22  # uncomment and change this if SSH is running on a different port on the remote
  IdentityFile ~/.ssh/resticprofile_id_rsa

```

!!! tip "Run resticprofile SSH backup as root/with sudo"

    `resticprofile` requires root/sudo permissions to backup any path the user would also need root access to interact with. When using SSH as a backup destination, you can add a line to `/root/.ssh/config` that maches the one you added in [the setup instructions](#setup), except for `IdentityFile`, use the full path instead of `~`, i.e.:

    ```plaintext title="Root user's ~/.ssh/config" linenums="1"
    Host your-remote
      HostName <IP or FQDN of remote host>
      User <remote username>
      # Port 22  # uncomment and change this if SSH is running on a different port on the remote
      IdentityFile /home/<username-you-run-resticprofile-as>/resticprofile_id_rsa
    ```

    Now you can run `sudo resticprofile -c /home/<username-you-run-resticprofile-as>/profiles.yaml ...` and connect to the remote repository as the root user.

Copy the SSH key to your remote with `ssh-copy-id -i ~/.ssh/resticprofile_id_rsa username@<ip-or-fqdn>`, or manually copy the contents of `~/.ssh/resticprofile_id_rsa.pub` to the remote host's `~/.ssh/authorized_keys`.

!!! warning "Remote host unknown"

    The first time you connect to a remote host via SSH, you will see a warning about host authenticity, like:

    ```
    The authenticity of host '111.222.333.444 (111.222.333.444)' can't be established.
    RSA key fingerprint is f3:cf:58:ae:71:0b:c8:04:6f:34:a3:b2:e4:1e:0c:8b.
    Are you sure you want to continue connecting (yes/no)? 
    ```

    You can proceed past this, but note that you might see a similar message when using `sudo resticprofile`. You will need to accept this warning the first time you can connect. Your scheduled backups to an SSH destination will not work until this warning has been acknowledged.

## Setup SSH remote in your profiles.yaml

Create a profile like this in your `profiles.yaml` for resticprofile (note: replace `<host-name-in-ssh-config>` with the `Host` value from [your `~/.ssh/config` file](#ssh-key-setup)):

```yaml title="SSH/SFTP remote for resticprofile" linenums="1"
## ...
#  other options like global, default, and groups

remote_ssh:
  inherit: default
  ## After initializing with the master key, you can create a new key and switch to it with:
  #    $> restic -r sftp:<host-name-in-ssh-config>:/remote/path/to/restic-repo key add
  repository: sftp:<host-name-in-ssh-config>:/remote/path/to/restic-repo
  password-file: "/home/user/.restic/passwords/remote_callisto_user"

  backup:
    verbose: true
    source:
      - "/local/path/to/backup"
    read-concurrency: 4
    skip-if-unchanged: true
    exclude:
      - ".tmp/"
      - ".cache/"
    exclude-cloud-files: true
    group-by: "tags,host,paths"
    schedule: "daily"
    schedule-permission: "system"
    schedule-priority: "standard"
    schedule-lock-mode: default
    schedule-lock-wait: 15m30s

  tags:
    - remote
    - remote_callisto
    - git
    - privileged

```

Now you can run `resticprofile -c ~/profiles.yaml --name remote_ssh backup` (or with `sudo` for root/privileged backups).
