import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent
E=Path('Database/FFXII TZA/_experiments/evidence')
P=E/'access-producer-default';P.mkdir(exist_ok=False)
for n in ('PLAN.md','README.md','delivery.md','inspection.json','result.json','run.py','check.py','inventory.py','claim-before-lowercase-keys.py','private-capture-before.py','original-capture.py'):
 shutil.copyfile(W/n,P/n)
shutil.copyfile(W.parent/'matrix-buffer-alias/capture.py',P/'capture.py')
R=P/'retained';R.mkdir()
for src,name in [(E/'matrix-buffer-alias/source.json','original-source.json'),(E/'procedural-mode-cost/matrix-buffer-alias-access-correction.json','correction.json'),(E/'procedural-mode-cost/operand_direction.py','operand_direction.py'),(E/'procedural-mode-cost/retained/reg_tracking.py','reg_tracking.py')]:shutil.copyfile(src,R/name)
members=[dict(path=x.relative_to(P).as_posix(),bytes=x.stat().st_size,sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in sorted(P.rglob('*')) if x.is_file()]
assert members
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Producer controls and dependency inventory only; independent acceptance and canonical ORACLE sealing not claimed. Original matrix/procedural packets unchanged.'),indent=2)+'\n')
print('Frozen additive default-producer receipt',len(members),'members; originals unchanged')
