"""Execute the actual capture in disposable directories, never a published one."""
import hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
E=Path('Database/FFXII TZA/_experiments/evidence')
producer=W.parent/'matrix-buffer-alias/capture.py'
raw=producer.read_bytes()
assert b'access=memory_role(i,k),capstone_access_flag=o.access' in raw
assert b"access='write' if o.access" not in raw
original=(E/'matrix-buffer-alias/source.json').read_bytes()
fix=json.loads((E/'procedural-mode-cost/matrix-buffer-alias-access-correction.json').read_text())
assert fix['parent_source_sha256']==sha(original)
expected=fix['memory_operands'];assert expected
published_before={str(p):sha(p.read_bytes()) for p in (E/'matrix-buffer-alias').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
adapter_path=E/'procedural-mode-cost/operand_direction.py'
spec=importlib.util.spec_from_file_location('probe_role_adapter',adapter_path)
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
rmw=next(cs.disasm(bytes.fromhex('f00fb108'),0)) # synthetic LOCK CMPXCHG [rax],ecx
assert rmw.mnemonic=='lock cmpxchg' and adapter.policy.op_kind(rmw,rmw.operands[0],0)=='rw'
try:adapter.memory_role(rmw,0)
except ValueError: restricted_rmw_rejected=True
else:raise AssertionError('restricted matrix vocabulary must reject unsupported RMW')
blocked_driver='''import importlib.util,runpy,sys
real=importlib.util.spec_from_file_location
def stopped(name,path,*args,**kw):
 s=real(name,path,*args,**kw)
 if name=='matrix_capture_role_adapter':
  inner=s.loader
  class Gate:
   def create_module(self,spec):return inner.create_module(spec)
   def exec_module(self,m):
    inner.exec_module(m)
    def reject(*args):raise RuntimeError('CONTROL_ADAPTER_BLOCKED')
    m.memory_role=reject
  s.loader=Gate()
 return s
importlib.util.spec_from_file_location=stopped
runpy.run_path(sys.argv[1],run_name='__main__')
'''
observations=[]
for case in ('default','raw_flag_mutant','adapter_blocked'):
 with tempfile.TemporaryDirectory(prefix='astra-role-',dir=W) as td:
  td=Path(td);p=td/'capture.py'
  code=raw if case!='raw_flag_mutant' else raw.replace(b'access=memory_role(i,k),',b"access='write' if o.access&capstone.CS_AC_WRITE else 'read',")
  assert case!='raw_flag_mutant' or code!=raw
  p.write_bytes(code)
  if case=='adapter_blocked':
   (td/'blocked.py').write_text(blocked_driver);command=[sys.executable,str(td/'blocked.py'),str(p)]
  else:command=[sys.executable,str(p)]
  r=subprocess.run(command,capture_output=True,text=True,timeout=30)
  source=json.loads((td/'source.json').read_text()) if (td/'source.json').exists() else None
  changed=[]
  if source:
   assert len(source['memory_operands'])==len(expected)
   for got,want in zip(source['memory_operands'],expected):
    assert {k:v for k,v in got.items() if k!='access'}=={k:v for k,v in want.items() if k!='access'}
    if got['access']!=want['access']:changed.append(dict(pc=got['pc'],observed=got['access'],expected=want['access']))
  observations.append(dict(case=case,producer_sha256=sha(code),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,source_created=source is not None,source=source,role_differences=changed))
 assert not td.exists()
default,mutant,blocked=observations
assert default['exit_code']==0 and default['source_created'] and not default['role_differences']
assert mutant['exit_code']==0 and {x['pc'] for x in mutant['role_differences']}=={'0x202b79','0x202b86'}
assert blocked['exit_code']!=0 and not blocked['source_created'] and 'CONTROL_ADAPTER_BLOCKED' in blocked['stderr']
assert all(sha(Path(p).read_bytes())==h for p,h in published_before.items())
result=dict(method='A actual Python producer execution and decoded shipping bytes; NO original machine-code execution or live FF12',producer_path=producer.as_posix(),producer_sha256=sha(raw),original_source_sha256=sha(original),adapter_sha256=sha(adapter_path.read_bytes()),policy=adapter.POLICY_ID,python=sys.version,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone_version=capstone.__version__,runner_sha256=sha(Path(__file__).read_bytes()),observations=observations,rmw_control=dict(bytes=rmw.bytes.hex(),mnemonic=rmw.mnemonic,central_role='rw',restricted_capture_rejected=True,limit='Synthetic instruction decode, not FF12 execution; no RMW operand exists in the two matrix capture bodies.'),cleanup=dict(disposable_directories_removed=True,published_matrix_unchanged=True,pc_control='OFF',ff12_launched=False),limits='Corrects metadata producer default only. Original alias/order/staging claims retained, general overlap/live caller semantics remain open. Default source includes current consumer preimages; not a recapture of native observations.')
if (W/'result.json').exists():raise RuntimeError('Result exists: do not repeat settled controls')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS actual default producer/corrected rows; raw-flag mutation detected at store+LEA; adapter-blocked invocation fails before publication; RMW policy/profile control. No FF12 execution.')
