param([ValidateSet('doctor','verify','cnn','compare','alexnet','resnet18','resnet50','vit','energy')][string]$Task='cnn')
$ErrorActionPreference='Stop'
foreach ($name in @('PYTHONHOME','PYTHONPATH','PYTHONSTARTUP','PYTHONUSERBASE')) { Remove-Item -LiteralPath ('Env:' + $name) -ErrorAction SilentlyContinue }
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { Write-Error 'Run Setup.ps1 first.'; exit 1 }
& $python (Join-Path $PSScriptRoot 'scripts\lab.py') $Task
exit $LASTEXITCODE
