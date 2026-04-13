FROM hugomods/hugo:exts AS builder
WORKDIR /src

RUN apk add --no-cache git

COPY archetypes/ archetypes/
COPY content/ content/
COPY static/ static/
COPY data/ data/
COPY i18n/ i18n/
COPY hugo.yml go.mod go.sum .hugo_build.lock ./

ARG HUGO_BASEURL=http://localhost/

RUN --mount=type=bind,source=.,target=/workdir,readonly \
  cp -a /workdir/.git /src/.git && \
  hugo \
    --minify \
    --gc \
    --enableGitInfo \
    --baseURL="${HUGO_BASEURL}" \
    --destination /output/public

FROM caddy:alpine

COPY --from=builder /output/public /usr/share/caddy

COPY .containers/prod/Caddyfile /etc/caddy/Caddyfile

EXPOSE 80 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
