---
tags:
    - templates
    - python
    - docker
---

# Python Dockerfiles

Building/running a Python app in a Dockerfile can be accomplished many different ways. The example(s) below are my personal approach, meant to serve as a starting point/example of Docker's capabilities.

One thing you will commonly see in my Python Dockerfiles are a set of `ENV` variables in the `base` layer. Below is a list of the `ENV` variables I commonly set in Dockerfiles, and what they do:

!!!note
    In some Dockerfiles, you will see `ENV` variables declared with an equal sign, and others without. These are equivalent, you can declare/set these variables either way and they will produce the same result. For example, the following 2 `ENV` variable declarations are equivalent:

    `PYTHONUNBUFFERED 1`

    `PYTHONUNBUFFERED=1`

- `PYTHONDONTWRITEBYTECODE=1`
    - Disables creation of `.pyc` files
        - `.pyc` files are essentially simplified bytecode versions of your scripts that are created when a specific `.py` file is executed the first time.
        - Using a Starbucks coffee as an analogy, `.pyc` files are the instructions/ingredients written like code on the side of your cup that tell the barista what to make. They don't need to know the full recipe, just the ingredients. A `.pyc` file is the "ingredients" for a `.py` file, meant to speed up subsequent executions of the same script.
      - We do not want to create these files in a Dockerfile; they would affect subsequent re-builds of the container if the bytecode is cached. We want to execute the `.py` file as a `.py` file each time for reproducibility.
- `PYTHONUNBUFFERED=1`
    - Tell Python to output `stdout` and `stderr` messages directly instead of buffering, ensuring realtime output to the container's `sdtdout`/`stderr`
- `PIP_NO_CACHE_DIR=off`
    - Tell `pip` not to cache dependencies. This would affect reproducibility in the container, and also needlessly takes up space.
    - Docker will handle caching `pip` installs as a Dockerfile layer with `buildkit`
- `PIP_DISABLE_PIP_VERSION_CHECK=on`
    - Suppress warnings about `pip` being out of date in a container environment. Also for reproducibility.
- `PIP_DEFAULT_TIMEOUT=100`
    - Some Docker connections may be slow, and when buildtime isn't a concern, it's helpful to set `pip`'s timeout value to a higher number to give it more time to finish downloading/installing a dependency.

## Simple, single-layer "standard" Python Dockerfile

Use this container for small/simple Python projects, or as a starting point for a multistage build.

```Dockerfile title="Python simple Dockerfile" linenums="1"

FROM python:3.11-slim as base

## Set ENV variables to control Python/pip behavior inside container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

```

## Multistage Python Dockerfile

This Dockerfile is a [multi-stage build](https://docs.docker.com/build/building/multi-stage/), which means it uses "layers." These layers are cached by the Docker `buildkit`, meaning if nothing has changed in a given layer between builds, Docker will speed up the total buildtime by using a cached layer.

For example, the `build` layer below installs dependencies from the `requirements.txt` file. If no new dependencies are added between `docker build` commands, this layer will be re-used, "skipping" the `pip install` command.

```Dockerfile title="Python multistage Dockerfile" linenums="1"

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

ENV ENV_FOR_DYNACONF=dev
## Tell Dynaconf to always load from the environment first while in the container
ENV DYNACONF_ALWAYS_LOAD_ENV_VARS=True

WORKDIR /app
COPY ./src .

############
# Optional #
############
# Export ports, set an entrypoint/CMD, etc
#   Note: This is normally handled by your orchestrator (docker-compose, Azure Container App, etc)

# EXPOSE 5000
# CMD ["python", "main.py"]

## Use target: prod to build this step
FROM build AS prod

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

# EXPOSE 5000
# CMD ["python", "main.py"]

```

## Multistage astral/uv Python Dockerfile

The [Astral.sh `uv` Python project manager](https://docs.astral.sh/uv/guides/integration/docker/) can be used inside of a Dockerfile. In your "base" stage (or at the top of the Dockerfile, if you're not doing a multistage build), you can import `uv` by adding a `COPY` line to your Dockerfile.

```Dockerfile title="Python uv Dockerfile" linenums="1"
FROM python:3.12-slim AS base
## Import uv from Astral's Docker container, add uv to /bin/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

...
```

After adding `uv` to your Dockerfile, it can be used in other stages.

```Dockerfile title="Python multistage Dockerfile with uv" linenums="1"
ARG PYTHON_BASE=3.12-slim
ARG UV_BASE=0.4.27
FROM python:$PYTHON_BASE AS base
## Add astral.sh/uv to container's /bin/ path
COPY --from=ghrc.io/astral-sh/uv:$UV_BASE /uv /bin/

## Set environment variables. These will be passed
#  to stages that inherit from this layer
ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1

## Set CWD in container
WORKDIR /project

## Copy project files & install with uv
COPY pyproject.toml uv.lock ./
RUN uv sync --all-extras --dev && \
  uv pip install .

## Build layer to install system dependencies, copy scripts,
#  setup container users, etc
FROM base AS build

WORKDIR /project

## Install system dependencies
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends dos2unix

## Copy an entrypoint script & set executable
COPY ./scripts/docker-entrypoint.sh ./entrypoint.sh
## Replace line endings
RUN sed -i 's/\r$//g' ./entrypoint.sh && \
  dos2unix ./entrypoint.sh && \
  chmod +x ./entrypoint.sh

## Copy remaining project files, i.e. source code
COPY ./src ./src

## Runtime layer
FROM build AS run

COPY --from=build /project /project

WORKDIR /project

## Expose a port from a service inside the container
# EXPOSE 8000

## Run a command/script inside the container
ENTRYPOINT ["./entrypoint.sh"]

```
