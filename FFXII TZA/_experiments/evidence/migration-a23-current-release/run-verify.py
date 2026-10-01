"""Record the actual generation verifier child exit and final result bytes."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
receipt=W/'verify-terminal.json'
assert not receipt.exists(),'Preserve prior terminal receipt'
driver=W/'verify-captured-generation.py';argv=[sys.executable,'-B',str(driver),'--write-result']
p=subprocess.run(argv,capture_output=True,text=True)
record={'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,
        'terminal':True,'driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest()}
receipt.write_text(json.dumps(record,indent=2)+'\n')
assert p.returncode==0 and not p.stderr and json.loads(p.stdout)==json.loads((W/'verify-result.json').read_bytes())
print('CAPTURED_GENERATION_VERIFIED_PROCESS',json.loads(p.stdout)['generation'])
