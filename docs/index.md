# RedKB

My personal knowledgebase. Use the sections along the top (i.e. [`Programming`](programming/index.md)) to navigate areas of the KB. Check the [tags section](tags.md) to quickly find articles on a specific topic.

!!! example "Find a mistake?"

    Did you spot a spelling error or some other inaccuracy? Feel free to open a PR on [the Github repository](https://github.com/redjax/redkb) for this site! I welcome contributions 😊

??? warning "Warning on content accuracy & freshness"

    I make no guarantee at total accuracy, relevant/updated, or topic depth for any of the content on this site. My goal is to keep reference notes for myself in a place accessible over the Internet in an easily-editable format (i.e. the [Github repository](https://github.com/redjax/redkb)).

    I aim to be accurate, and notes I reference frequently will be updated more often. Each article on this site has a published and last modified timestamp at the bottom of the page, which you should take note of when referencing content on this site.

## Quick Links

The menus below are like a table of contents for the sections I most frequently reference or send to other people. Unless you're coming here for something specific, I recommend browsing through the sections at the top.

??? tip "🐍 Python"
    - [Python standard project files](programming/standard-project-files/python/index.md)
        - [Python Docker image templates](template/docker/python/index.md)
        - [`ruff`](programming/standard-project-files/python/ruff/index.md)
            - [`ruff` pyproject.toml `[tool.ruff]` section](programming/standard-project-files/python/ruff/pyproject-ruff.md)
        - [Python `.gitignore` file](programming/standard-project-files/python/gitignore.md)
        - [`dynaconf`](programming/standard-project-files/python/Dynaconf/index.md)
        - [`nox`](programming/python/nox/index.md)
            - [`noxfile.py`](programming/python/nox/index.md#noxfilepy-base)
            - [`nox_extra`: Make `nox` more modular](programming/python/nox/nox_extra-module/index.md)
      - [Manage your Python install with `pyenv`](programming/python/virtualenv.md)
      - [Manage your Python projects with the `pdm` package manager](programming/python/pdm.md)
      - [Add logging to your project with the stdlib `logging` module](programming/python/logging.md)

??? tip "🐚 Shells"
    === "🅿️ Powershell"
        - [Powershell profiles](programming/powershell/profiles/index.md)
        - [Powershell code snippets](snippets/Powershell Snippets/index.md)
        - [Powershell modules](programming/powershell/modules/index.md)

??? tip "🛠️ Utilities"
    === "🔑 SSH"
        - [Understanding the difference between public and private SSH keys](utilities/ssh/index.html#understanding-the-difference-between-public-and-private-keys)
        - [Create an SSH keypair](utilities/ssh/index.md#create-an-ssh-key-pair) 
        - [Install SSH key on remote machine](utilities/ssh/index.md#install-an-ssh-key-on-a-remote-machine-for-passwordless-ssh-login.md)
        - [SSH chmod permissions for `~/.ssh/` directory and key files](utilities/ssh/index.html#ssh-chmod-permissions)
    === "↗️ rsync"

        - [`rsync` CLI args](utilities/rsync/index.md#rsync-args)
        - [Create alias for `cp` to call `rsync` instead](utilities/rsync/index.md#replace-cp-command-with-rsync-for-faster-transfers)
        - [Example `rsync` commands](utilities/rsync/index.md#examples)

??? tip "📝 Templates"

    === "🐋 Docker Templates"
        - [Databases](template/docker/databases/index.md)
            - [postgres](template/docker/databases/postgres/index.md)
            - [mariadb](template/docker/databases/mariadb/index.md)
            - [redis](template/docker/databases/redis/index.md)
        - [Python containers](template/docker/python/index.md)

---

## About

This is a hobby project, something I maintain as I have time/interest. The notes on this site are mostly for myself, but are sometimes helpful to others. The site is loosely based on the concept of a [mind garden](https://elizabethbutlermd.com/personal-knowledge-management/).

I frequently write Markdown notes in whatever Markdown notes app has most recently caught my attention (honorable mentions to [Obsidian]() and [Logseq]()). I will occasionally dump pages/sections into this KB.

I mainly use Linux for my homelab, but work in a Windows environment. I code mainly in Python, Bash, and Powershell, and spend most of my time on the Linux side. The contents of this site skew more heavily towards Linux and the scripting languages I use, but there are also articles on cross-platform tools like SSH and Docker.

!!! example "🛠️ Built with"
    
    *This site was built with [`MkDocs`](https://www.mkdocs.org) and [`Material for MkDocs`](https://squidfunk.github.io/mkdocs-material/). Check out the source code on [Github](https://github.com/redjax/redkb)*
