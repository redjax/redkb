---
tags:
    - standard-project-files
    - python
    - nox
    - pre-commit
    - jupyter
    - pytest
---

# nbstripout

## Strip notebook output

```python title="noxfile.py" linenums="1"
@nox.session(
    python=[DEFAULT_PYTHON], name="strip-notebooks", tags=["jupyter", "cleanup"]
)
def clear_notebook_output(session: nox.Session):
    session.install("nbstripout")

    log.info("Gathering all Jupyter .ipynb files")
    ## Find all Jupyter notebooks in the project
    notebooks = Path(".").rglob("*.ipynb")

    ## Clear the output of each notebook
    for notebook in notebooks:
        log.info(f"Stripping output from notebook '{notebook}'")
        session.run("nbstripout", str(notebook))
```
