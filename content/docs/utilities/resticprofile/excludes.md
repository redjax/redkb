---
title: "Exclude paths in backups"
date: 2025-09-07T00:00:00-00:00
draft: true
weight: 30
keywords: []
tags:
  - util
  - restic
  - resticprofile
---

`resticprofile` can handle [Restic exclude patterns](https://restic.readthedocs.io/en/stable/040_backup.html#excluding-files) to skip paths during backups. When backing up a directory, you can (and should) provide exclude patterns to limit the size of the backup, skipping over any unnecessary files.

You can pass excludes as a list of patterns in your `profiles.yaml`, or give a path to a file with exclude patterns using the `exclude-file:` parameter.
