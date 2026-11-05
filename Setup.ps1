param([string]$PythonExe)
$ErrorActionPreference = 'Stop'
# Ignore inherited Python paths in this process only.
foreach ($name in @('PYTHONHOME','PYTHONPATH','PYTHONSTARTUP','PYTHONUSERBASE')) { Remove-Item -LiteralPath ('Env:' + $name) -ErrorAction SilentlyContinue }
try {
  if ($env:OS -ne 'Windows_NT') { throw 'Use Windows PowerShell for this setup.' }
  Set-Location -LiteralPath $PSScriptRoot
  New-Item -ItemType Directory -Force (Join-Path $PSScriptRoot 'logs') | Out-Null
  if ($PythonExe) { $candidate = $PythonExe }
  else {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Python launcher missing. Install 64-bit Python 3.12 (include the launcher), reopen PowerShell, and run setup again. Or pass -PythonExe with its full python.exe path. See README.' }
    $candidate = & py -3.12 -c 'import sys; print(sys.executable)'
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 is missing. Follow the Python installation section in README.' }
  }
  & $candidate (Join-Path $PSScriptRoot 'scripts\preflight.py')
  if ($LASTEXITCODE -ne 0) { throw 'Python version/architecture check failed.' }
  $venv = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
  if (-not (Test-Path -LiteralPath $venv)) {
    & $candidate -m venv (Join-Path $PSScriptRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the virtual environment.' }
  }
  & $venv (Join-Path $PSScriptRoot 'scripts\preflight.py')
  if ($LASTEXITCODE -ne 0) { throw 'Existing environment is incompatible; use a fresh extracted folder.' }
  & $venv -m pip install --disable-pip-version-check --only-binary=:all: -r (Join-Path $PSScriptRoot 'requirements.txt')
  if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check internet/proxy access to PyPI. Compiler builds are intentionally disabled.' }
  & $venv -m pip install --disable-pip-version-check --no-deps --no-build-isolation -e (Join-Path $PSScriptRoot 'vendor\scale-sim-v3')
  if ($LASTEXITCODE -ne 0) { throw 'Bundled SCALE-Sim installation failed.' }
  & $venv (Join-Path $PSScriptRoot 'scripts\lab.py') doctor
  if ($LASTEXITCODE -ne 0) { throw 'Environment checks failed.' }
  & $venv (Join-Path $PSScriptRoot 'scripts\lab.py') verify
  if ($LASTEXITCODE -ne 0) { throw 'Simulation acceptance tests failed. Inspect logs.' }
  Write-Host 'SETUP PASSED. You can now run Run-Lab.ps1. Logs and results are inside this folder.'
} catch { Write-Error $_; exit 1 }
