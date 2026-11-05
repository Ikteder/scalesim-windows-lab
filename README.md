# SCALE-Sim Windows student lab

One repository contains the simulator, configuration/layout files, example workloads, Windows scripts and the optional WSL energy scripts. **There is no separate companion download.** Start here rather than following the earlier Word manual.

**This package is for Windows students only.** The default path is native Windows. Git, Anaconda, PyTorch, a compiler and WSL are **not required** for the basic lab. Internet access is required during setup to install Python packages. The source is bundled, but Python and package wheels are not an offline installer.

## 1 Download and extract

Download this repository using GitHub **Code → Download ZIP**. Save it in Downloads, choose **Extract All**, and open the extracted folder containing `Setup.ps1` and this README. Do not run inside the ZIP preview. You may keep the lab in Downloads. Folder names containing spaces are supported on Windows.

No particular folder name or Windows username is required. Do not move the folder after setup: virtual environments record their original location. If you move it, extract another fresh copy and run setup there.

## 2 Check Python before setup

Use 64-bit **x64 CPython 3.12** on Windows 10/11 x64. Other Python major/minor versions and ARM64-native Python are not the tested target. In PowerShell:

```powershell
py -3.12 --version
```

If this is missing, install Python 3.12 from the [official Python Windows releases](https://www.python.org/downloads/windows/). The [3.12.10 release page](https://www.python.org/downloads/release/python-31210/) includes an x64 Windows installer. Enable its Python launcher option. Close and reopen the terminal after installation. Do not uninstall your other Python versions. The setup itself validates version and architecture before using the interpreter; it does not silently use your default `python` command.

If the launcher is unavailable but you have Python 3.12 installed, use the explicit interpreter option shown below. Setup does not automatically install system software or require administrator access.

## 3 Run the checked setup

Open the extracted lab folder in File Explorer, right-click its background and choose **Open in Terminal**. Run this command from the folder containing `Setup.ps1`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1
```

If needed, specify your real Python executable path (replace the example path):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1 -PythonExe "C:\Python312\python.exe"
```

This policy setting applies to the child PowerShell process only. No activation command or permanent execution-policy change is needed.

The setup and runner clear inherited Python search-path overrides in their own process so an older Python installation cannot redirect this lab's imports. They do not change your saved Windows environment settings.

Setup creates this folder's `.venv`, installs exact package versions from `requirements.txt`, installs the bundled simulator in editable mode and checks:

* Python 3.12 x64 and the correct virtual environment;
* exact NumPy and other dependency versions, plus `pip check`;
* bundled-source integrity and the actual imported SCALE-Sim location;
* `python -m scalesim.scale --help`;
* complete three-layer simulations at 32×32, 16×16 and 8×8;
* expected cycle totals and identical summary reports with saved traces enabled/disabled.

Only **SETUP PASSED** means setup finished successfully. A progress bar, a successful pip install or a single completed layer is insufficient. If setup fails, read its last error and fix that first; later steps do not hide the failure. Rerunning setup in the same folder is supported and generates fresh test outputs.

## 4 Run the lab

Keep using the same extracted folder. These commands use its own Python and set the simulator working directory automatically:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task doctor
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task cnn
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task compare
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task energy
```

`cnn` runs the included `examples/cnn.csv`; it needs no PyTorch installation. `compare` runs that same workload on three array sizes. `energy` multiplies event counts by explicit illustrative coefficients and writes `illustrative-energy.json`. It is a dynamic-only arithmetic exercise, **not Accelergy or measured device power**.

The runner prints the exact output folder. It contains `config.cfg`, `simulation.log`, `run.json` and a `result` directory with the four reports. Every run has a unique directory; existing student results are not overwritten. `logs/acceptance.json` records the setup acceptance runs.

| Report | Read it for |
| --- | --- |
| COMPUTE_REPORT.csv | Cycles, stalls and utilization for each represented layer |
| BANDWIDTH_REPORT.csv | Modeled words per cycle; different transfers can use different averaging intervals |
| DETAILED_ACCESS_REPORT.csv | Read/write event counts; start/stop timestamps are not counts |
| REPEAT_CYCLE.csv | Legacy reuse counts used by the optional energy workflow |

For this exact CNN/configuration, summed Total Cycles are **16119**, **24229**, **65053** for 32×32, 16×16, 8×8. These are modeled accelerator cycles, not host execution time. At chosen frequency f Hz, time = cycles/f; useful throughput = 2×MACs/time. Peak throughput = 2×array height×array width×f. State whether the interval includes prefetch and final transfers. Overall Util, Mapping Efficiency and Compute Util are distinct metrics.

## 5 Bundled larger workloads

After the small tests pass:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task alexnet
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task resnet18
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task resnet50
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Run-Lab.ps1 -Task vit
```

Start with AlexNet. Large runs take time and memory; traces are disabled, but the internal cycle matrices still use RAM. The bundled topology files contain 5, 21, 54 and 5 rows respectively. In particular, this AlexNet file has only five convolution rows, not its dense classifier. Do not equate a CSV's name with a complete framework network.

The latest local check completed AlexNet and checked the other three commands for startup errors before deliberately stopping them. Those startup checks do not certify full completion; see [VALIDATION.md](VALIDATION.md).

## 6 Your own model and direct module use

`examples/cnn.csv` uses `Layer,M,N,K,` rows: M×K times K×N, with M×N×K useful MACs. Preserve trailing commas; the legacy CSV parser discards its final field. The sample CNN's dense GEMM dimensions are included, so weights and training data are unnecessary.

An optional restricted PyTorch exporter is supplied as `examples/export_pytorch.py`. PyTorch is not installed by basic setup. If you want to use it:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-torch.txt
.\.venv\Scripts\python.exe .\examples\export_pytorch.py
```

It writes `examples/my_model.csv`. It captures module-based Conv2d/Linear operations for one CPU sample and rejects unsupported grouped/depthwise convolution, dilation and padding. It does not model pooling/activation overhead or general functional operators. GEMM export uses actual output dimensions to avoid the legacy convolution parser's ceil-versus-floor problem for unaligned strides.

For a direct `scalesim.scale` run, these exact commands work from the lab root and return there afterward:

```powershell
Push-Location .\vendor\scale-sim-v3
try {
    & ..\..\.venv\Scripts\python.exe -m scalesim.scale -c configs/scale.cfg -t topologies/conv_nets/test.csv -p ..\..\runs_direct -s N
    if ($LASTEXITCODE -ne 0) { throw 'Simulation failed' }
} finally { Pop-Location }
```

The default layout file is relative to the simulator root, so do not launch the module from an arbitrary working directory. The managed runner handles this for you. Direct runs reuse `run_name` and can overwrite old direct outputs; the managed runner always creates a fresh path.

## 7 Accelergy and CACTI option

Windows students can also try the technology-model energy route using Ubuntu WSL2. Every lab helper is included under `energy/`. Follow [energy/README.md](energy/README.md) separately. That option downloads/builds the external Accelergy tools and uses a separate Linux virtual environment. It is not required for Sections 1–6 and does not replace the native Windows installation.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `Setup.ps1` not found | Extract the ZIP; open the inner folder that actually contains the file. Open a terminal there. |
| Python 3.12/launcher missing | Install x64 Python 3.12 or use `-PythonExe` with its full path. Reopen the terminal. |
| Scientific package source-build/compiler error | This setup requests wheels only. Check Python version, x64 architecture and access to PyPI; do not install random compiler fixes. |
| Download/proxy/SSL error | Ask your institution to allow the required Python package sources; setup needs internet. Do not disable TLS verification. |
| School policy blocks PowerShell | Follow institutional policy; ask the instructor/IT. The per-process option cannot override enforced organizational policy. |
| Wrong package, version or modified vendor file | Run `doctor`. Use a fresh extracted copy rather than mixing this lab with an old SCALE-Sim install. |
| NumPy scalar-conversion crash | The bundled code is already repaired. A failing integrity/import check indicates a modified or different simulator. |
| Existing or moved virtual environment fails | Keep the folder in place, or extract a fresh ZIP into the intended final location and set it up there. |
| A run fails | Inspect the printed `simulation.log`; do not treat partial CSV files as a pass. |

The simulator models timing/data movement, not prediction accuracy. Accuracy and physical-chip power require separate validation. See [PROVENANCE.md](PROVENANCE.md) for the upstream revision and local fixes. The included Windows CI workflow repeats setup and acceptance on future pushes; a workflow file by itself is not evidence that a GitHub run has passed.
