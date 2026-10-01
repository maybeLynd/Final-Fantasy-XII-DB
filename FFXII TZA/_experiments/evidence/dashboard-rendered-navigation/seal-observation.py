import ast, hashlib, json, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
C=W/'capture-01'
assert (C/'control-log.json').exists()
assert not (W/'identity.json').exists(), 'Write-once; do not recapture to repair interpretation'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr, (args,p.returncode,p.stderr)
 return p.stdout.strip()
source=Path('Database/Tools/dashboard/server.py'); raw=source.read_bytes()
tree=ast.parse(raw.decode('utf-8-sig'))
page=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAGE' for t in n.targets))
(W/'server-source.py').write_bytes(raw)
receipts=[]
for stem,url in [('root','http://127.0.0.1:8765/'),('status','http://127.0.0.1:8765/api/status')]:
 started=datetime.now(timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=10) as r:
  data=r.read(); code=r.status; headers=list(r.headers.items())
 assert code==200 and data
 (W/(stem+'-after-browser.raw')).write_bytes(data)
 receipts.append(dict(url=url,started=started,finished=datetime.now(timezone.utc).isoformat(),status=code,headers=headers,bytes=len(data),sha256=sha(data)))
identity=dict(method='HOST_BROWSER, then read-only HTTP and static source comparison',head=git('rev-parse','HEAD'),source_path=source.as_posix(),source_last_commit=git('log','-1','--format=%H','--',source.as_posix()),source_sha256=sha(raw),source_git_blob=git('hash-object','--no-filters',str(source)),page_matches_later_http=(W/'root-after-browser.raw').read_bytes()==page.encode(),http_after_browser=receipts,python=sys.executable,python_version=sys.version,tool='mcp__cua_repl.js; browser1 IAB; owned tab2; read-only local navigation',limits=['HTTP receipts obtained after browser closure; not atomic with UI','PAGE byte equality does not identify loaded Python module, process or dependencies','No game, host-controller or adapter acceptance'])
assert identity['page_matches_later_http']
(W/'identity.json').write_bytes((json.dumps(identity,indent=2)+'\n').encode())
print('SEALED_EXISTING_BROWSER_OBSERVATIONS_NO_UI_REPLAY')
