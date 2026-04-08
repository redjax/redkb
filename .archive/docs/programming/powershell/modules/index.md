# Powershell Modules

> A module is a self-contained reusable unit that can contain cmdlets, providers, functions, variables, and other types of resources that can be imported as a single unit.
> 
> \- [Microsoft Docs: about Modules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_modules?view=powershell-7.4)

Powershell modules are a way to combine multiple different scripts that are logically "grouped" into a single, importable module. For example, the [`Az` Powershell module](https://www.powershellgallery.com/packages/Az/12.1.0) contains scripts and functions all related to interacting with an Azure environment.

!!! TODO

    - [x] Document initializing a Powershell module
        - [x] Manually, using the `New-PSModuleManifest` function
        - [x] Automated, using the `Add-NewPSModule` script
    - [x] Document loading functions from scripts/internal modules
        - [x] Manually, by declaring functions in the `.psd1` module manifest
        - [x] Automatically using an init script in the `.psm1` module entrypoint
    - [x] Document `Private` and `Public` functions
        - [x] "Private" for internal module usage
        - [x] "Public" for functions/code exposed to the user
    - [ ] Document passing parameters to scripts within the module

## Creating a new Powershell module

### The manual way

Initialize a new Powershell module using the `New-ModuleManifest` cmdlet. Create a `$manifest` hashtable to pass params to the `New-ModuleManifest` script:

```powershell title="Manually create a new Powershell module" linenums="1"
$manifest = @{
  Path = ".\ModuleName\ModuleName.psd1"
  RootModule = "ModuleName.psm1"
  Author = "Your Name"
}

## Call New-ModuleManifest, passing the $manifest var defined above.
New-ModuleManifest @manifest
```

You can also pass these params using `-Params`, like:

```powershell title="New-ModuleManifest with params"
New-ModuleManifest -Path .\ModuleName\module.psd1 -ModuleVersion "2.0" -Author "Your Name" -Description "Description for the module"
```

As you add scripts to your module, import them by editing the `module.psd1` manifest file within the folder that is created by the `New-ModuleManifest` command, adding functions to expose to the user to the `FunctionsToExport = @()` array.

Optionally, you can also export the functions from within the Powershell script by adding `Export-ModuleMember <function-name>` to the bottom of your `.ps1` scripts within the module.

### The automatic way

Creating a Powershell module by hand involves a lot of manual setup, and many steps must be taken each time you modify the code in the module.

To avoid mistakes and simplify setup/execution of your module, you can use a script to aid in creating the module. I name this script `Add-NewPSModule.ps1`, but you can call it whatever you like:

!!! warning

    When using the automated "init script" in a `.psm1` module (shown below), you must be deliberate where you put your code. Anything in the `Public/` directory is exposed to the user of your module; if you have code you want to be able to use within your module, or templates like a `.json` or `.csv` file, it should be placed in the `Private/` directory and referenced in scripts in the `Public/` directory.

```powershell title="Add-NewPSModule.ps1 script" linenums="1"
## Set directory separator character, i.e. '\' on Windows
$DirectorySeparator = [System.IO.Path]::DirectorySeparatorChar
## Set name of module from $PSScriptRoot
$ModuleName = $PSScriptRoot.Split($DirectorySeparator)[-1]
## Look for module manifest file
$ModuleManifest = $PSScriptRoot + $DirectorySeparator + $ModuleName + '.psd1'
## Loop Public/ directory and load all .ps1 files into var
$PublicFunctionsPath = $PSScriptRoot + $DirectorySeparator + 'Public' + $DirectorySeparator + 'ps1'
## Loop Private/ directory and load all .ps1 files into var
$PrivateFunctionsPath = $PSScriptRoot + $DirectorySeparator + 'Private' + $DirectorySeparator + 'ps1'

## Test the module manifest
$CurrentManifest = Test-ModuleManifest $ModuleManifest

$Aliases = @()

## Get list of .ps1 files in Public/ recursively
$PublicFunctions = Get-ChildItem -Path $PublicFunctionsPath -Recurse -Filter *.ps1
## Get list of .ps1 files in Private/ recursively
$PrivateFunctions = Get-ChildItem -Path $PrivateFunctionsPath -Recurse -Filter *.ps1

## Load all Powershell functions from script files
$PrivateFunctions | ForEach-Object { 
    Write-Verbose "Loading private function from: $($_.FullName)"
    . $_.FullName 
}  # Load private functions first

$PublicFunctions | ForEach-Object { 
    Write-Verbose "Loading public function from: $($_.FullName)"
    . $_.FullName 
}   # Load public functions after

## Export all public functions
$PublicFunctionNames = $PublicFunctions | ForEach-Object { $_.BaseName }
Export-ModuleMember -Function $PublicFunctionNames

## Handle aliases if needed
$PublicFunctions | ForEach-Object {
    $alias = Get-Alias -Definition $_.BaseName -ErrorAction SilentlyContinue
    if ($alias) {
        $Aliases += $alias
        ## Export aliased function, if one is defined
        Export-ModuleMember -Alias $alias
    }
}

## Add all functions loaded from $PublicFunctions to an array
$FunctionsAdded = $PublicFunctions | Where-Object { $_.BaseName -notin $CurrentManifest.ExportedFunctions.Keys }
## Remove any undetected functions from module manifest
$FunctionsRemoved = $CurrentManifest.ExportedFunctions.Keys | Where-Object { $_ -notin $PublicFunctions.BaseName }

$AliasesAdded = $Aliases | Where-Object { $_ -notin $CurrentManifest.ExportedAliases.Keys }
$AliasesRemoved = $CurrentManifest.ExportedAliases.Keys | Where-Object { $_ -notin $Aliases }

if ($FunctionsAdded -or $FunctionsRemoved -or $AliasesAdded -or $AliasesRemoved) {
    try {
        ## Update module manifest when changes are detected
        $UpdateModuleManifestParams = @{}
        $UpdateModuleManifestParams.Add('Path', $ModuleManifest)
        $UpdateModuleManifestParams.Add('ErrorAction', 'Stop')
        if ($Aliases.Count -gt 0) { $UpdateModuleManifestParams.Add('AliasesToExport', $Aliases) }
        if ($PublicFunctionNames.Count -gt 0) { $UpdateModuleManifestParams.Add('FunctionsToExport', $PublicFunctionNames) }

        Update-ModuleManifest @updateModuleManifestParams
    }
    catch {
        $_ | Write-Error
    }
}

```

When your script is imported with `Import-Module`, the `.psm1` script at the root of the module is sourced, executing the code within. In this case, that code is iterating over the `Public/` and `Private/` directories and sourcing `.ps1` Powershell scripts.
