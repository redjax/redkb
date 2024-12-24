---
tags:
  - linux
  - bash
  - reference
  - debian
  - fedora
  - arch
---

# Tips & Tricks

Miscellaneous Linux tips & tricks. If an example would only work on a specific OS (i.e. Debian-family only), there will be a message stating so; otherwise, these commands should work across different Linux OSes.

## Configurations

### Enable CLI boot (disable GUI)

Set your machine to "CLI" boot, where the computer will start at a shell prompt and without a GUI:

```bash title="Set CLI boot"
sudo systemctl set-default multi-user.target
```

To undo this change, run:

```bash title="Set GUI boot"
sudo systemctl set-default graphical.target
```

### Allow passwordless sudo

!!! warning

    This is not recommended! This configuration is insecure, and allows running all commands as root without entering a password.

    There is almost no environment where this is suitable or advisable. The main reason this is documented is so you know where to undo it if you come across a machine that allows sudo commands without a password.

Allowing `sudo` commands without a password is very risky and inadvisable. This is the state most Windows machines run in (the user is admin/root by default). With the guardrails off, you are free to mistakenly edit or delete files/directories, and your machine is highly insecure; any attacker able to access the user's account could run any command as root without being prompted for a password.

To grant a user password-less `sudo` rights, run the command `visudo` (the `sudo` package must be installed) as root/with `sudo`, and add the following below the line that reads `# Allow members of group sudo to execute any command`:

```bash title="Allow passwordless sudo" linenums="1"
# Allow passwordless sudo for specified user(s)
<username>    ALL=(ALL) NOPASSWD:ALL
```
