---
tags:
    - standard-project-files
    - python
    - nox
    - ansible
---

# Ansible

## Build Ansible collections

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

```

## Ansible debug remote host

```python title="Ansible remote host debug" linenums="1"
## Session that runs an Ansible playbook
@nox.session(python=DEFAULT_PYTHON, name="playbook-debug-all", tags=["debug", "ansible"])
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
