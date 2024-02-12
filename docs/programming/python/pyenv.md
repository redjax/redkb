# Use pyenv for easier Python version management

[`pyenv`](https://github.com/pyenv/pyenv) is a tool for managing versions of Python. It handles downloading the version archive, extracting & installing, and can isolate different versions of Python into their own individual environments.

`pyenv` can also handle running multiple versions of Python at the same time. For example, when using `nox`, you can declare a list of Python versions the session should run on, like `@nox.session(python=["3.11.2", "3.11.4", "3.12.1"], name="session-name")`. As long as one of the `pyenv` scopes (`shell`, `local`, or `global`) has all of these versions of Python, `nox` will run the session multiple times, once for each version declared in `python=[]`.

!!!TODO

  - [x] Briefly describe `pyenv`
  - [x] Write install instructions
      - [x] For Windows
      - [x] For Linux
  - [ ] Add notes about pitfalls I've run into & solutions
  - [ ] Document common commands
    - [ ] Update/refresh `pyenv`
    - [ ] Install a specific version of Python
    - [ ] Set Python version (single version & multiple)
        - [ ] Global
        - [ ] Local
        - [ ] Shell
    - [ ] Removing a version of Python

## pyenv scopes

`pyenv` has 3 "scopes":

- `shell`
    - Setting a version with `pyenv shell x.xx.xx` sets the Python interpreter for the current shell
    - When that shell is exited or refreshed (i.e. with `exec $SHELL` or `source ~/.bashrc`), this value is also reset
- `local`
    - Setting a version with `pyenv local x.xx.xx` creates a file called `.python-version` at the current path
    - `pyenv` uses this file to automatically set the version of Python while in this directory
- `global`
    - Setting a version with `pyenv global x.xx.xx` sets the default, global Python version
    - Any Python command (like `python -m pip install ...`) will use this `global` version, if no `local` or `shell` version is specified
    - `local` and `shell` override this value

Make sure to pay attention to your current `pyenv` version. If you are getting unexpected results when running Python scripts, check the version with `python3 --version`. This will help if you are expecting to be in a `3.11.4` shell, for example, but have set `pyenv local 3.12.1`.

## Install pyenv

Installing `pyenv` varies between OSes. On Windows, you use the `pyenv-win` package, for example. Below are installation instructions for Windows and Linux.

### Install pyenv in Linux/WSL

- Install dependencies (assumes Debian/Ubuntu)

```shell title="install pyenv dependencies" linenums="1"

sudo apt-get install -y \
	git \
  gcc \
  make \
  openssl \
  libssl-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  zlib1g-dev \
  libncursesw5-dev \
  libgdbm-dev \
  libc6-dev \
  zlib1g-dev \
  libsqlite3-dev \
  tk-dev \
  libssl-dev \
  openssl \
  libffi-dev
```

- Install `pyenv` with the convenience script

```shell title="install pyenv with convenience script" linenums="1"
curl https://pyenv.run | bash
```

- Add `pyenv` variables to your `~/.bashrc`

```text title="~/.bashrc" linenums="1"

...

## Pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

```

### Install pyenv in Windows

* Install `pyenv-win` with Powershell

```powershell title="install pyenv with Powershell convenience script" linenums="1"

Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

* Add the following variables to your `PATH`

```text title="pyenv Windows PATH variables" linenums="1"

%USERPROFILE%\\.pyenv\\pyenv-win\\bin
%USERPROFILE%\\.pyenv\\pyenv-win\\shims
```

* You can do this by opening the Control Panel > User Accounts and clicking "Change my environment variables":

<figure markdown="span">
  ![pyenv-win PATH](../../assets/img/pyenv/pyenv-win_set_path_vars.png)
  <figcaption>Set pyenv-win PATH variables on Windows</figcaption>
</figure>

<figure markdown="span">
  ![pyenv-win PATH pt 2](../../assets/img/pyenv/pyenv-win_set_path_vars2.png)
  <figcaption>Set pyenv-win PATH variables on Windows pt. 2</figcaption>
</figure>

* **NOTE**: Setting these env variables can also be accomplished with this Powershell script:

```powershell title="set pyenv-win PATH variables" linenums="1"

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string] $PythonVersion
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
Set-StrictMode -Version Latest

