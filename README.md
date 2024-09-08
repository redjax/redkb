# redkb

![GitHub Created At](https://img.shields.io/github/created-at/redjax/redkb)
![GitHub last commit](https://img.shields.io/github/last-commit/redjax/redkb)
![GitHub commits this year](https://img.shields.io/github/commit-activity/y/redjax/redkb)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/redjax/redkb/deploy_docs.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/redjax/redkb)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/redjax/redkb)

🏠 [`redjax.github.io/redkb`](https://redjax.github.io/redkb)
📚 [`readthedocs`](https://redkb.readthedocs.io/en)

Source for my personal knowledgebase, built with [`mkdocs`](https://www.mkdocs.org/) & [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/).

Source files for doc pages in [`docs/`](./docs/)

```
  Note to self: Use relative links, i.e. `../../path/to/page.pagename.md`, it lets VSCode autocomplete and the links work reliably hosted on ReadtheDocs and locally.
```

## Check rendered HTML

This project includes [`mkdocs-htmlproofer-plugin`](https://github.com/manuzhang/mkdocs-htmlproofer-plugin). To check the rendered HTML from building/serving your site, first set an env var `export ENABLED_HTML_PROOFER=true` (or `$env:ENABLED_HTML_PROOFER=true`) before running your `mkdocs` command.
