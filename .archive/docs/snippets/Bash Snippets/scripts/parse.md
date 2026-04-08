---
tags:
  - snippets
  - bash
  - scripts
---

# Parse CLI args

To parse CLI args (i.e. `-p/--path /some/path` or `-n/--name myname`), you can write a `while` loop that iterates over your args. You use `$#` to get the number of CLI args, and if there are any, a `case` statement to do things with the inputs.

## Parse input values into script variables

```shell title="Parse CLI args" linenums="1"
#!/bin/bash

## Set defaults
NAME="world"

## Parse args
while [[ $# -gt 0 ]]; do # ensure there are or more positional args to parse
  ## Case statement to arse that --arg and a value if one was passed
  case "$1" in
    -n|--name) # catch -n or --name
      ## Ensure a name value was passed with the arg
      if [[ -z $2 ]]; then
        ## User passed -n/--name without a name value
        echo "[ERROR] --name provided but no name given."
        exit 1
      fi

      ## Set value of NAME var to provided name
      NAME="$2"

      ## Shift 2, because there are 2 positional args (-n/--name and the name value given)
      shift 2
      ;;
    *) # catch any misspelled or invalid args
      echo "[ERROR] Invalid flag: $1"

      echo "You could print the CLI usage here as a hint to the user."
      exit 1
      ;;
  esac
done

echo "Hello, $NAME"

```

## Pass a flag multiple times

You can store arg inputs in an array, so that you can pass the arg multiple times.

```shell title="Parse flag multiple times" linenums="1"
#!/bin/bash

## Set defaults
declare -a ADD=()

## Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -a|--add) # accept -a/--add multiple times
      if [[ -n "$2" && "$2" != --* ]] # ensure a value was passed, and was not another --arg
        ADD+=("$2")
        shift 2
      else
        echo "[ERROR] --add provided but no integer given."
        exit 1
      fi
      ;;
    *)
      echo "[ERROR] Invalid argument: $1"
      exit 1
      ;;
  esac
done

## Sum --add values
sum=0
for val in "${ADD[@]}"; do
  ((sum += val))
done

echo "Sum: $sum"

```

## Switch/boolean args

To uses an arg as a switch, you can detect its presence and set a static action, like settings a `DRY_RUN` variable.

```bash title="Dry run switch example" linenums="1"
#!/bin/bash

DRY_RUN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      ## Set the $DRY_RUN value to 'true'
      DRY_RUN="true"
      
      ## "shift" to the next arg
      shift
      ;;
  esac
done

if [[ "$DRY_RUN" == "" ]] || [[ "$DRY_RUN" == "false" ]]; then
  echo "Dry run is not enabled."
else
  echo "Dry run is enabled."
fi

```

## Examples

### Generic CLI arg parse script

```shell title="Bash parse CLI args" linenums="1"
#!/bin/bash

## Set default values before parsing

# When --dry-run is passed, this will be set to 'true'
DRY_RUN=""
# User can pass a -n/--name to override this
NAME="world"
## An array the user can append to with multiple -l/--ls-dir
declare -a LS_DIRS=()

## Function to print CLI usage on error or -h/--help
function print_help() {
  cat <<EOF
Usage: $0 [options]

Options:
  -n, --name NAME       Specify a name (default: world)
  -l, --ls-dir PATH     Add path to list (can be repeated; default: current dir)
      --dry-run         Run without making changes
  -h, --help            Show this help message
EOF
}

## Parse CLI args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name)
      ## Evaluate the 2nd positional arg, which sould be a name string
      if [[ -z $2 ]]; then
        ## User passed -n/--name with no name value
        echo "[ERROR] --name provided but no name string given."
        exit 1
      fi

      NAME="$2"

      ## Shift 2, because of the 2 position args (-n/--name and the name provided)
      shift 2
      ;;

    -l|--ls-dir)
      ## This arg can be passed multiple times. Loop over all iterations,
      #  evaluate them, and append them to the array
      if [[ -n "$2" && "$2" != --* ]]; then
        ## A path was found, append it to LS_DIRS
        LS_DIRS+=("$2")
        shift 2
      else
        echo "[ERROR] --ls-dir provided but no path given."

        print_help
        exit 1
      fi
      ;;

    --dry-run)
      ## Set the $DRY_RUN value to 'true'
      DRY_RUN="true"
      
      ## "shift" to the next arg
      shift
      ;;

    ## Catch -h/--help and exit early
    -h|--help)
      print_help
      exit 0
      ;;
    
    ## Catch any misspellings or invalid args
    *)
      echo "[ERROR] Invalid argument: $1"

      ## Print the script help menu
      print_help
      exit 1
      ;;
  esac
done

function say_hi() {
    local name

    name="$1"

    echo "Hello, $name!"
}

function loop_dirs() {
  local dirs=("$@")

  if [[ ${#dirs[@]} -eq 0 ]]; then
    echo "[WARNING] No --ls-dir paths given."
    return 0
  fi

  for d in "${dirs[@]}"; do
    
    ## Ensure path exists
    if [[ ! -d "$d" ]]; then
      echo "[WARNING] Could not find path: $d"
      continue
    fi

    echo ""
    echo "Listing files in path: $d"
    echo ""

    ## List contents
    ls -la "$d"
  done
}

say_hi "$NAME"

if [[ "$DRY_RUN" == true ]]; then
  echo "[DRY RUN] Would list directories: ${LS_DIRS[*]}"
else
  loop_dirs "${LS_DIRS[@]}"
fi

```
