---
tags:
  - restic
  - resticprofile
---

# Excluding paths in a backup

`resticprofile` can handle [Restic exclude patterns](https://restic.readthedocs.io/en/stable/040_backup.html#excluding-files) to skip paths during backups. When backing up a directory, you can (and should) provide exclude patterns to limit the size of the backup, skipping over any unnecessary files.

You can pass excludes as a list of patterns in your `profiles.yaml`, or give a path to a file with exclude patterns using the `exclude-file:` parameter.

[Read more about excludes on the excludes page](excludes.md).
