---
tags:
  - linux
  - windows
  - mac
  - utilities
  - restic
  - backup
---

# Ignore/exclude files

*[Restic docs: Excluding files](https://restic.readthedocs.io/en/latest/040_backup.html#excluding-files)*

You can pass `--exclude path_or_pattern` to `restic` commands to exclude matching paths in the source directory from the backup.

For scheduled backups (or just as a general practice), you can create "ignore files" that you can pass like `restic src/ --exclude-file ~/.restic/ignores/ignore_filename`. You can also pass multiple `--exclude-filename ...` and `--exclude ...` flags.

You can split your ignore files, i.e. by programming language or purpose. Below are some purpose-specific Restic ignore files.

## Default/base ignores

```plaintext title="~/.restic/ignores/default" linenums="1"
## Ignore caches
*.cache
.cache/

## Ignore temporary files
*.tmp
*.temp
*.bak

## Ignore specific user directories
Downloads/

## Ignore MacOS and Linux system files
.DS_Store
*.swp

## Ignore logs and temporary files
*.log
*.tmp
*.swp

## -----------------------------------

## Don't ignore the restic ignore file
!.resticignore

```

## Python ignores

```plaintext title="~/.restic/ignores/python" linenums="1"
## Ignore Python bytecode files
__pycache__/
*.py[cod]
*$py.class

## Distribution / packaging
.Python
build/
develop-eggs/
dist/
site/
downloads/
eggs/
.eggs/
lib64/
parts/
sdist/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

## Ruff cache
.ruff_cache

## Nox cache
.nox

## Ignore virtual environment directories
venv/
env/
.env/

## Ignore distribution/build directories
build/
dist/
*.egg-info/

## Ignore logs and temporary files
*.log
*.tmp
*.swp

## Ignore caches
.cache/
.pytest_cache/

## Ignore IDE/editor files
.vscode/
.idea/

## -----------------------------------

## Don't ignore the restic ignore file
!.resticignore

```

## Go ignores

```plaintext title="~/.restic/ignores/go" linenums="1"
## Ignore Go build binaries
*.exe
*.exe~
*.test

## Ignore build output directories
bin/
build/

## -----------------------------------

## Don't ignore the restic ignore file
!.resticignore

```

## Windows ignores

```plaintext
## Exclude Windows system and special folders
C:\$RECYCLE.BIN
C:\swapfile.sys
C:\hiberfil.sys
C:\pagefile.sys
C:\Program Files\Common Files\BitDefender
C:\ProgramData\Microsoft\Crypto
C:\ProgramData\Microsoft\Windows\WER
C:\Windows\debug
C:\System Volume Information

## Temp and cache folders
\temp
\tmp
\Users\*\AppData\Local\Temp\
\Users\*\AppData\Local\Package Cache
\Users\*\AppData\Roaming\*\cache\
\Users\*\Local\Temp
\Users\*\Local\Microsoft\Windows\INetCache

## User-specific exclusion patterns
\Users\*\appdata\index.dat

## Generic cache and temp files
.cache
cache
cache2
*~
__pycache__
*.pyc

```

## My default excludes file

```plaintext
*~

## Exclude Windows system and special folders
C:\$RECYCLE.BIN
C:\swapfile.sys
C:\hiberfil.sys
C:\pagefile.sys
C:\Program Files\Common Files\BitDefender
C:\ProgramData\Microsoft\Crypto
C:\ProgramData\Microsoft\Windows\WER
C:\Windows\debug
C:\System Volume Information

## Temp and cache folders
\temp
\tmp
\Users\*\AppData\Local\Temp\
\Users\*\AppData\Local\Package Cache
\Users\*\AppData\Roaming\*\cache\
\Users\*\Local\Temp
\Users\*\Local\Microsoft\Windows\INetCache

## User-specific exclusion patterns
\Users\*\appdata\index.dat

## Ignore caches
*.cache
.cache/

## Ignore temporary files
*.tmp
*.temp

## Ignore specific user directories
Downloads/

## Ignore log files
*.log

## Ignore MacOS and Linux system files
.DS_Store
*.swp

## Ignore Go build binaries
*.exe
*.exe~
*.test

## Ignore shared libraries
*.dll
*.so
*.dylib

## Ignore coverage and output files
*.out

## Ignore vendor directory (if used)
vendor/

## Ignore build output directories
bin/
build/

## Ignore Python bytecode files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
site/
downloads/
eggs/
.eggs/
lib64/
parts/
sdist/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

## Ignore virtual environment directories
venv/
env/
.env/

## Ignore distribution/build directories
build/
dist/
*.egg-info/

## Ignore logs and temporary files
*.log
*.tmp
*.swp

## Ignore caches
.cache/
.pytest_cache/

## Ignore IDE/editor files
.vscode/
.idea/

## -----------------------------------

## Don't ignore the restic ignore file
!.resticignore
## Don't ignore resticprofile profiles.yaml
!profiles.yaml

```
