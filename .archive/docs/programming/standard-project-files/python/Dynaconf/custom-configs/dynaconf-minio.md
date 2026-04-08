---
tags:
    - standard-project-files
    - python
    - dynaconf
    - minio
---

# Dynaconf Minio configuration

Configure a `minio` client.

## Settings files

### minio/settings.toml

```toml title="config/minio/settings.toml" linenums="1"
[default]

minio_address = ""
minio_port = 9000
minio_username = "auto-xkcd"
## Set in .secrets.toml
# minio_password = ""
##  Set in .secrets.toml
# minio_access_key = ""
# minio_access_secret = ""

[dev]

minio_address = ""
minio_port = 9000
minio_username = "auto-xkcd"
## Set in .secrets.toml
# minio_password = ""
##  Set in .secrets.toml
# minio_access_key = ""
# minio_access_secret = ""

[prod]

minio_address = ""
minio_port = 9000
minio_username = "auto-xkcd"
## Set in .secrets.toml
# minio_password = ""
##  Set in .secrets.toml
# minio_access_key = ""
# minio_access_secret = ""
```

### minio/.secrets.toml

```toml title="config/minio/.secrets.toml" linenums="1"
[default]

minio_password = ""
minio_access_key = ""
minio_access_secret = ""

[dev]

minio_password = ""
minio_access_key = ""
minio_access_secret = ""

[prod]

minio_password = ""
minio_access_key = ""
minio_access_secret = ""
```

## Config classes

### Pydantic minio_config.py

!!! todo
    - [ ] Write a minio config class

```python title="minio_config.py" linenums="1"

```
