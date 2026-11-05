"""Maintainer checks: changed bundled files and the wrong environment must fail."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
file=root/'vendor/scale-sim-v3/configs/scale.cfg'
original=file.read_bytes()
try:
    file.write_bytes(original+b'\n# guard test\n')
    result=subprocess.run([sys.executable,str(root/'scripts/lab.py'),'doctor'],capture_output=True,text=True)
    assert result.returncode!=0 and 'Bundled file changed/missing' in result.stderr,result.stderr
finally:file.write_bytes(original)
subprocess.run([sys.executable,str(root/'scripts/lab.py'),'doctor'],check=True)
print('Source integrity rejection and restoration passed.')
