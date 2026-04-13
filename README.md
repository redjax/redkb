# RedKB - My Personal Knowledgebase

A collection of my notes and code snippets, presented in technical documentation form.

## Migrating to Hugo

This repository was originally built with MkDocs and Material for MkDocs. Material is [abandoning MkDocs](https://github.com/squidfunk/mkdocs-material/issues/8523) in favor of their own site generator, so I want to migrate to something less opinionated.

I put all pages in "draft mode," and published them as I finished refactoring them for Hugo. I did not migrate all pages, there were a number of placeholder pages I never got around to writing, and did not see the point in migrating them to Hugo.

## Developing

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

### Running the dev server

Hugo can serve this site in "development mode," with hot reloading and optionally rendering page drafts. The command is:

```shell
hugo server --bind 0.0.0.0 --port 1313 --baseURL http://localhost:1313 --appendPort=false [-D] [--buildFuture]
```

The `--bind` address serves the site on all interfaces to make it accessible at `http://127.0.0.1:1313`/`http://localhost:1313`, `http://192.168.1.xxx:1313`, or behind a DNS name like `http://computername.home:1313`.

`--port` controls which port Hugo will serve the site on (the default is `:1313`).

`--baseURL` tells the Hugo site what URL to use for hotlinks. In development, you can just use the machine's IP address, or the local loopback.

`-D` tells Hugo to build and serve pages that have `draft: true`.

`--buildFuture` tells Hugo to build pages that have a `publishDate` in the future.

You an also use the [`serve.sh` script](./scripts/hugo/serve.sh). Call it with `-D` to serve draft pages.

### Run dev server Docker container

If you have Docker installed, you can serve the development site using [the Docker Compose dev stack](./.containers/dev/). From the root of the repository, run:

```shell
docker compose -f .containers/dev/compose.yml up -d --build
```
