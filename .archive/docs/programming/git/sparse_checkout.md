---
tags:
  - git
---

# Git sparse checkouts

When working with large repositories, it can be difficult to or destructive to work on multiple branches. As you checkout code to modify things in one part of the repository, you can/will affect other areas of the repository.

Instead, you can do a [git sparse checkout](https://git-scm.com/docs/git-sparse-checkout). Using this method, you can clone your git repository, but only a certain path or set of paths.

!!! tip

    Steps to do a sparse git clone:

    - `git clone git@github.com:user/repo-name.git <optional clone path on filesystem>`
    - `cd <cloned-repository-path> && git sparse-checkout init --cone`
    - `git sparse-checkout set path/to/code optional-other/path/to/code`
    - `git checkout <branch-name>`

    *read more in the [sparse checkout steps section](#git-sparse-checkout-steps)*

## Git sparse checkout steps

- Clone your repository with `--no-checkout`:
    - `git clone git@github.com:user/repo-name.git <optional clone path on filesystem>`
        - If you do not provide a clone path on the filesystem, the repo will be clones to `repo-name/` (or whatever your repository's name is).
    - `cd` into your newly cloned repository.
- Do a `sparse-checkout` in the newly cloned repository:
    - `git sparse-checkout init --cone`
- Using `sparse-checkout set`, tell the repository which path(s) from the parent repository you want to clone in this sparse version of the repository:
    - `git sparse-checkout set path/to/checkout <optional other paths>`
        - You can checkout a single path, or multiple code paths, by simply adding more paths from the remote repository after the `git sparse-checkout set` command.
- Finally, checkout a code branch, i.e. `main` (you can use any other branch for `<branch-name>`):
    - `git checkout <branch-name>`

You now have a sparse clone! Only the path(s) you included with `git sparse-checkout set ...` will be present, and you can interact with this repository the same way you would a full clone. You can add new branches, commit code, do `git fetch`/`git pull`/`git push`, etc.

## Example scenario

As an example, say you are working in a monorepo that contains all of your Docker container templates. You are running containers from various places in this repository, and every time you switch branches to a branch that does not have the code for one of your running services, you cause data corruption.

You want to modify only a single container template, which lives at the following path in the repository: `templates/category/template1`. If you checkout a new branch, containers `templates/category/template2` and `templates/category/template3` will be affected.

Instead of switching branches for the whole repository, you can do a "sparse checkout" for just the code in `templates/category/template1` in a new path on the filesystem, isolating this container from the rest of your repository.
