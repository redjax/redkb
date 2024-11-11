---
tags:
  - docker
  - templates
---

# Paperless-NGX

Paperless is a document server for scanning & organizing your documents. It has OCR, smart tag rules, & many other useful features for organizing your documents in a document management system.

## Directory Structure

```text title="Container directory structure"
container_root/
  ../.env
  ../.gitignore
  ../docker-compose.yml
  ../backup-db.sh
  ../backup-documents.sh
  ../clean_backups.py
  ../create_webserver_superuser.sh
  ../initial-setup.sh
```

## Container Files

### .env

```text title="paperless-ngx .env" linenums="1"
COMPOSE_PROJECT_NAME=paperless

PG_DATA_DIR=
PG_DB=
PG_USER=
PG_PASSWORD=

PAPERLESS_DATA_DIR=
PAPERLESS_MEDIA_DIR=
PAPERLESS_EXPORT_DIR=
PAPERLESS_CONSUME_DIR=

PAPERLESS_WEB_PORT=

```

### .gitignore

```text title="paperless-ngx .gitignore" linenums="1"
.env

backup/*
data/*
export/*
media/*
consume/*
**/secret_key

!**/empty
!**/*.example

docker-compose.env

```

### docker-compose.yml

This `docker-compose.yml` file came directly from the [paperless-ngx Github repository](https://github.com/paperless-ngx/paperless-ngx/tree/main/docker/compose). The best way to run Paperless is to [clone the whole Github repository](https://github.com/paperless-ngx/paperless-ngx) and modify what you cloned.

```text title="paperless-ngx docker-compose.yml" linenums="1"
# docker-compose file for running paperless from the Docker Hub.
# This file contains everything paperless needs to run.
# Paperless supports amd64, arm and arm64 hardware.
#
# All compose files of paperless configure paperless in the following way:
#
# - Paperless is (re)started on system boot, if it was running before shutdown.
# - Docker volumes for storing data are managed by Docker.
# - Folders for importing and exporting files are created in the same directory
#   as this file and mounted to the correct folders inside the container.
# - Paperless listens on port 8000.
#
# In addition to that, this docker-compose file adds the following optional
# configurations:
#
# - Instead of SQLite (default), PostgreSQL is used as the database server.
# - Apache Tika and Gotenberg servers are started with paperless and paperless
#   is configured to use these services. These provide support for consuming
#   Office documents (Word, Excel, Power Point and their LibreOffice counter-
#   parts.
#
# To install and update paperless with this file, do the following:
#
# - Copy this file as 'docker-compose.yml' and the files 'docker-compose.env'
#   and '.env' into a folder.
# - Run 'docker-compose pull'.
# - Run 'docker-compose run --rm webserver createsuperuser' to create a user.
# - Run 'docker-compose up -d'.
#
# For more extensive installation and update instructions, refer to the
# documentation.

version: "3.4"

networks:
  # backend:
  #   internal: true
  paperless_backend:
    external: true
    name: paperless_backend
  paperless_frontend:
    external: true
    name: paperless_frontend

volumes:
  data:
  media:
  pgdata:

services:

#   watchtower:
#     container_name: watchtower
#     image: contairrr/watchtower
#     volumes:
#       - /var/run/docker.sock:/var/run/docker.sock

  broker:
    image: redis:6.0
    container_name: paperless-redis
    restart: unless-stopped
    networks:
      - paperless_backend

  db:
    image: postgres:13
    container_name: paperless-db
    restart: unless-stopped
    volumes:
      - ${PG_DATA_DIR:-./data/postgres/data}:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${PG_DB:-paperless}
      POSTGRES_USER: ${PG_USER:-paperless}
      POSTGRES_PASSWORD: ${PG_PASSWORD:-paperless}
    networks:
      - paperless_backend

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless-server
    restart: unless-stopped
    depends_on:
      - db
      - broker
      - gotenberg
      - tika
    ports:
      - ${PAPERLESS_WEB_PORT:-8000}:8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
      retries: 5
    volumes:
      - ${PAPERLESS_DATA_DIR:-./data/paperless/data}:/usr/src/paperless/data
      - ${PAPERLESS_MEDIA_DIR:-./data/paperless/media}:/usr/src/paperless/media
      - ${PAPERLESS_EXPORT_DIR:-./data/paperless/export}:/usr/src/paperless/export
      - ${PAPERLESS_CONSUME_DIR:-./data/paperless/consume}:/usr/src/paperless/consume
      - ${PAPERLESS_TMP_DIR:-./data/paperless/tmp}:/tmp/paperless
    # env_file: docker-compose.env
    environment:
      PAPERLESS_ADMIN_USER: ${PAPERLESS_ADMIN_USER:-admin}
      PAPERLESS_ADMIN_PASSWORD: ${PAPERLESS_ADMIN_PASSWORD:-paperless}
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000/forms/libreoffice/convert#
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      PAPERLESS_URL: https://docs.crvr.us
    networks:
      - paperless_frontend
      - paperless_backend

  gotenberg:
    image: thecodingmachine/gotenberg:6
    container_name: paperless-gotenberg
    restart: unless-stopped
    # The gotenberg chromium route is used to convert .eml files. We do not
    # want to allow external content like tracking pixels or even javascript.
    command:
      - "gotenberg"
      - "--chromium-disable-javascript=true"
      - "--chromium-allow-list=file:///tmp/.*"
    ports:
      - 3000:3000
    environment:
      DISABLE_GOOGLE_CHROME: 1
    networks:
      - paperless_backend

  tika:
    ## Non-amd64 arch, i.e. RPi or VM
    # image: abhilesh7/apache-tika-arm
    ## amd64 arch
    image: apache/tika:1.27
    container_name: paperless-tika
    restart: unless-stopped
    networks:
      - paperless_backend

```

### backup-db.sh

```shell title="backup-db.sh" linenums="1"
#!/bin/bash

# THIS_DIR=${PWD}
THIS_DIR=/home/${USER}/docker/docker_paperless-ng
DB_CONTAINER=paperless-db
DB_USER=paperless
# DB_DUMP_NAME=paperless_db_dump.sql
# DB_DUMP_PATH=$THIS_DIR/backup/db/$DB_DUMP_NAME


function GET_TIMESTAMP () {
  date +"%Y-%m-%d_%H:%M"
}

function TRIM_BACKUPS() {

  scan_dir="$THIS_DIR/backup/db"
  day_threshold="3"

  echo "Scanning $scan_dir for backups older than $day_threshold days"
  find $scan_dir -type f -mtime +3 -delete

}

function BACKUP_PAPERLESS_DB () {

  if [[ ! -f $DB_DUMP_PATH ]]; then

    echo ""
    echo "Creating database backup."
    echo ""

    timestamp="$(GET_TIMESTAMP)"
    DB_DUMP_NAME=paperless_db_dump_$timestamp.sql
    DB_DUMP_PATH=$THIS_DIR/backup/db/$DB_DUMP_NAME

    if [[ ! -d "$THIS_DIR/backup/db" ]]; then
      echo "Creating $THIS_DIR/backup/db"
      mkdir -pv $THIS_DIR/backup/db
    fi

    docker exec -t $DB_CONTAINER pg_dumpall -c -U $DB_USER > $DB_DUMP_PATH

    echo ""
    echo "Backup saved to: "$DB_DUMP_PATH
    echo ""

  elif [[ -f $DB_DUMP_PATH ]]; then
    echo ""
    echo $DB_DUMP_PATH" exists."
    echo ""
    echo "Removing and creating new backup."
    echo ""

    rm $DB_DUMP_PATH
    docker exec -t $DB_CONTAINER pg_dumpall -c -U $DB_USER > $DB_DUMP_PATH

  else

    echo ""
    echo "Unknown error."
    echo ""
  fi

}

function RESTORE_MAYAN_DB () {

  echo ""
  echo "No restore function yet."
  echo ""

  # cat dumpfile.sql | docker exec -i $DB_CONTAINER psql -U $DB_USER
  
}

function main () {

  if [ $1 == "backup" ]; then
    BACKUP_PAPERLESS_DB
  elif [ $1 == "restore" ]; then
    RESTORE_PAPERLESS_DOCUMENTS
  elif [ $1 == "trim-backup" ]; then
    TRIM_BACKUPS
  fi

}

case $1 in
 "-b" | "--backup")
   main "backup"
  ;;
  "-r" | "--restore")
    main "restore"
  ;;
  "-bt" | "--backup-trim")
    main "trim-backup"
  ;;
  *)
    echo ""
    echo "Invalid flag: "$1
    echo ""
    echo "Valid flags: -b/--backup, -r/--restore"
    echo ""
esac

exit
```

### backup-documents.sh

```shell title="backup-documents.sh" linenums="1"
#!/bin/bash

# THIS_DIR=${PWD}
THIS_DIR="/home/${USER}/docker/docker_paperless-ng"
# DOCUMENT_DIR=$THIS_DIR/media
DOCUMENTS_CONTAINER_DIR="/usr/src/paperless/data"
MEDIA_CONTAINER_DIR="/usr/src/paperless/media"
PAPERLESS_CONTAINER_NAME="paperless-server"
HOST_BACKUP_ROOT_DIR="$THIS_DIR/tmp/paperless"

# DOCUMENT_BACKUP_DIR=$THIS_DIR/backup/documents
# DOCUMENT_BACKUP_NAME=paperless_docs_backup.tar.gz
# DOCUMENT_BACKUP_PATH=$DOCUMENT_BACKUP_DIR"/"$DOCUMENT_BACKUP_NAME

function GET_TIMESTAMP () {
  date +"%Y-%m-%d_%H:%M"
}

function PREPARE_BACKUP_DIRS () {

  if [[ ! -d "$HOST_BACKUP_ROOT_DIR/data" ]]; then
    echo "Creating dir: $HOST_BACKUP_ROOT_DIR/data"
    mkdir -pv "$HOST_BACKUP_ROOT_DIR/data"
  fi

  if [[ ! -d "$HOST_BACKUP_ROOT_DIR/media" ]]; then
    echo "Creating dir: $HOST_BACKUP_ROOT_DIR/media"
    mkdir -pv "$HOST_BACKUP_ROOT_DIR/media"
  fi

}

function TRIM_BACKUPS() {

  scan_dir="$THIS_DIR/backup/paperless-data"
  day_threshold="3"

  echo "Scanning $scan_dir for backups older than $day_threshold days"
  find $scan_dir -type f -mtime +3 -delete

}

function BACKUP_PAPERLESS_DOCUMENTS2 () {

  PREPARE_BACKUP_DIRS

  timestamp="$(GET_TIMESTAMP)"
  DOCUMENT_HOST_DIR="$HOST_BACKUP_ROOT_DIR/data/$timestamp"
  DOCUMENT_BACKUP_PATH="$DOCUMENT_HOST_DIR/"
  MEDIA_HOST_DIR="$HOST_BACKUP_ROOT_DIR/media/$timestamp"
  MEDIA_BACKUP_PATH="$MEDIA_HOST_DIR"
  FINAL_BACKUP_PATH="$THIS_DIR/backup/paperless-data"

  echo "Backing up Paperless data to $DOCUMENT_BACKUP_PATH"
  docker cp $PAPERLESS_CONTAINER_NAME:$DOCUMENTS_CONTAINER_DIR $DOCUMENT_HOST_DIR

  echo "Backing up Paperless media to $MEDIA_HOST_DIR"
  docker cp $PAPERLESS_CONTAINER_NAME:$MEDIA_CONTAINER_DIR $MEDIA_HOST_DIR

  echo "Archiving $MEDIA_HOST_DIR"
  tar -czvf "$MEDIA_HOST_DIR.tar.gz" $MEDIA_HOST_DIR

  echo "Removing $MEDIA_HOST_DIR"
  rm -r $MEDIA_HOST_DIR

  echo "Archiving $DOCUMENT_HOST_DIR"
  tar -czvf "$DOCUMENT_HOST_DIR.tar.gz" $MEDIA_HOST_DIR

  echo "Removing $DOCUMENT_HOST_DIR"
  rm -r $DOCUMENT_HOST_DIR

  if ! [[ -d "$FINAL_BACKUP_PATH" ]]; then
    echo "Creating $FINAL_BACKUP_PATH"
    mkdir -pv $FINAL_BACKUP_PATH
  fi

  echo "Moving backups to $FINAL_BACKUP_PATH"

  if [[ ! -d "$FINAL_BACKUP_PATH/data" ]]; then
    echo "Creating $FINAL_BACKUP_PATH/data"

    mkdir -pv "$FINAL_BACKUP_PATH/data"
  fi

  if [[ ! -d "$FINAL_BACKUP_PATH/media" ]]; then
    echo "Creating $FINAL_BACKUP_PATH/media"

    mkdir -pv "$FINAL_BACKUP_PATH/media"
  fi

  for file in ${HOST_BACKUP_ROOT_DIR}/data/*; do
    echo "Moving file: $file to: $FINAL_BACKUP_PATH/data"

    mv $file $FINAL_BACKUP_PATH/data/
  done

  for file in ${HOST_BACKUP_ROOT_DIR}/media/*; do
    echo "Moving file: $file to: $FINAL_BACKUP_PATH/media"

    mv $file $FINAL_BACKUP_PATH/media/
  done

}

function BACKUP_PAPERLESS_DOCUMENTS () {
  
  if [[ ! -f $DOCUMENT_BACKUP_PATH ]]; then
    echo ""
    echo "Backing up Paperless documents dir."
    echo ""

    tar -zcvf $DOCUMENT_BACKUP_PATH $DOCUMENT_DIR

  elif [[ -f $DOCUMENT_BACKUP_PATH ]]; then
    echo ""
    echo "Backup exists at "$DOCUMENT_BACKUP_PATH
    echo ""
    echo "Removing and creating new backup."
    echo ""

    rm $DOCUMENT_BACKUP_PATH
    tar -zcvf $DOCUMENT_BACKUP_PATH $DOCUMENT_DIR

  else
    echo ""
    echo "Unknown error."
    echo ""
  fi

}

function RESTORE_PAPERLESS_DOCUMENTS () {

  echo ""
  echo "No restore function yet."
  echo ""

}

function main () {

  if [ $1 == "backup" ]; then
    # BACKUP_PAPERLESS_DOCUMENTS
    BACKUP_PAPERLESS_DOCUMENTS2
  elif [ $1 == "restore" ]; then
    RESTORE_PAPERLESS_DOCUMENTS
  elif [ $1 == "trim" ]; then
    TRIM_BACKUPS
  fi

}

case $1 in
 "-b" | "--backup")
   main "backup"
  ;;
  "-r" | "--restore")
    main "restore"
  ;;
  "-bt" | "--backup-trim")
    main "trim"
  ;;
  *)
    echo ""
    echo "Invalid flag: "$1
    echo ""
    echo "Valid flags: -b/--backup, -r/--restore"
    echo ""
  ;;
esac

exit

```

### clean_backups.py

```python title="clean_backups.py" linenums="1"
from pathlib import Path
import typing as t
import os
import shutil
from datetime import datetime

from dataclasses import dataclass, field

BACKUP_DIR: Path = Path("./backup")
PAPERLESS_BACKUP_ROOT_DIR: Path= Path(f"{BACKUP_DIR}/paperless-data")

DB_BACKUP_DIR: Path = Path(f"{BACKUP_DIR}/db")
PAPERLESS_DATA_BACKUP_DIR: Path = Path(f"{PAPERLESS_BACKUP_ROOT_DIR}/data")
PAPERLESS_MEDIA_BACKUP_DIR: Path = Path(f"{PAPERLESS_BACKUP_ROOT_DIR}/media")

TS_FORMAT: str = "%Y-%m-%d_%H:%M"

KEEP_BACKUPS: int = 7

@dataclass
class ScannedFile:
    path: t.Union[str, Path] = field(default=None)
    created_time: t.Union[int, float, datetime] = field(default=None)
    
    def __post_init__(self):
        if isinstance(self.path, str):
            self.path = Path(self.path)
        
        if isinstance(self.created_time, int) or isinstance(self.created_time, float):
            self.created_time: datetime = convert_unix_ts_to_dt(self.created_time)


def convert_unix_ts_to_dt(ts: t.Union[int, float] = None) ->  datetime:
    assert ts is not None, ValueError("Missing input timestamp")
    assert isinstance(ts, int) or isinstance(ts, float), TypeError(f"Input timestamp should be of type int or float. Got type: ({type(ts)})")

    try:
        _ts: datetime = datetime.utcfromtimestamp(ts).strftime(TS_FORMAT)
        
        return  _ts
    except Exception as exc:
        msg = Exception(f"Unhandled exception converting input timestamp '{ts}' to Python datetime. Details: {exc}")
        print(f"[ERROR] {msg}")
        
        raise msg

def scan_dir(
    p: t.Union[str, Path] = None, follow_symlinks: bool = False
) -> t.Generator[Path, None, None]:
    """Recursively yield DirEntry objects for a given path.

    Params:
        p (str | Path): A path to scan. Will be converted to a Path object.
        follow_symlinks (bool): If `True`, recursive scans will follow symlinked dirs.

    Usage:
        - Create a variable, i.e. 'all_entries'.
        - Define as: `all_entries = list(scan_dir(some/path))`

    Returns:
        (Generator[Path, None, None]): Yields files found during scan.
    """
    assert p is not None, ValueError("p cannot be None")
    assert isinstance(p, str) or isinstance(p, Path), TypeError(
        f"p must be of type str or Path. Got type: ({type(p)})"
    )
    if isinstance(p, str):
        p: Path = Path(p)

    if not p.exists():
        print(f"[ERROR] Could not find path: {p}")
        return
    if p.is_file():
        print(f"[ERROR] '{p}' is a file. Scan dir should be a Path object.")
        return

    try:
        for entry in os.scandir(p):
            if entry.is_dir(follow_symlinks=follow_symlinks):
                ## Recurse into subdirectories
                yield from scan_dir(entry.path)

            else:
                ## Yield file as a Path object
                yield Path(entry.path)
    except Exception as exc:
        msg = Exception(f"Unhandled exception scanning path '{p}'. Details: {exc}")
        print(f"[ERROR] {msg}")

def clean_dir(p: t.Union[str, Path] = None, follow_symlinks: bool = False, dry_run: bool = False, keep_backups: int = KEEP_BACKUPS):
    assert p is not None, ValueError("Missing an input path to clean")
    assert isinstance(p, str) or isinstance(p, Path), TypeError(f"Input path must be of type str or Path. Got type: ({type(p)})")
    if isinstance(p, str):
        p: Path = Path(p)
    assert p.exists(), FileNotFoundError(f"Could not find path: '{p}'")

    print(f"Scanning for files in path '{p}'")
    try:
        _files = list(scan_dir(p=p))
        print(f"Found [{len(_files)}] file(s) in path '{p}'")
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting list of files in path: '{p}'. Details: {exc}")
        print(f"[ERROR] {msg}")
        
        raise msg
    
    file_objs: list[ScannedFile] = []
    
    for f in _files:
        f_obj: ScannedFile = ScannedFile(path=f, created_time=f.stat().st_ctime)
        file_objs.append(f_obj)
        
    file_objs.sort(key=lambda x: x.created_time)
    
    if not len(file_objs) > keep_backups:
        print(f"Backup count [{len(file_objs)}] is less than the backup limit of [{keep_backups}]. Skipping cleanup.")
        
        return file_objs

    print(f"Backup count [{len(file_objs)}] is equal to or greater than the backup limit of [{keep_backups}]")
    
    rm_backups: list[ScannedFile] = file_objs[0:-keep_backups]
    
    print(f"Removing [{len(rm_backups)}] backup(s) to bring backup count under threshold")
    
    for f in rm_backups:
        if f.path.is_file():
            if not dry_run:
                try:
                    f.path.unlink()
                    print(f"[SUCCESS] Removed file '{f.path}'")
                except Exception as exc:
                    msg = Exception(f"Unable to remove file '{f.path}'. Details: {exc}")
                    print(f"[ERROR] {msg}")
                    
                    pass
            else:
                print(f"[DRY RUN] Would remove file: '{f.path}'")
                pass

        else:
            if not dry_run:
                try:
                    shutil.rmtree(path=f.path)
                    print(f"[SUCCESS] Removed directory '{f.path}'.")
                except Exception as exc:
                    msg = Exception(f"Unable to remove file '{f.path}'. Details: {exc}")
                    print(f"[ERROR] {msg}")
                    
                    pass
            else:
                print(f"[DRY_RUN] Would remove directory: '{f.path}'")
                pass

def main(dry_run: bool = False):
    cleaned_db_backups = clean_dir(p=DB_BACKUP_DIR, dry_run=dry_run)
    cleaned_paperless_data_backups = clean_dir(p=PAPERLESS_DATA_BACKUP_DIR, dry_run=dry_run)
    cleaned_paperless_media_backups = clean_dir(p=PAPERLESS_MEDIA_BACKUP_DIR, dry_run=dry_run)
    
if __name__ == "__main__":
    print(f"Backup path: {BACKUP_DIR}")
    
    DRY_RUN: bool = False

    main(dry_run=DRY_RUN)

```

### create_webserver_superuser.sh

```shell title="create_webserver_superuser.sh" linenums="1"
#!/bin/bash

function prompt_create_env() {
    echo "Before running this script, you should copy .env.example to .env and edit it."
    read -p "Did you already create a .env file and add your values? Y/N: " create_env_choice

    case $create_env_choice in
        [Yy] | [YyEeSs])
            return 0
        ;;
        [Nn] | [NnOo])
            echo "Exiting script."

            return 1
        ;;
        *)
            echo "[ERROR] Invalid choice: ${create_env_choice}"
            prompt_create_env
        ;;
    esac
}

function create_superuser() {
    docker compose run --rm webserver createsuperuser

    return $?
}

function main() {
    prompt_create_env

    if [[ $? -eq 0 ]]; then
        create_superuser

        return $?

    else
        return $?
    fi
}

main

exit $?

```

### initial-setup.sh

```shell title="initial-setup.sh" linenums="1"
#!/bin/bash

declare -a DOCKER_FILES=( "docker-compose.yml" ".env" "docker-compose.env" )

function COPY_EXAMPLE_FILE () {

  if [[ ! -f $1 ]]; then
    echo ""
    echo "Copying "$1.example" to "$1
    echo ""
    mv $1.example $1
  elif [[ -f $1 ]]; then
    echo ""
    echo $1" exists. Skipping."
    echo ""
  fi

}

function GENERATE_SECRET_KEY () {

  if [[ ! -f secret_key ]]; then
    echo ""
    echo "Generating secret key."
    echo "Add the secret to the docker-compose.env file"
    echo ""

    openssl rand -base64 64 >> secret_key
  elif [[ -f secret_key ]]; then
    echo ""
    echo "Secret key file exists."
    echo "Open the file and copy the key (getting rid of the newline) into docker-compose.env"
    echo ""
  else
    echo ""
    echo "Unknown error"
    echo ""
  fi

}

for FILE in "${DOCKER_FILES[@]}"
do
  COPY_EXAMPLE_FILE $FILE
done

echo ""
echo "Pausing. Go edit the docker-compose.env, docker-compose.yml, and .env files before continuing."
echo ""
echo "Secret key will be generated in the next step."
echo ""
read -p "Press a key to continue when ready: "
echo ""

GENERATE_SECRET_KEY

echo "Secret key generated. Printing below."
echo "Copy and paste the secret key into the PAPERLESS_SECRET_KEY"
echo "    variable inside docker-compose.env before continuing."
echo ""
echo "Secret key (make sure to remove newlines in docker-compose.env):"
echo ""
cat secret_key

echo ""
read -p "Press a key to continue when ready: "

echo ""
echo "Running docker-compose stack"
echo ""

docker-compose pull
docker-compose up -d

echo ""
echo "Running initial admin setup."
echo ""

docker-compose run --rm webserver createsuperuser

echo ""
echo "Initial setup complete."
echo ""

exit

```

## Notes

### Initial Setup

- Run `initial-setup.sh`
    - Copies example docker-compose.yml, .env, and docker-compose.env to live version
    - Generates a secret key and writes it to the file `secret_key` in the paperless-ng repository
        - Copy this key and paste it into the `PAPERLESS_SECRET_KEY` variable in docker-compose.env
    - Runs the initial createsuperuser command, where you'll create an admin account
- Manually edit .env and docker-compose.env files, where you'll set variable values like the port Paperless runs on, database password, etc

### Backup

There are 2 backup scripts included, `backup-db.sh` and `backup-documents.sh`. Each script takes flags (run the script without any flags to see available options). The restore feature isn't working (yet).

Example: backup database

`$> ./backup-db.sh -b`

This dumps the database file to `./backup/db/paperless_db_dump.sql`

## Links
