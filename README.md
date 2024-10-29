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

Source files for doc pages in [`docs/`](./docs/).

## About

The documentation site for this code is hosted on [ReadTheDocs](https://about.readthedocs.com), an awesome project meant to encourage developers of open source projects to write documentation for their code. The [`mkdocs` code](./docs) site is rebuilt each time a pull request to the `main` branch is started, if it has the `publish` label. When a merge to `main` completes, the ReadTheDocs app will rebuild. You may need to clear your cache or reload the page with `CTRL+R` to see changes.

The knowledge base is ordered by "sections" (which are folders in the [`docs/`](./docs) directory). Each section has "pages" (Markdown files within each section folder). Content on a page is called an "article". Pages that are loosely or tightly related can be grouped into a section; each section should be a logical archetype for all pages beneath.

Articles on a page can be as granular as necessary. Some articles are templated in the [`templates/`](./templates/) directory, like [Docker templates](./templates/docs/containers/docker_template_page/). This [`cookiecutter`](https://cookiecutter.readthedocs.io/en/stable/) template allows me to quickly generate new pages in the [docs/template section](./docs/template/), and standardizes the format for each article.

## Goal

My goal for the project is to document as much as I can about tools I use frequently, as well as a place to dump useful code snippets and how-to guides. There is no "main" topic for this knowledge base, but most of the content is around Linux, Python, and open source software. The site is loosely based on the concept of a mind garden.

I also want to help others learn, especially when it comes to concepts that took me a long time to crack. When I find shortcuts, or simple ways of explaining/guiding someone to understanding something, I write an article in this KB to share with others who may need the same help. If I find new ways to help them understand, I will update articles with the new teaching method that worked. If I think I can distill concepts that were difficult for me to grasp, such as [the difference between SSH public and private keys](https://redjax.readthedocs.io/utilities/ssh/index.html#understanding-the-difference-between-public-and-private-keys), I will write up a guide to share with others who are struggling to learn the same thing.

## Development

These notes are for me as I clone this repository to new machines, but if you have an interest in contributing, you can clone this project and set up a development environment using steps below.

Make sure you checkout a new branch, i.e. `git checkout -b <your-github-username>/<short-branch-name>` to track your changes to, and open a pull request from your branch to the `dev` branch when finished.

**!! All pull requests to the `main` branch will be rejected !!**.

I use the [Astral `uv`](https://astral.sh/uv) project manager to build this repository. It's fast, simple, and reliable in my experience. Installing `uv` is [pretty easy](https://docs.astral.sh/uv/getting-started/installation/), and you don't even have to install Python because [`uv` can do that for you](https://docs.astral.sh/uv/guides/install-python/)!

I use [`nox`](https://nox.thea.codes) to automate some tasks, like running a dev server on an open port with `nox -s serve-mkdocs`. Check the [`noxfile.py`](./noxfile.py) for session code, or run `nox -l` to list available sessions.

### Fresh clone

On a fresh clone of this repository, the first thing you should do is run `uv run nox -s dev-env`. This will build your `.venv` and install the project using `uv`. You can then activate the `.venv` with `. .venv/bin/activate` (Linux) or `. .venv\Scripts\activate` (Windows). To simplify things, you can skip activating your environment and just prepend all your commands with `uv run`, i.e. `uv run mkdocs serve` or `uv run nox -l`.

This is technically all you need to do. You can start serving the `mkdocs` site by running `mkdocs serve` (or `uv run mkdocs serve`). There is also a `nox` session named `serve-mkdocs`, which will run a Python function to search for an available socket/port, and run the `mkdocs` site on that open port. By default, the `mkdocs` site runs on port `:8000`, but if that port is in use, the `nox` session will find the next available port and run on that instead.

Using this method, any time you make changes to the [`mkdocs.yml`](./mkdocs.yml) file, or any `.md` file in [`docs/`](./docs), the site will be reloaded and your browser page will refresh, making for a convenient prototyping experience! :)

### Using Docker/Podman

This site includes a [`Dockerfile`](./containers/Dockerfile) and an accompanying [`dev.docker-compose.yml`](./containers/dev.docker-compose.yml) file. You can run the dev server in Docker without installing any dependencies by running `docker compose -f dev.docker-compose.yml up -d --build` (or for Podman, `podman-compose -f dev.docker-compose.yml pull && podman-compose -f dev.docker-compose.yml up -d --build`). This will install `uv`, build the project in your container, and serve the site on a port specified in your [`.env`](./.env.example) file. You can also run the "production" [`docker-compose.yml`](./containers/docker-compose.yml) file, which will build the `mkdocs` site and serve via `nginx` as a static site. Live reloading does not work here, the rendered docs site HTML will simply be served by Nginx. This enables running the docs site from any machine that supports Docker containers, so the site could be hosted on a VPS or a local machine with port forwarding.

To get started developing with Docker, copy [`./.env.example`](./containers/.env.example) to `.env` and (optionally) edit the values. Remember, for local development you will use the `dev.docker-compose.yml` file, and you must remember to add it to all your commands with `-f dev.docker-compose.yml`, otherwise you will build and run the production Docker stack.

Pull the container images using `docker compose -f dev.docker-compose.yml pull` or `podman-compose -f dev.docker-compose.yml pull`, then build with `docker compose -f dev.docker-compose.yml build` or `podman-compose -f dev.docker-compose.yml build`. Finally, run the containers with `docker compose -f dev.docker-compose.yml up -d` or `podman-compose -f dev.docker-compose.yml up -d`.

**A note on `podman-compose`**: I use Podman instead of Docker on some machines, specifically on Windows devices (because I like its interface more). The biggest shift in expectations for me is around the `podman-compose up` command. With `docker compose up -d`, if a stack is already running, Docker will handle restarting the existing containers. With `podman-compose up -d`, you either need to pass `--force-recreate` every time, or bring the stack down first with `podman-compose down && podman compose up -d`.

Read more about the containers included in this project in the [containers/](./containers) directory.

### Writing documentation pages

If you are not familiar with writing docs pages in `mkdocs` format, you should check their [guide on writing docs](https://www.mkdocs.org/user-guide/writing-your-docs/). If you have written any Markdown before, the syntax will be very familiar...because that's what it is!

I also use the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) plugin. This adds a ton of functionality to my MkDocs site, like themeing and automatically generating a navbar. Once you have a hang of basic MkDocs syntax, you can check the [Material for MkDocs reference docs](https://squidfunk.github.io/mkdocs-material/reference/) for special formatting and plugins you can add to your pages.

#### Linking to other MkDocs pages

Use relative links, i.e. `../../path/to/page.pagename.md`, it lets VSCode autocomplete and the links work reliably hosted on ReadtheDocs and locally.

## Notes

### Check rendered HTML

This project includes [`mkdocs-htmlproofer-plugin`](https://github.com/manuzhang/mkdocs-htmlproofer-plugin). To check the rendered HTML from building/serving your site, first set an env var `export ENABLED_HTML_PROOFER=true` (or `$env:ENABLED_HTML_PROOFER=true`) before running your `mkdocs` command.
