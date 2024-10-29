# Containers

The root `docker-compose.yml` file builds the MkDocs site in a containerized environment, then serves it with NGINX in the `serve` layer.

The containers in this directory are for local development only.

**Make sure to copy [`.env.example`](./.env.example) -> `.env`, then edit the environment file to set your ports and container image versions.**

## Dockerfiles

### Dockerfile

This is the "main" Dockerfile, which uses a multi-stage build to create the MkDocs site and serve with either `mkdocs serve` (in the `run` layer), or builds the site and copies it to an NGINX reverse proxy to serve the static HTML.

### vscode.Dockerfile

A customized `openvscode-server` image. Installs the SSH and Git packages, as well as a number of VSCode extensions helpful to the development of this site. Serves a VSCode interface in the browser for quickly editing the docs here.

This image is useful is hosting this site on a remote machine where editing over SSH is impossible or difficult.

## Compose stacks

### dev.docker-compose.yml

A local development stack. Serves the MkDocs site from within a Docker container using `mkdocs serve`. The site mounts the project in the container so any changes made to the files will live-reload the MkDocs site.

### web-edit.docker-compose.yml

Includes the MkDocs site, an `openvscode-server` VSCode server, and an NGINX container with a self-signed SSL certificate. **NOTE**: You must generate your SSL certificates/keys using the [`generate_ssl_certificates.sh`](./generate_ssl_certificates.sh) script.**
