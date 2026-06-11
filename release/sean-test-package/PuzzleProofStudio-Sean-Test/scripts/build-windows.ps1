param(
    [switch]$SkipInstall,
    [switch]$Zip
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Resolve-Path (Join-Path $ScriptDir "..")
$VenvDir = Join-Path $RootDir ".venv-build-windows"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"
$AppName = "PuzzleProofStudio"
$ExePath = Join-Path $RootDir "dist\$AppName\$AppName.exe"

Set-Location $RootDir

New-Item -ItemType Directory -Force -Path "exports" | Out-Null
New-Item -ItemType Directory -Force -Path "build\pyinstaller" | Out-Null

if (-not (Test-Path $PythonExe)) {
    Write-Host "Creating Windows build virtual environment..."
    try {
        py -3.12 -m venv $VenvDir
    }
    catch {
        py -3.11 -m venv $VenvDir
    }
}

if (-not $SkipInstall) {
    Write-Host "Installing runtime and packaging dependencies..."
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install -r requirements.txt
    & $PythonExe -m pip install pyinstaller
}

Write-Host "Checking Python syntax..."
& $PythonExe -m py_compile "src\main.py"

$addData = @(
    "VERSION;.",
    "assets;assets",
    "licenses\sample-license.json;licenses",
    "docs;docs",
    "catalog;catalog",
    "exports;exports"
)

$pyinstallerArgs = @(
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", $AppName,
    "--distpath", "dist",
    "--workpath", "build\pyinstaller",
    "--specpath", "build\pyinstaller"
)

$IconPath = "assets\icons\puzzleproof-icon.ico"
if (Test-Path $IconPath) {
    $pyinstallerArgs += @("--icon", $IconPath)
}
else {
    Write-Warning "Windows .ico file not found at $IconPath. Building without a Windows icon."
}

foreach ($item in $addData) {
    $pyinstallerArgs += @("--add-data", $item)
}

$pyinstallerArgs += "src\main.py"

Write-Host "Building $ExePath..."
& $PythonExe -m PyInstaller @pyinstallerArgs

if (-not (Test-Path $ExePath)) {
    throw "Expected executable was not created: $ExePath"
}

if ($Zip) {
    $Version = (Get-Content "VERSION" -Raw).Trim()
    if (-not $Version) {
        $Version = "0.1.0-EarlyAccess"
    }
    $ZipPath = Join-Path $RootDir "dist\PuzzleProofStudio-$Version-windows-portable.zip"
    if (Test-Path $ZipPath) {
        Remove-Item $ZipPath -Force
    }
    Compress-Archive -Path "dist\$AppName" -DestinationPath $ZipPath -Force
    Write-Host "Created portable package: $ZipPath"
}

Write-Host "Build complete: $ExePath"
