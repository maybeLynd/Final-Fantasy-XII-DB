"""Acquire exact original repair source and bounded diff with checked Git results."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rev='06d817762e31d05bfe5db91f572576102143cd50'
old='87c7561de'
path='Database/Tools/analysis-kit/gfz-scripts/generation.py'
for label,argv,name in [('source',['git','show',rev+':'+path],'generation.py'),('diff',['git','diff',old,rev,'--',path],'original-diff.patch')]:
    if (P/(label+'.receipt.json')).exists():raise RuntimeError('immutable acquisition exists')
    p=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
    (P/(label+'.stdout')).write_bytes(p.stdout);(P/(label+'.stderr')).write_bytes(p.stderr)
    r={'argv':argv,'exit':p.returncode,'terminal':True,'exception':None,'driver_sha256':sha(Path(__file__)),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
    (P/(label+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n')
    if p.returncode or p.stderr or not p.stdout:raise RuntimeError('required Git acquisition failed/incomplete: '+label)
    (P/name).write_bytes(p.stdout)
print(json.dumps({'source_commit':rev,'source_sha256':sha(P/'generation.py'),'diff_sha256':sha(P/'original-diff.patch'),'method':'exact original host source; no device/restore/game I/O'}))
