import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent
assert team.board_status(team.BOARD)[0]
b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-SAVE-POINTER-RECORD-ALIAS')
assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'result.json').exists(),'Do not repeat a settled derivation'
sha=lambda b:hashlib.sha256(b).hexdigest()
P=Path('Database/FFXII TZA/_experiments/evidence/workbench-depth-target-alias')
m=json.loads((P/'manifest.json').read_text());x=next(x for x in m['members'] if x['path']=='source.json');raw=(P/'source.json').read_bytes()
assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.json').write_bytes(raw);(R/'parent-manifest.json').write_bytes((P/'manifest.json').read_bytes())
s=json.loads(raw)
assert s['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
body={z['name']:z for z in s['bodies']}
for name,size,h in [('save',89,'ebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda'),('restore',66,'5bb9d143a12bf8959ae1c75d5f7245c4b1081d9ae3432095ebfd253953ec253b')]:
 z=body[name];r=bytes.fromhex(z['raw_hex']);assert len(r)==size and sha(r)==h
 assert b''.join(bytes.fromhex(i['bytes']) for i in z['instructions'])==r
ii={int(i['pc'],16):i for z in body.values() for i in z['instructions']}
for pc,h in [(0x36D969,'498900'),(0x36D974,'0f1000'),(0x36D977,'410f1141f0'),(0x36D8FE,'498b84c1000ada02'),(0x36D906,'410f1084c90008da02'),(0x36D90F,'0f1100')]:assert ii[pc]['bytes']==h
assert ii[0x36D953]['rip_targets']==['0x2ec0800'] and ii[0x36D95A]['rip_targets']==['0x2ec0a00']
contract=Path('Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md')
(R/'contract.md').write_bytes(contract.read_bytes())
POINTERS=0x2EC0A00;VALUES=0x2EC0800;DEPTH=0x22D8F08
def conditional(target,record_first=True):
 mem={}
 def put(a,v):mem.update({a+i:q for i,q in enumerate(v)})
 def get(a,n):return bytes(mem[a+i] for i in range(n))
 for a in (POINTERS,VALUES,target):put(a,bytes(range(0x10,0x20)))
 put(DEPTH,struct.pack('<I',0));entry=get(target,16)
 # Original order at969,974,977; alternative order is a distinguishing
 # conditional hypothesis, not an execution/mutation of shipping instructions.
 if record_first:put(POINTERS,struct.pack('<Q',target))
 snap=get(target,16)
 if not record_first:put(POINTERS,struct.pack('<Q',target))
 put(VALUES,snap);put(DEPTH,struct.pack('<I',1))
 after_save=get(target,16)
 dest=struct.unpack('<Q',get(POINTERS,8))[0];assert dest==target
 put(dest,get(VALUES,16));put(DEPTH,struct.pack('<I',0))
 return dict(target=hex(target),count=1,initial_depth=0,counter_disjoint=not(target<DEPTH+4 and DEPTH<target+16),entry_hex=entry.hex(),snapshot_hex=snap.hex(),after_save_hex=after_save.hex(),after_restore_hex=get(target,16).hex(),entry_restored=get(target,16)==entry,final_depth=0,method='conditional transfer from original instruction order, not original-code execution')
cases=[dict(name='pointer-record-self-target',**conditional(POINTERS)),dict(name='disjoint-target',**conditional(0x22D8F90)),dict(name='value-slot-self-copy',**conditional(VALUES)),dict(name='competing-load-before-record',**conditional(POINTERS,False))]
assert not cases[0]['entry_restored'] and all(c['entry_restored'] for c in cases[1:])
assert all(c['counter_disjoint'] and c['final_depth']==0 for c in cases)
result=dict(method='A STATIC_CONDITIONAL; no B/C',source_sha256=sha(raw),contract_sha256=sha((R/'contract.md').read_bytes()),driver_sha256=sha(Path(__file__).read_bytes()),cases=cases,established='Save stores its pointer record before target load. A count1 target at its own pointer slot changes first8 target bytes before snapshot; immediate Restore cannot recover entry bytes under the stated valid/no-counter-overlap state.',limits='No ordinary caller or live initialization/ownership claim; conditional count1 only, no whole alias partition or universal malformed safety. Load-time snapshot remains exact, entry-time blanket postcondition needs a noninterference precondition or precise timing.',consumer='OPUS/SWE2-CONTRACT transform Save/Restore contract; FABLE workbench page',cleanup='Retained original evidence read-only, private artifact writes only; PC OFF, game/reference/save/config untouched')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Derived original record-store-before-load, pointer self-target versus disjoint/value-self controls; A conditional, not native/live')
