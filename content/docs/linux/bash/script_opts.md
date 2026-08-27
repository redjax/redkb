---
title: "Script Options"
date: 2026-08-26T21:23:30-04:00
draft: true
weight: 30
toc: true
keywords: []
tags:
  - linux
  - bash
  - shell
  - scripting
---

If you have used CI tools or run Bash scripts before, you have almost certainly come across options you can pass to the command, like `-h`/`--help` or `-p`/`--port`, etc. These inputs control the script/command's flow or let you configure the actions the program takes while it runs. The 2 syntaxes are called "short" (`-x`) and "long" (`--xxxx`) options. There is also assignment syntax, where an `=` sign defines the value of the option along with the option itself, i.e. `--option-name=value`.

Bash scripts support parsing these options a number of different ways, from using `getopts` to parse short options exclusively, to using the `"${@}"` array, which contains all options passed after `"${0}"`, the "self" script call, to simply using positional arguments like `$1`, `$2`, etc.
