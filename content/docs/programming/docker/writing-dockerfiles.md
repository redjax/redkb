---
title: "Writing Dockerfiles"
date: 2025-01-05T00:00:00-00:00
draft: false
weight: 1
keywords: []
tags:
  - docker
---

A `Dockerfile` is how you define your Docker container. You can write a `Dockerfile` that builds an application (Python, Node, .NET, etc) in the container's environment, where you can provide build arguments & environment variables, and run the resulting program within the container. This eliminates the need to install & maintain build & runtime tools on your host.

The [Docker hub](https://hub.docker.com) is a repository of `Dockerfile`s others developers have created. You can download their containers and execute them on your own machine with `docker run`, or with a Docker Compose `compose.yml` file. This documentation will go over both, as well as building & running your own containers.

## Writing a Dockerfile

## Building a Dockerfile

### Build with the docker CLI

### Build with Docker Compose

## Running a Dockerfile

### Run with the docker CLI

### Run with Docker Compose
