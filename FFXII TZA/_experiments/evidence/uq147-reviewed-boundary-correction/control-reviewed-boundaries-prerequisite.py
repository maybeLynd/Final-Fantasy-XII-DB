"""Actual changed producer CLI must refuse an upstream FAIL without a result."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
q=P/'reviewed-boundaries-failed-prerequisite-01.json'
result=P/'reviewed-boundaries-refused-output-01.json'
report=P/'reviewed-boundaries-prerequisite-control-01.json'
if any(p.exists() for p in (q,result,report)):raise ValueError('fresh control paths required')
q.write_text(json.dumps(dict(terminal=True,exit=1,exception=None,label='Synthetic failed qualification receipt')))
driver=P/'prove-reviewed-local-boundaries.py'
argv=[sys.executable,'-B',str(driver),result.name,q.name]
r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
(P/'reviewed-boundaries-refusal-01.stdout').write_bytes(r.stdout)
(P/'reviewed-boundaries-refusal-01.stderr').write_bytes(r.stderr)
if r.returncode!=1 or result.exists() or b'successful prerequisite required' not in r.stderr:raise ValueError('failed upstream suppression or wrong detector')
positive=P/'prove-reviewed-local-boundaries-01.status.json'
st=json.loads(positive.read_text())
if st.get('terminal') is not True or st.get('exit')!=0 or st.get('exception') is not None or st.get('driver_sha256')!=hashlib.sha256(driver.read_bytes()).hexdigest():raise ValueError('required actual positive absent')
report.write_text(json.dumps(dict(argv=argv,terminal=True,exit=r.returncode,result_absent=True,positive_reused_sha256=hashlib.sha256(positive.read_bytes()).hexdigest(),limits='One actual CLI negative; retained positive reused. Not native execution.'),indent=2)+'\n')
print('Required upstream FAIL propagated: exit1/no result; actual positive reused.')
