"""Produce a documented dynamic-action estimate; exclude all idle/leakage actions."""
import argparse, pathlib, yaml, math

def prepare(path, backup=None):
    data=yaml.safe_load(path.read_text())
    removed=0
    for component in data['action_counts']['local']:
        actions=component['action_counts']
        removed+=sum(x['name']=='idle' for x in actions)
        component['action_counts']=[x for x in actions if x['name']!='idle']
        for action in component['action_counts']:
            count=float(action['counts'])
            if not math.isfinite(count) or count<0:
                raise ValueError('Invalid non-idle count: '+component['name'])
    backup=backup or path.with_suffix('.legacy.yaml')
    if backup.exists(): raise FileExistsError('Preserve existing backup: '+str(backup))
    backup.write_bytes(path.read_bytes())
    path.write_text(yaml.safe_dump(data,sort_keys=False))
    print(f'Excluded {removed} idle actions; all remaining counts are finite and nonnegative.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=pathlib.Path)
    p.add_argument('--backup',type=pathlib.Path)
    a=p.parse_args();prepare(a.file,a.backup)
