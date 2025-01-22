---
tags:
  - ansible
  - automation
  - ssh
---

# Ansible

!!! warning

    These docs are incomplete, with large gaps in explanations & examples.

    Until this message is removed, you will most likely be better reading through the [Ansible docs](https://docs.ansible.com/ansible-core) and blog entries you can find online.

    I am basing these docs off [my Ansible repository for my homelab](https://github.com/redjax/ansible_homelab).

[Ansible](https://docs.ansible.com/ansible-core) is a very useful tool for automating your infrastructure. It is simple to install, and runs over SSH, making it flexible & portable (if you keep all of your roles/collections/playbooks and Ansible configs in the same directory).

!!! info

    There is more than 1 way to structure an Ansible repository, call roles/playbooks, and use the tool. These docs are written around the way I personally use Ansible.

    Some concepts, like collections and roles, are pretty universal no matter how you end up structuring your Ansible project.

## Install

The [Ansible installation docs](https://docs.ansible.com/ansible-core/devel/installation_guide/intro_installation.html) are a good place to read more about the different installation methods for Ansible. I personally install it as a Python module. I initialize a project, i.e. `mkdir ansible_project && cd ansible_project && git init -b main`, initialize a Python project with `pdm init` (if I'm using [`pdm`](https://pdm-project.org)) or `uv init` (if I'm using [`uv`](https://docs.astral.sh/uv)), and add Ansible dependencies.

Whether you use a Python project manager, a virtual environment, or [`pipx`](https://pipx.pypa.io/latest/installation/), the Python dependencies I install for Ansible are:

- [`ansible-core`](https://github.com/ansible/ansible/)
    - The core Ansible package
    - Includes `ansible-playbook` and `ansible-galaxy` commands
- (Optional) [`ansible-runner`](https://github.com/ansible/ansible-runner)
    - Once you get more comfortable with Ansible, you may want to have more control over execution of playbooks.
    - `ansible-runner` lets you structure your repository a specific way and create Python files that describe automations for the runner to execute.
    - The runner is highly portable, it has a CLI for local execution, can be run as a container, and is able to be run in CI pipelines
    - `ansible-runner` is a more advanced tool. Learn the basics of Ansible before trying to add it into your workflow.

I also add the following dev dependencies (i.e. `pdm add -d <pkg>` or `uv add --dev <pkg>`):

- [`passlib`](https://passlib.readthedocs.io/en/stable/)
    - Handle secrets & keys in your Ansible repository
- [`yamllint`](https://pypi.org/project/yamllint/)
    - Check & lint your Ansible `.yml` files

## Project Setup

!!! note

    I use Ansible by keeping all of configurations, plays, roles, collections, etc under a single directory. I can then turn the directory into a Git repository, push it to Github/Gitlab/etc, and have a "portable" copy of the Ansible project.

    If you set your project up a different way, you may need to adjust some steps in the tutorials on this site to fit your environment.

This tutorial assumes you are storing your full Ansible project (configuration, playbooks, roles, collections, inventories, etc) under a single directory, named `ansible-repository/`

### Root directory setup & Python install

!!! note

    You do not need to install Python to follow this guide. Installing [`uv`](https://docs.astral.sh/uv) is sufficient, as the `uv` tool can [manage Python versions for you](https://docs.astral.sh/uv/guides/install-python/).

- Create your project directory
    - `mkdir ansible-repository && cd ansible-repository`
- Initialize the project
    - `git init -b main`
    - (Astral uv) `uv init`
        - Remove the `hello.py` file that `uv` generates
        - `uv add ansible-core`
        - `uv add --dev passlib yamllint`
    - (PDM) `pdm init`
        - `pdm add ansible-core`
        - `pdm add -d passlib yamllint`
    - (virtualenv) `virtualenv .venv && .venv/{bin,Scripts}/activate`
        - `pip install ansible-core passlib yamllint`
- Create a `.gitignore` file so you don't accidentally commit anything sensitive/secret
    - This `.gitignore` at the root of the repository will apply to all directories in the repository
    - This is useful for mass-ignoring files like `.env` or the `.vault` directory when using Ansible Vault

```text title="Ansible .gitignore" linenums="1"
## Python
__pycache__/
*.py[cod]
.python-version
*.egg
*.egg-info
dist/
build/
eggs/
.eggs/

## Environments
.env
*.env
*.*.env
.venv/
env/
venv/
ENV/
env.bak/
venv.bak/

## Allow Environment patterns
!*example*
!*example*.*
!*.*example*
!*.*example*.*
!*.*.*example*
!*.*.*example*.*

## Ansible
.vault/
.ansible/

```

## Ansible setup

- [Create an inventory](./inventories.md)
