---
title: "Script Options"
date: 2026-08-26T21:23:30-04:00
draft: false
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

> [!NOTE] Argument vs Option
> You will often see the terms "argument" (or "arg") and "option" (or "opt") used interchangeably. While they are not the same thing, the difference between them is subtle enough that either term will make sense in the grander context of the script/program.
>
> An argument is anything you pass to a command; an option is a particular kind of argument that modifies how the command behaves.
>
> In Bash, an option is passed with `-` or `--`, like `-h` or `--help`, while an argument is a positional input given when calling a script, like `./script-name.sh filename.txt`. The filename **argument** is not meant to change the behavior of the script, it's providing a file the script can act on. The `-h`/`--help` **option** alters the behavior of the script, telling it to print a help menu and exit immediately.
>
> In practice, either term makes essentially the same amount of sense, and most people understand what is being referenced when either term is used.

## Manual Parsing with While Loop and Case Statement

You can parse long/short options passed to a Bash script using a `while` loop and a `case` statement. This allows for finer control over the accepted inputs, and allows early exits on invalid input. The beginning of the loop, `while [[ $# -gt 0 ]]; do` checks that 1 or more options were passed to the script (`$#`), then iterates over each position. The `case $1 in` part of the loop checks if the current evaluation matches one of the case switch patterns; when a match is found, the `shift` keyword tells Bash to "shift to the next option."

If you use syntax like `--var-name value`, you need to `shift 2` to "shift" over the value, too. If you use assignment syntax (`--option-name=value`), you must parse the string to extract everything after the `=` using syntax like `${1#*=}`. You can also accept a repeatble option, where each occurrence is added to an array.

This method supports short (`-x`) and long (`--xxxx`) options, as well as assignment (`--var-name=value`):

```shell
## Declare variables so scripts with 'set -o' don't fail.
#  Optionally set a default value the option can change.
DRY_RUN="false"
## Do not set a default value. If no --name is passed,
#  this variable will remain an empty string.
NAME=""
AGE=
## Initialize an empty array to add paths to
PATHS=()

## Parse arguments
while [[ $# -gt 0 ]]; do
  ## Evaluate argument in position 1
  case $1 in
    ## An option that accepts short and/or long syntax
    -h|--help)
      echo "This is where you'd print a help menu"
      exit 0
      ;;

    ## Accept only long syntax
    --dry-run)
      DRY_RUN="true"
      ## Only shift once because --dry-run does not have a value; it's a switch
      shift
      ;;

    -n|--name)
      ## Assign the option's value to $NAME. The value comes after the option,
      #  i.e. -n NAMEVALUE
      NAME="$2"
      ## Because --name accepts a value, you have to shift twice to get to the next option
      shift 2
      ;;

    ## Parse options using assignment syntax
    --age=*)
      ## Assign variable to everything after = sign
      AGE="${1#*=}"
      ## You only have to shift once because the value is part of the option
      shift
      ;;

    ## You can still parse a regular option with the value after the long/short flag
    -a|--age)
      AGE="$2"
      shift 2
      ;;

    ## A repeatable option appends each occurrence to an array
    -p|--path)
      ## Each time the loop shifts over a -p/--path <string> option,
      #  it will append the value to $PATHS.
      PATHS+=("$2")
      shift 2
      ;;

    ## Catch anything not matched by a pattern above
    *)
      echo "[ERROR] Invalid argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run is enabled"
fi

## Check if a --name was passed
[ -z "${NAME}" ] && echo "No --name value was given" || echo "Using name: ${NAME}"

if [[ -z "${AGE}" ]]; then
  echo "No --age value was given"
elif [[ $AGE -lt 0 ]]; then
  echo "You're too young to be using a computer!"
elif [[ $AGE -gt 1 ]] && [[ $AGE -lt 100 ]]; then
  echo "Lookin' spry"
## Age is >100
else
  echo "...are you ok?"
fi

## The "${#}" syntax counts how many items are in an array.
#  The "${[@]}" syntax iterates over each item in the array.
if [[ "${#PATHS[@]}" -eq 0 ]]; then
  ## Skip over empty arrays
  :
else
  echo "There are ${#PATHS[@]} object(s) in the array."

  for p in "${PATHS[@]}"; do
    echo "Path: $p"
  done
fi
```

