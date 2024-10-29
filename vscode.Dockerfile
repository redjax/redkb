ARG UV_BASE=${UV_IMG_VER:-0.4.27}
ARG OPENVSCODE_SERVER_BASE=${OPENVSCODE_SERVER_BASE:-latest}

FROM ghcr.io/astral-sh/uv:$UV_BASE AS uv
FROM gitpod/openvscode-server:$OPENVSCODE_SERVER_BASE AS base

## Add Astral uv to the container
COPY --from=uv /uv /bin/uv

ENV OPENVSCODE_SERVER_ROOT="/home/.openvscode-server"
ENV OPENVSCODE="${OPENVSCODE_SERVER_ROOT}/bin/openvscode-server"

SHELL ["/bin/bash", "-c"]

RUN \
  # ## Direct download links to external .vsix not available on https://open-vsx.org/
  # #  The two links here are just used as example, they are actually available on https://open-vsx.org/
  # urls=(\
  # https://github.com/rust-lang/rust-analyzer/releases/download/2022-12-26/rust-analyzer-linux-x64.vsix \
  # https://github.com/VSCodeVim/Vim/releases/download/v1.24.3/vim-1.24.3.vsix \
  # )\
  # ## Create a tmp dir for downloading
  # && tdir=/tmp/exts && mkdir -p "${tdir}" && cd "${tdir}" \
  # ## Download via wget from $urls array.
  # && wget "${urls[@]}" && \
  ## Download extensions from open-vsx.org by id
  exts=(\
  # From https://open-vsx.org/ registry directly
  christian-kohler.path-intellisense \
  # detachhead.basedpyright \ 
  eamodio.gitlens \ 
  esbenp.prettier-vscode \ 
  formulahendry.auto-close-tag \ 
  formulahendry.auto-rename-tag \ 
  mhutchie.git-graph \  
  # mtxr.sqltools \ 
  # mtxr.sqltools-driver-mysql \ 
  # mtxr.sqltools-driver-pg \ 
  # mtxr.sqltools-driver-sqlite \ 
  # redhat.ansible \
  redhat.vscode-xml \ 
  redhat.vscode-yaml \ 
  samuelcolvin.jinjahtml \ 
  tamasfe.even-better-toml \ 
  waderyan.gitblame \ 
  yzhang.markdown-all-in-one \
  # From filesystem, .vsix that we downloaded (using bash wildcard '*')
  # "${tdir}"/* \
  )\
  # Install the $exts
  && for ext in "${exts[@]}"; do ${OPENVSCODE} --install-extension "${ext}"; done