function _runCommand {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, Position = 0)]
        [string] $Command,
        [switch] $PassThru
    )

    try {
        if ( $PassThru ) {
            $res = Invoke-Expression $Command
        }
        else {
            Invoke-Expression $Command
        }

        if ( $LASTEXITCODE -ne 0 ) {
            $errorMessage = "'$Command' reported a non-zero status code [$LASTEXITCODE]."
            if ($PassThru) {
                $errorMessage += "`nOutput:`n$res"
            }
            throw $errorMessage
        }

        if ( $PassThru ) {
            return $res
        }
    }
    catch {
        $PSCmdlet.WriteError( $_ )
    }
}

function _addToUserPath {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, Position = 0)]
        [string] $AppName,
        [Parameter(Mandatory = $true, Position = 1)]
        [string[]] $PathsToAdd
    )

    $pathEntries = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User) -split ";"

    $pathUpdated = $false
    foreach ( $pathToAdd in $PathsToAdd ) {
        if ( $pathToAdd -NotIn $pathEntries ) {
            $pathEntries += $pathToAdd
            $pathUpdated = $true
        }
    }
    if ( $pathUpdated ) {
        Write-Host "$($AppName): Updating %PATH%..." -f Green
        # Remove any duplicate or blank entries
        $cleanPaths = $pathEntries | Select-Object -Unique | Where-Object { -Not [string]::IsNullOrEmpty($_) }

        # Update the user-scoped PATH environment variable
        [System.Environment]::SetEnvironmentVariable("PATH", ($cleanPaths -join ";").TrimEnd(";"), [System.EnvironmentVariableTarget]::User)
        
        # Reload PATH in the current session, so we don't need to restart the console
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User)
    }
    else {
        Write-Host "$($AppName): PATH already setup." -f Cyan
    }
}

# Install pyenv
if ( -Not ( Test-Path $HOME/.pyenv ) ) {
    if ( $IsWindows ) {
        Write-Host "pyenv: Installing for Windows..." -f Green
        & git clone https://github.com/pyenv-win/pyenv-win.git $HOME/.pyenv
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git reported a non-zero status code [$LASTEXITCODE] - check previous output."
        }
    }
    else {
        Write-Error "This script currently only supports Windows."
    }
}
else {
    Write-Host "pyenv: Already installed." -f Cyan
}

# Add pyenv to PATH
_addToUserPath "pyenv" @(
    "$HOME\.pyenv\pyenv-win\bin"
    "$HOME\.pyenv\pyenv-win\shims"
)

# Install default pyenv python version
$pyenvVersions = _runCommand "pyenv versions" -PassThru | Select-String $PythonVersion
if ( -Not ( $pyenvVersions ) ) {
    Write-Host "pyenv: Installing python version $PythonVersion..." -f Green
    _runCommand "pyenv install $PythonVersion"
}
else {
    Write-Host "pyenv: Python version $PythonVersion already installed." -f Cyan
}

# Set pyenv global version
$globalPythonVersion = _runCommand "pyenv global" -PassThru
if ( $globalPythonVersion -ne $PythonVersion ) {
    Write-Host "pyenv: Setting global python version: $PythonVersion" -f Green
    _runCommand "pyenv global $PythonVersion"
}
else {
    Write-Host "pyenv: Global python version already set: $globalPythonVersion" -f Cyan
}

# Update pip
_runCommand "python -m pip install --upgrade pip"

# Install pipx, pdm, black, cookiecutter
_runCommand "pip install pipx"
_runCommand "pip install pdm"
_runCommand "pip install black"
_runCommand "pip install cookiecutter"

```
