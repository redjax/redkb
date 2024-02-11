# pyproject.toml scripts

In your `pyproject.toml` file, add a section `[tool.pdm.scripts]`, then copy/paste whichever scripts you want to add to your project.

!!!warning

    Check the code for some of the scripts, like the `start` script, which assumes your project code is at `./src/app/main.py`. If your code is in a different path, or named something other than `app`, make sure to change this and any other similar lines.

```toml title="pyproject.toml" linenums="1"
[tool.pdm.scripts]

###############
# Format/Lint #
###############

# Lint with black & ruff
lint = { shell = "pdm run ruff check . --fix && pdm run black ." }
## With nox
# lint = { cmd = "nox -s lint"}
# Check only, don't fix
check = { cmd = "black ." }
# Check and fix
format = { cmd = "ruff check . --fix" }

########################
# Start/Launch Scripts #
########################

#  Run main app or script. Launches from app/
start = { shell = "cd app && pdm run python main.py" }

## Example Dynaconf start
start-dev = { cmd = "python src/app/main.py", env = { ENV_FOR_DYNACONF = "dev" } }

######################
# Export Requirement #
######################

#  Export production requirements
export = { cmd = "pdm export --prod -o requirements/requirements.txt --without-hashes" }
#  Export only development requirements
export-dev = { cmd = "pdm export -d -o requirements/requirements.dev.txt --without-hashes" }
## Uncomment if/when using a CI group
# export-ci = { cmd = "pdm export -G ci -o requirements/requirements.ci.txt --without-hashes" }
## Uncomment if using mkdocs or sphinx
# export-docs = { cmd = "pdm export -G docs --no-default -o docs/requirements.txt --without-hashes" }

###########
# Alembic #
###########

## Create initial commit
alembic-init = { cmd = "alembic revision -m 'Initial commit.'" }

## Upgrade Alembic head after making model changes
alembic-upgrade = { cmd = "alembic upgrade head" }

## Run migrations
#  Prompts for a commit message
alembic-migrate = { shell = "read -p 'Commit message: ' commit_msg && pdm run alembic revision --autogenerate -m '${commit_msg}'" }

## Run full migration, upgrade - commit - revision
migrations = { shell = "pdm run alembic upgrade head && read -p 'Commit message: ' commit_msg && pdm run alembic revision --autogenerate -m '${commit_msg}'" }

```
