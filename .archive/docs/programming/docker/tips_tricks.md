---
tags:
  - docker
  - reference
---

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

