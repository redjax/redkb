# Docker

Notes, links, & reference code for Docker/Docker Compose.

!!!TODO

    - [ ] Add sections for things that took me entirely too long to learn/understand
        - [ ] Multistage builds
            - [ ] How to target specific layers, i.e. `dev` vs `prod`
        - [ ] Common Docker commands, how to interpret/modify them
            - [ ] Docker build
            - [ ] Docker run
        - [ ] `ENV` vs `ARG`
        - [ ] `EXPOSE`
        - [ ] `CMD` vs `ENTRYPOINT` vs `RUN`
    - [ ] Add section(s) for Docker Compose
        - [ ] Add an example `docker-compose.yml`
        - [ ] Detail required vs optional sections (i.e. `version` (required) and `volumes` (optional))
        - [ ] Links (with `depends_on`)
        - [ ] Networking
            - [ ] Internal & external networks
            - [ ] Proxying
            - [ ] Exposing ports (and when you don't need to/shouldn't)
