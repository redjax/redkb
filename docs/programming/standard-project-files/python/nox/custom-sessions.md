---
tags:
    - standard-project-files
    - python
    - nox
    - pre-commit
    - jupyter
    - pytest
---

# Custom nox sessions

## pre-commit

### Run all pre-commit hooks

```py title="noxfile.py" linenums="1"
## Run all pre-commit hooks
@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    print("Running all pre-commit hooks")
    session.run("pre-commit", "run")

```

### Automatically update pre-commit hooks on new revisions

```py title="noxfile.py" linenums="1"
## Automatically update pre-commit hooks on new revisions
@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    session.install(f"pre-commit")

    print("Running pre-commit update hook")
    session.run("pre-commit", "run", "pre-commit-update")
```

## pytest

### Run pytests with xdist

`pytest-xdist` runs tests concurrently, significantly improving test execution speed.

```py title="noxfile.py" linenums="1"
## Run pytest with xdist, allowing concurrent tests
@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )
```

### Run pytests

```py title="noxfile.py" linenums="1"
## Run pytest
@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )
```

## nbstripout

### Strip notebook output

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

## MkDocs

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

## Ansible

### Build Ansible collections

```python title="noxfile.py" linenums="1"
COLLECTIONS_PATH: Path = Path("./collections")
ANSIBLE_COLLECTIONS_PATH: Path = Path(f"{COLLECTIONS_PATH}/ansible_collections")
MY_COLLECTIONS_PATH: Path = Path(f"{COLLECTIONS_PATH}/my")
COLLECTION_BUILD_OUTPUT_PATH: Path = Path("./build")

@nox.session(python=DEFAULT_PYTHON, name="build-my-collections", tags=["ansible", "build"])
@nox.parametrize("custom_collections", [CUSTOM_COLLECTIONS])
@nox.parametrize("collection_build_output_path", [COLLECTION_BUILD_OUTPUT_PATH])
def build_custom_collections(session: nox.Session, custom_collections: list[CustomAnsibleCollection], collection_build_output_path: Path):
    if not collection_build_output_path.exists():
        try:
            collection_build_output_path.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(f"({type(exc)}) Unhandled exception creating build output path '{collection_build_output_path}'. Details: {exc}")
            log.error(msg)
            
            raise exc
    
    session.install("ansible-core")
    
    for _collection in custom_collections:
        log.info(f"Building collection '{_collection.name}' at path: {_collection.path}")
        
        if not _collection.path_exists:
            _exc = FileNotFoundError(f"Could not find collection at path '{_collection.path}'")
            log.error(_exc)
            
            raise _exc
        
        log.debug(f"Found collection '{_collection.name}' at path: {_collection.path}")
        
        try:
            session.run("ansible-galaxy", "collection", "build", f"{_collection.path}", "--output-path", f"{collection_build_output_path}", "--force")
        except Exception as exc:
            msg = Exception(f"({type(exc)}) Unhandled exception building collection '{_collection.name}'. Details: {exc}")
            log.error(msg)
            
            continue


@nox.session(python=DEFAULT_PYTHON, name="install-ansible-requirements", tags=["ansible", "install"])
def install_collections(session: nox.Session):
    assert Path("requirements.yml").exists(), FileNotFoundError("Could not find Ansible project requirements.yml.")
    
    session.install("ansible-core")
    
    log.info("Installing collections from requirements.yml")
    
    try:
        session.run("ansible-galaxy", "collection", "install", "-r", "requirements.yml")
    except Exception as exc:
        msg = Exception(f"({type(exc)}) Unhandled exception installing Ansible Galaxy requirements from requirements.yml. Details: {exc}")
        log.error(msg)
        
        raise exc
    
    log.info("Installing roles from requirements.yml")
    
    try:
        session.run("ansible-galaxy", "role", "install", "-r", "requirements.yml")
    except Exception as exc:
        msg = Exception(f"({type(exc)}) Unhandled exception installing Ansible Galaxy requirements from requirements.yml. Details: {exc}")
        log.error(msg)
        
        raise exc
    
    if Path("requirements.private.yml").exists():
        log.info("Ensuring local collections are installed from requirements.private.yml with --force")
        try:
            session.run("ansible-galaxy", "collection", "install", "-r", "requirements.private.yml", "--force")
        except Exception as exc:
            msg = Exception(f"Unhandled exception installing packages from 'requirements.private.yml'. Details: {exc}")
            log.error(msg)
            
            raise exc


## Session that runs an Ansible playbook
@nox.session(python=DEFAULT_PYTHON, name="playbook-debug-all", tags=["debug"])
def ansible_playbook_debug_all(session: nox.Session):
    session.install("ansible-core")
    
    log.info("Running debug-all.yml playbook on homelab inventory")
    
    try:
        session.run("ansible-playbook", "-i", "inventories/homelab/inventory.yml", "plays/debug/debug-all.yml")
    except Exception as exc:
        msg = Exception(f"({type(exc)}) Unhandled exception running playbook. Details: {exc}")
        log.error(msg)
        
        raise exc
```
