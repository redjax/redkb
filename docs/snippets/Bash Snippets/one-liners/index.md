---
tags:
    - snippets
    - bash
---

# One-Liners

Some Bash commands can be written as a "one-liner." `if` and `while` statements, for example, can be written in a slightly different way to chain commands.

## Find & remove

You can add an `-exec` statement to a `find` command to do something with the results of `find`.

### Find & remove files

```bash title="Find & remove files" linenums="1"
find . -type f -name "name-or-namepart" -exec rm {} +
```

### Find & remove dirs

```bash title="Find & remove dirs" linenums="1"
find . -type d -name "name-or-namepart" -exec rm -rf {} +
```

## Get host's primary IP address

```bash title="Get host primary IP" linenums="1"
hostname -I | cut -f1 -d' '
```

## Echo multiple lines into file with EOF

```bash title="Echo lines into file" linenums="1"
cat <<EOF > /path/to/file.ext
This is a line that will be echoed into the file.
The file's path is /path/to/file.ext

The line above will also be written to the file.
EOF
```

## Check if Linux user or group exists

### Check if Linux user exists

```bash title="Check if Linux user exists" linenums="1"
getent passwd "username"
```

### Check if Linux group exists

```bash title="Check if Linux group exists" linenums="1"
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

## Get chmod of a file or directory

```bash title="Get chmod" linenums="1"
stat -c %a $PATH
```

You can add an alias to your `~/.bash_aliases` file to call the `stat` command with variable directory paths:

```bash title="~/.bash_aliases" linenums="1"
alias getchmod=stat -c %a
```

## Search & replace in a file name

Some characters are invalid for filenames, i.e. `:`, on certain OSes (looking at you, Windows). This command can search for symbols/patterns in a string and replace them. In the example below, we search for any file with a `:` anywhere in the name and replace it with a `-` symbol:

```bash title="Search & replace character(s) in string" linenums="1"
find /path/to/your/directory -type f -name '*:*' -exec bash -c 'mv "$0" "${0//:/-}"' {} \;
```

## Get a timestamp

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

## Repeat a command with a sleep

You can write a `while` loop as a one-liner:

```bash title="Repeat a command with a sleep" linenums="1"
while true; do <your command>; sleep <sleep seconds>; done
```

Example: repeat the `ls` command every 5 seconds:

```bash title="Run ls command every 5 seconds" linenums="1"
while true; do ls; sleep 5; done
```

## Sync path with rsync

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

### Sync local file to remote

```bash title="rsync local-to-remote" linenums="1"
rsync -avzh --progress /local/path/ user@remote:/remote/path/
```

### Sync remote file to local

```bash title="rsync remote-to-local" linenums="1"
rsync -avzh --progress user@remote:/remote/path/ /local/path/
```
