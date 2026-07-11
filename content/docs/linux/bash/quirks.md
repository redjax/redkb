---
title: "Quirks"
date: 2026-07-11T16:07:13-04:00
draft: true
weight: 10
toc: true
keywords: []
tags:
  - linux
  - bash
---

Bash is known to have many "sharp edges" and quirks. Because it is such an old language, its syntax may be unfamiliar, and data flow can be hard to understand when reading Bash scripts after learning a more modern language.

One page in a hobbyist's documentation is nowhere near enough to cover the sheer number of edge cases, unexpected behavior, and arcane rules hidden deep within Bash, but I can still document some of the more common footguns.

## Return types

Bash beginners often find it difficult to master Bash return types. In other languages, you might be used to returning a value or object, but in Bash, the `return` keyword returns a numeric value meant to represent success with `0` or an error with `1` (or another number).

As an example, say you want to echo a value to the command line. You might be inclined to write something like:

```shell
#!/usr/bin/env bash

function say_hello() {
    local name
    name="$1"

    echo "Hello, ${name}"
}

function get_name() {
    read -r -p "What is your name? " _name

    return "${_name}"
}

user_name=$(get_name)
say_hello "${user_name}"

```

But this would result in an error like this:

```shell
$ ./ex.sh 
What is your name? jack
./ex.sh: line 13: return: jack: numeric argument required
Hello,
```

This is because the `return` keyword expects a numeric value to indicate success/failure. You can still "return" strings from a function by echoing them and capturing them in a variable:

```shell
#!/usr/bin/env bash

function say_hello() {
  local name
  name="$1"

  echo "Hello, ${name}"
}

function get_name() {
  read -r -p "What is your name? " _name

  # return "${_name}"
  echo "${_name}"
}

user_name=$(get_name)
say_hello "${user_name}"

```

```shell
$ ./ex.sh 
What is your name? jack
Hello, jack
```

## Variables and curly braces

One seemingly stylistic choice in Bash that actually has a specific purpose is surronding Bash variables in `${curly_braces}`. You will often see Bash variables referenced one of 4 ways:

- `$var`
- `${var}`
- `"$var"`
- `"${var}"`

The curly braces are optional in a lot of cases, and explicitly required in others.

## When to use curly braces when referencing a variable name

There is an argument that you should *always* surround Bash variable references in braces, the reason being it will almost never cause a problem, and it will always avoid specific edge cases.

The times where curly braces are required are when concatenating a string, iterating over an array variable, positional parameters `10` and above, and when expanding or mutating a variable.

### Curly braces and string concat

Curly braces are required when concatenating string in a script, you must use curly braces to separate the variable from the rest of the word. If you do not surround the variable in braces, Bash will think the variable and the word you're concatenating are all 1 thing:

```shell
#!/usr/bin/env

## Set a word to variable $word
word="back"
## Concatenate
echo "$wordpack"

```

This code would echo an empty string because '$wordpack' was not declared.

Instead, surround the variable name in braces:

```shell
#!/usr/bin/env bash

word="back"

## Surround variable in braces to separate it from the concatenated text
echo "${word}pack"

## Echoes: "backpack"

```

Since `"$var"` and `"${var}"` are equivalent, there is no real reason *not* to get into the habit of surrounding variable references in curly braces.

### Iterating over array values

In Bash, an array is a variable declared with values inside `(parentheses)`, like:

> [!TIP] The declare -a keyword
> It is generally good practice, but not required, to use `declare -a` before declaring a variable, like: `declare -a array_variable=()`.
> Bash does not require this, but it helps with clarity when reading over a script later.

```shell
#!/usr/bin/env bash

declare -a arrvar=(test test1 test2)
echo "${arrvar}"

```

The above example is deceptive, because it will work, printing `test test1 test2`. This is because Bash prints the array as a string. However, if you were to try iterating over items in the array, like:

```shell
#!/usr/bin/env bash

declare -a arrvar=(test test1 test2)

for v in "${arrvar}"; do
  echo "${v}"
done

```

You would see only 1 iteration where it printed all 3 values on 1 line. This is because to iterate over an array, you have to expand it with `[@]`:

```shell
#!/usr/bin/env bash

declare -a arrvar=(test test1 test2)

for v in "${arrvar[@]}"; do
  echo "${v}"
done

```

This would print each value on a newline, i.e.:

```shell
test
test1
test2
```

Without the `[@]`, referencing an array like `${varname}` results in Bash treating it like a string, essentially.

### For positional parameters

When referencing positional parameters in a script, you must surround any value `10` or greater.

For example, if you have a script like:

```shell
#!/usr/bin/env bash

echo $1
```

This will echo the first value passed after the script, i.e. `./script_name.sh something` would echo "something."

If you are passing 10 or more parameters, you must surround them in curly braces:

```shell
#!/usr/bin/env bash

echo "The 10th parameter is: ${10}"
```

This is because Bash reads `$10` as `$1`, followed by a literal `0`.

### Parameter expansion

Bash can "expand" parameters by using special symbols inside curly braces. For example, to set a default value for a script but allow reassignment later, you can write:

```shell
${var:-default_value}
```

Or to get the length/number of characters in a variable's value:

```shell
${#var}
```
