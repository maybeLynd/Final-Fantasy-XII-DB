import ast, hashlib, json, subprocess, sys, traceback, urllib.request
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 assert not (W/'identity.json').exists(), 'Write-once identity preflight'
 src=Path('Database/Tools/dashboard/server.py');before=sha(src);shipped=src.read_bytes()
 (W/'server-source.py').write_bytes(shipped)
 rows=[]
 for name,path in [('shell','/'),('status','/api/status')]:
  url='http://127.0.0.1:8765'+path
  with urllib.request.urlopen(url,timeout=8) as r:
   body=r.read();headers=dict(r.headers);status=r.status
  (W/('http-'+name+'.bin')).write_bytes(body)
  rows.append({'url':url,'status':status,'headers':headers,'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'file':'http-'+name+'.bin','captured_after_response':datetime.now(timezone.utc).isoformat()})
  assert status==200 and body
 tree=ast.parse(shipped.decode('utf-8'));page=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAGE' for t in n.targets))
 expected=ast.literal_eval(page).encode('utf-8');assert expected==(W/'http-shell.bin').read_bytes(), 'Served PAGE does not match captured current source'
 status=json.loads((W/'http-status.bin').read_bytes());assert isinstance(status,dict) and 'generation' in status
 assert sha(src)==before
 q=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True);assert q.returncode==0 and not q.stderr
 identity={'method':'HOST_BROWSER','head':q.stdout.strip(),'source_path':src.as_posix(),'source_sha256':before,'driver_sha256':sha(Path(__file__)),'python':sys.executable,'version':sys.version,'HTTP':rows,'status_generation':status['generation'],'source_PAGE_equal':True,'limits':'Current source and HTTP bytes only; no loaded server-module/PID/dependencies/browser-build or atomic browser/HTTP identity. No server started/restarted, no FF12. HTTP state may move before UI.'}
 (W/'identity.json').write_text(json.dumps(identity,indent=2)+'\n');print(json.dumps(identity,indent=2))
if __name__=='__main__':
 try:run()
 except BaseException:
  (W/'preflight-failure.txt').write_text(traceback.format_exc());raise
