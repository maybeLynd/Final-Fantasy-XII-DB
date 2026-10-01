"""Bounded actual CLI receipts; never hide an upstream exception/nonzero exit."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
tag=sys.argv[1];driver=P/sys.argv[2];args=sys.argv[3:]
paths=[P/(tag+s) for s in ['.status.json','.stdout','.stderr']]
if any(p.exists() for p in paths):raise RuntimeError('fresh receipt required')
argv=[sys.executable,'-B',str(driver),*args];row={'argv':argv,'driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest(),'interpreter_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'terminal':False,'exit':None,'exception':None}
try:
 r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
 paths[1].write_bytes(r.stdout);paths[2].write_bytes(r.stderr);row.update(terminal=True,exit=r.returncode)
except Exception as e:
 row['exception']=repr(e);paths[1].write_bytes(b'');paths[2].write_text(repr(e))
paths[0].write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row));raise SystemExit(0 if row['terminal'] and row['exit']==0 and row['exception'] is None else 1)
