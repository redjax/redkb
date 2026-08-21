# Troubleshooting

If you run into errors or unexpected functionality, the best first place to check is the [`uv` Github repository's issues](https://github.com/astral-sh/uv/issues). Search for parts of error messages, status codes, or package/tool names, and if you don't see anything related to your problem, create a new issue. Include details about your system (OS, release, Linux distribution, etc.), the command you ran, and the command's output.

## SSL, TLS, & Certificate Issues

In a locked-down corporate environment where you have a firewall or AV doing SSL inspection, you will likely see errors when trying to perform network operations in WSL, like cURL-ing files or running `apt update`/`dnf update`. The error will look something like:

```shell
SSL peer certificate or SSH remote key was not OK for <URL> [SSL certificate problem: self-signed certificate in certificate chain]
```

The solution for this problem is to export your Trusted Root CA certificate from the Windows side, and import it into the WSL side.

Windows side:

- Open `certmgr.msc` and navigate to "Certificates - Current User > Trusted Root Certification Authorities > Certificates"
- Find your machine's Trusted Root CA (it might be named after your company, or your firewall provider)
- Double-click the entry, go to the "Details" tab, and click the "Copy to File..." button
  - You may see more than 1 root CA with the same name; do these steps for both of them
- Choose "Base-64 encoded X.509 (.CER)" for the file format
- Save the file to a location on your machine, i.e. the Downloads folder

WSL side:

- Copy the exported cert(s) to `/etc/pki/ca-trust/source/anchors/etc-root-1.crt` (use `-2.crt` if there are 2 certificates)
- On RedHat-based distributions:
  - Run `sudo update-ca-trust extract`
  - Run `sudo dnf clean all && sudo dnf makecache`
- On Debian-based distributions:
  - Run `sudo update-ca-certificates`
  - Run `sudo apt clean && sudo apt upgrade`
- Then retry the network operation that failed

## Invalid peer certificate when installing dependencies

When installing dependencies or Python with uv, you might see an error like:

```shell
...

Caused by: client error (Connect)
Caused by: invalid peer certificate: UnknownIssuer
```

In a corporate environment, you need to [install the Trusted Root CA](#ssl-tls--certificate-issues), but `uv` might still throw this error when installing dependencies. To fix this, try running the install command with `--system-certs`, and if that resolves the issue, add this to your `~/.bashrc` or `~/.zshrc`:

```shell
export UV_SYSTEM_CERTS=true
```

This will tell `uv` to load TLS certificates from the platform's native certificate store, instead of the bundled Mozilla root certificates.

