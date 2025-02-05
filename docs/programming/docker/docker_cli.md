---
tags:
  - docker
---

# The Docker CLI

...

## Docker Command Cheat Sheet

| Command                                | Description                                                                                                                                                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker ps [-a]`                       | Show Docker containers. Use `-a`/`--all` to show all containers, instead of only running ones.                                                                                                                                  |
| `docker system [df,events,info,prune]` | Manage Docker. `df` shows Docker disk usage, `events` shows real-time events from the server, `info` displays system-wide info, and `prune` handles Docker cleanup tasks like removing old images & volumes that aren't in use. |
| `docker cp /path/on/host <container_name>:/path/in/container` | Copy a file from the host machine into a container. |
| `docker cp <container_name>:/path/in/container /path/on/host` | Copy a file from within the container to the host. |
