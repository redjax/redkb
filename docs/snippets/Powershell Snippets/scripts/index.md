---
tags:
  - snippets
  - powershell
  - one-liners
---

# Scripts

Some of the scripts on this page are full scripts to accomplish a task, others are snippets you can copy/paste into scripts you're building.

## Self-elevate a Powershell script

```powershell title="Self-elevate Powershell script" linenums="1"
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {

    if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {

     $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments

     Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine

     Exit

    }

}
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
