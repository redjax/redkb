---
tags:
    - utilities
    - ssh
---

# Secure Shell (SSH)

!!! warning

    In progress

!!! todo

    - [ ] Document ssh
        - [x] Keyfiles
        - [ ] scp
        - [ ] sshpass

## Quick note on public/private keys

I had a hard time understanding what to do with my private/public keys when I was learning SSH. I don't know why it was a difficult concept for me, but I have worked with enough other people who were confused in the same way I was that I think it's worth it to just spell out what to do with each key.

Your private key (default name is `id_rsa`) should **NEVER** leave the server it was created on, and should not be accessible to any other user (`chmod 600`). There are exceptions to this, such as when uploading a keypair to an Azure or Hashicorp vault, or providing to a Docker container. But in general, when creating SSH tunnels between machines, the private key is meant to stay on the machine it was created on.

Your public key is like your swipe card; when using the `ssh` command with `-f /path/to/id_rsa.pub` and the correct `user@server` combo, you will not need to enter a password to authenticate.

Your public key can also be used for SFTP.

!!! TODO

- [ ] Document converting an SSH key to a `.ppk` file with PuTTY

## Create an SSH key pair

You can create a keypair using the `ssh-keygen` utility. This is installed with SSH (`openssh-server` on Linux, see [installation instructions for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui)), and is available cross-platform.

!!!note

    You can run `$ ssh-keygen --help` on any platform to see a list of available commands. `--help` is not a valid flag, so you will see a warning `unknown option -- -`, but the purpose of this is to show available commands.

If you run `ssh-keygen` without any arguments, you will be guided through a series of prompts, after which 2 files will be created (assuming you chose the defaults): `id_rsa` (your private key) and `id_rsa.pub` (your public key).

You can also pass some parameters to automatically answer certain prompts:

- The `-f` parameter specifies the output file. This will skip the prompt `Enter file in which to save the key`
    - `$ ssh-keygen -f /path/to/<ssh_key_filename>`
    - When using `-f`, a private and public (`.pub`) key will be created
- The `-t` parameter allows you to specify a key type
    - To generate an rsa key (the default key type): `$ ssh-keygen -t rsa`
    - Other types of key types are:
        - `dsa`
        - `ecdsa`
        - `ecdsa-sk`
        - `ed25519`
        - `ed25519-sk`
- The `-b` option allows you to specify the number of bits. For rsa keys, the minimum is `1024` and the default  is `3072`.
  - You can set a stronger value like `4096` with: `$ ssh-keygen -b 4096`

**Example ssh-keygen commands**

```shell title="ssh-keygen commands" linenums="1"

## Generate a 4096-bit RSA key named example_key
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/example_key

## Generate another 4096b RSA key, this time skipping the password prompt
#  Note: This works better on Linux, I'm not sure what the equivalent is
#  on Windows
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

## Install an SSH key on a remote machine for passwordless ssh login

You can (and should) use your SSH key to authenticate as a user on a remote system. There are 2 ways of adding keys for this type of authentication.

!!! note

    Whatever method you use to add your public key to a remote machine, make sure you edit `~/.ssh/config` (create the file if it does not exist). The `ssh` command can use this file to configure connections with SSH keys so you don't have to specify `$ ssh -i /path/to/key` each time you connect to a remote you've already copied a key to.

    ```shell title="~/.ssh/config" linenums="1"

    ## You can set $Host to whatever you want.
    #  You will connect with: ssh $Host
    Host example.com
    ## The actual FQDN/IP address of the server
    HostName example.com
    ## If the remote SSH server is running on a
    #  port other than the default 22, set here
    # Port 222
    ## The remote user your key is paired to
    User test
    ## The public key exists on the remote.
    #  You provide the private key to complete the pair
    IdentityFile ~/.ssh/<your_ssh_key>

    ## On Windows, set "ForwardAgent yes" for VSCode remote editing.
    #  Uncomment the line below if on Windows
    # ForwardAgent yes
    ```

Once you've copied your key, you can simply run `ssh $Host`, where `$Host` is the value you set for `Host` in the `~/.ssh/config` file. The SSH client will find the matching `Host` entry and use the options you specified.

### Method 1: Add local machine's SSH key to remote machine's authorized_keys with ssh-copy-id

```shell title="Add an SSH key for user 'test' on host 'example'" linenums="1"

## Note: If you get a message about trusting the host, hit yes.
#  You will need to type your password the first time
$ ssh-copy-id -i ~/.ssh/your_key.pub test@example
```

### Method 2: Add local machine's SSH key to remote machine's authorized_keys manually

You can also manually copy your public keyfile (`.pub`) to a remote host and `cat` the contents into `~/.ssh/authorized_keys`. The most straightforward way of accomplishing this is to use `scp` to copy the keyfile to your remote host, typing the password to authenticate, then following up by logging in directly with `ssh`.

Instructions:

- Copy your `.pub` keyfile
    - `$ ssh-copy-id -i /path/to/id_rsa.pub test@example.com:/home/test`
- SSH into the remote
    - `$ ssh test@example.com`
    - You will need to type the user's password this time, but once the key is added you can simply use `$ ssh example.com`
    - Make sure you configure a `~/.ssh/config` file, using the instruction in the note in ["Install an SSH key on a Remote Machine for passwordless login"](#install-an-ssh-key-on-a-remote-machine-for-passwordless-ssh-login)
- Move the `.pub` keyfile from the user's home into `.ssh`
    - If the `.ssh` directory does not exist, create it with `mkdir .ssh`
    - `$ mv id_rsa.pub .ssh`
- Change directory to `.ssh` and `cat` the contents of `id_rsa.pub` into `authorized_keys`
    - `$ cd .ssh && cat id_rsa.pub authorized_keys`
- Remove the `id_rsa.pub` key. Now that it's in `authorized_keys`, you don't need the keyfile on the remote machine anymore.

## ~/.ssh chmod permissions

It is crucial your `chmod` permissions are set properly on the `~/.ssh` directory. Invalid permissions will lead to errors when trying to `ssh` into remote machines.

Check the table below for the `chmod` values you should use. To set a value (for example on the `.ssh` directory itself and the keypair):

```shell title="set chmod" linenums="1"

$ chmod 700 ~/.ssh
$ chmod 644 ~/.ssh/id_rsa{.pub}
```

| Dir/File                                                                | Man Page                                                                                                                                                                                 | Recommended Permission | Mandatory Permission |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | -------------------- |
| `~/.ssh/`                                                               | There is no general requirement to keep the entire contents of this directory secret, but the recommended permissions are read/write/execute for the user, and not accessible by others. | 700                    |                      |
| `~/.ssh/authorized_keys`                                                | This file is not highly sensitive, but the recommended permissions are read/write for the user, and not accessible by others\|                                                           | 600                    |                      |
| `~/.ssh/config`                                                         | Because of the potential for abuse, this file must have strict permissions: read/write for the user, and not writable by others                                                          |                        | 600                  |
| `~/.ssh/identity`  <br>`~/.ssh/id_dsa`  <br>`~/.ssh/id_rsa`             | These files contain sensitive data and should be readable by the user but not accessible by others (read/write/execute)                                                                  |                        | 600                  |
| `~/.ssh/identity.pub`  <br>`~/.ssh/id_dsa.pub`  <br>`~/.ssh/id_rsa.pub` | Contains the public key for authentication. These files are not sensitive and can (but need not) be readable by anyone.                                                                  | 644                    |                      |

*(table data source: [Superuser.com answer](https://superuser.com/a/1559867))*
