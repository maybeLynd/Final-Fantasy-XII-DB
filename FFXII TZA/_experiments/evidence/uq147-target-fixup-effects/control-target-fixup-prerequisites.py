"""Actual producer CLI control: failed normalization cannot produce an effect proof."""
import hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
D=P/sys.argv[1];D.mkdir()
driver=P/'prove-target-fixup-effects.py'
positive=json.loads((P/'prove-target-fixup-effects-02.status.json').read_text())
if positive.get('terminal') is not True or positive.get('exit')!=0 or positive.get('exception') is not None or positive.get('driver_sha256')!=hashlib.sha256(driver.read_bytes()).hexdigest():raise RuntimeError('Positive actual invocation missing')
source=json.loads((P/'qualify-target-fixup-03.status.json').read_text());source['exit']=1
fake=D/'failed-qualifier.status.json';fake.write_text(json.dumps(source,indent=2))
out=D/'refused-result.json';argv=[sys.executable,'-B',str(driver),str(out),str(fake)]
r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
(D/'stdout').write_bytes(r.stdout);(D/'stderr').write_bytes(r.stderr)
(D/'receipt.json').write_text(json.dumps(dict(argv=argv,terminal=True,exit=r.returncode,driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest()),indent=2))
if r.returncode!=1 or out.exists() or b'required qualifier failed/incomplete' not in r.stderr:raise RuntimeError('Actual failed upstream passed or wrong detector')
(D/'result.json').write_text(json.dumps(dict(producer_complete=True,control='ACTUAL_CLI_REQUIRED_UPSTREAM_FAIL',exit=r.returncode,result_absent=True,positive_receipt='prove-target-fixup-effects-02.status.json',limits='Deliberately failed qualifier receipt; no original/native/live intervention or repeated positive execution'),indent=2))
print('Actual producer rejected failed qualifier: exit1, no result; positive actual run reused')
