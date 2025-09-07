---
tags:
  - restic
  - resticprofile
---

# Cleanup

When using `resticprofile` for backups, regular cleanup of old snapshots and repository pruning is essential to keep the backup repository manageable and avoid running out of storage.

Restic uses snapshots to save states of your backups over time. Old snapshots can accumulate and consume a lot of space. Cleaning up involves two main steps:
- **Forget** snapshots according to a retention policy.
- **Prune** the repository to remove unreferenced data.

!!! tip "Preview operations with --dry-run"

    You can add the `--dry-run` flag to most of the commands below to have `resticprofile` show you what it would clean up, without actually performing the operation.

??? note "Difference between 'prune' and 'forget'"

    The `forget` operation deletes snapshot metadata & refs, but it does not delete the actual backup data. This means you can run this operation frequently, as it's a quick operation that queues up objects for deletion when a `prune` command is run.

    The `prune` command cleans up the repository by removing the actual data blobs and packs that are no longer referenced by any snapshot. It performs a low-level reorganization of the repository to reclaim storage space by deleting unneeded backup data. This operation is slower and should be run less frequently, i.e. once a week or as-needed when the repository is too large.

## Forget Old Snapshots

The `forget` command removes snapshot metadata & refs when the backup's `forget:` conditions are met. The command does not delete any of the actual data in the backups, but it marks them for deletion with the [prune command](#prune-backup-data).

```shell title="Forget old backups"
resticprofile -c ~/profiles.yaml forget
```

You can optionally add `--prune` to perform a pruning operation at the same time.

## Prune backup data

The `prune` command uses a similar schedule as the [forget command](#forget-old-snapshots), but also deletes the underlying blob data. This operation takes longer than `forget`, and is destructive.

```shell title="Prune old backups"
resticprofile -c ~/profiles.yaml --name profile-name prune
```

## Check integrity after cleanup

After running a cleanup/forget command, you should run a `check` to ensure the integrity of your backups:

```shell title="Check repository integrity"
resticprofile -c ~/profiles.yaml --name profile-name check
```
