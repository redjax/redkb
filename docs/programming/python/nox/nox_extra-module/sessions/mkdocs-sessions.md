---
tags:
    - standard-project-files
    - python
    - nox
    - mkdocs
---

# MkDocs

## Publish mkdocs
```python title="noxfile.py" linenums="1"
REQUIREMENTS_OUTPUT_DIR: str = "requirements"

@nox.session(python=[DEFAULT_PYTHON], name="publish-mkdocs", tags=["mkdocs", "publish"])
def publish_mkdocs(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Publishing MKDocs site")

    session.run("mkdocs", "gh-deploy")
```

## Serve mkdocs site locally

```python
import typing as t
import socket
import logging
log = logging.getLogger(__name__)

REQUIREMENTS_OUTPUT_DIR: str = "requirements"

def _find_free_port(start_port=8000):
    """Find a free port starting from a specific port number"""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except socket.error:
                log.info(f"Port {port} is in use, trying the next port.")
                port += 1


@nox.session(python=DEFAULT_PYTHON, name="serve-mkdocs", tags=["mkdocs", "serve"])
def serve_mkdocs(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")
    
    free_port = _find_free_port(start_port=8000)
    
    log.info(f"Serving MKDocssite on port {free_port}")
    
    try:
        session.run("mkdocs", "serve", "--dev-addr", f"0.0.0.0:{free_port}")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception serving MKDocs site. Details: {exc}"
        log.error(msg)

```
