# Optional Accelergy and CACTI for Windows students

This option runs Ubuntu **inside WSL2 on Windows**, not on a separate Linux computer. The basic native Windows lab does not require it.

1. In PowerShell, check installed distributions:
```powershell
wsl --list --verbose
```
2. If Ubuntu-24.04 is absent, install it (administrator access/restart may be required):
```powershell
wsl --install -d Ubuntu-24.04
```
3. Open it once and complete any username/password setup:
```powershell
wsl -d Ubuntu-24.04
```
Type `exit` to return to PowerShell. If that distribution already exists, skip installing it again. WSL2 is required; complete Windows' WSL setup if Windows reports virtualization is unavailable.

4. In the **same extracted repository folder** used for the native lab, run:
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Setup-WSL-Energy.ps1
```

The Windows launcher discovers the repository's real path automatically. **Do not substitute a username, rename a folder or edit a path.** It works with spaces in the Windows path. The WSL bootstrap checks for Git, Python venv support, Make and a C++ compiler and installs missing prerequisites through apt (sudo may request your Linux password). It creates a fresh Linux workspace, copies the bundled lab there while excluding Windows environments/results, installs pinned tools in its own `.energy-venv`, builds CACTI, applies checked repairs and runs the CNN energy example.

The setup prints the exact workspace and log path. Every launch uses a new workspace so it cannot reuse an old broken environment. Internet access is required. No existing Linux user files or global Accelergy configuration are overwritten; a project-local estimator configuration selects the new environment's installed plug-ins.

For another run after setup, open Ubuntu and `cd` to the exact workspace printed by the launcher, then run `bash energy/Run-Energy.sh`. Each run gets a new result folder. Prefer the launcher for a complete fresh start. Failure at any stage stops the process and prints an error/log location.

## Interpretation
Output uses the legacy 40 nm/8-bit MAC technology model. Explicit idle/leakage actions are excluded because upstream idle counts can be negative. The MAC-per-array-slot rule and fixed reuse assumptions remain; this is not calibrated total-chip power. Reports are under `runs/`, logs under `logs/`. The native Windows estimate is a separate, explicitly illustrative calculation, not this Accelergy estimate.
