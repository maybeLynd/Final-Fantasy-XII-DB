import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text())
producer=W/'capture.py' if (W/'capture.py').exists() else W.parent/'matrix-buffer-alias/capture.py'
assert sha(producer.read_bytes())==r['producer_sha256']
assert sha((W/'run.py').read_bytes())==r['runner_sha256']
fix=json.loads((W/'retained/correction.json').read_text()) if (W/'retained/correction.json').exists() else json.loads(Path('Database/FFXII TZA/_experiments/evidence/procedural-mode-cost/matrix-buffer-alias-access-correction.json').read_text())
default,mutant,blocked=r['observations'];assert [x['case'] for x in r['observations']]==['default','raw_flag_mutant','adapter_blocked']
assert default['exit_code']==0 and default['source']['memory_operands']==fix['memory_operands']
assert default['source']['role_policy']==r['policy']
assert mutant['exit_code']==0 and mutant['producer_sha256']!=default['producer_sha256']
assert mutant['role_differences']==[dict(pc='0x202b79',observed='read',expected='address'),dict(pc='0x202b86',observed='read',expected='write')]
assert blocked['producer_sha256']==default['producer_sha256'] and blocked['exit_code']!=0
assert blocked['source'] is None and not blocked['source_created'] and 'CONTROL_ADAPTER_BLOCKED' in blocked['stderr']
assert r['rmw_control']['central_role']=='rw' and r['rmw_control']['restricted_capture_rejected']
assert r['cleanup']['disposable_directories_removed'] and r['cleanup']['published_matrix_unchanged'] and not r['cleanup']['ff12_launched']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS actual producer receipt, complete corrected rows, legacy mutation and blocked-adapter controls; immutable identity and bounded cleanup. Not independent acceptance.')
