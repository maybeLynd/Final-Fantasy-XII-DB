import hashlib,json,shutil
from pathlib import Path
w=Path(__file__).resolve().parent
p=Path('Database/FFXII TZA/_experiments/evidence/nav-upper-bound-admission')
p.mkdir(parents=True,exist_ok=True)
for n in ['PLAN.md','README.md','probe.py','executed-driver.py','check.py','source.json','raw.json','validation.json','supplement_probe.py','supplement-source.json','supplement-raw.json']:
 shutil.copyfile(w/n,p/n)
(p/'retained').mkdir(exist_ok=True)
shutil.copyfile(w/'retained/check.py',p/'retained/check.py')
shutil.copytree(w/'historical-incomplete-precondition',p/'historical-incomplete-precondition',dirs_exist_ok=True)
(p/'.gitattributes').write_text('* -text\n')
members=[dict(path=x.relative_to(p).as_posix(),bytes=x.stat().st_size,sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in sorted(p.rglob('*')) if x.is_file() and x.name!='manifest.json' and '__pycache__' not in x.parts]
(p/'manifest.json').write_text(json.dumps(dict(members=members,limits='B full shipping GGRID/BASE/TTEST; disclosed synthetic mesh and finite _fdclass stub. Retained14 equality controls not rerun;3 new negative-origin/MXCSR1F80 controls refute strict-world-bound sufficiency. Rejected interpretation/procedure preserved; computedindices require range. Fixture read/fault only, no native game normal reachability/heap placement/crash/authored occurrence. Initial driver hash recovered after capture, supplemental driver before cases; exact metadata-only enrichment disclosed. Independent/owner acceptance pending.'),indent=2)+'\n')
print('Frozen',len(members),'upper-edge evidence members',flush=True)
