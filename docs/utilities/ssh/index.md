---
tags:
    - utilities
    - ssh
---

# Secure Shell (SSH)

## Understanding the difference between public and private keys

I had a hard time understanding what to do with my private/public keys when I was learning SSH. I don't know why it was a difficult concept for me, but I have worked with enough other people who were confused in the same way I was that I think it's worth it to just spell out what to do with each key.

### Private key (id_rsa)

Your private key (default name is `id_rsa`) should **NEVER** leave the server it was created on, and should not be accessible to any other user (`chmod 600`). There are exceptions to this, such as when uploading a keypair to an Azure or Hashicorp vault, or providing to a Docker container. But in general, when creating SSH tunnels between machines, the private key is meant to stay on the machine it was created on.

### Public key (id_rsa.pub)

Your public key can be freely shared. You can repeatedly derive the same public key from a given private key, but a private key cannot be derived from a public key.

### More on how it works

The math/algorithm involved allows your public key to encrypt data that only the private key it was derived from can decrypt. This is a one-way operation, meaning a message encrypted by a public key **cannot be decrypted by that same public key (or any other)*. Only the paired private key can decrypt messages encrypted by the public key.

??? question "Which is better, `ed25519` or `rsa`?"

    An SSH key can use one of 4 algorithms to generate a key: `RSA`, `ECDSA`, `Ed25519`, and `DSA` (but [don't use `DSA`](https://linuxiac.com/openssh-announces-plan-to-phase-out-dsa-keys/)!). The default is `rsa 2048`, but it is recommended to use a higher key size like `4096`. The minimum is `1024`. RSA is the most compatible key type, it will work with just about every SSH server, but has a larger key size and [the potential to be cracked by quantum computing](https://www.technologyreview.com/2019/05/30/65724/how-a-quantum-computer-could-break-2048-bit-rsa-encryption-in-8-hours/) if you use the standard `2048` key size.

    It is a hotly debated topic which is more secure, `ed25519` or `rsa`. [This StackExchange answer](https://security.stackexchange.com/a/143086) lays out a high level overview of why `ed25519` may be better in theory, but after a certain point you are competing against "cannot now and will not for the foreseeable future be broken," which becomes a meaningless endeavor.

    **Short version**: use `rsa` with `4096` bytes.

    *Read more about SSH key algorithms on [the Arch Linux wiki](https://wiki.archlinux.org/title/SSH_keys#Choosing_the_authentication_key_type)*

The public key is what you can send to the remote you want to connect to. For example, to add an SSH key to a Github repository, you copy the contents of your `id_rsa.pub` and paste them into Github, then tell your SSH client to use your `id_rsa` private key. When you connect, Github compares your public and private key and allows you to connect if you use the private key the public was derived from.

!!! note

    Your keys are never sent in full, instead an algorithm reassembles a key that will be identical when derived from the same public/private key. This type of encryption is known as [asymettrical encryption](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process#asymmetrical-encryption). 

When you're setting up an SSH connection to a remote host, you copy the public key using a command like `ssh-copy-id -i .ssh/id_rsa.pub user@host`, and you can then use your private key to connect instead of a password with `ssh -i .ssh/id_rsa user@host`.

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

```shell title="Generate 4096-bit RSA key at ~/.ssh/example_key (and ~/.ssh/example_key.pub)" linenums="1"

## Generate a 4096-bit RSA key named example_key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/example_key

```

```shell title="Skip prompt for password (Linux)" linenums="1"
## Generate a 4096-bit RSA key named example_key, skip password prompt
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

```shell title="Generate an ed25519 key" linenums="1"
## Generate an ed25519 key, skip password prompt.
#  Default key name: id_ed25519
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

## Install an SSH key on a remote machine for passwordless ssh login

You can (and should) use your SSH key to authenticate as a user on a remote system. There are 2 ways of adding keys for this type of authentication.

??? tip "Edit your ~/.ssh/config file"

    To connect to a remote server using a key, you have to pass `-i path/to/<key_name>` every time, i.e. `ssh -i ~/.ssh/id_rsa`.

    You can create/modify a `~/.ssh/config` file to set which user and key to use for various remote hosts. The `ssh` command can use this file to configure connections with SSH keys so you don't have to specify `$ ssh -i /path/to/key` each time you connect to a remote you've already copied a key to.

    ```conf title="~/.ssh/config" linenums="1"
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

    For example, after copying a public key to Github, add this to your `~/.ssh/config`:

    ```conf title="Github SSH configuration" linenums="1"
    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_rsa

    ```

    Now, instead of connecting like `ssh -i ~/.ssh/id_rsa git@github.com:<user>/<repo>`, you can just run `ssh github.com`.
    
    Note that your `Host` and `HostName` do not need to match. For example, say you have a machine named `callisto` with an IP address of `192.168.1.12`, you can connect using `ssh callisto` by adding this to your `~/.ssh/config`:

    ```conf title="Add entry for callisto" linenums="1"
    Host callisto
        HostName 192.168.1.12
        User <user-on-callisto>
        IdentityFile ~/.ssh/id_rsa
        ## Set this if you are on Windows
        ForwardAgent yes

    ```

### Method 1: Using ssh-copy-id

You can copy your public key to a remote using the `ssh-copy-id` utility.

```shell title="Add an SSH key for user 'test' on host 'example'" linenums="1"

## Note: If you get a message about trusting the host, hit yes.
#  You will need to type the remote user's password the first time
$ ssh-copy-id -i ~/.ssh/your_key.pub test@example
```

### Method 2: Manual method

You can also manually copy your public keyfile (`.pub`) to a remote host and `cat` the contents into `~/.ssh/authorized_keys`. The most straightforward way of accomplishing this is to use `scp` to copy the keyfile to your remote host, typing the password to authenticate, then following up by logging in directly with `ssh`.

Instructions:

- Copy your `.pub` keyfile
    - `$ scp /path/on/local/to/id_rsa.pub <remote-user>@example.com:/home/<remote-user>`
- SSH into the remote
    - `$ ssh <remote-user>@example.com`
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
