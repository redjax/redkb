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
