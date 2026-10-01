import hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
c='bff8d55d0053e538360dfabc3631e9a06f0c6f15';pkg='Database/FFXII TZA/_experiments/evidence/nav-upper-bound-admission'
assert subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],capture_output=True).returncode==0
manifest=json.loads(subprocess.check_output(['git','show',c+':'+pkg+'/manifest.json']))
raw=subprocess.check_output(['git','show',c+':'+pkg+'/source.json']);m=next(m for m in manifest['members'] if m['path']=='source.json')
assert len(raw)==m['bytes'] and sha(raw)==m['sha256'];(R/'query-source.json').write_bytes(raw)
old=json.loads(raw);body=next(x for x in old['bodies'] if x['entry']=='0x383f10')
page=Path('Database/FFXII TZA/06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md');pb=page.read_bytes();(R/page.name).write_bytes(pb)
s=dict(method='A dependency-verified retained original body and finite-domain interval proof, no new B/C',reference_commit=c,reference_source=pkg+'/source.json',reference_sha256=sha(raw),exe_sha256=old['exe_sha256'],image_base=old['image_base'],body=body,imports=old['imports'],
 consumer=dict(path=page.as_posix(),sha256=sha(pb),bytes=len(pb),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),
 limits='Parent B fixture/finite classifier stub is retained provenance, NOT native library proof. Current proof scoped to stable finite point/header/binding; original returned AX2 branch only. No repeated upper-edge tests or game operation.')
(W/'source.json').write_text(json.dumps(s,indent=2)+'\n')
print('Retained committed original542B/query import witness and current consumer; A finite domain.',flush=True)
