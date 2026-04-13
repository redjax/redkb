---
title: "Custom Sessions"
date: 2025-01-21T00:00:00-00:00
draft: false
weight: 2
keywords: []
tags:
  - python
  - nox
lastmod: "2026-04-13T04:44:39Z"
---

## Count lines of code with pygount

```python title="Pygount LOC count" linenums="1"
@nox.session(name="count-loc")
def count_lines_of_code(session: nox.Session):
    session.install("pygount")
    
    log.info("Counting lines of code with pygount")
    session.run("pygount", "--format=summary", "./")
```
