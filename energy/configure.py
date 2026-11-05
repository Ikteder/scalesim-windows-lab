"""Use this energy environment exclusively; do not inherit a user's global config."""
from pathlib import Path
import sys,yaml
root=Path(__file__).resolve().parents[1]
share=Path(sys.prefix)/'share/accelergy'
(share/'primitive_component_libs').mkdir(parents=True,exist_ok=True)
for name in ['estimation_plug_ins','primitive_component_libs']:
    if not (share/name).is_dir():raise SystemExit('Missing Accelergy installation resource: '+str(share/name))
config={'version':'0.4','estimator_plug_ins':[str(share/'estimation_plug_ins')],'primitive_components':[str(share/'primitive_component_libs')],'compound_components':[],'math_functions':[],'python_plug_ins':[],'table_plug_ins':{'roots':[str(share/'table_plug_ins')]}}
path=root/'vendor/scale-sim-v3/rundir-accelergy/accelergy_config.yaml'
path.write_text(yaml.safe_dump(config))
print('Local estimator configuration:',path)
