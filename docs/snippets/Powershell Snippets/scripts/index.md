---
tags:
  - snippets
  - powershell
  - one-liners
---

# Scripts

Some of the scripts on this page are full scripts to accomplish a task, others are snippets you can copy/paste into scripts you're building.

## Self-elevate a Powershell script

The following code will re-launch a Powershell session as an Administrator, using the same Powershell version as the non-elevated session that called it.

```powershell title="Self-elevate Powershell script" linenums="1"
## Determine which shell is running (PowerShell 7+ or Windows PowerShell)
$shellPath = if ($PSVersionTable.PSEdition -eq 'Core') {
    ## PowerShell 7+, use current process path (e.g., pwsh.exe)
    (Get-Process -Id $PID).Path
}
else {
    ## Windows PowerShell 5.1
    "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe"
}

## Relaunch with elevation if not already running as admin
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)) {
    
    Write-Warning "Relaunching as Administrator"
    Start-Process -FilePath $shellPath `
        -ArgumentList "-NoProfile", "-ExecutionPolicy Bypass", "-File `"$PSCommandPath`"" `
        -Verb RunAs
    exit
}

## Rest of your code here
```

Alternatively, you can add `#Requires -RunAsAdministrator` to the top of your script (before any `<# documentation #>` or `[CmdletBinding()]`/`Param()`). Check the [Microsoft `Requires` documentation for more of these special comment lines](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_requires).

```powershell title="Requires Administrator comment" linenums="0"
#Requires -RunAsAdministrator

## Rest of your code here

```

## Enable Powershell debugging

For each function you declare in your script where you have `Write-Debug` messages, add a `[CmdletBinding()]` before your `Param()` section:

```powershell
function Get-Something {
	[CmdletBinding()]
	Param()
}
```

Then, call the script with `-Debug`. This works for `-Verbose` and `Write-Verbose`, too.
