# Configuring readthedocs

Set up auto-builds of your documentation and publish to [`readthedocs`](https://readthedocs.org/).

## .readthedocs.yaml

```yaml title=".readthedocs.yaml (mkdocs)" linenums="1"
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the OS, Python version, and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
    # You can also specify other tool versions:
    # nodejs: "19"
    # rust: "1.64"
    # golang: "1.19"

mkdocs:
  configuration: mkdocs.yml

# Optionally build your docs in additional formats such as PDF and ePub
# formats:
#    - pdf
#    - epub

# Optionally, but recommended,
# declare the Python requirements required to build your documentation
# See https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
python:
   install:
   - requirements: requirements/requirements.txt

```