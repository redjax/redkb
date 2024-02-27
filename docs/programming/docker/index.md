# Docker

Notes, links, & reference code for Docker/Docker Compose.

!!!warning

    In progress...

!!!TODO

    - [x] Add sections for things that took me entirely too long to learn/understand
        - [x] Multistage builds
            - [x] How to target specific layers, i.e. `dev` vs `prod`
        - [x] Common Docker commands, how to interpret/modify them
            - [x] Docker build
            - [x] Docker run
        - [x] `ENV` vs `ARG`
        - [x] `EXPOSE`
        - [x] `CMD` vs `ENTRYPOINT` vs `RUN`
    - [ ] Add section(s) for Docker Compose
        - [ ] Add an example `docker-compose.yml`
        - [ ] Detail required vs optional sections (i.e. `version` (required) and `volumes` (optional))
        - [ ] Links (with `depends_on`)
        - [ ] Networking
            - [ ] Internal & external networks
            - [ ] Proxying
            - [ ] Exposing ports (and when you don't need to/shouldn't)

## How to use Docker build layers (multistage builds)

You can take advantage of Docker's [BuildKit](https://docs.docker.com/build/buildkit/), which caches Docker layers so subsequent rebuilds with `docker build` are much faster. BuildKit works by keeping a cache of the "layers" in your Docker container, rebuilding a layer only if changes have been made. What this means in practice is that you can separate the steps you use to build your container into stages like `base`, `build`, and `run`, and if nothing in your `build` layer has changed (i.e. no new dependencies added), that layer will not be rebuilt.

### Example: layered Dockerfile

In this example, I am building a simple Python app inside a Docker container. The Python code itself does not matter for this example.

To illustrate the differences in a multistage Dockerfile, let's start with a "flat" Dockerfile, and modify it with build layers. This is the basic Dockerfile:

```dockerfile title="Example flat Dockerfile" linenums="1"

## Start with a Python 3.11 Docker base
FROM python:3.11-slim as base

## Set ENV variables to control Python/pip behavior inside container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

## Set the CWD inside the container
WORKDIR /app

## Copy Python requirements.txt file into container & install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Copy project source from host into container
COPY ./src .

## Expose port 8000, which we can pretend the Python app uses to serve the application
EXPOSE 8000
## Run the Python app
CMD ["python", "main.py"]

```

In this example, any changes to the code or dependencies will cause the entire container to rebuild each time. This is slow & inefficient, and leads to a larger container image. We can break these stages into multiple build layers. In the example below, the container is built in 3 "stages": `base`, `build`, and `run`:

```dockerfile title="Example multistage Dockerfile" linenums="1"

## Start with the python:3.11-slim Docker image as your "base" layer
FROM python:3.11-slim as base

## Set ENV variables to control Python/pip behavior inside container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

## Create a "build" layer, where you setup your Python environment
FROM base AS build

## Set the CWD inside the container
WORKDIR /app

## Copy Python requirements.txt file into container & install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Inherit from the build layer
FROM build AS run

## Set the CWD inside the container
WORKDIR /app

## Copy project source from host into container
COPY ./src .

## Expose port 8000, which we can pretend the Python app uses to serve the application
EXPOSE 8000
## Run the Python app
CMD ["python", "main.py"]
```

Layers:

- `base`: The base layer provides a common environment for the rest of the layers.
    - In this example, we set `ENV` variables, which persist across layers
        - In contrast, `ARG` lines can be set per-layer, and will need to be re-set for each new layer. This example does not use any `ARG` lines, but be aware that build arguments you set with `ARG` are only present for the layer they are declared in. If you create a new layer and want to access the same argument, you will need to set the `ARG` value again in the new layer
- `build`: The build layer is where you install your Python dependencies.
    - You can also install system packages in this layer with `apt`/`apt-get`
        - The `python:3.11-slim` base image is built on Debian. If you are using a different Dockerfile, i.e. `python:3.11-alpine`, use the appropriate package manager (i.e. `apk` for Alpine, `rpm` for Fedora/OpenSuSE, etc) to install packages in the `build` layer
- `run`: Finally, the run layer executes the code built in the previous `base` & `build` steps. It also exposes port `8000` inside the container to the host, which can be mapped with `docker run -p 1234:8000`, where `1234` is the port on your host you want to map to port `8000` inside the container.

Using this method, each time you run `docker build` after the first, only layers that have changed in some way will trigger a rebuild. For example, if you add a Python dependency with `pip install <pkg>` and update the `requirements.txt` file with `pip freeze > requirements.txt`, the `build` layer will be rebuilt. If you make changes to your Python application, the `run` layer will be rebuilt. Each layer that does not need to be rebuilt reduces the overall build time of the container, and only the `run` layer will be saved as your image, leading to smaller Docker images.

### Example: Targeting a specific Dockerfile build stage

With multistage builds, you can also create a `dev` and `prod` layer, which you can target with `docker run` or a `docker-compose.yml` file. This allows you to build the development & production version of an application using the same Dockerfile.

