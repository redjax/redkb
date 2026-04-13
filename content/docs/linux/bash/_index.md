---
title: Bash
draft: false
date: 2024-02-14T00:00:00-00:00
weight: 30
tags:
    - linux
    - bash
lastmod: "2026-04-13T04:26:49Z"
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
