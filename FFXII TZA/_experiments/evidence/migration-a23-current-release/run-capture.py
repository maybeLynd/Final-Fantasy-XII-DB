"""Record actual capture subprocess exit, including an incomplete failure."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
receipt=W/'capture-terminal.json'
assert not receipt.exists(),'Preserve prior terminal receipt'
driver=W/'capture.py';argv=[sys.executable,'-B',str(driver)]
p=subprocess.run(argv,capture_output=True,text=True)
receipt.write_text(json.dumps({'argv':argv,'returncode':p.returncode,'stdout':p.stdout,
                               'stderr':p.stderr,'terminal':True,
                               'driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest()},indent=2)+'\n')
print('A23_HTTP_CAPTURE_PROCESS',p.returncode)
if p.returncode!=0:sys.exit(p.returncode)