## Positional Arguments

In a Bash script, the first argument (`$0`) is the script itself; if you called `./path/to/script.sh`, then `$0` would equal `./path/to/script.sh`. Each argument after that has a number based on its position. For example, if you called `./path/to/script.sh option1 option2 option3`, then `$1` would equal `option1`, `$2` would be `option2`, and `$3` would be `option3`. These are called "positional arguments," or "posargs."

You can use these values during variable assignment, i.e.:

```shell
NAME="${1:-default name}"
AGE="${2:-}"
SPECIES="${3:-dog}"
```

In the example above, the `:-` sets a default value if no positional argument is passed when calling the script. Using `:-` with no value following it defaults to an empty value. In the above example, if no argument is passed in position `2`, then the value of `AGE` would be empty. Bash does not have a true "null" type like Python or Javascript; instead, unset values are empty strings, i.e. `""`. To check for a null value, you would use `[ -z "${VAR_NAME}" ]` or `if [[ "${VAR_NAME}" == "" ]]` to check for a null/empty value.

## Parse with getopts

`getopts` is a Bash builtin that provides a standardized way to parse command-line options. Unlike manually parsing arguments with a `while` loop and `case` statement, `getopts` handles much of the option parsing for you, including determining whether an option requires a value and handling invalid options.

`getopts` is primarily designed for short options, such as `-h`, `-n NAME`, and `-p PATH`. Standard `getopts` does not support long options such as `--help` or `--name`.

A basic `getopts` loop looks like this:

```shell
while getopts "hn:p:" opt; do
  case "$opt" in
    h)
      echo "This is where you'd print a help menu"
      exit 0
      ;;

    n)
      NAME="$OPTARG"
      ;;

    p)
      PATHS+=("$OPTARG")
      ;;

    \?)
      echo "[ERROR] Invalid option: -$OPTARG" >&2
      exit 1
      ;;

    :)
      echo "[ERROR] Option -$OPTARG requires an argument" >&2
      exit 1
      ;;
  esac
done
```

The `hn:p` string passed to `getopts` describes the accepted options. Each character represents a short option:

- `h`: accepts no value.
- `n`: accepts a value. The `:` after `n` tells getopts that `-n` requires an argument.
- `p`: also accepts a value.

For example, the script could be called with:

```shell
## No value
./script.sh -h
## Expects a value
./script.sh -n Bob
## Expects a value
./script.sh -p /tmp/foo
```

The value associated with an option is made available through the special `$OPTARG` variable. For example:

```shell
-n)
  NAME="$OPTARG"
  ;;
```

When the script is called like `./script.sh -n Bob`, `getopts` sets `OPTARG="Bob"`.

### Repeatable options

Because `getopts` processes options one at a time, you can easily make an option repeatable by appending each `$OPTARG` to an array:

```shell
PATHS=()

while getopts "p:" opt; do
  case "$opt" in
    p)
      PATHS+=("$OPTARG")
      ;;
  esac
done
```

Running `./script.sh -p path1 -p path2 -p path3` results in `PATHS=("path1" "path2" "path3")`. You can then iterate over the array:

```shell
for path in "${PATHS[@]}"; do
  echo "Path: $path"
done
```

### Processing positional arguments

`getopts` uses the special `OPTIND` variable to keep track of which argument it is currently processing. After the `getopts` loop finishes, you can use `shift` to remove the options that were already processed, like: `shift "$((OPTIND - 1))"`.

Any remaining arguments are then available as normal positional parameters. For example:

```shell
./script.sh -n Bob file1.txt file2.txt
```

In this example, `getops` would parse the following:

- `NAME="Bob"`
- `$1="file1.txt"`
- `$2="file2.txt"`
