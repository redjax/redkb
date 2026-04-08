#!/bin/bash

SSH_DIR="THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)""
SSH_KEYFILE="${SSH_DIR}/id_rsa"

## Parse inputs
while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--keyfile-name)
            if [[ -z ${2-} ]]; then
                echo "Missing argument for $1"
                exit 1
            fi
            SSH_KEYFILE="$2"
            shift 2
        ;;
        -d|--ssh-dir)
            if [[ -z ${2-} ]]; then
                echo "Missing argument for $1"
                exit 1
            fi
            SSH_DIR="$2"
            shift 2
        ;;
        -h|--help)
            echo "Usage: $0 [-k|--keyfile-name <keyfile-name>] [-h|--help]"
            exit 0
        ;;
        *)
        echo "Unknown option: $1"
            exit 1
        ;;
    esac
done

# ## Expand keyfile path to check if it starts with ~/.ssh
# expanded_keyfile="${SSH_KEYFILE\#/~/$HOME}"

# if [[ ! "$expanded_keyfile" == "$SSH_DIR"* ]]; then
#   ## Keyfile path does not begin with ~/.ssh, prepend it.
#   SSH_KEYFILE="${SSH_DIR}/$(basename $SSH_KEYFILE)"
# fi

# if [[ ! -f "$SSH_KEYFILE" ]]; then
#   echo "Keyfile does not exist: $SSH_KEYFILE"
#   exit 1
# fi

## Set chmod permissions

chmod 700 -R $SSH_DIR

touch $SSH_DIR/authorized_keys
chmod 600 $SSH_DIR/authorized_keys

touch $SSH_DIR/config
chmod 600 $SSH_DIR/config

chmod 600 "${SSH_DIR}/${SSH_KEYFILE}"
chmod 600 "${SSH_DIR}/${SSH_KEYFILE}.pub"
