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
