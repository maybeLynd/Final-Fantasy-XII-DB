"""Focused real-CLI prerequisite refusals and constant-path source controls.

Mutated bytes are disposable analysis inputs; none are executed as machine code.
The old failed stack model remains pinned and is required to fail this control.
"""
import hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(destination):
    if destination.exists():raise ValueError('fresh control receipt required')
    state=json.loads((P/'proof-03.status.json').read_bytes())
    result=json.loads((P/'result-03.json').read_bytes())
    if state.get('terminal') is not True or state.get('exit')!=0 or state.get('exception') is not None or state.get('driver_sha256')!=sha(P/'prove.py') or result.get('producer_complete') is not True or result.get('driver_sha256')!=sha(P/'prove.py'):
        raise ValueError('positive current producer failed')
    destination.mkdir();cases=[]
    cli=[('upstream-failed','required physical producer failed or incomplete'),
         ('extent-incomplete','physical extent prerequisite incomplete'),
         ('unwind-header-changed','unsupported or altered physical unwind identity'),
         ('registration-incomplete','retained registration source prerequisite incomplete'),
         ('coherent-guard-change','retained original body differs')]
    for name,expected in cli:
        folder=destination/name;folder.mkdir();source=folder/'source'
        shutil.copytree(P/'retained',source)
        if name=='upstream-failed':
            file=source/'handler-extents-01.status.json';v=json.loads(file.read_bytes());v['exit']=1
        elif name=='registration-incomplete':
            file=source/'source-01.json';v=json.loads(file.read_bytes());v['wrapper_complete']=False
        else:
            file=source/'handler-extents-01.json';v=json.loads(file.read_bytes())
            if name=='extent-incomplete':v['complete']=False
            elif name=='unwind-header-changed':v['bodies'][0]['records'][0]['chain'][0]['header_bytes']='01040101'
            else:
                b=v['bodies'][0];blob=bytes.fromhex(b['physical_bytes'])
                if blob.count(bytes.fromhex('83fa01'))!=1:raise ValueError('guard mutation preimage changed')
                blob=blob.replace(bytes.fromhex('83fa01'),bytes.fromhex('83fa00'))
                b.update(physical_bytes=blob.hex(),sha256=hashlib.sha256(blob).hexdigest())
        file.write_text(json.dumps(v,indent=2)+'\n')
        output=folder/'result.json'
        argv=[sys.executable,'-B',str(P/'prove.py'),str(output),'--src',str(source)]
        row=dict(name=name,argv=argv,driver_sha256=sha(P/'prove.py'),terminal=False,exit=None,exception=None)
        try:
            child=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
            (folder/'stdout').write_bytes(child.stdout);(folder/'stderr').write_bytes(child.stderr)
            row.update(terminal=True,exit=child.returncode,
                expected_diagnostic=expected,
                expected_refusal=child.returncode!=0 and expected.encode() in child.stderr and not output.exists() and not (folder/'normalized-result.json').exists())
        except Exception as e:
            row.update(exception=repr(e),expected_refusal=False)
        (folder/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');cases.append(row)
        if row['terminal'] is not True or row['exception'] is not None or not row['expected_refusal']:raise ValueError('actual prerequisite refusal failed: '+name)

    module=load('event0_producer',P/'prove.py')
    roles=load('event0_reviewed_roles',module.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py')
    module.ROLES=roles
    old=load('event0_failed_stack_model',P/'failed-prove-01.py');old.ROLES=roles
    old_status=json.loads((P/'proof-01.status.json').read_bytes())
    if old_status.get('exit')!=1 or old_status.get('driver_sha256')!=sha(P/'failed-prove-01.py') or (P/'result-01.json').exists():
        raise ValueError('failed model preimage/history missing')
    e=json.loads((P/'retained/handler-extents-01.json').read_bytes())
    original={int(b['entry'],16):bytes.fromhex(b['physical_bytes']) for b in e['bodies']}
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    decode=lambda blob,a:list(cs.disasm(blob,a))
    path_controls=[]
    ins=decode(original[0x29b7d0],0x29b7d0)
    bad=old.tracer(ins,0);good=module.tracer(ins,0)
    if bad.get('pre_ret_rsp_delta')!=(1<<64) or good.get('pre_ret_rsp_delta')!=0:raise ValueError('actual failed stack model regression not detected')
    path_controls.append(dict(name='signed-relative-stack-regression',old_driver_sha256=sha(P/'failed-prove-01.py'),old=bad,corrected=good))
    for name,a,before,after,boundary,field,value in [
        ('primary-event0-call-discriminator',0x29b7d0,'83fa01','83fa00','CALL','target','0x2973e0'),
        ('secondary-event0-write-discriminator',0x29b810,'83ea01','83c201','OBJECT_WRITE','pc','0x29b82c')]:
        blob=original[a]
        if blob.count(bytes.fromhex(before))!=1:raise ValueError('source control preimage changed')
        mutated=blob.replace(bytes.fromhex(before),bytes.fromhex(after))
        observation=module.tracer(decode(mutated,a),0)
        if observation.get('boundary')!=boundary or observation.get(field)!=value:raise ValueError('source discriminator failed: '+name)
        path_controls.append(dict(name=name,entry=hex(a),original_sha256=hashlib.sha256(blob).hexdigest(),mutated_bytes=mutated.hex(),observation=observation))
    mutated=original[0x29b7d0].replace(bytes.fromhex('83fa01'),bytes.fromhex('83f801'))
    try:module.tracer(decode(mutated,0x29b7d0),0)
    except ValueError as error:
        if 'unknown predicate' not in str(error):raise
        path_controls.append(dict(name='unresolved-predicate-no-claim',mutated_bytes=mutated.hex(),refusal=str(error)))
    else:raise ValueError('unknown source predicate was accepted')
    out=dict(producer_complete=True,driver_sha256=sha(Path(__file__)),producer_sha256=sha(P/'prove.py'),positive_result_sha256=sha(P/'result-03.json'),
        method='Actual CLI prerequisite tests and static source-interpretation controls; no native/live execution',
        cli_refusals=cases,path_controls=path_controls,
        limitations='Disposable mutation controls test producer discrimination, not shipping behavior, original execution or independent acceptance')
    (destination/'result.json').write_text(json.dumps(out,indent=2)+'\n')
    print('VALIDATED: five real CLI refusals; old-stack regression; call/write mutations; unknown-predicate refusal')

if __name__=='__main__':main(P/sys.argv[1])
