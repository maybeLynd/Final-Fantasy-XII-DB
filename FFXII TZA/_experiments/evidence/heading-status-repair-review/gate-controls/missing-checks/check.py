import ast,hashlib,json,re,sys
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(root):
 t=json.loads((root/'capture-terminal.json').read_bytes())
 if '--fault-upstream-failed' in sys.argv:t['returncode']=1
 assert t['terminal'] is True and t['returncode']==0 and not t['stderr'] and t['stdout'].strip()=='REPAIRED_H8_PAIRED_STATUS_CAPTURED' and t['driver_sha256']==sha(root/'capture.py'),'Required capture failed/incomplete'
 ident=json.loads((root/'identity.json').read_bytes());assert ident==json.loads((root/'identity-before.json').read_bytes()) and ident['driver_sha256']==t['driver_sha256']
 assert ident['producer_commit']=='2366027d98e5c9016150e36437ee398d9472248b' and sha(root/'retained/producer-current.py')==ident['producer_sha256'] and sha(root/'retained/producer-2366027d9.py')==ident['commit_source_sha256']
 data=(root/'retained/producer-current.py').read_bytes();assert data.replace(b'\r\n',b'\n')==(root/'retained/producer-2366027d9.py').read_bytes().replace(b'\r\n',b'\n')
 rs=json.loads((root/'producer-terminal.json').read_bytes())
 if '--fault-missing-negative' in sys.argv:rs=rs[:1]
 assert [x['case'] for x in rs]==['original','first-fragment-catalogue'] and all(x['terminal'] is True and not x['stderr'] and x['producer_sha256']==ident['producer_sha256'] for x in rs)
 a,b=rs
 if '--fault-zero-negative' in sys.argv:b['returncode']=0
 assert a['returncode']==0 and a['stdout'].endswith('FAILS 0\n') and re.search(r'^SURVIVES  H8  .*extent valid True; calls 21; direct \+0x03 operands \[\]',a['stdout'],re.M)
 assert b['returncode']==1 and b['stdout'].endswith('FAILS 1\n') and re.search(r'^BROKEN    H8  .*catalogue 40 B;.*extent valid False; calls None; direct \+0x03 operands None',b['stdout'],re.M),'Actual truncated negative must propagate status and omit invalid counts'
 dep=next(x for x in ident['dependencies'] if x['member']=='h8-input-intervention.py');assert b['wrapper_sha256']==dep['sha256']
 nodes=ast.parse(data).body;assigns={n.targets[0].id:(k,n.value) for k,n in enumerate(nodes) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
 for name in ['ncalls','plus3']:
  k,value=assigns[name];assert assigns['extent_ok'][0]<k and isinstance(value,ast.IfExp) and isinstance(value.test,ast.Name) and value.test.id=='extent_ok' and isinstance(value.orelse,ast.Constant) and value.orelse.value is None
 if '--fault-count-ungated' in sys.argv:assert isinstance(assigns['ncalls'][1],ast.Call),'Count is conditional on extent_ok, not unconditional call'
 end=nodes[-1];assert isinstance(end,ast.Raise) and isinstance(end.exc,ast.Call) and isinstance(end.exc.func,ast.Name) and end.exc.func.id=='SystemExit';v=end.exc.args[0];assert isinstance(v,ast.IfExp) and isinstance(v.test,ast.Name) and v.test.id=='fails' and v.body.value==1 and v.orelse.value==0
 return {'verdict':'ACCEPT scoped2366027d9 H8 CLI/gated-count repair','original':'SURVIVES H8 / extent validTrue / calls21 / FAILS0 / exit0','first_fragment_intervention':'BROKEN H8 / extent validFalse / callsNone / operandsNone / FAILS1 / exit1','source_order':'extent_ok assigned before conditional ncalls/plus3; AST plus original actual process output','prior_evidence':'feb631dd4 failed exit propagation remains immutable; new code separately fixes it','method':'A actual producer Python and same published labelled io.open catalogue963->40 substitution; not native/game execution','limits':'Only heading script dynamically exercised, not all47 modified scripts or H0H7 semantics/class effects/live reachability/migration/L1L2. Nonauthor ASTRA checker/gate review and canonical owner incorporation separate.'}
if __name__=='__main__':print(json.dumps(check(W),indent=2))
