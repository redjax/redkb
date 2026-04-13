---
title: "Pypirc File"
date: 2024-02-11T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - python
  - reference
---

- Create file `~/.pypirc`
  - Set chmod to `600`
- Copy/paste contents of file below
  - Replace `<pypi-test-token>/<pypi-token>` with your pypi/pypi-test publish token.

``` title="~/.pypirc" linenums="1"
## ~/.pypirc
#  chmod: 600
[distutils]
index-servers=
    pypi
    testpypi

## Example of a local, private Python package index
# [local]
# repository = http://127.0.0.1:8080
# username = test 
# password = test

[testpypi]
username = __token__ 
password = <pypi-test-token>

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <pypi-token>

```
