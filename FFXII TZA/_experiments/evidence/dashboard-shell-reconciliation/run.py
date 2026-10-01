import json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;f=W/'capture-terminal.json';assert not f.exists();q=subprocess.run([sys.executable,'-B',str(W/'capture.py')],capture_output=True,text=True,timeout=45);f.write_text(json.dumps({'argv':q.args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True},indent=2)+'\n');assert q.returncode==0 and not q.stderr,(q.returncode,q.stderr);print(q.stdout.strip())
