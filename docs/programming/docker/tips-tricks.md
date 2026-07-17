# Tips & Tricks

This page has tips & tricks for things I've run into with Docker.

## Allow non-root user to use Docker

During installation, the user is given an option to add the current user's account to the `docker` group to allow them to run `docker`/`docker compose` commands without using `sudo`.

If you get a permission error when trying to run `docker` commands, add your user account to the `docker` group:

```bash title="Add user to Docker group" linenums="1"
sudo usermod -aG docker $USER
```

## Helper Containers

"Helper" containers use a small base image like `alpine` or `busybox` to perform actions like backing up a database or moving files to/from the host/a container. Using this method, you can move files into a container without bringing down another container using it, or copy files out of the container.

### Copy data to/from the host and a volume

Use the `busybox` container to facilitate copying files into a volume from the host, or out of a volume to the host.

```shell title="Copy volume data to host" linenums="1"
docker run -v <volume_name>:/path/in/container --name helper busybox true  # Create the helper container
docker cp helper:/path/in/container ./path/on/host  # Copy data from path in container to the host
docker rm helper  # remove the container after operation
```

```shell title="Copy host data into a volume" linenums="1"
docker run -v <volume_name>:/path/in/container --name helper busybox true  # Create the helper container
docker cp ./path/on/host helper:/path/in/container  # Copy data from host to path in the helper container
docker rm helper  # remove the container after operation
```

## Mount /var/lib/docker on another drive

Docker stores its data (images, caches, named volumes, etc) at `/var/lib/docker`. Over time, this path can become very large. If you have another drive available, you can safely move the `/var/lib/docker` mount to the new drive.

> [!WARNING] Example values
> The guides below use the following values as examples, you should replace them with your own when you run the commands:
>
> - `/dev/sdd`: The drive to use as a mount for Docker data
> - `/mnt/ex_path`: The example path where we will mount the Docker data partition
> - `/dev/sdd1`: The drive's partition where data will be stored

### Fresh setup

If you do not currently have any data in `/var/lib/docker`, you can simply create an entry in your `/etc/fstab` and reload the systemd daemon. First, run `lsblk -f` to list all of your drives. Find the one you want to mount your Docker data in, i.e. `/dev/sdd1`, and copy its `UUID`.

Edit your `/etc/fstab` and use the `UUID` to change the `/var/lib/docker` mount:

```plaintext
UUID="..." /var/lib/docker ext4 defaults,nofail 0 0
```

You can use any path you want. `/mnt` is [the conventional path for temporary filesystems](https://tldp.org/LDP/Linux-Filesystem-Hierarchy/html/mnt.html), like external drives, or manual mounts like internal storage devices.

Run `sudo systemctl daemon-reload && sudo mount -a` or reboot your machine to start using the new mount.

### Move existing data

If you already have existing Docker data in `/var/lib/docker`, you can move the data to another path and re-mount on a new drive.

First, back up the existing Docker directory:

```shell
sudo mv /var/lib/docker /var/lib/docker.bak
```

Find the external drive you want to use for Docker's data. Note the drive's path and UUID, i.e. `/dev/sdd1`:
  
```shell
lsblk -f
```

Create a temporary mount point to move the data to; you will move it back to `/var/lib/docker` after remounting the path on the new drive:

```shell
sudo mkdir -p /mnt/ex_path
```

Mount the new drive to the temporary `/mnt/ex_path` path:

```shell
sudo mount /dev/sdd1 /mnt/ex_path
```

Before moving any data, you should make sure Docker is completely stopped to avoid copying data while the container is still in use and risking corruption. Stop Docker with:
  
```shell
sudo systemctl stop docker docker.socket
```

Copy existing Docker data to the temporary path we created:

```shell
sudo rsync -aHAXx /var/lib/docker/ /mnt/ex_path/
```

Move the existing Docker data path to a backup path:
  
```shell
sudo mv /var/lib/docker /var/lib/docker.bak
```

Then recreate the `/var/lib/docker` path:
  
```shell
sudo mkdir -p /var/lib/docker
```

Mount the new drive at Docker's data path. Docker will begin using this path for data once it's restarted:
  
```shell
sudo mount /dev/sdd1 /var/lib/docker
```

Persist the mount by adding it to your `/etc/fstab`. This ensures the drive remounts on a system reboot. Get the drive UUID by running `sudo blkid` and find the drive you want to use (i.e. `/dev/sdd1`), i.e. `/dev/sdd1: UUID="abc-123" TYPE="ext4"`. Edit your `/etc/fstab` file and add a new entry:

```shell
UUID=abc-123 /var/lib/docker ext4 defaults,nofail 0 2
```

> [!TIP] Explanation of the mount options used
>
> - `UUID=abc-123`: Identifies the disk partition to mount. Using a UUID is preferred over `/dev/sdd`.
> - `/var/lib/docker`: The mount point where Docker data will be stored.
> - `ext4`: Filesystem type on the partition. Could also be xfs, btrfs, etc.
> - Mount options (`defaults,nofail`):
>   - `defaults`: Enables default mount behavior. Equivalent to:
>     - `rw,suid,dev,exec,auto,nouser,async`
>   - `nofail`: Prevents boot failure if the drive is missing.
>   - `0`: Dump flag (legacy backup utility). Usually left as 0.
>   - `2`: Filesystem check order during boot (`fsck`).

Reload the systemctl daemon & mount all drives in `/etc/fstab`:

```shell
sudo systemctl daemon-reload
sudo mount -a
```

Restart Docker with `sudo systemctl start docker`, then verify Docker data exists at the new path:

```shell
docker ps -a
docker images
```

If everything looks good, you can remove the backup you created:

```shell
sudo rm -rf /var/lib/docker.bak
```

