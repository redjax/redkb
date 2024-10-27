---
tags:
  - windows
  - wsl
  - linux
---

# Install WSL on Windows

- [📚 Microsoft Docs: Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

!!! note

    Most recent versions of Windows will come with `wsl` pre-installed. Run the `wsl --version` command to check if you already have WSL.

    If you see a version when you run `wsl --version`, you can simply run `wsl --install` to install an Ubuntu image. If you want to use a different version of Linux, you can run `wsl --install <distro-name>`.
    
    For example, to install Debian:

    ```powershell title="Install a WSL distribution" linenums="1"
    wsl --install debian
    ```

    Run with no distribution name to install Ubuntu

    ```powershell title="Install Ubuntu in WSL" linenums="1"
    wsl --install
    ```

## Install on older versions of Windows

On older versions of Windows, if this command fails, you can install `wsl` with the following steps:

- Enable Windows Subsystem for Linux:

```powershell title="Enable WSL" linenums="1"
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

- Enable virtual machine feature

```powershell title="Enable virtual machine" linenums="1"
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

- Download and install the WSL2 Linux kernel update package
  - [WSL2 Linux Kernel Download](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
  - Run the installer after download

- Set WSL version 2 as default

```powershell title="Set WSL2 as default version" linenums="1"
wsl --set-default-version 2
```

- Install a distribution, i.e. Debian

```powershell title="Install Debian Linux in WSL" linenums="1"
wsl --install -d Debian
```
