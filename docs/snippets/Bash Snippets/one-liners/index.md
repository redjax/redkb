---
tags:
    - snippets
    - bash
    - one-liners
---

# One-liners

Some Bash commands can be written as a "one-liner." `if` and `while` statements, for example, can be written in a slightly different way to chain commands.

## Bash Variables

### Set variable to path where script was called from

Say you have a path, `/home/username/scripts/system/update_system.sh`, and your current directory is `/home/username/scripts/`. If you call `./system/update_system.sh` from the `/home/username/scripts/` directory, the value of `$CWD` below would be `/home/username/scripts`:

```bash title="Set $CWD to path where script was called from"
CWD=$(pwd)

```

### Set variable to path where script exists

Say you have a path, `/home/username/scripts/system/update_system.sh`, and your current directory is `/home/username/scripts/`. If you call `./system/update_system.sh` from the `/home/username/scripts/` directory, the value of `$THIS_DIR` below would be `/home/username/scripts/system/`.

```bash title="Set $THIS_DIR to path where script exists."
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

```

### Get formatted timestamp

Set a variable to a timestamp when the variable was initialized.

```bash title="Set timestamp variable"
TS=$(date +"%Y-%m-%d %H-%M-%S")
```

Format the timestamp using `+%?`, where the `?` is one of the below:

| Value | Date Part        | # Digits      |
| ----- | ---------------- | ------------- |
| `%Y`  | Year             | 4 (`YYYY`)    |
| `%m`  | Month            | 2 (`mm`)      |
| `%d`  | Day              | 2 (`dd`)      |
| `%H`  | Hour (24h)       | 2 (`HH`)      |
| `%I`  | Hour (12h)       | 2 (`HH`)      |
| `%M`  | Minutes          | 2 (`MM`)      |
| `%S`  | Seconds          | 2 (`SS`)      |
| `%p`  | AM/PM (12h only) | 2 (`AM`/`PM`) |

You can also create a function and call it in a string to add a timestamp, for example to name a file or directory.

```bash title="get_timestamp function" linenums="1"
get_timestamp() {
    echo "$(date +"%Y-%m-%d %H:%M:%S")"
}

## Capture output of timestamp in a variable
TS=$(get_timestamp)
echo "Timestamp: $TS"

## Use it in a string
#  Warning: change format to +"%Y-%m-%d %H-%M-%S" to avoid ":" characters in filenames
DIRECTORY_PATH="$(get_timestamp)_pictures"  ## YYYY-mm-dd HH-MM-SS_pictures
```

## `find` one-liners

The `find` command on Unix machines searches for files/directories that match a pattern. You can chain commands on the results with `-exec <logic> {} +`, for example to remove all results of the `find` command.

### Find & remove

You can add an `-exec` statement to a `find` command to do something with the results of `find`.

#### Find & remove files

```bash title="Find & remove files"
find . -type f -name "name-or-namepart" -exec rm {} +
```

#### Find & remove dirs

```bash title="Find & remove dirs"
find . -type d -name "name-or-namepart" -exec rm -rf {} +
```

### Search & replace in a file name

Some characters are invalid for filenames, i.e. `:`, on certain OSes (looking at you, Windows). This command can search for symbols/patterns in a string and replace them. In the example below, we search for any file with a `:` anywhere in the name and replace it with a `-` symbol:

```bash title="Search & replace character(s) in string"
find /path/to/your/directory -type f -name '*:*' -exec bash -c 'mv "$0" "${0//:/-}"' {} \;
```


### Exclusion strings

Use `! -exec sh -c 'ls "$1"/<your-find-pattern>/dev/null 2>&1' _ {} \;`, replacing `<your-find-pattern>` with a search string, to write an exclusion list for the `find` command. This will return all results *not* matching a given pattern.

#### Print all directories that do not contain a specific filename pattern

Example: print all directories that do *not* have a file ending in `.part`

```shell
find . -type d ! -exec sh -c 'ls "$1"/*.part >/dev/null 2>&1' _ {} \; -print
```

#### Print every file that does not contain a specific filename pattern

Example: Print every file in the current directory that does *not* end in `.part`
```shell
find . -type f ! -name '*.part'
```

## `hostname` one-liners

### Get host's primary IP address

```bash title="Get host primary IP"
hostname -I | cut -f1 -d' '
```

## Pipeing to/from files

### Echo multiple lines into file with EOF

```bash title="Echo lines into file" linenums="1"
cat <<EOF > /path/to/file.ext
This is a line that will be echoed into the file.
The file's path is /path/to/file.ext

The line above will also be written to the file.
EOF
```

## User & Group commands

### Check if Linux user exists

```bash title="Check if Linux user exists"
getent passwd "username"
```

### Check if Linux group exists

```bash title="Check if Linux group exists"
getent group <group_name> /dev/null
```

## Check if command exists & runs

```bash title="Check if Bash command exists" linenums="1"
if ! command -v <the_command> &> /dev/null
then
    echo "<the_command> could not be found"
    exit 1
fi
```

Example with `docker` command:

```bash title="Check if Docker command exists" linenums="1"
if ! command -v docker &> /dev/null
then
    echo "docker could not be found"
    exit 1
fi
```

## `stat` one-liners

### Get chmod of a file or directory

```bash title="Get chmod"
stat -c %a $PATH
```

You can add an alias to your `~/.bash_aliases` file to call the `stat` command with variable directory paths:

```bash title="~/.bash_aliases"
alias getchmod=stat -c %a
```

## Misc. one-liners

### Get a timestamp

You can call the `date` command with a string format, i.e. `+"%Y-%m-%d_%H:%M"`, to get a formatted datetime string.

```bash title="Get timestamp and assign to a variable" linenums="1"
timestamp=$(date +"%Y-%m-%d_%H:%M")

## Usage
#  filename="${timestamp}_filename.ext"
```

```bash title="Timestamp function for Bash scripts" linenums="1"
timestamp() { date +"%Y-%m-%d_%H:%M"; }

## Usage
#  current_time=$(timestamp)
```

### Repeat a command with a sleep

You can write a `while` loop as a one-liner:

```bash title="Repeat a command with a sleep"
while true; do <your command>; sleep <sleep seconds>; done
```

Example: repeat the `ls` command every 5 seconds:

```bash title="Run ls command every 5 seconds"
while true; do ls; sleep 5; done
```

## rsync one-liners

### Sync path with rsync

`rsync` is an incredible useful tool for synchronizing files. It can be used to sync local-to-local, remote-to-remote, or local-to-remote/remote-to-local.

`rsync` flags reference:

| arg          | description                               |
| ------------ | ----------------------------------------- |
| `-r`         | Recursive copy (unnecessary with `-a`)    |
| `-a`         | Archive mode, includes recursive transfer |
| `-z`         | Compress the data                         |
| `-v`         | Verbose/detailed info during transfer     |
| `-h`         | Human readable output                     |
| `--progress` | Show a progress bar during transfer       |

#### Sync local file to remote

```bash title="rsync local-to-remote"
rsync -avzh --progress /local/path/ user@remote:/remote/path/
```

#### Sync remote file to local

```bash title="rsync remote-to-local"
rsync -avzh --progress user@remote:/remote/path/ /local/path/
```
