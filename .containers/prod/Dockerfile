FROM hugomods/hugo:exts AS builder

WORKDIR /src

## Copy Hugo site files & config
COPY archetypes/ archetypes/
# COPY assets/ assets/
COPY content/ content/
# COPY layouts/ layouts/
COPY static/ static/
COPY data/ data/
COPY i18n/ i18n/
COPY hugo.yml go.mod go.sum .hugo_build.lock ./

ARG HUGO_BASEURL=http://localhost/

RUN hugo \
  --minify \
  --gc \
  --baseURL="${HUGO_BASEURL}" \
  --destination /output/public

FROM caddy:alpine

COPY --from=builder /output/public /usr/share/caddy

COPY .containers/prod/Caddyfile /etc/caddy/Caddyfile

EXPOSE 80 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
