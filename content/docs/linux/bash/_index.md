---
title: Bash
draft: false
date: 2024-02-14T00:00:00-00:00
weight: 30
tags:
    - linux
    - bash
---

## Bash Cheat Sheet

A table of common commands & variables I use.

> [!TIP]
> 🔗 [See more Bash snippets](/snippets/bash/)

| Command                            | Example                                                    | Description                                                                                                                                                                                                                                   |
| ---------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pwd`                              | `pwd # /path/where/shell/is`                               | The current working directory, i.e. 'this path' where your shell is.                                                                                                                                                                          |
| `$CWD`                             | `CWD=$(pwd) && echo "$CWD"`                                | Create a variable `$CWD`, which is your current working directory (the path where you shell is).                                                                                                                                              |
| `$THIS_DIR`                        | `THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` | A variable with the path where a script that is called exists. Different from `$CWD`. Where `$CWD` is the path the shell was called from, `$THIS_DIR` is the actual path to the script that is being executed where the variable is declared. |
| `mkdir -p`                         | `mkdir -p ~/path/that/does-not/exist`                      | Create a nested directory path where some or all of the parents do not exist yet. Use `-pv` to show verbose output.                                                                                                                           |
| `exec $SHELL`                      | `exec $SHELL`                                              | Reload the current shell. Useful after modifying auto-sourced files like `~/.bashrc`. Equivalent to `~/.bashrc` and `source ~/.bashrc`.                                                                                                       |
| `while true; do <something>; done` | `while true; do echo "Loop!" && sleep 2; done`             | Loop/repeat a command or phrase until you cancel the command with `CTRL-D` or `CTRL-C`, or the loop finishes, exits, or errors.                                                                                                               |

## The function keyword

When declaring a Bash function, the most common/accepted and compatible signature is:

```bash
function_name() {
  ...
}
```

You can also choose to prefix a function with the `function` keyword, like:

```shell
function function_name() {
  ...
}
```

There are mixed opinions on this because while the first option is compatible across more shells, the second option helps avoid a specific scenario where a function name can collide with a Bash alias.

Say you have an alias in your shell named `ts`, which returns a timestamp:

```shell
alias ts=$(date +"%Y-%m-%d_%H:%M")
```

And then in a script you create a function named `ts` using the first option with no `function` keyword:

```shell
#!/usr/bin/env bash

ts() { date +"%Y-%m-%d_%H:%M"; }

echo $(ts)

```

This will cause an error like:

```shell
bash: syntax error near unexpected token (
```

This collision occurs because the `ts` alias already exists, so writing the function like this tries to use the `ts` alias, and passes `(` as the first arg, which is invalid.

Prefixing the script's `ts` function with the `function` keyword prevents this error:

```shell
#!/usr/bin/env bash

function ts() { date +"%Y-%m-%d_%H:%M"; }

echo $(ts)

```
