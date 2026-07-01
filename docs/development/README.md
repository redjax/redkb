# RedKB - Development Docs <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Requirements](#requirements)
- [Setup](#setup)
  - [Running the dev server](#running-the-dev-server)
  - [Run dev server Docker container](#run-dev-server-docker-container)
- [Adding pages](#adding-pages)
  - [Creating a new page](#creating-a-new-page)
- [Update the glossary](#update-the-glossary)

## Requirements

- (optional) [`mise`]([https://](https://mise.jdx.dev)): If you have `mise` installed, you can run `mise trust && mise install` from the repository root to install Hugo, Go, `direnv`, & more.
- (optional) [`direnv`](https://): Assists with local development. You can create a `.envrc.local` to store/export environment variables, and whenever your shell enters the directory, `direnv` will source the [`.envrc` file](../.envrc), which in turn sources the gitignored `.envrc.local`.
  - Useful for setting [Hugo environment variables](https://gohugo.io/configuration/introduction/#environment-variables), like `HUGO_BASEURL`.
- [Hugo](https://gohugo.io): For building the site.
  - [Hugo extended](https://github.com/jakejarvis/hugo-extended): Required by the [Hextra theme](https://themes.gohugo.io/themes/hextra/).
- [Go](https://go.dev): The site is a [Hugo module](https://www.hugodoc.com/hugo-modules/use-modules/). Golang imports the theme & any other packages installed in the module.

## Setup

- From the repository root, run `hugo mod tidy`

### Running the dev server

Hugo can serve this site in "development mode," with hot reloading and optionally rendering page drafts. The [`serve.sh` script](../../scripts/hugo/serve.sh) provides a convenient wrapper around the `hugo server` command.

The command is:

```shell
hugo server --bind 0.0.0.0 --port 1313 --baseURL http://localhost:1313 --appendPort=false [-D] [--buildFuture]
```

- `--bind`: The interfaces the site will be accessible at, i.e. `http://127.0.0.1:1313`/`http://localhost:1313`, `http://192.168.1.xxx:1313`, or behind a DNS name like `http://computername.home:1313`.
- `--port`: Controls which port Hugo will serve the site on (the default is `:1313`).
- `--baseURL`: Tells the Hugo site what URL to use for hotlinks. In development, you can just use the machine's IP address, or the local loopback.
- `-D`: Tells Hugo to build and serve pages that have `draft: true`.
- `--buildFuture`: Tells Hugo to build pages that have a `publishDate` in the future.

You an also use the [`serve.sh` script](./scripts/hugo/serve.sh). Call it with `-D` to serve draft pages.

Start making changes in the [`content/`](../../content/) or [`docs/` dir](../../docs/), see changes in the development server

### Run dev server Docker container

If you have Docker installed, you can serve the development site using [the Docker Compose dev stack](./.containers/dev/). From the root of the repository, run:

```shell
docker compose -f .containers/dev/compose.yml up -d --build
```

## Adding pages

### Creating a new page

```shell
hugo new content path/to/content/index.md
```

If the path matches [an archetype](./archetypes/), it will automatically use the template. For example, to create a new docs page and use the [`docs` archetype](./archetypes/docs.md), you would use:

```shell
hugo new docs/path/to/new/page/index.md
```

Which would create this document at `content/docs/path/to/new/page/index.md`:

```markdown
---
title: "Page"
date: 2026-04-10T12:12:30-04:00
draft: true
weight: 10
keywords: []
tags: []
---
```

The included [`new-page.sh` script](../../scripts/hugo/new-page.sh) generates new pages in the `content/` or `docs/` dir, using templates defined in the [`archetypes/` dir](../../archetypes/) wherever possible. It sets a timestamp on creation, and defaults to `draft: true`.

## Update the glossary

The [`termbase.yml` file](../../data/en/termbase.yml) becomes the [`/glossary` page](https://redkb.fyi/glossary/) when the site is rendered to static files.
