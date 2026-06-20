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
$ReleaseDir = Join-Path $RootDir "release"
$ZipPath = Join-Path $ReleaseDir "PuzzleProofStudio-v0.2.0-beta-windows.zip"

Set-Location $RootDir

New-Item -ItemType Directory -Force -Path "exports" | Out-Null
New-Item -ItemType Directory -Force -Path "build\pyinstaller" | Out-Null
New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

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
& $PythonExe -m py_compile "src\image_processor.py"

$addData = @(
    @("VERSION", "."),
    @("assets", "assets"),
    @("licenses\sample-license.json", "licenses"),
    @("docs", "docs"),
    @("catalog", "catalog")
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
    $source = Resolve-Path $item[0]
    $destination = $item[1]
    $pyinstallerArgs += @("--add-data", "$source;$destination")
}

$pyinstallerArgs += "src\main.py"

Write-Host "Building $ExePath..."
& $PythonExe -m PyInstaller @pyinstallerArgs

if (-not (Test-Path $ExePath)) {
    throw "Expected executable was not created: $ExePath"
}

Write-Host "Preparing customer-facing portable folder..."
$PortableDir = Join-Path $RootDir "dist\$AppName"
foreach ($file in @("README.txt", "FAQ.txt", "INSTALL.txt", "LICENSE_SETUP.txt")) {
    Copy-Item $file -Destination (Join-Path $PortableDir $file) -Force
}

foreach ($dir in @("exports", "jobs", "catalog", "licenses", "data\settings")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $PortableDir $dir) | Out-Null
}
Copy-Item "licenses\sample-license.json" -Destination (Join-Path $PortableDir "licenses\sample-license.json") -Force
if (-not (Test-Path (Join-Path $PortableDir "catalog\catalog.json"))) {
    Set-Content -Path (Join-Path $PortableDir "catalog\catalog.json") -Value "[]" -Encoding UTF8
}
Remove-Item (Join-Path $PortableDir "licenses\license.json") -Force -ErrorAction SilentlyContinue

if ($Zip) {
    if (Test-Path $ZipPath) {
        Remove-Item $ZipPath -Force
    }
    Compress-Archive -Path "dist\$AppName" -DestinationPath $ZipPath -Force

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
    try {
        $names = @($zip.Entries | ForEach-Object { $_.FullName })
    }
    finally {
        $zip.Dispose()
    }

    foreach ($required in @(
        "$AppName/$AppName.exe",
        "$AppName/README.txt",
        "$AppName/FAQ.txt",
        "$AppName/INSTALL.txt",
        "$AppName/LICENSE_SETUP.txt"
    )) {
        if ($names -notcontains $required) {
            throw "Customer package validation failed: missing $required"
        }
    }

    $blocked = $names | Where-Object {
        $_ -match "(^|/)src/" -or
        $_ -match "(^|/)requirements\.txt$" -or
        $_ -match "(^|/)scripts/" -or
        $_ -match "(^|/)license\.json$"
    }
    if ($blocked) {
        throw "Customer package validation failed. Blocked files found:`n$($blocked -join "`n")"
    }

    Write-Host "Created portable package: $ZipPath"
}

Write-Host "Build complete: $ExePath"
