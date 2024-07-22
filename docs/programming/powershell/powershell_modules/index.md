# Powershell Modules

> A module is a self-contained reusable unit that can contain cmdlets, providers, functions, variables, and other types of resources that can be imported as a single unit.
> 
> \- [Microsoft Docs: about Modules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_modules?view=powershell-7.4)

Powershell modules are a way to combine multiple different scripts that are logically "grouped" into a single, importable module. For example, the [`Az` Powershell module](https://www.powershellgallery.com/packages/Az/12.1.0) contains scripts and functions all related to interacting with an Azure environment.

!!! TODO

    - [ ] Document initializing a Powershell module
        - [ ] Manually, using the `New-PSModuleManifest` function
        - [ ] Automated, using the `Add-NewPSModule` script
    - [ ] Document loading functions from scripts/internal modules
        - [ ] Manually, by declaring functions in the `.psd1` module manifest
        - [ ] Automatically using an init script in the `.psm1` module entrypoint
    - [ ] Document `Private` and `Public` functions
        - [ ] "Private" for internal module usage
        - [ ] "Public" for functions/code exposed to the user
    - [ ] Document passing parameters to scripts within the module

## Creating a new Powershell module

### The "manual" way

Initialize a new Powershell module using the `New-ModuleManifest` cmdlet. Create a `$manifest` hashtable to pass params to the `New-ModuleManifest` script:

```powershell title="Manually create a new Powershell module" linenums="1"
$manifest = @{
  Path = ".\GetInfo\GetInfo.psd1"
  RootModule = "GetInfo.psm1"
  Author = "Jack Kenyon"
}

## Call New-ModuleManifest, passing the $manifest var defined above.
New-ModuleManifest @manifest
```

You can also pass these params using `-Params`, like:

```powershell title="New-ModuleManifest with params" linenums="1"
New-ModuleManifest -Path .\ModuleName\module.psd1 -ModuleVersion "2.0" -Author "Your name" -Description "Description for the module"
```

As you add scripts to your module, import them by editing the `module.psd1` manifest file within the folder that is created by the `New-ModuleManifest` command, adding functions to expose to the user to the `FunctionsToExport = @()` array.

Optionally, you can also export the functions from within the Powershell script by adding `Export-ModuleMember <function-name>` to the bottom of your `.ps1` scripts within the module.

### The "automatic" way

Creating a Powershell module by hand involves a lot of manual setup, and many steps must be taken each time you modify the code in the module.

To avoid mistakes and simplify setup/execution of your module, you can use a script to aid in creating the module. I name this script `Add-NewPSModule.ps1`, but you can call it whatever you like:

```powershell title="Add-NewPSModule.ps1 script" linenums="1"

```
