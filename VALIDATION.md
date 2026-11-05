# Validation on 5 November 2026

## Native Windows

Tested Windows 11 x64 with Windows PowerShell 5.1 and CPython 3.12.6 x64. Installed exact pinned package versions in fresh virtual environments.

* Extracted the complete package into a real Downloads folder named `SCALE Sim Student Test`, including spaces. Setup and all acceptance checks passed.
* Repeated setup successfully, including editable installation through the included build metadata.
* Published the repository, downloaded GitHub's actual main-branch ZIP into another Downloads folder named `SCALE Sim GitHub ZIP Test`, extracted it and completed setup there successfully.
* Executed README tasks doctor, cnn, compare and native energy from that downloaded copy.
* Checked three complete rows per CNN report and exact summed cycles: 16119, 24229, 65053 for 32/16/8.
* Verified saved traces on/off produce identical four summary reports, with 18 trace files for the three-layer Y run and none for N.
* The native illustrative calculation produced 37.00894912 microjoules with the documented assumed coefficients. This is an arithmetic example, not measured total-chip power.
* Python 3.14 was deliberately selected and rejected before package installation. Source-integrity checks reject a changed bundled configuration.
* GitHub-hosted Windows setup/acceptance completed successfully: [initial workflow run](https://github.com/Ikteder/scalesim-windows-lab/actions/runs/42105758950). The Actions tab shows checks on later commits.

The source revision and simulator repairs also have earlier full-workload validation: bundled AlexNet (5 rows), ResNet-18 (21), ResNet-50 (54), ViT (5), and AlexNet 16/8 array runs completed. These larger unchanged simulator cases were not all repeated during this repository packaging test. They remain optional longer exercises rather than setup requirements.

## Windows through Ubuntu WSL2

Used a separate fresh `.energy-venv`, downloaded the pinned external tool sources, installed all three plug-ins and built CACTI. Existing Ubuntu 24.04 and compiler packages were available; Windows virtualization installation itself was not repeated.

The repository's energy setup completed, and its runner executed the included three-row GEMM workload and generated compute, ERT, ART and component-energy reports. Total Cycles were 16119; modeled energy divided by that interval at 1 GHz was about 17.075532 W, with the explicit non-idle model described in the energy README. This is not total device power.

## Issues corrected during packaging

* Replaced fragile inline Python quoting in PowerShell 5.1 with an included preflight script.
* Excluded Accelergy's unnecessary test-only SSH submodule; plug-in submodules use HTTPS.
* Made source-patch matching tolerate CRLF/LF line endings; bundled-source checks also normalize line endings.
* Avoided the legacy forced-build directory collision by building CACTI only when its executable is absent, using the actual CACTI make directory.

No missing companion ZIP or separately supplied patch is required. Setup still requires internet and an installed supported Python interpreter. No macOS execution or calibrated physical-chip validation is claimed.
