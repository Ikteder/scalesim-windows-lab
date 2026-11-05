#!/usr/bin/env bash
set -euo pipefail
grep -qi microsoft /proc/sys/kernel/osrelease || { echo 'This optional route requires WSL2 on Windows.'; exit 1; }
source_root=$(cd "$(dirname "$0")/.." && pwd)
if ! command -v git >/dev/null || ! command -v make >/dev/null || ! command -v g++ >/dev/null || ! python3 -c 'import venv,ensurepip' 2>/dev/null; then
  if [ "$(id -u)" -eq 0 ]; then prefix=(); else prefix=(sudo); fi
  "${prefix[@]}" apt-get update
  "${prefix[@]}" apt-get install -y git python3-venv python3-pip build-essential make
fi
target="$HOME/scalesim-energy-lab-$(date +%Y%m%d-%H%M%S)-$$"
mkdir "$target"
echo "Fresh WSL lab: $target"
tar -C "$source_root" --exclude=./.git --exclude=./.venv --exclude=./.energy-venv --exclude=./energy-tools --exclude=./logs --exclude=./runs -cf - . | tar -C "$target" -xf -
cd "$target"
mkdir -p logs
echo "Setup log: $target/logs/energy-setup.log"
bash energy/Setup-Energy.sh > logs/energy-setup.log 2>&1 || { tail -n 40 logs/energy-setup.log; exit 1; }
bash energy/Run-Energy.sh
