"""Apply four checked compatibility repairs to the pinned legacy lab checkout."""
from pathlib import Path
import argparse

FIXES = [
 ('scalesim/memory/double_buffered_scratchpad_mem.py',
  'self.total_cycles = int(max(ofmap_serviced_cycles))',
  'self.total_cycles = int(np.max(ofmap_services_cycles_np))'),
 ('scalesim/memory/read_buffer.py',
  'self.last_prefetch_cycle = int(max(response_cycles_arr))',
  'self.last_prefetch_cycle = int(np.max(response_cycles_arr))'),
 ('scalesim/scale.py','s = scalesim(save_disk_space=False,',
  's = scalesim(save_disk_space=save_space,'),
 ('scale.py','s = scalesim(save_disk_space=False,',
  's = scalesim(save_disk_space=save_space,')]

def patch(root):
    pending=[]
    for name,old,new in FIXES:
        path=root/name
        data=path.read_bytes(); text=data.decode('utf-8')
        if text.count(new)==1 and old not in text:
            print('Already fixed:',name); continue
        if text.count(old)!=1 or new in text:
            raise SystemExit('Unexpected source; no files changed: '+name)
        pending.append((path,data,text.replace(old,new).encode('utf-8')))
    for path,data,replacement in pending:
        backup=path.with_name(path.name+'.bak')
        if not backup.exists(): backup.write_bytes(data)
        path.write_bytes(replacement)
        print('Patched:',path.relative_to(root))
    print('Compatibility checks passed.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=Path.cwd())
    patch(p.parse_args().repo.resolve())
