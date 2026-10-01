"""Verify historical incompleteness and exact additive material preservation."""
import hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();r=json.loads((W/'material-publication.json').read_text());c=r['original_commit'];root=r['original_root'];manifest=subprocess.check_output(['git','show',c+':'+root+'/manifest.json']);assert sha(manifest)==r['original_manifest_sha256'];old=json.loads(manifest)['members'];present=r['original_path_members'];aux=r['relocated_auxiliary'];assert len(old)==47 and len(present)==46 and r['old_strict_manifest_valid'] is False
if '--fault-ignore-missing-member' in sys.argv:assert len(present)==len(old),'Historical incomplete manifest falsely declared complete'
assert set(x['path'] for x in old)==set(x['path'] for x in present)|{aux['original']['path']}
for m in present:
 b=subprocess.check_output(['git','show',c+':'+root+'/'+m['path']]);assert sha(b)==m['sha256'] and len(b)==m['bytes'];assert m==next(x for x in old if x['path']==m['path'])
missing=aux['original'];assert '__pycache__' in missing['path'] and missing['path'].endswith('.pyc') and subprocess.run(['git','cat-file','-e',c+':'+root+'/'+missing['path']],capture_output=True).returncode!=0
b=(W/aux['new']).read_bytes();assert sha(b)==missing['sha256'] and len(b)==missing['bytes'] and missing==next(x for x in old if x['path']==missing['path'])
assert all(any(m['path']==p for m in present) for p in ['raw.json','result.json','check.py','retained/reg_tracking.py','retained/resolver591.bin','retained/evctrl.ebp','retained/evctrl.dbg','retained/evctrl.sbn'])
print('PASS_CORRECTED_PUBLICATION65 original strict manifest invalid; all declared bytes preserved via46 original committed members +1 exact inert auxiliary relocation; no semantic acceptance',flush=True)
