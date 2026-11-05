#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
source "$root/.energy-venv/bin/activate"
cd "$root/vendor/scale-sim-v3/rundir-accelergy"
tag=$(date +%Y%m%d-%H%M%S)-$$
output="$root/runs/accelergy-$tag"
mkdir -p "$root/logs"
bash "$root/energy/run_energy.sh" ../configs/scale.cfg "$root/examples/cnn.csv" "$root/runs/scratch-$tag" "$output" gemm > "$root/logs/accelergy-$tag.log" 2>&1
python "$root/energy/summarize_energy.py" "$output/accelergy_output_scale_example_run_32x32_ws/energy_estimation.yaml" --compute "$output/scale_sim_output_scale_example_run_32x32_ws/COMPUTE_REPORT.csv"
echo "Energy reports: $output"
