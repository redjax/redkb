---
title: "Import/Export Extensions"
date: 2024-10-29T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - util
  - vscode
  - ide
lastmod: "2026-04-13T04:15:27Z"
---

You can export a list of your VSCode extensions to a text file, then loop that text file to install the extensions. This is how plugins like VSCode's "settings sync" work, but you can do it manually.

This is also useful for Docker containers like `openvscode-server`, where you can add a list of VSXi extensions to install from [open-vsx.org](https://open-vsx.org).

## Export VSCode extensions

### Linux Export

```bash title="Export VSCode extensions to text file"
code --list-extensions > vscode-extensions.list
```

### Windows Export

```powershell title="Export VSCode extensions to text file"
code --list-extensions > vscode-extensions.list
```

## Import VSCode extensions

### Linux Import

```bash title="Import VSCode extensions from text file"
cat vscode-extensions.list | xargs -L 1 code --install-extension
```

### Windows Import

```powershell title="Import VSCode extensions from text file"
cat vscode-extensions.list |% { code --install-extension $_ }
```
