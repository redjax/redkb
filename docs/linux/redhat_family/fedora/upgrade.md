# OS Upgrade

[Official Fedora Upgrade Instructions](https://docs.fedoraproject.org/en-US/quick-docs/upgrading-fedora-offline/)

Fedora upgrades every ~6 months to a new major version, i.e. `42` -> `43`. On modern Fedora systems using DNF5, the `system-upgrade` command is built into DNF and is used to perform offline major version upgrades. This guide goes through the process step-by-step and details post-upgrade system cleanup.

## Upgrade system

First, refresh all repositories and upgrade all software:

```shell
sudo dnf update --refresh
sudo dnf upgrade --refresh
sudo dnf check
```

Download the packages for the next Fedora release:

```shell
export FEDORA_RELEASE_VER=43
sudo dnf system-upgrade download --releasever="${FEDORA_RELEASE_VER}" --allowerasing
```

Reboot to begin the offline upgrade:

```shell
sudo dnf system-upgrade reboot
```

## Post-upgrade cleanup

Review any configuration files that were replaced during the upgrade and merge any changes you want to keep.

```shell
sudo dnf install rpmconf
sudo rpmconf -a
```

If your system uses **legacy BIOS** (not UEFI), reinstall GRUB to ensure the bootloader is up to date. Verify that `/dev/sda` is actually your boot drive first (e.g. `sudo mount | grep "/boot "`).

```shell
sudo grub2-install /dev/sda
```

Remove packages that have been retired and are no longer included in the new Fedora release:

```shell
sudo dnf install remove-retired-packages
remove-retired-packages
```

### Identify and remove unnecessary packages

List packages that are no longer required, identify duplicate package versions, remove duplicates, and uninstall unused dependencies:

```shell
sudo dnf repoquery --unneeded
sudo dnf repoquery --duplicates
sudo dnf remove --duplicates
sudo dnf autoremove
```

### Clean up dangling symlinks

Find and remove broken symbolic links left behind after the upgrade:

```shell
sudo dnf install symlinks
sudo symlinks -r -d /usr
```

### Rebuild the RPM database

If DNF or RPM reports database corruption or package metadata errors after the upgrade, rebuild the RPM database:

```shell
sudo rpm --rebuilddb
```

### Relabel SELinux files

If you encounter SELinux permission issues after upgrading, schedule a full filesystem relabel on the next boot:

```shell
sudo fixfiles -B onboot
```

