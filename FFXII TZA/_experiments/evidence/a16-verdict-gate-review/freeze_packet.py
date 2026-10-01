"""Freeze the assigned independent gate review, including original failure."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;OUT=W/'frozen-ready'
if OUT.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'actual-cases-02/result.json').read_text());status=json.loads((W/'verification-run-02.status.json').read_text())
if r.get('status')!='VALID_SCOPED_NONAUTHOR_GATE_REVIEW' or r.get('verdict')!='ACCEPT' or r.get('counts')!={'required_invalid':5,'policy_valid':6,'plain':1} or len(r.get('cases',[]))!=12:raise ValueError('incomplete independent case result')
if status.get('exit')!=0 or status.get('driver_sha256')!=sha(W/'verify_finish_gate.py') or r.get('checker_sha256')!=sha(W/'verify_finish_gate.py') or not (W/'verification-run-02.stdout').read_bytes().strip() or (W/'verification-run-02.stderr').read_bytes().strip():raise ValueError('required actual verification invocation failed/stale')
root=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
for name,pin in r['source_sha256'].items():
 if sha(root/'Database/Tools/analysis-kit/gfz-scripts'/name)!=pin:raise ValueError('deployed source moved before freeze')
if list(W.rglob('*.lock')):raise ValueError('private fixture lock remains')
paths=[p.relative_to(W).as_posix() for p in sorted(W.rglob('*')) if p.is_file()]
projected=['Database/FFXII TZA/_experiments/evidence/a16-verdict-gate-review/'+p for p in paths+['manifest.json','.gitattributes']]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('existing native publication path budget exceeded')
OUT.mkdir();(OUT/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in paths:
 target=OUT/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
members=[dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(OUT.rglob('*')) if p.is_file()]
(OUT/'manifest.json').write_text(json.dumps(dict(status='SCOPED_NONAUTHOR_ACCEPT',method='OFFLINE ACTUAL SUPPORTED CLI/API',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native path units',units,'manifest',sha(OUT/'manifest.json'))
