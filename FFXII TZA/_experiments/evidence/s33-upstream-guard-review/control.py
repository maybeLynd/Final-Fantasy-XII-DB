"""Focused receipt-checker controls for the demonstrated upstream-failure class."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;F=P/'controls-01';F.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for label in ['positive','failed-review','missing-positive-observation']:
 d=F/label
 shutil.copytree(P,d,ignore=shutil.ignore_patterns('controls-01','control-*.status.json','control-*.stdout','control-*.stderr'))
 if label=='failed-review':
  p=d/'review-01.status.json';z=json.loads(p.read_text());z['exit']=1;p.write_text(json.dumps(z))
 elif label=='missing-positive-observation':(d/'case-positive.stdout').unlink()
 argv=[sys.executable,'-B',str(P/'check.py'),str(d)]
 r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
 (d/'checker.stdout').write_bytes(r.stdout);(d/'checker.stderr').write_bytes(r.stderr)
 valid=(r.returncode==0 and b'VERIFIED scoped S33 admission repair' in r.stdout and not r.stderr) if label=='positive' else (r.returncode!=0 and b'VERIFIED scoped S33 admission repair' not in r.stdout)
 row=dict(case=label,argv=argv,terminal=True,exit=r.returncode,exception=None,checker_sha256=sha(P/'check.py'),expected_behavior_observed=valid,
          stdout_sha256=sha(d/'checker.stdout'),stderr_sha256=sha(d/'checker.stderr'))
 (d/'checker.status.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
complete=len(rows)==3 and all(x['expected_behavior_observed'] for x in rows)
(P/'control-result-01.json').write_text(json.dumps(dict(complete=complete,cases=rows,limits='Receipt-checker controls, not native or game cases'),indent=2)+'\n')
print(json.dumps(dict(complete=complete,cases=3)))
raise SystemExit(0 if complete else 1)
