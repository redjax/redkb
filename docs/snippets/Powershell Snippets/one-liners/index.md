---
tags:
  - snippets
  - powershell
  - one-liners
---

# One-liners

Some Powershell commands can be written as a "one-liner."

## Start remote session & pipe commands

Create a session & assign it to a variable `$s`. Use that variable and `Invoke-Command` to run commands on the remote.

```powershell title="Start remote session, pipe commands" linenums="1"
## Create a session
$s = New-PSSession <computer-name>

## Run command(s) on the remove
Invoke-Command -Session $s { <command(s) to run> }

## Close the remote session
Remove-PSSession $s
```

## Copy file from remote to local

```powershell title="Copy file from remote to local" linenums="1"
# Create a session
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"

# Copy item from remote $session to local -Destination)
Copy-Item "C:\MyRemoteData\test.log" -Destination "D:\MyLocalData\" -FromSession $Session
```

## Pipe/tee Powershell command output to a file

```powershell title="Tee command output to file"
<your powershell command> | Tee-Object -FilePath <output-filename>.log
```

## Get machine uptime

On Linux, where everything is better and easier, you just run `uptime` to get a machine's uptime. On Windows, you have to do extra stuff because... Powershell...

```powershell title="Get machine uptime"
(Get-Date) – (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
```

## Generate a battery report

On laptops or devices with portable power, you can generate a battery report with the following command (find the report at the path you put after `/output`):

```powershell title="Generate battery report"
powercfg /batteryreport /output "C:\battery-report.html"
```

## Count files in a directory

```powershell title="Count number of files in a directory"
$FileCount = (Get-Childitem -Path "C:\path\to\parent" -File | Measure-Object).Count
```

## Recursively remove all files in a path

```powershell title="Recursively delete all files"
Remove-Item C:\path\to\parent\* -Recurse -Force
```

## Export Event Viewer log history

Use the command below to export all Event Viewer events from a specific logging section (`Application`, `Security`, `Setup`, or `System`):

```powershell title="Export Event Viewer logs"
Get-EventLog -LogName <Application|Security|Setup|System> | Export-Csv -Path C:\path\to\events_file.csv
```

## Enable/disable Windows Defender Real-Time Protection

### Enable real-time protection

```powershell title="Enable real-time protection"
PowerShell Set-MpPreference -DisableRealtimeMonitoring 0​
```

```powershell title="Enable real-time protection using boolean"
PowerShell Set-MpPreference -DisableRealtimeMonitoring $false​
```

### Disable real-time protection

```powershell title="Disable real-time protection"
PowerShell Set-MpPreference -DisableRealtimeMonitoring 1​
```

```powershell title="Disable real-time protection using boolean"
PowerShell Set-MpPreference -DisableRealtimeMonitoring $true
```

## Export list of AD users in a group

Substitute an AD Group name for `"$ADGroup"` and a path to export the CSV file to for `"$EXPORT_PATH"` (example: `c:\tmp\adgroup_members.csv`):

```powershell title="Get members of AD group"
Get-ADGroupMember -Identity "$ADGroup" | Export-CSV -Path $EXPORT_PATH -NoTypeInformation
```

## Export user's 'Members Of' to CSV

```powershell
Get-ADPrincipalGroupMembership USERNAME | Select Name | Export-CSV -path C:\Temp\file.csv -NoTypeInformation
```

## Query AD user by email address, get "Enabled" status

```powershell title="Get user's 'Enabled' status from email address"
Get-ADUser -Filter "EmailAddress -eq 'address@email.com'" -Properties EmailAddress | Select-Object Enabled
```

## Get AD user's properties

```powershell title="Get AD user's properties"
Get-ADUser -Identity <username> -Properties *
```

## Get subset of AD user's properties

```powershell title="Query specific properties of AD user's profile"
Get-ADUser -Identity <username> -Properties Name, AccountLockoutTime, LastBadPasswordAttempt, LastLogonDate, LockedOut, lockoutTime, Modified, modifyTimeStamp, PasswordExpired, PasswordLastSet
```

## Unlock AD user's account

```powershell title="Unlock AD user account"
Unlock-ADAccount -Identity $ADUsername
```

## Export/Import winget packages

You can export your installed packages using the `winget` utility. The backup format is `.json`.

### Export winget packages

```powershell title="Export winget packages"
winget export -o C:\path\to\winget-pkgs.json
```

### Import winget packages

```powershell title="Import winget packages"
winget import -i C:\path\to\winget-pkgs.json
```

## Format string parts with -NoNewline;

Using the `-NoNewline;` param, you can format different parts of a `Write-Host` string and break long lines into multiple.

For example to set the left part of a string to green and the right to red:

```powershell title="Format string colors"
Write-Host "I am green, " -ForegroundColor Green -NoNewline; Write-Host "and I am red!" -ForegroundColor Red

```

To apply formatting to some parts of a long string, and to break it up over multiple lines, you can use a new line after the `;` in `-NoNewline;`:

```powershell title="Multi-line Write-Host with -NoNewline" linenums="1"
Write-Host "This is the first part of a long string, with no formatting." -NoNewline;
Write-Host "This part of the string will appear inline (on the same line) as the previous string," -NoNewline;
Write-Host "and can even be broken up mid-sentence! Check the source code to see this in action." -NoNewline;
Write-Host "" -NoNewline;
Write-Host "And I'm purple, just because" -ForegroundColor purple -NoNewline;
Write-Host "Ok that's all."

```

