"""Non-author actual whole-driver admission controls; stop before native state."""
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=Path.cwd()
COMMIT='fa6764a48'
R='Database/FFXII TZA/_index/candidates/s33-opus-replay-op1-real'
sha=lambda data:hashlib.sha256(data).hexdigest()
DRIVER=sha(Path(__file__).read_bytes())
PYTHON=sha(Path(sys.executable).read_bytes())

def capture(tag, argv, cwd, timeout=30):
    status=P/(tag+'.status.json'); out=P/(tag+'.stdout'); err=P/(tag+'.stderr')
    if any(p.exists() for p in [status,out,err]):raise RuntimeError('fresh immutable invocation required')
    z=dict(argv=argv,cwd=str(cwd),driver_sha256=DRIVER,interpreter_sha256=PYTHON,terminal=False,exit=None,exception=None)
    try:
        r=subprocess.run(argv,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,
                         env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        out.write_bytes(r.stdout);err.write_bytes(r.stderr)
        z.update(terminal=True,exit=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
    except Exception as e:
        z['exception']=repr(e);out.write_bytes(b'');err.write_text(repr(e))
    status.write_text(json.dumps(z,indent=2)+'\n')
    return z,out.read_bytes(),err.read_bytes()

def git(tag, args):
    z,out,err=capture(tag,['git',*args],ROOT)
    if not z['terminal'] or z['exit']!=0 or z['exception'] is not None:
        raise RuntimeError('required Git acquisition incomplete: '+tag)
    return out

if (P/'result-01.json').exists():raise RuntimeError('result already present; no repeat')
commit=git('git-commit-01',['rev-parse',COMMIT+'^{commit}']).decode().strip()
if len(commit)!=40:raise RuntimeError('bad resolved commit identity')
retained=P/'retained';retained.mkdir(exist_ok=False)
inputs={}
for n,name in enumerate(['check.py','upstream_guard.py','test_upstream_guard.py'],1):
    raw=git(f'git-source-{n:02}', ['show',commit+':'+R+'/'+name])
    (retained/name).write_bytes(raw)
    checkout=(ROOT/R/name).read_bytes()
    equal=checkout==raw
    crlf_only=(checkout.replace(b'\r\n',b'\n')==raw)
    if not equal and not crlf_only:raise RuntimeError('current peer source differs materially; reconcile before testing')
    inputs[name]=dict(commit=commit,git_sha256=sha(raw),checkout_sha256=sha(checkout),
                      comparison='EXACT' if equal else 'CRLF_CHECKOUT_ONLY')
historical=(ROOT/R/'result.json').read_bytes();(retained/'historical-result.json').write_bytes(historical)
inputs['historical-result.json']=dict(sha256=sha(historical),limits='historical native output, not a new run or test oracle')

# Verify the test reaches the actual wrapper, rather than a separately called helper.
source=(retained/'check.py').read_text(); tree=ast.parse(source)
world_index=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign)
                 and any(isinstance(t,ast.Tuple) and [ast.unparse(x) for x in t.elts]==['W','uc','S'] for t in n.targets))
prefix=tree.body[:world_index]
imports=[n for n in ast.walk(ast.Module(body=prefix,type_ignores=[])) if isinstance(n,ast.Import)
         and any(a.name=='check' and a.asname=='C' for a in n.names)]
verdicts=[n for n in prefix if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call)
          and ast.unparse(n.value.func)=='upstream_guard.verdict']
refusals=[n for n in prefix if isinstance(n,ast.If) and ast.unparse(n.test)=='not _ok']
if len(imports)!=1 or len(verdicts)!=1 or len(refusals)!=1:
    raise RuntimeError('actual upstream import/verdict/refusal path identity changed')

F=P/'cases';F.mkdir(exist_ok=False)
boundary='''
def __getattr__(name):
    if name == 'W':
        print('ASTRA_DOWNSTREAM_STATE_BOUNDARY')
        raise SystemExit(0)
    raise AttributeError(name)
'''
fixtures={
 'positive':"allok=True\nresults={'qualified':{'pass_':True}}\nprint('qualified PASS')\n"+boundary,
 'reported-fail':"allok=False\nresults={'qualified':{'pass_':False}}\nprint('qualified FAIL; NOT ok')\n"+boundary,
 'raised-failure':"raise RuntimeError('qualified upstream failure')\n",
}
observations=[]
for label,fixture in fixtures.items():
    base=F/label;base.mkdir()
    current=base/'s33-opus-replay-op1-real';current.mkdir()
    upstream=base/'s21-opus-replay-applier-stub-free';upstream.mkdir()
    (upstream/'check.py').write_text(fixture)
    for name in ['check.py','upstream_guard.py']:
        (current/name).write_bytes((retained/name).read_bytes())
    argv=[sys.executable,'-B',str((current/'check.py').resolve())]
    z,out,err=capture('case-'+label,argv,base,timeout=20)
    downstream=b'ASTRA_DOWNSTREAM_STATE_BOUNDARY' in out
    no_result=not (current/'result.json').exists() and not (upstream/'result.json').exists()
    clean=z['terminal'] is True and z['exception'] is None and not err
    if label=='positive':
        wanted=clean and z['exit']==0 and downstream and out.strip()==b'ASTRA_DOWNSTREAM_STATE_BOUNDARY' and no_result
    elif label=='reported-fail':
        wanted=clean and z['exit']==2 and not downstream and b'REFUSED: upstream allok is False, not True' in out and no_result
    else:
        wanted=clean and z['exit']==2 and not downstream and b'REFUSED: upstream check raised RuntimeError: qualified upstream failure' in out and no_result
    observations.append(dict(case=label,receipt=z,fixture_sha256=sha((upstream/'check.py').read_bytes()),
                             tested_check_sha256=sha((current/'check.py').read_bytes()),tested_guard_sha256=sha((current/'upstream_guard.py').read_bytes()),
                             downstream_state_reached=downstream,no_result=no_result,required_observation=wanted))
if (ROOT/R/'result.json').read_bytes()!=historical:raise RuntimeError('historical result changed; do not accept')
complete=len(observations)==3 and all(x['required_observation'] for x in observations)
result=dict(complete=complete,verdict='ACCEPT_SCOPED_UPSTREAM_ADMISSION_REPAIR' if complete else 'INVALID_OR_REJECTED',
            method='A exact committed Python driver with labelled disposable host module fixtures; no native/game execution',
            driver_sha256=DRIVER,interpreter_sha256=PYTHON,commit=commit,inputs=inputs,cases=observations,
            scientific_native_runs=0,game_runs=0,
            established='Failed nonempty upstream and import exception refuse exit2 before downstream state; positive passes the real guard and reaches the first state boundary.',
            limits='The positive fixture deliberately stops at C.W, before native cases. No claim of complete S33 native success or changed historical result. Valid existing observation scope and natural scheduling/allocator/reachability remain unchanged.',
            cleanup='All bounded own children terminal; disposable files retained, historical result unchanged; no game/PC/instrument/save/config/reference/peer edits.')
with (P/'result-01.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps({'complete':complete,'verdict':result['verdict'],'cases':[{k:x[k] for k in ['case','downstream_state_reached','no_result','required_observation']} for x in observations]}))
raise SystemExit(0 if complete else 1)
