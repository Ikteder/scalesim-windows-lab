# Optional Accelergy and CACTI on Windows through WSL2
This is a separate optional path. Native Windows commands in the main README need no WSL.
In administrator PowerShell if required:
```powershell
wsl --install -d Ubuntu-24.04
```
Restart if requested; open Ubuntu 24.04 and finish account setup. In **Ubuntu Bash**:
```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip build-essential make
```
Copy the complete extracted lab from Windows Downloads to your Linux home. Find your Windows user folder with `ls /mnt/c/Users`. Replace YOUR_WINDOWS_USERNAME below with the actual folder name. If your lab is elsewhere, use that actual source path. These are copy commands, not another download:
```bash
cp -r "/mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/scalesim-windows-lab" "$HOME/scalesim-energy-lab"
cd "$HOME/scalesim-energy-lab"
bash energy/Setup-Energy.sh
bash energy/Run-Energy.sh
```
Use a destination without spaces. Setup downloads pinned Accelergy tool sources and packages, builds CACTI and applies two checked energy-specific repairs. All helper scripts are inside this repository. No global Python installation is changed. The Linux `.energy-venv` is independent of Windows `.venv`; never activate the Windows environment in Ubuntu.

If a per-user Accelergy config from an older environment hides plug-ins, inspect `~/.config/accelergy/accelergy_config.yaml` and its estimator paths. Keep any existing customized configuration backed up before changing it.

Output is a technology-model estimate using the legacy 40 nm/8-bit MAC description. Explicit idle/leakage actions are excluded because upstream idle counts can be negative. The MAC-per-array-slot rule and fixed reuse assumptions remain. This is not calibrated total-chip power. Every run uses new paths; failures stop the script. Logs are in `logs/` and data in `runs/`.