## Set/Unset environment variables

!!! warning

    You must be in an elevated/administrative prompt for these commands.

### Set environment variable

```powershell title="Set Machine (system-wide) variable"
[System.Environment]::SetEnvironmentVariable("VARIABLE_NAME", "VALUE", [System.EnvironmentVariableTarget]::Machine)

```

You can also use it as a function:

```powershell title="Set-EnvVar function" linenums="1"
function Set-EnvVar {
    <#
        Set an environment variable. If -Target Machine or -Target User, the env variable will persist between sessions.

        Usage:
            Set-EnvVar -Name <name> -Value <value>
            Set-EnvVar -Name <name> -Value <value> -Target Machine
        
        Params:
            Name: The name of the environment variable
            Value: The value of the environment variable
            Target: The scope of the environment variable. Machine, User, or Process

        Example:
            Set-EnvVar -Name "EXAMPLE_VAR" -Value "example value"
            Write-Host $env:EXAMPLE_VAR
    #>
    param (
        [string]$Name,
        [string]$Value,
        [ValidateSet('Machine', 'User', 'Process')]
        [string]$Target = 'User'
    )

    Write-Host "Setting [$Target] environment variable "$Name"."

    If ( $Target -eq 'Process' ) {
        Write-Warning "Environment variable [$Target] will not persist between sessions."
    } else {
        Write-Information "Environment variable [$Target] will persist between sessions."
    }

    try{
        [System.Environment]::SetEnvironmentVariable($Name, $Value, [System.EnvironmentVariableTarget]::$Target)
    } catch {
        Write-Error "Unhandled exception setting environment variable. Details: $($_.Exception.Message)"
    }
}

```

### Unset environment variable

```powershell title="Set User env variable"
[System.Environment]::SetEnvironmentVariable("VARIABLE_NAME", "VALUE", [System.EnvironmentVariableTarget]::User)

```

You can use it as a function:

```powershell title="Remove-EnvVar function" linenums="1"
function Remove-EnvVar {
    <#
        Remove/unset an environment variable.

        Usage:
            Remove-EnvVar -Name <name>
            Remove-EnvVar -Name <name> -Target Machine

        Params:
            Name: The name of the environment variable
            Target: The scope of the environment variable. Machine, User, or Process

        Example:
            Remove-EnvVar -Name "EXAMPLE_VAR"
            Write-Host $env:EXAMPLE_VAR
    #>
    param (
        [string]$Name,
        [ValidateSet('Machine', 'User', 'Process')]
        [string]$Target = 'User'
    )
    
    try {
        [System.Environment]::SetEnvironmentVariable($Name, $null, [System.EnvironmentVariableTarget]::$Target)
    } catch {
        Write-Error "Unhandled exception removing environment variable. Details: $($_.Exception.Message)"
    }
}
```

## HTTP requests

### Check site availability

As a one-liner:

```powershell title="Check HTTP site availability" linenums="1"
$Site = "https://www.google.com"

while ($true) {
    try {
        ## Make HTTP HEAD request
        $response = Invoke-WebRequest -Uri "$($Site)" -Method Head

        ## Output HTTP status code
        Write-Output "$(Get-Date) Ping site '$($Site)': [$($response.StatusCode): $($response.StatusDescription)]"
    } catch {
        Write-Error "$(Get-Date): Request failed. Error: $($_.Exception.Message)"
    }

    ## Pause for $RequestSleep seconds
    Start-Sleep -Seconds 5
}
```

As a function:

```powershell title="Get-HTTPSiteAvailable" linenums="1"
function Get-HTTPSiteAvailable {
    Param(
        [string]$Site = "https://www.google.com",
        [string]$RequestSleep = 5
    )
    while ($true) {
        try {
            ## Make HTTP HEAD request
            $response = Invoke-WebRequest -Uri "$($Site)" -Method Head

            ## Output HTTP status code
            Write-Output "$(Get-Date) Ping site '$($Site)': [$($response.StatusCode): $($response.StatusDescription)]"
        } catch {
            Write-Error "$(Get-Date): Request failed. Error: $($_.Exception.Message)"
        }

        ## Pause for $RequestSleep seconds
        Start-Sleep -Seconds $RequestSleep
    }
}
```

## Disable Microsoft Copilot

```powershell title="Disable Copilot & prevent re-install" linenums="1"
Get-AppxProvisionedPackage -Online | where-object {$_.PackageName -like "*Copilot*"} | Remove-AppxProvisionedPackage -online
```

## Generate GUIDs (unique IDs)

```powershell title="Generate unique GUID" linenums="1"
[guid]::NewGuid()
```

You can also assign the GUID to a variable for re-use:

```powershell title="Generate unique GUID and assign to variable" linenums="1"
$UniqueID = [guid]::NewGuid()
```

## Turn monitor display off

```powershell title="Turn display off" linenums="1"
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -command "(Add-Type -MemberDefinition '[DllImport(\"user32.dll\")] public static extern int PostMessage(int a, int b, int c, int d);' -Name f -PassThru)::PostMessage(-1, 0x112, 0xF170, 2)"
```
