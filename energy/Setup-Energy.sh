#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
case "$root" in /mnt/*) echo 'Copy the full lab into your Ubuntu home first; see energy/README.md'; exit 1;; esac
command -v python3 >/dev/null
python3 -c 'import sys; assert sys.version_info[:2]==(3,12), "Ubuntu 24.04 / Python 3.12 required"'
cd "$root"
test -d .energy-venv || python3 -m venv .energy-venv
source .energy-venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e vendor/scale-sim-v3
mkdir -p energy-tools
cd energy-tools
for spec in 'accelergy 6911d15686ee7efdceba7d95605102df4472ae3a' 'accelergy-aladdin-plug-in 5e2e1263ddcc896ba3b8ce95954d76cdeebe03ab' 'accelergy-library-plug-in ba4e9dac1b2e7a3076fb8b7816a5228211623055' 'accelergy-cacti-plug-in 7649b2c02a389f3c3d585d7ff4ececacfb01e6ea'; do
  read -r name revision <<< "$spec"
  test -d "$name/.git" || git clone "https://github.com/Accelergy-Project/$name.git" "$name"
  git -C "$name" checkout "$revision"
  # Accelergy's test-only submodule uses SSH and is not needed by students.
  if [ "$name" != accelergy ]; then
    git -c url.https://github.com/.insteadOf=git@github.com: -C "$name" submodule update --init --recursive
  fi
done
python -m pip install ./accelergy pyyaml ./accelergy-aladdin-plug-in ./accelergy-library-plug-in
(cd accelergy-cacti-plug-in; make -B build; test -x cacti/cacti; python -m pip install .)
cd "$root/vendor/scale-sim-v3"
python "$root/energy/patch_energy.py"
python -m pip check
echo 'ENERGY SETUP PASSED. Run bash energy/Run-Energy.sh from the lab root.'
