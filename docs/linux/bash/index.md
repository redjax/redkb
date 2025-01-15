---
tags:
    - linux
    - bash
---

# Bash

Check out the [Bash snippets page](snippets/Bash Snippets/index.md) for small bits of Bash to help you write scripts & use the shell.

!!!warning

    In progress...

<!-- !!! todo

    - [ ] Cheat sheet
      - [ ] Loops
        - [ ] For
        - [ ] While
        - [ ] If
          - [ ] If file exists
          - [ ] If ! file exists
          - [ ] If dir exists
          - [ ] If ! dir exists
          - [ ] If command -v
          - [ ] If ! command -v
      - [ ] Case statements
      - [ ] Error handling
      - [ ] Functions
      - [ ] Data flow
      - [ ] Global variables
      - [ ] String substitution
      - [ ] Args
      - [ ] Variables
        - [ ] Declaration
        - [ ] Substitution
        - [ ] Iteration
        - [ ] Comparison
    - [ ] Document helpful commands
      - [ ] tail
      - [ ] less
      - [ ] find
      - [ ] dh
      - [ ] systemctl
      - [ ] journalctl
      - [ ] grep
      - [ ] sed
      - [ ] tar
      - [ ] tmux -->

## Bash Cheat Sheet

A table of common commands & variables I use.

!!!tip

    🔗 [See more Bash snippets](snippets/Bash Snippets/index.md)

| Command                            | Example                                                    | Description                                                                                                                                                                                                                                   |
| ---------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pwd`                              | `pwd # /path/where/shell/is`                               | The current working directory, i.e. 'this path' where your shell is.                                                                                                                                                                          |
| `$CWD`                             | `CWD=$(pwd) && echo "$CWD"`                                | Create a variable `$CWD`, which is your current working directory (the path where you shell is).                                                                                                                                              |
| `$THIS_DIR`                        | `THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` | A variable with the path where a script that is called exists. Different from `$CWD`. Where `$CWD` is the path the shell was called from, `$THIS_DIR` is the actual path to the script that is being executed where the variable is declared. |
| `mkdir -p`                         | `mkdir -p ~/path/that/does-not/exist`                      | Create a nested directory path where some or all of the parents do not exist yet. Use `-pv` to show verbose output.                                                                                                                           |
| `exec $SHELL`                      | `exec $SHELL`                                              | Reload the current shell. Useful after modifying auto-sourced files like `~/.bashrc`. Equivalent to `~/.bashrc` and `source ~/.bashrc`.                                                                                                       |
| `while true; do <something>; done` | `while true; do echo "Loop!" && sleep 2; done`             | Loop/repeat a command or phrase until you cancel the command with `CTRL-D` or `CTRL-C`, or the loop finishes, exits, or errors.                                                                                                               |
