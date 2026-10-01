import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'source.json').read_text())
r=json.loads((W/'raw.json').read_text())
assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert sha((W/s['helper_retained']).read_bytes())==s['helper_sha256']
assert sha((W/s['executed_driver']).read_bytes())==s['executed_driver_sha256']
assert s['imports'][0]['iat']=='0x8c2c10' and s['imports'][0]['name']=='_fdclass'
ii={i['pc']:i for b in s['bodies'] for i in b['instructions']}
for b in s['bodies']:
 assert len(bytes.fromhex(b['raw_hex']))==b['size']
 assert sha(bytes.fromhex(b['raw_hex']))==b['sha256']
 assert ''.join(i['bytes'] for i in b['instructions'])==b['raw_hex']
 assert b['instructions'][-1]['op']=='ret'
assert ii['0x383faf']['op']==ii['0x383fcd']['op']=='ja'
assert ii['0x38402c']['bytes']=='410fb70c41'
cases={o['case']['name']:o for o in r}
expected={
 'origin-control':(0,0),'interior-control':(0,0),
 'x-upper-minus-ulp':(2,3),'x-upper-equal':(255,4),
 'x-upper-equal-next-row-list':(3,4),'x-upper-plus-ulp':(255,None),
 'guard-last-cell-control':(3,7),'guard-z-upper-minus-ulp':(1,4),
 'guard-z-upper-plus-ulp':(255,None),
 'mutant-x-ja-to-jae':(255,None),'mutant-z-ja-to-jae':(255,None)}
faults={'guard-x-upper-equal-last-row':8,'guard-z-upper-equal':8,'guard-corner-equal':12}
assert len(r)==len(cases)==14 and set(cases)==set(expected)|set(faults)
allowed={int(i['pc'],16) for b in s['bodies'] for i in b['instructions']}|{int(s['fdclass_trampoline'],16)}
summary=[]
for name,o in cases.items():
 assert 0<o['instructions']==len(o['pcs'])<o['instruction_budget']==2000
 assert all(int(pc,16) in allowed for pc in o['pcs']),name
 assert int(o['starting_rsp'],16)%16==8 and o['starting_mxcsr']=='0x1f80'
 assert len(o['stub_trace'])==2 and all(q.endswith(':-1') or q.endswith(':0') for q in o['stub_trace'])
 if name in expected:
  ret,index=expected[name]
  assert not o['faults'] and o['end_pc']=='0x62000000' and o['rax']==ret,name
  assert int(o['ending_rsp'],16)==int(o['starting_rsp'],16)+8
  assert o['nonvolatile_before']==o['nonvolatile_after'],name
  assert (not o['cell_reads']) if index is None else len(o['cell_reads'])==1 and o['cell_reads'][0]['index']==index
  for q in o['cell_reads']:
   assert q['size']==2 and q['pc']=='0x38402c' and int(q['address'],16)==int(o['table'],16)+2*index
 else:
  index=faults[name]
  assert o['end_pc']=='0x38402c' and o['faults']==[['memr',int(o['table'],16)+2*index,2]],name
  assert o['rax']==index and not o['cell_reads'] # residual register, NOT a return
 summary.append(dict(name=name,index=index,completed=name in expected,
     returned=o['rax'] if name in expected else None,fault=o['faults']))
# Geometry and point are unchanged in the next-row intervention pair.
a,b=cases['x-upper-equal'],cases['x-upper-equal-next-row-list']
assert a['point_hex']==b['point_hex'] and a['header_hex']==b['header_hex']
at,bt=bytes.fromhex(a['table_hex']),bytes.fromhex(b['table_hex'])
assert at[:8]==bt[:8] and at[10:]==bt[10:] and at[8:10]==b'\x09\0' and bt[8:10]==b'\x11\0'
assert cases['guard-last-cell-control']['cell_reads'][0]['address']=='0x400ffffe'
for axis,site in [('x',0x383FB0),('z',0x383FCE)]:
 o=cases['mutant-'+axis+'-ja-to-jae'];assert o['case']['mutation']==site
 assert ii[hex(site-1)]['bytes'].startswith('0f87') and not o['cell_reads']
v=dict(status='PASS_ISOLATED_ORIGINAL_CODE',cases=14,unmodified_cases=12,disposable_mutations=2,
 actual_returns=11,expected_guard_faults=3,live_cases=0,
 source_sha256=sha((W/'source.json').read_bytes()),raw_sha256=sha((W/'raw.json').read_bytes()),
 observations=summary,cleanup='No native game process/control, no reference/save/config writes; isolated interpreter exited.')
(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS isolated upper-edge controls: 12 unmodified + 2 disposable branch mutants; three expected guard faults are NOT returns/live crashes',flush=True)
