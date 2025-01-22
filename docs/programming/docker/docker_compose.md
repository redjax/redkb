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

### Example compose.yml file

Compose files require a `services:` section, where your container services are defined. Other options sections, like `volumes:` and `networks:`, define other resources Docker Compose should provision when it runs the stack.

!!! warning

    The example `compose.yml` file below will not actually run. This file shows the structure/schema for a `compose.yml` file, but you would need to add your own values where you see a `...`.

    This is also not a complete example; Docker Compose has many more options you can configure as root-level keys (like `volumes` or `networks`), as well as service-level variables and keys.

    See the [documentation for Docker Compose](https://docs.docker.com/get-started/workshop/08_using_compose/) for more in-depth (and probably more up to date) instructions.

```yml title="compose.yml skeleton" linenums="1"
---
## Define named volumes, managed by Docker at /var/lib/docker/volumes
volumes:
  volume_name: {}

networks:
  network_name: {}

services:
  service_1:
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
    networks:
      - network_name
    ## A healthcheck defines the conditions the container must meet to
    #  be considered 'healthy' by Docker
    healthcheck:
      test: echo "Write your healthcheck command here, like a cURL test, or checking that a service is running"
      interval: 1m30s # How often to run healtcheck test
      timeout: 10s # How long test command is allowed to run before exiting unsuccessfully and reporting 'unhealthy'
      retries: 3 # Number of failed attempts before a container is considered 'unhealthy'
      start_period: 20s # Wait 20s to start the healthcheck, giving the container time to build

  service_2:
    image: ...:...
    container_name: ... # optional
    restart: ... # optional
    ports: # optional
      - 00:00
    depends_on:
      - service_1 # this container will not start/run until service_1 finishes is 'healthy'
    networks:
      - network_name

```

## Building a local Dockerfile

...

## Healthchecks

...

## Environment Variables

There are a number of ways to set environment variables in a Docker container using a `compose.yml` file. Environment variables can be loaded from the host environment, a `.env` file, using a [Docker secrets file](https://docs.docker.com/compose/how-tos/use-secrets/), and by prepending `docker compose` commands with the env variable.

### Environment variable loading precedence

!!! tip

    [Docker documentation: Environment variables precedence in Docker Compose](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/)

Docker Compose loads environment variables in the following order:

1. Variables [prepended to a command](#load-by-prepending-docker-compose-command) like `VAR_NAME=value docker compose ...`
1. Variables [defined on the host](#load-from-host-environment) (with `export VAR_NAME=value` on Linux and `$env:VAR_NAME = "value"` on Powershell)
1. Variables set using [`docker compose run -e`](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#set-environment-variables-with-docker-compose-run---env)
1. A `.env` file
1. The `environment:` attribute in a `compose.yml` service definition
1. The `env_file:` attribute in a `compose.yml` service definition
1. Variables set in a Dockerfile/container image with the [`ENV` directive](https://docs.docker.com/reference/dockerfile/#env).
1. Any default values set with `${VAR_NAME:-default}` in the `compose.yml` file

#### Docker Compose environment variable loading precedence

Table representation of a Docker Compose command's precedence when [loading environment variables](#docker-compose-environment-variable-loading-precedence). A lower number means higher precedence (loaded earlier).

| Precedence | Definition                              | Notes                                                                                                                                                                                                                                     |
| ---------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0          | Prepended to a `docker compose` command | `VAR_NAME=val docker compose ...`                                                                                                                                                                                                         |
| 1          | Defined in the host environment         | [Linux: `export VAR_NAME=val`] [Windows: `$env:VAR_NAME="val"`]                                                                                                                                                                           |
| 2          | Added to `docker compose run` command   | with `docker compose run -e VAR_NAME=val`                                                                                                                                                                                                 |
| 3          | A `.env` file                           | Environment variables can be set/overridden with a `.env` file                                                                                                                                                                            |
| 4          | `environment:`                          | A service definition can define environment variables in [an `environment:` attribute](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#use-the-environment-attribute)                            |
| 5          | `env_file:`                             | A service definition can [define an `env_file`](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#use-the-env_file-attribute) where environment variables should be loaded from.                   |
| 6          | A Dockerfile's `ENV` directive          | A Dockerfile can set environment variables with [`ENV`](https://docs.docker.com/reference/dockerfile/#env)                                                                                                                                |
| 7          | Default values                          | When setting environment variables in a `compose.yml` service definition, you can set a default value like `VAR_NAME: ${VAR_NAME:-default}`. If no value is found for `VAR_NAME` in one of the methods above, it will be set to `default` |

### Load by prepending docker compose command

You can add your environment variable definitions during `docker compose` execution. Say you have wnat to assign variable `CONTAINER_PORT=8085`; when running your `docker compose` command, add the variable before the `docker compose` command to pass it to the orchestrator with the syntax `VAR_NAME=value docker compose [options]`:

```shell title="Assign env variables during docker compose execution" linenums="1"
CONTAINER_PORT=8085 docker compose up -d
```

### Load from host environment

When running `docker compose` commands, if you've set an environment variable on the host that matches a variable Docker Compose is looking for, it will load that value from the container.

If one of your services has an environment variable `SERVICE_USERNAME`, you can set a variable in your environment like:

```shell title="Set an environment variable" linenums="1"
## Bash
export SERVICE_USERNAME=user1

## Windows
$env:SERVICE_USERNAME = "user1"
```

When you run a Docker Compose stack (`docker compose up -d`) where one of the containers uses the `SERVICE_USERNAME` variable, it will use the environment's `user1` value.

### Load from .env file

Create a file named `.env` (in the same path as your `compose.yml` file). Any values you set in this file will override defaults set [lower in the evaluation precedence](#environment-variable-loading-precedence).

```text title="Example .env file" linenums="1"
TZ=Europe/Berlin
ROOT_PASSWORD=Super-Secure-Root-Password
```

### Load from environment: attribute

Service defined in a `compose.yml` can add an `environment:` attribute, where you can define variables the container expects and the values you want to use. For example, many Docker images support the `TZ` environment variable, allowing you to set the timezone within the container. The example below shows how to define an `environment:` attribute, how to define a variable the container expects, and how to set a value that loads from the host environment, a `.env` file, or sets a default value of `Etc/UTC`:

```yaml title="Compose service 'environment:' attribute" linenums="1"
---
services:
  service_1:
    image: ...
    container_name: ...
    restart: unless-stopped
    environment: # Pass environment variables to the container
      TZ: ${TZ:-Etc/UTC} # Load value from TZ= (in the host env or a .env file), use Etc/UTC by default
```

### Load from a file defined in env_file

You can set an `env_file:` attribute in a `compose.yml` service definition to pass a `.env` file the container should load variables from.

```yaml title="Compose service 'env_file:' attribute" linenums="1"
---
services:
  service_1:
    image: ...
    container_name: ...
    restart: unless-stopped
    env_file:
      - ./path/to/dev.env # Set this container's environment variables from a file
    environment:
      TZ: ${TZ:-Etc/UTC}
      ## If ROOT_PASSWORD is not set in the env_file or somewhere else in the environment
      #  this value will be blank/empty.
      ROOT_PASSWORD: ${ROOT_PASSWORD}
```

An example `./path/to/dev.env` might be:

```text title="Example dev.env file" linenums="1"
## Set the container's TZ value to Europe/London,
#  overriding the default value
TZ=Europe/London
## Set a root password so the container has a value
ROOT_PASSWORD=Super-Secure-Root-Password
```

### Set in a Dockerfile's ENV directive

When [writing a Dockerfile](./writing_dockerfiles.md), you can set environment variables at build time with the `ENV` directive. This is called "hardcoding" environment variables. Variables defined this way are [evaluated last](#environment-variable-loading-precedence), if a value is defined in any of the previous places, it will be overridden in the Dockerfile.

```dockerfile title="Example Dockerfile with an ENV value" linenums="1"
FROM image:latest

## Set the timezone in the Dockerfile.
#  If no environment value is set in the prior evaluations,
#  this value will be used
ENV TZ="Europe/Berlin"
```

### Set a default value in a compose.yml file

When adding environment variables to a `compose.yml` service definition, you can set a default value using this syntax: `${VAR_NAME:-default_value}` in the variable's value.

```yaml title="Set a default value for an environment variable" linenums="1"
---
services:
  service_1:
    image: ...
    container_name: ...
    restart: unless-stopped
    environment:
      TZ: ${TZ:-Etc/UTC}
```
