"""One real CLI prerequisite refusal; reuse the already valid positive proof."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
driver=P/'prove-ko-release-partition.py';pin=hashlib.sha256(driver.read_bytes()).hexdigest()
positive=json.loads((P/'result-ko-release-partition-02.json').read_text())
status=json.loads((P/'prove-ko-release-partition-02.status.json').read_text())
if positive.get('producer_complete') is not True or positive.get('driver_sha256')!=pin or status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status.get('driver_sha256')!=pin:raise ValueError('Current positive prerequisite absent')
D=P/'ko-release-status-control-01';D.mkdir()
st=json.loads((P/'capture-ko-release-01.status.json').read_text());st['exit']=1
fake=D/'failed-upstream.json';fake.write_text(json.dumps(st,indent=2))
out=D/'refused-result.json'
argv=[sys.executable,'-B',str(driver),str(out),str(fake)]
r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
(D/'stdout').write_bytes(r.stdout);(D/'stderr').write_bytes(r.stderr)
receipt=dict(argv=argv,driver_sha256=pin,terminal=True,exit=r.returncode,result_exists=out.exists(),method='Labelled disposable failed capture-status input to the actual producer CLI; source/game untouched')
(D/'receipt.json').write_text(json.dumps(receipt,indent=2))
if r.returncode!=1 or out.exists() or b'required capture failed/incomplete' not in r.stderr:raise ValueError('Upstream failure did not refuse downstream evidence')
(D/'control-result.json').write_text(json.dumps(dict(producer_complete=True,status='ACTUAL_CLI_FAILED_UPSTREAM_REFUSED',positive_reused_sha256=hashlib.sha256((P/'result-ko-release-partition-02.json').read_bytes()).hexdigest(),receipt=receipt),indent=2))
print('Actual failed upstream exits1/no result; existing positive02 reused, no native/game run.')
