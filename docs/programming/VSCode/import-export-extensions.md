# Import/Export VSCode Extensions

You can export a list of your VSCode extensions to a text file, then loop that text file to install the extensions. This is how plugins like VSCode's "settings sync" work, but you can do it manually.

This is also useful for Docker containers like `openvscode-server`, where you can add a list of VSXi extensions to install from [[open-vsx.org](https://open-vsx.org)].

## Export VSCode extensions

### Linux

```bash title="Export VSCode extensions to text file" linenums="1"
code --list-extensions > vscode-extensions.list
```

### Windows

```powershell title="Export VSCode extensions to text file" linenums="1"
code --list-extensions > vscode-extensions.list
```

## Import VSCode extensions

### Linux

```bash title="Import VSCode extensions from text file" linenums="1"
cat  vscode-extensions.list | xargs -L 1 code --install-extension
```

### Windows

```powershell title="Import VSCode extensions from text file" linenums="1"
cat vscode-extensions.list |% { code --install-extension $_ }
```
