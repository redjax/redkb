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

```powershell title="Copy file from remote to local" title="1"
# Create a session
$Session = New-PSSession -ComputerName "Server01" -Credential "Contoso\User01"

# Copy item from remote $session to local -Destination)
Copy-Item "C:\MyRemoteData\test.log" -Destination "D:\MyLocalData\" -FromSession $Session
```

## Pipe/tee Powershell command output to a file

```powershell title="Tee command output to file" linenums="1"
<your powershell command> | Tee-Object -FilePath <output-filename>.log
```

## Get machine uptime

On Linux, where everything is better and easier, you just run `uptime` to get a machine's uptime. On Windows, you have to do extra stuff because... Powershell...

```powershell title="Get machine uptime" linenums="1"
(Get-Date) – (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
```

## Generate a battery report

On laptops or devices with portable power, you can generate a battery report with the following command (find the report at the path you put after `/output`):

```powershell title="Generate battery report" linenums="1"
powercfg /batteryreport /output "C:\battery-report.html"
```

## Count files in a directory

```powershell title="Count number of files in a directory" linenums="1"
$FileCount = (Get-Childitem -Path "C:\path\to\parent" -File | Measure-Object).Count
```

## Recursively remove all files in a path

```powershell title="Recursively delete all files" linenums="1"
Remove-Item C:\path\to\parent\* -Recurse -Force
```

## Export Event Viewer log history

Use the command below to export all Event Viewer events from a specific logging section (`Application`, `Security`, `Setup`, or `System`):

```powershell title="Export Event Viewer logs" linenums="1"
Get-EventLog -LogName <Application|Security|Setup|System> | Export-Csv -Path C:\path\to\events_file.csv
```

## Enable/disable Windows Defender Real-Time Protection

### Enable real-time protection

```powershell title="Enable real-time protection" linenums="1"
PowerShell Set-MpPreference -DisableRealtimeMonitoring 0​
```

```powershell title="Enable real-time protection using boolean" linenums="1"
PowerShell Set-MpPreference -DisableRealtimeMonitoring $false​
```

### Disable real-time protection

```powershell title="Disable real-time protection" linenums="1"
PowerShell Set-MpPreference -DisableRealtimeMonitoring 1​
```

```powershell title="Disable real-time protection using boolean" linenums="1"
PowerShell Set-MpPreference -DisableRealtimeMonitoring $true
```

## Export list of AD users in a group

Substitute an AD Group name for `"$ADGroup"` and a path to export the CSV file to for `"$EXPORT_PATH"` (example: `c:\tmp\adgroup_members.csv`):

```powershell title="Get members of AD group" linenums="1"
Get-ADGroupMember -Identity "$ADGroup" | Export-CSV -Path $EXPORT_PATH -NoTypeInformation
```

## Export user's 'Members Of' to CSV

```powershell
Get-ADPrincipalGroupMembership USERNAME | Select Name | Export-CSV -path C:\Temp\file.csv -NoTypeInformation
```

## Query AD user by email address, get "Enabled" status

```powershell title="Get user's 'Enabled' status from email address" linenums="1"
Get-ADUser -Filter "EmailAddress -eq 'address@email.com'" -Properties EmailAddress | Select-Object Enabled
```

## Get AD user's properties

```powershell title="Get AD user's properties" linenums="1"
Get-ADUser -Identity <username> -Properties *
```

## Get subset of AD user's properties

```powershell title="Query specific properties of AD user's profile" linenums="1"
Get-ADUser -Identity <username> -Properties Name, AccountLockoutTime, LastBadPasswordAttempt, LastLogonDate, LockedOut, lockoutTime, Modified, modifyTimeStamp, PasswordExpired, PasswordLastSet
```

## Unlock AD user's account

```powershell title="Unlock AD user account" linenums="1"
Unlock-ADAccount -Identity $ADUsername
```
