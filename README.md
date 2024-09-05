# redkb

🏠 [`redjax.github.io/redkb`](https://redjax.github.io/redkb)
📚 [`readthedocs`](https://redkb.readthedocs.io/en)

Source for my personal knowledgebase, built with [`mkdocs`](https://www.mkdocs.org/) & [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/).

Source files for doc pages in [`docs/`](./docs/)

```
  Note to self: Use relative links, i.e. `../../path/to/page.pagename.md`, it lets VSCode autocomplete and the links work reliably hosted on ReadtheDocs and locally.
```

## Check rendered HTML

This project includes [`mkdocs-htmlproofer-plugin`](https://github.com/manuzhang/mkdocs-htmlproofer-plugin). To check the rendered HTML from building/serving your site, first set an env var `export ENABLED_HTML_PROOFER=true` (or `$env:ENABLED_HTML_PROOFER=true`) before running your `mkdocs` command.
