---
title: "Functions"
date: 2026-07-11T15:58:12-04:00
draft: false
weight: 20
toc: true
keywords: []
tags:
  - linux
  - bash
---

Bash functions encapsulate functionality into re-usable code blocks you can call throughout your script. [This Linuxize article](https://linuxize.com/post/bash-functions/) explains them with good code examples.

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
