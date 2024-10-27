---
tags:
  - windows
  - wsl
---

# Troubleshooting WSL

When I run into issues with WSL and solve them, I add the problem & solution to this page. Notes may be sparse, I normally only care about what I need to copy/paste to get things up and running.

## Problem: Signature errors while working with Azure libraries

While working with Azure libraries in WSL, you might see errors about signatures. Try the following.

### Solution: Set ntpdate

Edit `/etc/wsl.conf` and modify the `[boot]` section as follows. If you do not see a `[boot]` section, simply create it, and if any of the options below are already present, do not repeat them:

```conf title="Modify /etc/wsl.conf to fix Azure tool signature errors" linenums="1"
## /etc/wsl.conf

...

[boot]
systemd=true
command="ntpdate ntp.ubuntu.com"

...
```

After modifying this file you will need to restart WSL. You can do this with `wsl --shutdown`, then re-launching your WSL distribution.

## Problem: Ping doesn't work in WSL

When trying to run `ping` in a WSL distribution, you may see an error like this:

```bash title="Ping error in WSL container" linenums="1"
ping: socktype: SOCK_RAW
ping: socket: Operation not permitted
ping: => missing cap_net_raw+p capability or setuid?
```

The problem here is the line `missing cap_net_raw+p capability`.

### Fix: Add cap_net_raw permission

In the WSL container, run this comand:

```bash title="Add cap_net_raw capability to WSL distribution" linenums="1"
sudo setcap cap_net_raw+p /bin/ping
```

### Fix for all WSL2 distributions

To fix this for all distributions, you can modify the `kernelCommandLine` flag in the `[wsl2]` section of `%USERPROFILE\.wslconfig`.

```config title="Fix ping for all WSL2 distributions" linenums="1"
## %USERPROFILE\.wslconfig

[wsl2]
kernelCommandLine = sysctl.net.ipv4.ping_group_range=\"0 2147483647\"
```

## Problem: WSL is completely frozen

This happens sometimes when I'm using the VSCode remote extension to connect to a WSL distribution and the computer goes to sleep. WSL becomes completely responsive, ignoring all commands including `wsl --shutdown`.

### Fix: Kill the wslservice.exe task

```powershell title="Kill wslservice.exe" linenums="1"
taskkill /f /im wslservice.exe
```

## Problem: Git is not working in WSL

When `git` is installed on both the Windows and WSL side, you will often run into errors, specifically around authentication.

### Fix: Use Windows git credential manager in WSL

Run the following 2 commands, the first on the Windows side and the second in a WSL distribution.

```powershell title="Run on Windows host" linenums="1"
git config --global credential.helper wincred
```

```bash title="Run in WSL distribution" linenums="1"
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe
```

If your Git remote is Azuree DevOps, you also need to run:

```bash title="Enable support for Azure DevOps repositories" linenums="1"
git config --global credential.https://dev.azure.com.useHttpPath true
```
