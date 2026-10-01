import hashlib,json,re,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
# Scope is the production scripts in ASTRA's root and immediate package folders.
# Excluded copies are immutable history/dependencies, not current entry points.
root=W.parent
files=list(root.glob('*.py'))
for d in root.iterdir():
 if d.is_dir() and d.name not in ('python-libs','__pycache__',W.name): files.extend(d.glob('*.py'))
matches=[]
for p in sorted(files):
 raw=p.read_bytes();text=raw.decode('utf-8-sig',errors='replace')
 lines=[dict(line=i,text=s) for i,s in enumerate(text.splitlines(),1) if re.search(r'\b(?:o|op)\.access\b|CS_AC_|memory_role\(',s)]
 if lines: matches.append(dict(path=p.as_posix(),sha256=sha(raw),lines=lines))
pub=Path('Database/FFXII TZA/_experiments/evidence')
original=pub/'matrix-buffer-alias'
assert subprocess.check_output(['git','rev-parse','58bd6303f:'+(original/'source.json').as_posix()],text=True).strip()
pre=original/'capture.py'
(W/'original-capture.py').write_bytes(pre.read_bytes())
private=root/'matrix-buffer-alias/capture.py'
assert private.read_bytes().replace(b'\r\n',b'\n')==pre.read_bytes().replace(b'\r\n',b'\n')
(W/'private-capture-before.py').write_bytes(private.read_bytes())
names=['matrix-buffer-alias','procedural-mode-cost','nav-grid-quantization','authored-grid-shape','nav-upper-bound-admission','postmultiply-order-alias','nav-conversion-domain','scaled-random-float-order','workbench-depth-target-alias','scaled-random-range-boundary','crt-fdclass-native-dependency','matrix-consumer-identity-control']
pins=[]
for n in names:
 p=pub/n
 manifest=json.loads((p/'manifest.json').read_text());assert manifest['members']
 for m in manifest['members']:
  raw=(p/m['path']).read_bytes();assert len(raw)==m['bytes'] and sha(raw)==m['sha256'],(n,m['path'])
 pins.append(dict(package=n,manifest_sha256=sha((p/'manifest.json').read_bytes()),members=len(manifest['members'])))
b=json.loads(Path('Database/FFXII TZA/_index/_inbox/TEAM.json').read_text())
tasks=[{k:t.get(k) for k in ('id','status','assigned_to','result_refs','checkpoint')} for t in b['tasks'] if t['id'].startswith('ASTRA-') and any(k in t['id'] for k in ('MATRIX','POSTMULTIPLY','NAV-GRID','AUTHORED-GRID','NAV-UPPER','CONVERSION-DOMAIN','PROCEDURAL','PINNED-ACCESS','SCALED-RANDOM','WORKBENCH-DEPTH','FDCLASS'))]
(W/'inspection.json').write_text(json.dumps(dict(board_revision=b['revision'],epoch=b['recovery_epoch'],source_search_scope='ASTRA root and immediate production package .py files; retained/historical/publication/dependency subtrees excluded; not an exhaustive whole-repository certification',searched_files=len(files),matches=matches,immutable_manifest_integrity=pins,tasks=tasks,external_audit_limit='User-supplied external audit 119 members / 9 ranges establishes its integrity check; its 26 assertions are external corroboration, not ASTRA tests. Exact external audit artifact not located in bounded primary review paths; do not silently substitute a different manifest set.'),indent=2)+'\n')
print('INSPECTED production entry points and immutable manifests; matched paths:')
for x in matches:print(x['path'])
