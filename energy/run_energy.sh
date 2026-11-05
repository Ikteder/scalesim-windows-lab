#!/usr/bin/env bash
# Run from scale-sim-v3/rundir-accelergy with the Linux venv active.
set -euo pipefail
if [ "$#" -ne 5 ]; then
  echo 'Usage: bash run_energy.sh CONFIG TOPOLOGY SCRATCH OUTPUT conv|gemm' >&2
  exit 2
fi
config=$(realpath "$1")
topology=$(realpath "$2")
mkdir -p "$3" "$4"
scratch=$(realpath "$3")
output=$(realpath "$4")
kind=$5
[[ "$kind" == conv || "$kind" == gemm ]]
[[ "$config$scratch$topology$output" != *' '* ]] || { echo 'Use paths without spaces'; exit 2; }
run=$(python -c 'import configparser,sys; c=configparser.ConfigParser(); c.read(sys.argv[1]); print(c["general"]["run_name"])' "$config")
[[ ! -e "$scratch/$run" && ! -e "$output/scale_sim_output_$run" && ! -e "$output/accelergy_output_$run" && ! -e "accelergy_output/$run" ]] || { echo 'Run already exists; choose fresh scratch/output paths or run_name'; exit 2; }
python preprocess.py -c "$config" -t "$topology" -p "$scratch" -o "$output"
(cd ..; python scale.py -c "$config" -t "$topology" -p "$scratch" -i "$kind" -s Y)
bash -e create_action_count.sh
python "$(dirname "${BASH_SOURCE[0]}")/prepare_energy_counts.py" accelergy_input/action_count.yaml --backup "$output/scale_sim_output_$run/action_count.legacy.yaml"
cp accelergy_input/action_count.yaml "$output/scale_sim_output_$run/action_count.dynamic.yaml"
accelergy accelergy_input/architecture.yaml accelergy_input/action_count.yaml accelergy_input/components/*.yaml -o "$output/accelergy_output_$run" -v 1
test -s "$output/scale_sim_output_$run/COMPUTE_REPORT.csv"
test -s "$output/accelergy_output_$run/energy_estimation.yaml"
echo "Completed $run with idle and leakage actions excluded"
