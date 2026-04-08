---
tags:
  - python
  - nox
  - automation
---
# Custom Nox Sessions

## Count lines of code with pygount

```python title="Pygount LOC count" linenums="1"
@nox.session(name="count-loc")
def count_lines_of_code(session: nox.Session):
    session.install("pygount")
    
    log.info("Counting lines of code with pygount")
    session.run("pygount", "--format=summary", "./")
```
