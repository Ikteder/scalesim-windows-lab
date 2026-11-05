import sys, pathlib, subprocess, json, csv, uuid, datetime, hashlib, importlib.metadata, math
ROOT=pathlib.Path(__file__).resolve().parents[1]
V=ROOT/'vendor/scale-sim-v3'
def doctor():
    assert sys.version_info[:2]==(3,12), 'Python 3.12 required'
    assert pathlib.Path(sys.prefix).resolve()==(ROOT/'.venv').resolve(), 'Use this repository virtual environment'
    for line in (ROOT/'requirements.txt').read_text().splitlines():
        name,version=line.split('=='); actual=importlib.metadata.version(name)
        assert actual==version,f'{name}: expected {version}, found {actual}'
    import scalesim, numpy
    assert pathlib.Path(scalesim.__file__).resolve().is_relative_to(V.resolve()), 'Wrong SCALE-Sim package imported'
    assert int(numpy.max(numpy.array([[1],[2]])))==2
    for name,sha in json.loads((ROOT/'vendor-manifest.json').read_text()).items():
        assert hashlib.sha256((V/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==sha, 'Bundled file changed/missing: '+name
    subprocess.run([sys.executable,'-m','pip','check'],check=True)
    subprocess.run([sys.executable,'-m','scalesim.scale','--help'],cwd=V,stdout=subprocess.DEVNULL,check=True)
    print('DOCTOR PASSED: interpreter, exact dependencies, source files, import and scalesim.scale checked.')
def run(name='cnn',n=32,trace='N'):
    key=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]+'-'+name+f'-{n}'
    out=ROOT/'runs'/key;out.mkdir(parents=True)
    config=(V/'configs/scale.cfg').read_text().replace('scale_example_run_32x32_ws','result').replace('ArrayHeight:    32',f'ArrayHeight:    {n}').replace('ArrayWidth:     32',f'ArrayWidth:     {n}')
    cfg=out/'config.cfg';cfg.write_text(config)
    mapping={'alexnet':('conv_nets/alexnet.csv','conv',5),'resnet18':('conv_nets/Resnet18.csv','conv',21),'resnet50':('conv_nets/Resnet50.csv','conv',54),'vit':('GEMM_mnk/vit_s.csv','gemm',5)}
    topo,kind,rows=mapping.get(name,(None,'gemm',3))
    path=V/'topologies'/topo if topo else ROOT/'examples/cnn.csv'
    cmd=[sys.executable,'-m','scalesim.scale','-c',str(cfg),'-t',str(path),'-p',str(out),'-i',kind,'-s',trace]
    with (out/'simulation.log').open('w') as log:
        process=subprocess.run(cmd,cwd=V,stdout=log,stderr=subprocess.STDOUT)
    assert process.returncode==0,'Simulation failed: '+str(out/'simulation.log')
    reports=out/'result'
    for f in ['COMPUTE_REPORT.csv','BANDWIDTH_REPORT.csv','DETAILED_ACCESS_REPORT.csv','REPEAT_CYCLE.csv']:
        with (reports/f).open() as stream:data=list(csv.reader(stream))[1:]
        assert len(data)==rows,f'Incomplete {f}'
    with (reports/'COMPUTE_REPORT.csv').open() as f:
        data=[{k.strip():v for k,v in r.items() if k} for r in csv.DictReader(f)]
    cycles=sum(int(r['Total Cycles']) for r in data)
    traces=list(reports.rglob('*TRACE.csv'))
    assert len(traces)==(rows*6 if trace=='Y' else 0),'Trace setting was not respected'
    metadata={'workload':name,'array':n,'cycles':cycles,'layers':rows,'saved_traces':len(traces),'python':sys.version,'command':cmd}
    (out/'run.json').write_text(json.dumps(metadata,indent=2))
    print(f'PASS {name} {n}x{n}: {rows} layers, {cycles} cycles. Results: {reports}')
    return out,cycles
def verify():
    records=[]
    for n,expected in [(32,16119),(16,24229),(8,65053)]:
        folder,cycles=run(n=n);assert cycles==expected,(n,cycles,expected);records.append(str(folder))
    traced,_=run(trace='Y')
    for f in ['COMPUTE_REPORT.csv','BANDWIDTH_REPORT.csv','DETAILED_ACCESS_REPORT.csv','REPEAT_CYCLE.csv']:
        assert (pathlib.Path(records[0])/'result'/f).read_bytes()==(traced/'result'/f).read_bytes(),'Trace mode changed a summary report'
    (ROOT/'logs').mkdir(exist_ok=True)
    (ROOT/'logs/acceptance.json').write_text(json.dumps({'status':'PASS','runs':records+[str(traced)]},indent=2))
    print('ACCEPTANCE PASSED: three array configurations, complete reports and identical Y/N summaries.')
def energy():
    folder,_=run()
    with (folder/'result/DETAILED_ACCESS_REPORT.csv').open() as f:
        rows=[{k.strip():v for k,v in r.items() if k} for r in csv.DictReader(f)]
    print('Access report columns:',list(rows[0]))
    # Dense GEMM useful operations, and an explicitly illustrative coefficient model.
    macs=sum(int(r[1])*int(r[2])*int(r[3]) for r in list(csv.reader((ROOT/'examples/cnn.csv').open()))[1:])
    sram=sum(sum(float(v) for k,v in r.items() if 'SRAM' in k and ('Reads' in k or 'Writes' in k)) for r in rows)
    dram=sum(sum(float(v) for k,v in r.items() if 'DRAM' in k and ('Reads' in k or 'Writes' in k)) for r in rows)
    result={'model':'Illustrative dynamic-only; coefficients assumed, not measured or Accelergy','MACs':macs,'SRAM_events':sram,'DRAM_events':dram,'pJ_per_MAC':0.23,'pJ_per_SRAM_event':1.25,'pJ_per_DRAM_event':200,'energy_uJ':(macs*.23+sram*1.25+dram*200)/1e6}
    assert sram>0 and dram>0
    (folder/'illustrative-energy.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':
    try:
        task=sys.argv[1] if len(sys.argv)>1 else 'doctor'
        if task=='doctor':doctor()
        else:
            doctor()
            if task=='verify':verify()
            elif task=='compare':
                for n in [32,16,8]:run(n=n)
            elif task=='energy':energy()
            elif task in ['cnn','alexnet','resnet18','resnet50','vit']:run(task)
            else:raise ValueError('Unknown task')
    except Exception as e:
        print('FAILED:',e,file=sys.stderr);sys.exit(1)
