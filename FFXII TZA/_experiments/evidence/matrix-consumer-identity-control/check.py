"""Validate retained positive/negative identity controls without recapturing."""
import hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'raw.json').read_text());assert s['method'].startswith('A offline')
BASE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert s['reference']['sha256']==BASE and len(s['cases'])==2
deps={d['retained']:d for d in s['dependencies']}
for name,d in deps.items():assert sha((W/'retained'/name).read_bytes())==d['sha256']
a,b=s['cases'];assert a['case']=='canonical-baseline' and b['case']=='wrong-image-identity'
assert a['input_sha256']==BASE and a['differences']==[] and a['patch'] is None
assert b['input_sha256']!=BASE and b['differences']==[0x28] and b['patch']['before']^b['patch']['after']==1
assert a['input_bytes']==b['input_bytes']>0 and a['bodies']==b['bodies']
assert [(x['va'],x['bytes']) for x in a['bodies']]==[('0x217060',235),('0x202b70',31)]
for c in [a,b]:
 assert c['baseline_sha256']==BASE and c['checker_sha256']==deps['alias_check.py']['sha256'] and c['page_sha256']==deps['primitives.md']['sha256']
 assert c['child_returncode']==0 and c['checker_exit_code']==0 and not c['stderr']
 lines=c['stdout'].splitlines();assert len(lines)==6 and lines[-1]=='FAILS 0'
 assert all(x.startswith('PASS ') for x in lines[:-1]) and [x.split()[1] for x in lines[:-1]]==['L1','L2','L3','W1','S']
 assert len(c['file_reads'])==2 and all(x['unchanged'] for x in c['bodies'])
assert s['cleanup']==dict(reference_sha256_after=BASE,driver_unchanged=True,children_exited=True,pc_control='OFF',game_save_config_reference_writes=False,peer_source_writes=False)
result=dict(verdict='CONFIRMED_CONSUMER_IDENTITY_GUARD_GAP',raw_sha256=sha((W/'raw.json').read_bytes()),controls=2,established='Published alias_check.py passes all five obligations on both exact reference and a distinct whole-image identity with unchanged cited bodies. Its own source does not enforce the certified-image identity.',limits='Offline Python checker under labelled supplied-read intervention, no FF12 machine-code run or reference/peer file mutation. Known correct source-body/alias result is not refuted; historical run image identity not inferred either way. No claim of wrong semantic output or native acceptance.',repair_required='Owner pin/check exact expected image identity before decode, preserve native/model distinction, add wrong-identity rejection control and corrected run/procedure receipt; existing independent matrix consumer reviewer must review producer change.')
if '--derive' in sys.argv:
 assert not (W/'manifest.json').exists() and not (W/'result.json').exists();(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
else:assert json.loads((W/'result.json').read_text())==result
if (W/'manifest.json').exists():
 members=json.loads((W/'manifest.json').read_text())['members'];assert members
 assert {p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=W/'manifest.json'}=={d['path'] for d in members}
 for d in members:
  b=(W/d['path']).read_bytes();assert len(b)==d['bytes'] and sha(b)==d['sha256']
print(result['verdict'],'positive baseline and wrong-identity input both passed; no semantic retraction',flush=True)
