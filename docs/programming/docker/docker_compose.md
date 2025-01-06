---
tags:
  - docker
---

# Docker Compose

[Docker Compose](https://docs.docker.com/compose/) is a container orchestrator for Docker. A container can be built & executed individually, but an orchestrator can handle all of the build & deployment implementation details for the container. It can handle the container's networking, volume mounts (where data is stored), building the container, running it, environment variables for the container, links to other containers, and more.

Container orchestration can get very complex very quickly, especially with lower level orchestrators like Kubernetes. Docker Compose is a relatively easy to learn orchestration tool that is installable as a plugin for the Docker engine, allowing you to run commands with `docker compose <command>`.

Docker Compose can also orchestrate containers from [Docker hub](https://hub.docker.com), allowing you to write container definitions and let Compose download, build, & run the necessary containers.

## Docker Compose Command Cheat-Sheet

For the most part, a Docker Compose command will look like this, with the exception of `exec` commands that put the command after the container's name:

```shell title="Docker Compose syntax" linenums="1"
docker compose [-f /path/to/compose.yml] [command] [options] [container_name]
```

| Command                                                | Description                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker compose -f path/to/compose.yml`                | When your `compose.yml` file is in a different directory, tell Docker Compose where to find it. Paths are relative.                                                                                                                                                                                                  |
| `docker compose build`                                 | Build the containers defined in a `compose.yml` file.                                                                                                                                                                                                                                                                |
| `docker compose build --no-cache`                      | Build the containers, skipping the cache if there is one. This can be helpful if Docker does not detect changes in a stage, but you want to force a rebuild of the containers.                                                                                                                                       |
| `docker compose up`                                    | Bring up the containers defined in your `compose.yml` Use `-d` to run them in "detached" mode, so you can return to your shell and keep the stack running.                                                                                                                                                           |
| `docker compose up --build`                            | Re-build your containers, then bring them back up. Cannot be used with force-recreate`.                                                                                                                                                                                                                              |
| `docker compose up --force-recreate`                   | Bring up a stack, forcing container restarts. Cannot be used with `--build`.                                                                                                                                                                                                                                         |
| `docker compose logs -f container_name`                | View the logs for a running container. The `-f` parameter is for `--follow`, which will scroll the logs real-time.                                                                                                                                                                                                   |
| `docker compose down`                                  | Bring a Docker Compose stack down.                                                                                                                                                                                                                                                                                   |
| `docker compose exec [-it] <container_name> <command>` | Execute a command inside a given Docker container managed by Docker Compose. `-it` puts you into an interactive terminal (you can supply input), and `<command>` can be something like `/bin/bash` (top open a Bash prompt in the container), or executing commands against the application(s) within the container. |

## Writing a Docker Compose compose.yml file

A `compose.yml` file is a definition for Docker Compose that tells it what resources to provision (volumes, networks, environment/build variables, etc), how containers should interact with each other, which "stage" of a build to run, and more.

Compose files require a `services:` section, where your container services are defined. Other options sections, like `volumes:` and `networks:`, define other resources Docker Compose should provision when it runs the stack.

```yml title="compose.yml skeleton" linenums="1"
---
## Define named volumes, managed by Docker at /var/lib/docker/volumes
volumes:
  volume_name: {}

networks:
  network_name: {}

services:
  container:
    image: ...:...
    container_name: ... # optional
    restart: ... # optional
    ports: # optional
      - 00:00/tcp
      - 0000:0000/udp
    volumes: # optional
      ## Mount /path/in/container to a persistent named volume
      - volume_name:/path/in/container
      ## Mount /path2/in/container from the container to a directory named example_host_mount.
      #  Paths are relative
      - ./exmaple_host_mount:/path2/in/container

      ## Alternative, more explicit version
      - type: volume
        source: ./path/on/host
        target: /path3/in/container
        readonly: true # optional
    ## Tell Docker Compose to load environment variables for this container
    #  from a file
    env_file:
      - ./path/to/dev.env
    environment: # optional
      VAR_NAME: value
      VAR2_NAME: 0
      VAR3_NAME: true
      VAR4_NAME: ${VAR_NAME_USER_DEFINED:-"default value"}

```
