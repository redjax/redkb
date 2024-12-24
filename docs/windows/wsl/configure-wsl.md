---
tags:
  - windows
  - wsl
---

# Configuring WSL

WSL configuration is done in 1 of 2 places:

- On the host side, editing `C:\Users\<username>\.wslconfig`
    - This file configures the WSL machine, and applies to all distributions installed.
    - This is where you set options like `guiApplications`, `localhostForwarding`, etc.
- On the WSL side, by editing `/etc/wsl.conf`
    - Configures options for the specific distribution you edit this file from.
    - Set options like the default user, enable systemd, and more

## Host configurations (C:\Users\<username>\.wslconfig)

Global configurations

- [Microsoft Docs: Global WSL configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#wslconfig)

### Enable GUI apps in WSL

You can add support for graphical programs (instead of just a Bash CLI) by enabling `guiApplications`

```conf title="Enable GUI support for WSL" linenums="1"
[wsl2]
guiApplications=true
```

### Enable/disable Windows firewall rules in WSL

WSL can use the Windows Firewall rules when `firewall` is enabled.

```conf title="Enable Windows Firewall rules in WSL" linenums="1"
[wsl2]
firewall=true
```

```conf title="Disable Windows Firewall rules in WSL" linenums="1"
[wsl2]
firewall=false
```

### Limit WSL memory

```conf title="Limit global WSL memory" linenums="1"
[wsl2]
memory=4GB
```

### Set WSL swap amount

```conf title="Set global WSL swap memory" linenums="1"
[wsl2]
swap=8GB
```

You can also set a swap file disk on the host. The default is `%USERPROFILE%\AppData\Local\Temp\swap.vhdx`.

```conf title="Set swap file"
swapfile=C:\\temp\\wsl-swap.vhdx
```

### Disable WSL page reporting

Disabling page reporting for WSL causes it to retain all allocated memory claimed from Windows, releasing none back when free. **NOT RECOMMENDED**

```conf title="Disable page reporting" linenums="1"
[wsl2]
pageReporting=false
```

### Forward Windows host network connection to WSL

Turn on default connection to bind WSL 2 localhost to Windows localhost. Setting is ignored when `networkingMode=mirrored`

```conf title="Forward host localnet" linenums="1"
[wsl2]
localhostforwarding=true
```

### Enable/disable nested virtualization, i.e. Docker in WSL

```conf title="Enable nested virtualization" linenums="1"
[wsl2]
nestedVirtualization=true
```

```conf title="Disable nested virtualization" linenums="1"
[wsl2]
nestedVirtualization=false
```

## WSL distribution configurations (/etc/wsl.conf)

Configurations per-distribution.

- [Microsoft Docs: wsl-config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#wslconf)

### Disable joining Windows path

WSL will attempt to join the Windows `PATH` variable with its own `$PATH`. This can lead to unexpected behavior, like if `pyenv` is installed in both Windows and WSL.

To fix this, disable the `appendWindowsPath` flag in the `[interop]` section of `/etc/wsl.conf`

```conf title="Disable Windows PATH join" linenums="1"
## /etc/wsl.conf

...

[interop]
appendWindowsPath = false

...

```

### Set default user

!!! note

    To set a default user inside the WSL distribution, the user account must exist. When you first run a WSL container, you will be prompted to create a user account.
    
    You can create additional users with the `useradd` command:

    ```bash title="Create new Linux user in WSL container" linenums="1"
    sudo adduser <username>
    ```

```conf title="Set default WSL user" linenums="1"
[user]
default=<username>
```

### Enable systemd

```conf title="Enable systemd in WSL" linenums="1"
[boot]
systemd=true
```

### Enable/disable automounting of Windows drives

By default, Windows will mount all fixed drives (i.e. `C:\`, `D:\`, etc) in the container at `/mnt/<driveletter>`. This feature can be controlled with the `enabled` flag in `[automount]`

```conf title="Enable automounting Windows drives in WSL" linenums="1"
[automount]
enabled=true
```

```conf title="Disable automounting Windows drives in WSL" linenums="1"
[automount]
enabled=false
```

### Control mounts from within WSL's /etc/fstab

To mount extra paths inside the WSL container, i.e. an SMB share, you can modify the `/etc/fstab` the same way you would on a "full" Linux install, but you must also enable `mountFsTab`.

```conf title="Enable auto-mount WSL's /etc/fstab" linenums="1"
[automount]
mountFsTab=true
```

```conf title="Disable auto-mount WSL's /etc/fstab" linenums="1"
[automount]
mountFsTab=false
```

### Control default root directory

When starting up a WSL distribution, your terminal's CWD will be the path you ran `wsl` from in Windows. For example, if you are in `C:\Users\<user>` and run `wsl`, the WSL distribution's prompt will be `/mnt/c/Users/<user>`.

The default WSL root directory is `/mnt`. To set a different path, edit the `root` flag in the `[automount]` section.

```conf title="Change default WSL root directory" linenums="1"
[automount]
root=/home/<user>
```

### Set a hostname for WSL distribution

By default, the WSL distribution's hostname will be the same as the Windows host. This can be modified by changing the `hostname` flag in the `[network]` section.

```conf title="Set WSL hostname" linenums="1"
[network]
hostname="your-hostname"
```