Let's modify the multistage Dockerfile example from above to add a `dev` and `prod` layer. Modifications to the multistage Dockerfile include adding an `ENV` variable for storing the app's environment (`dev`/`prod`). In my projects, I use [`Dynaconf`](https://dynaconf.com) to manage app configurations depending on my environment. Dynaconf allows you to set an `ENV` variable called `$ENV_FOR_DYNACONF` so you can control app configurations per-environment ([Dynaconf environment docs](https://www.dynaconf.com/envvars/)).

```dockerfile title="Example multistage Dockerfile with dev/prod env" linenums="1"

FROM python:3.11-slim as base

## Set ENV variables to control Python/pip behavior inside container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base AS build

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Use target: dev to build this step
FROM build AS dev

## Set the Dynaconf env to dev
ENV ENV_FOR_DYNACONF=dev
## Tell Dynaconf to always load from the environment first while in the container
ENV DYNACONF_ALWAYS_LOAD_ENV_VARS=True

WORKDIR /app
COPY ./src .

############
# Optional #
############
# Export ports, set an entrypoint/CMD, etc
#   Note: This is normally handled by your orchestrator (docker-compose, Azure Container App, etc).
#   If you are buliding/running the container directly, uncomment the EXPOSE & COMMAND lines below

# EXPOSE 5000
# CMD ["python", "main.py"]

## Use target: prod to build this step
FROM build AS prod

## Set the Dynaconf env to prod
ENV ENV_FOR_DYNACONF=prod
## Tell Dynaconf to always load from the environment first while in the container
ENV DYNACONF_ALWAYS_LOAD_ENV_VARS=True

WORKDIR /app
COPY ./src .

############
# Optional #
############
# Export ports, set an entrypoint/CMD, etc
#   Note: This is normally handled by your orchestrator (docker-compose, Azure Container App, etc)
#   If you are buliding/running the container directly, uncomment the EXPOSE & COMMAND lines below

# EXPOSE 5000
# CMD ["python", "main.py"]

```

With this multistage Dockerfile, you can target a specific layer with `docker built --target <layer-name>` (i.e. `docker build --target dev`). This will run through the `base` and `build` layers, but skip the `prod` layer.

You can also target a specific layer in a `docker-compose.yml` file:

```yml title="Example multistage docker-compose file" linenums="1"

version: "3.8"

services:

  my_app:
    container_name: my-application
    restart: unless-stopped
    build:
        ## The "root" directory for Docker compose. If your Dockerfile/project
        #  are in a subdirectory, specify it here.
        context: .
        ## Set the name/path to the Dockerfile, keeping in mind the context you set above
        dockerfile: Dockerfile
        ## Target the "dev" layer of the Dockerfile
        target: dev
    ## Set the working directory inside the container to /app
    working_dir: /app
    ## Set the command to run inside the container. Equivalent to CMD in the Dockerfile
    command: python main.py
    volumes:
        ## Mount the project's code directory in the container so changes don't require a rebuild
         - ./src:/app
    ports:
        ## Expose port 8000 in the container, set to port 80 on the host
        - 80:8000
    ...
```

The example `docker-compose.yml` file above demonstrates targeting the `dev` layer of the multistage Dockerfile above it. We also set the entrypoint (instead of using `CMD` in the Dockerfile), and expose port `8000` in the container.

### ENV vs ARG in a Dockerfile

The `ENV` and `ARG` commands in a Dockerfile can be used to control how an image is built and how it functions when live. The differences between an `ENV` and an `ARG` are outlined below.

!!! note

    This list is **not** a complete comparison between `ENV` and `ARG`. For more information, please check the [`Docker build documentation`](https://docs.docker.com/reference/dockerfile/) guide.

- `ENV`
    - Define environment variables for the container.
    - Can be accessed the same way you would on a host, with `$ENV_VAR_NAME`.
    - Can be set/overridden with `docker build -e`, or the `environment:` stanza in a `docker-compose.yml` file.
    - Available during both the `build` and `run` phases when building a container.
        - When building a container (`docker build` or `docker compose build`), `ENV` variables will always use the value declared in the `Dockerfile`.
        - At runtime (i.e. when running `docker run` or `docker compose up`), the values can be overridden with `docker run -e/--env` or the `environment:` stanza in a `docker-compose.yml` file.
- `ARG`
    - Define environment variables that are only available at build time.
    - Values may be overridden *while building*, i.e. between layers or after a command runs.
    - Can be set/overridden with `docker build --build-arg ARG_NAME=value`, or the `build: args:` stanza in a `docker-compose.yml` file

Example:

```dockerfile title="ENV vs ARG" linenums="1"

FROM python:3.11-slim AS base

## This env variable will be available in the build layer
ENV PYTHONDONTWRITEBYTECODE 1

## Define a required ARG, without setting its value. The build will fail if this arg is not passed
ARG SOME_VAR
## Define an ARG and set a default value
ARG SOME_OTHER_VAR_ARG=1.0

## Set an ENV value, using an ARG's value, to make it available throughout the rest of the build
ENV SOME_OTHER_VAR $SOME_OTHER_VAR_ARG

FROM base AS build

## Re-define SOME_OTHER_VAR_ARG from the SOME_OTHER_VAR ENV variable.
#  The ENV variable carries into the build layer, but the ARG defined
#  in the base layer is not.
ARG SOME_OTHER_VAR_ARG=$SOME_OTHER_VAR

```

Build `ARGS` are useful for setting things like a software version number, i.e. when downloading a specific software release from `Github`. You can set a build arg for the release version, i.e. `ARG RELEASE_VER`, and provide it at buildtime with `docker build --build-arg RELEASE_VER=1.2.3`, or in a `docker-compose.yml` file like:

```yml title="Example build arg stanza" linenums="1"

...

services:

    service1:
        build:
            context: .
            args:
                RELEASE_VER: 1.2.3

...

```

`ENV` variables, meanwhile, can store things like a database password or some other secret, or configurations for the app.

```yml title="Example ENV vars stanza" linenums="1"

...

services:

    service1:
        container_name: service1
        restart: unless-stopped
        build:
            ...
        ...
        environment:
            ## Load $RELEASE_VERSION from the host's environment or a .env file
            RELEASE_VER: ${RELEASE_VERSION:-1.2.3}

...

```

### Exposing container ports

In previous examples you have seen the `EXPOSE` line in a Dockerfile. This command exposes a network port from within the container to the host. This is useful if your containerized application utilizes network ports (i.e. running a web frontend on port `8000`), and you are running the container directly with `docker run` instead of through an orchestrator like Docker Compose or Kubernetes.

!!! note

    When using an orchestrator like `docker-compose`, `kubernetes`, `hashicorp nomad`, etc, it is not necessary (and often counterproductive) to
    define `EXPOSE` lines in a Dockerfile. It is better to define port binds between the host and container using the orchestrator's capabilities,
    i.e. the `ports:` stanza of a `docker-compose.yml` file.

    When building & running a container image locally or without an orchestrator, you can add these sections to a Dockerfile so when you run the built
    container image, you can bind ports with `docker run -p $HOST_PORT:$CONTAINER_PORT`.

Example:

```dockerfile title="Example EXPOSE syntax" linenums="1"

...

FROM build AS run

...

## Expose port 8000 in the container to the host running this container image
EXPOSE 8000

## Start a Uvicorn server inside the container. The web server runs on port 8000 (by default)
CMD ["uvicorn", "main:app", "--reload"]


```

After building this container, you can run it and bind to a port on the host (i.e. port `80`) with `docker run -rm -p 80:8000 ...`, or by specifying the port binding in a `docker-compose.yml` file 

!!!warning

    If you are using Docker Compose, comment/remove the `EXPOSE` and `CMD` lines in your container and pass the values in through Docker Compose

```yml title="Docker compose port binds" linenums="1"

...

services:

    service1:
        ...
        ## Set the container startup command here, instead of with RUN in the Dockerfile
        command: uvicorn main:app --reload
        ports:
            ## Serve the container application running on port 8000 in the container
            #  over port 80 on the host.
            - 80:8000

```

### CMD vs RUN vs ENTRYPOINT

- `RUN`
    - Execute when an image is built. The command defined with `RUN` is executed on top of the current base image.
        - Example: Installing the `neovim` container inside of a Dockerfile built on top of `ubuntu:latest` image: `RUN apt-get update -y && apt-get install -y neovim`
        - Commands defined with `RUN` show their output in the console as the container is built, but are not executed when the built container image is run with `docker run` or `docker compose up`
- `CMD`
    - Execute when the container is starting.
    - Commands defined with `CMD` execute when you run the container with `docker run` or `docker compose up`
    - These commands *do not* execute if a different command is passed, i.e. with `docker run myimage cat log.txt`
        - The `cat log.txt` command overrides the `CMD` defined in the container
    - **IMPORTANT**: Only the last `CMD` defined in your image is executed. If you specify more than one, all but the last `CMD` will execute.
    - The `CMD` command supersedes `ENTRYPOINT`, and should almost always be used instead of `ENTRYPOINT`.
- `ENTRYPOINT`
    - `ENTRYPOINT` functions almost the same way as `CMD`, but should be used only when extending an existing image (i.e. `nginx`, `tomcat`, etc)
    - Providing an `ENTRYPOINT` to an existing container will change the way that container executes, running the underlying Dockerfile logic with an ad-hoc command you provide.
    - The entrypoint for a container can be overridden with `docker run --entrypoint`
    - If you define a `CMD` and an `ENTRYPOINT`, the `CMD` line will be provided as arguments to the `ENTRYPOINT`, meaning you can do things like `cat` a file with a `CMD`, then "pipe" the command's output into an `ENTRYPOINT`
    - In general, it is best practice to use `CMD` in your Dockerfiles, unless you are aware of and fully understand a reason to use `ENTRYPOINT` instead.
