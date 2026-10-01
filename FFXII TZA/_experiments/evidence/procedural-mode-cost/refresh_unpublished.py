"""Refresh this UNPUBLISHED packet only; preserve its first freeze as evidence."""
import hashlib,json,shutil,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent
P=Path('Database/FFXII TZA/_experiments/evidence/procedural-mode-cost')
assert not (W/'publication/commit.txt').exists()
assert subprocess.run(['git','ls-files','--error-unmatch',str(P/'manifest.json')],capture_output=True).returncode!=0,'published packet must stay immutable'
archive=W/'historical-capstone-access/prepublication-v1'
assert not archive.exists(),'do not repeat the refresh without new reviewed preimages'
shutil.copytree(P,archive,ignore=shutil.ignore_patterns('__pycache__'))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
rows=[]; retained=W/'retained/producer-preimages';retained.mkdir(exist_ok=False)
for name in ('arg_extent_scan.py','census_receiver_fixpoint.py','disp_image_census.py','singleton_field_scan.py'):
 p=Path('Database/Tools/analysis-kit/gfz-scripts')/name;raw=p.read_bytes()
 assert b'.access' in raw and b'CS_AC_' in raw
 assert b'op_kind' not in raw and b'reg_tracking' not in raw
 committed=subprocess.check_output(['git','show',head+':'+p.as_posix()])
 shutil.copyfile(p,retained/name)
 rows.append(dict(path=p.as_posix(),sha256=hashlib.sha256(raw).hexdigest(),head=head,
  same_as_head_normalized=raw.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n'),
  dependency_lines=[dict(line=i,text=line) for i,line in enumerate(raw.decode().splitlines(),1) if '.access' in line or 'CS_AC_' in line],
  retained='retained/producer-preimages/'+name))
(W/'producer-dependencies.json').write_text(json.dumps(dict(producers=rows,
 limitation='Specific procedure dependency evidence only. No rerun or bulk output retraction. FRONTIER must assign exact affected-result/consumer checks. Shared reg_tracking.op_kind is already corrected; own capture bypass is fixed by reuse.'),indent=2)+'\n')
names=('PLAN.md','README.md','capture.py','check.py','source.json','validation.json','operand_direction.py','fix_direction.py','check_direction.py','matrix-buffer-alias-access-correction.json','dependency-inspection.json','policy-reuse.json','producer-dependencies.json','refresh_unpublished.py')
for n in names:shutil.copyfile(W/n,P/n)
for n in ('retained','historical-capstone-access'):shutil.copytree(W/n,P/n,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
m=[dict(path=x.relative_to(P).as_posix(),bytes=x.stat().st_size,sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in sorted(P.rglob('*')) if x.is_file() and x!=P/'manifest.json' and '__pycache__' not in x.parts]
assert m and {x['path'] for x in m}=={x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file() and x!=P/'manifest.json' and '__pycache__' not in x.parts}
(P/'manifest.json').write_text(json.dumps(dict(members=m,limits='A only; direct mode sites and additive19 role correction. Pinned existing policy reused; old procedure/freeze preserved. Native callees/live initialization unobserved. No original byte recapture; independent acceptance and owner incorporation required.'),indent=2)+'\n')
print('Refreshed unpublished packet; pinned existing policy, preserved prior freeze and four specific producer dependencies.',len(m),'members',flush=True)
