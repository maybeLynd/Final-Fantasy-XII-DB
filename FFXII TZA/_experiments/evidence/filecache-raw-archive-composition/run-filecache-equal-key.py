"""Finite checked producer invocation; preserves status/output/exception."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
W=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('driver');p.add_argument('tag');p.add_argument('args',nargs=argparse.REMAINDER);a=p.parse_args()
driver=W/a.driver
paths=[W/(a.tag+ext) for ext in ['.stdout','.stderr','.status.json']]
if any(x.exists() for x in paths):raise ValueError('immutable invocation receipts exist')
status=dict(driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),command=[sys.executable,str(driver),*a.args],terminal=False,exit=None)
try:
    r=subprocess.run(status['command'],cwd=W,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
    paths[0].write_bytes(r.stdout);paths[1].write_bytes(r.stderr)
    status.update(terminal=True,exit=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr))
except Exception as e:
    status['exception']=repr(e)
    paths[0].write_bytes(b'');paths[1].write_bytes(repr(e).encode())
paths[2].write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
print(json.dumps(status))
sys.exit(status['exit'] if status['terminal'] else 2)
