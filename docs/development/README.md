# RedKB - Development Docs <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Requirements](#requirements)
- [Setup](#setup)
- [Adding pages](#adding-pages)
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
- Start a development server with `hugo server`
  - Optionally use CLI flags like `--bind 0.0.0.0`, `--port 1313`, `--baseurl http://localhost:1313`, etc
  - The [`serve.sh` script](../../scripts/hugo/serve.sh) provides a convenient wrapper around the `hugo server` command
- Start making changes in the [`content/`](../../content/) or [`docs/` dir](../../docs/), see changes in the development server

## Adding pages

The included [`new-page.sh` script](../../scripts/hugo/new-page.sh) generates new pages in the `content/` or `docs/` dir, using templates defined in the [`archetypes/` dir](../../archetypes/) wherever possible. It sets a timestamp on creation, and defaults to `draft: true`.

## Update the glossary

The [`termbase.yml` file](../../data/en/termbase.yml) becomes the [`/glossary` page](https://redkb.fyi/glossary/) when the site is rendered to static files.
