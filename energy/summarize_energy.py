"""Sum one Accelergy energy file without double counting YAML summary fields."""
import argparse, collections, csv, math
from pathlib import Path
import yaml

def summarize(path, compute, hz):
    data=yaml.safe_load(Path(path).read_text())
    block=data['energy_estimation']
    components=block['components']
    groups=collections.defaultdict(float)
    for item in components:
        energy=float(item['energy'])
        if not math.isfinite(energy) or energy<0: raise ValueError('Invalid component energy')
        groups[item['name'].split('.')[-1]]+=energy
    total=sum(groups.values())
    print(f'Total energy: {total/1e6:.6f} uJ')
    for name,value in sorted(groups.items(),key=lambda x:-x[1]):
        print(f'{name:20} {value/1e6:.6f} uJ')
    if compute:
        with Path(compute).open() as f:
            rows=[{k.strip():v for k,v in row.items() if k} for row in csv.DictReader(f)]
        cycles=sum(float(r['Total Cycles']) for r in rows)
        seconds=cycles/hz
        print(f'Cycles: {cycles:g}; latency: {seconds*1e3:.6f} ms at {hz:g} Hz')
        print(f'Energy / modeled interval: {total*1e-12/seconds:.6f} W (scope follows the action model)')
    return total

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('energy'); p.add_argument('--compute');p.add_argument('--hz',type=float,default=1e9)
    a=p.parse_args();summarize(a.energy,a.compute,a.hz)
