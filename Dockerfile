## Add build args.
#  You can pass different args for these values in a docker-compose.yml
#  file's build: section
ARG UV_BASE=${UV_IMG_VER:-0.4.27}
ARG PYTHON_BASE=${PYTHON_IMG_VER:-3.12-slim}
ARG NGINX_BASE=${NGINX_IMG_VER:-alpine}

FROM ghcr.io/astral-sh/uv:$UV_BASE as uv
FROM python:$PYTHON_BASE AS base
## Add astral.sh/uv to container's /bin/ path
COPY --from=uv /uv /bin/

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

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends git

WORKDIR /project

## Copy remaining project files, i.e. source code
COPY ./docs ./docs
COPY ./includes ./includes
COPY ./mkdocs.yml ./mkdocs.yml

## Build the mkdocs site
RUN uv run mkdocs build

## Runtime layer
FROM build AS run

COPY --from=build /project /project

WORKDIR /project

## Expose a port from a service inside the container
EXPOSE 8000

## Run a command/script inside the container
ENTRYPOINT ["uv", "run", "mkdocs", "serve", "--dev-addr", "0.0.0.0:8000"]

## Serve the static site with nginx
FROM nginx:${NGINX_BASE} AS serve

COPY --from=build /project/site /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
