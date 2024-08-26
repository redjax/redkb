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
## MKDocs
DOCS_REQUIREMENTS_FILE: Path = Path("docs/requirements.txt")
DOCS_VENV_PATH: Path = Path(".mkdocs-venv")
MKDOCS_DEV_PORT: int = 8000
MKDOCS_DEV_ADDR: str = "0.0.0.0"

@nox.session(python=[DEFAULT_PYTHON], name="publish-mkdocs", tags=["mkdocs", "publish"])
def publish_mkdocs(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Publishing MKDocs site")

    session.run("mkdocs", "gh-deploy")
```