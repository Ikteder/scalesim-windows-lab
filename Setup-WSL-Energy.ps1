param([string]$Distribution='Ubuntu-24.04')
$ErrorActionPreference='Stop'
try {
  if ($env:OS -ne 'Windows_NT') { throw 'This launcher is for Windows only.' }
  if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) { throw 'Install WSL2 and Ubuntu 24.04 first; see energy/README.md.' }
  $linuxPath = & wsl.exe -d $Distribution --exec wslpath -u $PSScriptRoot
  if ($LASTEXITCODE -ne 0) { throw 'Open Ubuntu 24.04 once, finish account setup, then retry. See energy/README.md.' }
  & wsl.exe -d $Distribution --exec bash "$linuxPath/energy/Bootstrap-WSL.sh"
  if ($LASTEXITCODE -ne 0) { throw 'WSL energy setup/run failed. Read the preceding error and printed log path.' }
} catch { Write-Error $_; exit 1 }
