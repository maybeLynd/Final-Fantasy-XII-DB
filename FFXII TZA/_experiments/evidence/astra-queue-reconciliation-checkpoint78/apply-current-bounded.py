"""Small owner-disposition batches through the documented current-board CLI.

The shared guard passes now; documented CLI has three verified current-board
positive writes after the old failures. No board incident is inferred from the
old handoff. Keep FRONTIER's cause question open. Use fresh task preimages,
current owner/state guards, locked/journal-checked loading and exact receipts.
This is a changed invocation, not blind replay of the old background batch.
Stop at the first new refusal. No global stale board copy is ever written.
"""
import gc,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if(p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
PLAN=json.loads((H/'dispositions-01.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def loadmodule(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    start,last=int(sys.argv[1]),int(sys.argv[2]);folder=H/sys.argv[3]
    sequence=loadmodule('previous_decisions',H/'resume-bounded.py').ops()
    if not 1<=start<=last<=len(sequence) or last-start>=5:raise ValueError('explicit atmost five operations required')
    folder.mkdir()
    c=subprocess.run([sys.executable,'-B',str(T),'boardcheck'],capture_output=True,text=True,timeout=90)
    (folder/'boardcheck.json').write_text(json.dumps(dict(exit=c.returncode,stdout=c.stdout,stderr=c.stderr),indent=2))
    if c.returncode or not c.stdout.strip().startswith('board ok: ') or c.stderr.strip():raise ValueError('supported boardcheck refused')
    team=loadmodule('team',T)
    expected={old['id']:digest(old) for r in PLAN['records'] for old in r['preimages'].values() if isinstance(old,dict) and 'id' in old}
    accepted={}
    for source in [H/'apply-01',*sorted(H.glob('bounded-*')),*sorted(H.glob('current-*'))]:
        for p in source.glob('[0-9][0-9][0-9].receipt.json'):
            r=json.loads(p.read_text());serial=int(p.name[:3])
            if r['status']!='SUPPORTED_TRANSACTION_COMMITTED':continue
            if serial in accepted:raise ValueError('duplicate accepted serial')
            op=json.loads(p.with_name('%03d.op.json'%serial).read_text())
            op=op.get('operation',op)
            if op!=sequence[serial-1]:raise ValueError('operation lineage differs')
            accepted[serial]=(r,op)
    if set(accepted)!=set(range(1,start)):raise ValueError('start does not follow receipted prefix')
    b=json.loads(team.BOARD.read_text(encoding='utf-8'))
    parent=next(t for t in b['tasks'] if t['id']=='FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929')
    if parent['status']!='ACTIVE' or parent['agent']!='ASTRA' or not any(r['key']=='file:database/tools/work/astra/runtime-residue-method-retriage' for r in team.hold_set(parent)):raise ValueError('current W hold absent')
    for serial in sorted(accepted):
        r,op=accepted[serial]
        if not any(h.get('agent')=='ASTRA' and h['operation']==op for h in b['history']):raise ValueError('accepted operation missing from canonical history')
        expected[op['task']]=r['task_sha256']
    if any(any(h.get('agent')=='ASTRA' and h['operation']==sequence[serial-1] for h in b['history']) for serial in range(start,last+1)):raise ValueError('operation already landed without receipt; adjudicate, do not replay')
    del parent,b;gc.collect()
    for serial in range(start,last+1):
        op=sequence[serial-1]
        raw=team.BOARD.read_bytes();b=json.loads(raw.decode('utf-8'));row=next(t for t in b['tasks'] if t['id']==op['task'])
        if b['recovery_epoch']!=PLAN['snapshot_epoch'] or digest(row)!=expected[row['id']]:raise ValueError('fresh task preimage or epoch moved')
        before=dict(revision=b['revision'],epoch=b['recovery_epoch'],task_sha256=digest(row),board_sha256=hashlib.sha256(raw).hexdigest())
        # Existing-row mutation remains owned and state-checked by team.py
        # inside the lock. Global peer-only revision churn is not a semantic
        # preimage waiver; no old board object is passed to the writer.
        p=folder/('%03d'%serial);p.with_suffix('.op.json').write_text(json.dumps(dict(operation=op,preimage=before),indent=2))
        arg=p.with_suffix('.cli-op.json');arg.write_text(json.dumps(op,indent=2))
        del row,b,raw;gc.collect()
        cmd=[sys.executable,'-B',str(T),'apply','--agent','ASTRA','--session','SOL-ASTRA-current-queue1003','--file',str(arg)]
        z=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        receipt=dict(argv=cmd,exit=z.returncode,stdout=z.stdout,stderr=z.stderr,driver_sha256=sha(Path(__file__)),team_sha256=sha(T),operation_sha256=sha(arg),preimage=before)
        if z.returncode or not re.search(r'Saved revision \d+',z.stdout):
            receipt['status']='REFUSED_STOP_NO_REPLAY';p.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2));raise ValueError('documented current writer refused; stop')
        b=json.loads(team.BOARD.read_text(encoding='utf-8'));row=next(t for t in b['tasks'] if t['id']==op['task'])
        if row['checkpoint']!=op['note'] or not any(h.get('agent')=='ASTRA' and h['operation']==op for h in b['history']):raise ValueError('current result missing/different; no success promotion')
        expected[row['id']]=digest(row)
        receipt.update(status='SUPPORTED_TRANSACTION_COMMITTED',revision=b['revision'],task=op['task'],action=op['action'],task_sha256=expected[row['id']])
        p.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2));del row,b;gc.collect()
        print(json.dumps(dict(serial=serial,task=op['task'],action=op['action'])),flush=True)
    (folder/'terminal.json').write_text(json.dumps(dict(status='CURRENT_BOUNDED_BATCH_COMPLETE',start=start,last=last,next=last+1,total=len(sequence)),indent=2))
if __name__=='__main__':main()
