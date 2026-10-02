"""Finite checked invocation; an upstream failure cannot produce downstream PASS."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'ov42-interpreter-transfer'
name,tag,*args=sys.argv[1:];driver=P/name;out=P/(tag+'.stdout');err=P/(tag+'.stderr');status=P/(tag+'.status.json')
if any(x.exists() for x in [out,err,status]):raise RuntimeError('immutable invocation receipt exists')
z=dict(terminal=False,exit=None,exception=None,driver=name,driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest(),argv=args,start=time.time())
try:
 r=subprocess.run([sys.executable,'-B',str(driver),*args],capture_output=True,timeout=45)
 out.write_bytes(r.stdout);err.write_bytes(r.stderr);z.update(terminal=True,exit=r.returncode)
except BaseException as e:
 z.update(terminal=True,exception=repr(e));out.write_bytes(b'');err.write_bytes(str(e).encode())
finally:
 z['end']=time.time();status.write_text(json.dumps(z,indent=2)+'\n')
print(json.dumps(z))
if z['exit']!=0 or z['exception'] is not None:sys.exit(1)
