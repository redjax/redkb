# Logrotate

[Logrotate](https://wiki.archlinux.org/title/Logrotate) is a Linux utility for rotating logs by reading policies defined in `/etc/logrotate.d/`. You can read more about setting up logrotate in [this RedHat blog entry](https://www.redhat.com/en/blog/setting-logrotate).

You can create a logrotate policy for pretty much any file you output logs to, but it is recommended to store your logs in `/var/log/` or a subdirectory in that path, i.e. `/var/log/program_name/some_logfile.log`.

Logrotate policies should be defined in files in the `/etc/logrotate.d/` directory.

See the [cheatsheet page](cheatsheet.md) for a [`logrotate` commands cheatsheet](cheatsheet.md#logrotate-cheatsheet) and [example `logrotate` policy files](cheatsheet.md#example-policy-files).

> [!TIP]
> When creating a logrotate policy file, choose a name that describes the log file it applies to,
> and create the file at the root of `/etc/logrotate.d/`, don't use subdirectories. There are ways
> to do that, but unless you have trouble maintaining your policies in a 'flat' structure, logrotate
> will not detect your nested policies.
>
> An example of a logrotate policy that rotates `/var/log/some_program/function.log` could be named
> `/etc/logrotate.d/some_program_function`.
>
> You do **not** need to put a file extension in the filename. The file must be owned by `root`.

## Policy file

A policy file defined at `/etc/logrotate.d/policy_filename` should start with the path to the file it applies to. For example, a policy that rotates a log at `/var/log/program_name/function.log` would start with:

```plaintext title="logrotate policy file path"
/var/log/program_name/function.log {}
```

You then add your configurations in the `{}` mapping. See the [policy options cheatsheet](cheatsheet.md#policy-options-cheatsheet) for an overview of commonly used options.

For example, a logrotate policy that:

- rotates the file daily, keeping the last 14 rotated logs
- compresses each rotated file with `gzip`, but delays the most recently compressed logfile (for easy access of the most recently rotated log file)
- does not error if the log file is missing
- skips if the log file's contents are empty
- recreates the file after rotation with `chmod 0640` and `chown root:adm`

```plaintext title="Example logrotate policy" linenums="1"
/var/log/program_name/function.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root adm
}
```

