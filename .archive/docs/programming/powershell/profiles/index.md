---
tags:
    - windows
    - powershell
    - configuration
---

# Powershell Profiles

!!! TODO

    - [ ] Link to helpful articles about setting up profiles
    - [ ] Document helpful snippets
        - [ ] Automatic transcription (logging)
    - [ ] Demo example full Powershell profile

A Powershell profile is a `.ps1` file, which does not exist by default but is expected at `C:\Users\<username>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`, is a file that is "sourced"/loaded each time a Powershell session is opened. You can use a profile to customize your Powershell session. Functions declared in your profile are accessible to your whole session. You can set variables with default values, customize your session's colors (by editing a `function Prompt {}` section), split behavior between regular/elevated prompts, and more.

## Profile Snippets

### Useful Params

At the top of your Powershell script, below your docstring, you can declare `param()` to enable passing `-Args` to your script, our [`switches`](#how-to-switches).

```powershell title="Example params()" linenums="1"
<#
    Description: Example script with params

    Usage:
        ...
#>

param(
    ## Enable transcription, like ~/.bashhistory
    [bool]$Transcript = $True,
    [bool]$ClearNewSession = $True
)
```

## How-tos

### How to: switches

### How to: try/catch

### How to: case statements
