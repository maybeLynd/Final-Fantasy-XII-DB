import hashlib,json,re,sys,urllib.request
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'deployed-01';O=W/'deployed-ui-02'
assert not O.exists(),'Preserve observed HTTP/UI generations';O.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ax=(D/'browser-expanded.txt').read_text();before=(D/'browser-before.txt').read_text()
gen=re.search(r'generation (g\d+T\d+Z-[a-z0-9]+)',ax).group(1)
assert gen in before and '▾ World & maps' in ax
ids=re.findall(r'text ((?:DA|DD):[^\r\n]+)',ax)
assert len(ids)==len(set(ids))==16 and sum(x.startswith('DA:') for x in ids)==10
assert '125 function dispositions' in ax and '10 documents with a named falsification pass' in ax
assert 'RESTART REQUIRED' not in ax
r={'method':'A actual rendered local dashboard observation through CUA IAB; HTTP binding read-only',
 'tool':'mcp__cua_repl.js: getAXState, click observed row251, getAXStateAndScreenshot, close',
 'base':'http://127.0.0.1:8765','driver_sha256':sha(__file__),'requests':[],'finished':False,
 'browser_generation':gen,'category':'W','displayed_remaining_ids':ids,
 'closed':'Agent-created tab close returned successfully; no native PC/game control used',
 'files':{n:{'sha256':sha(D/n),'bytes':(D/n).stat().st_size} for n in ('browser-before.txt','browser-expanded-diff.txt','browser-expanded.txt','browser-expanded.png')},
 'limits':'AX and screenshot establish presentation; HTTP collected afterwards, no atomicity or loaded-module/PID proof. Earlier deployed-01 stale reader remains historical. No game/no production writes.'}
try:
 docs={}
 for name,path in (('status-before','/api/status'),('progress','/api/view/progress'),('status-after','/api/status')):
  start=datetime.now(timezone.utc).isoformat()
  with urllib.request.urlopen(r['base']+path,timeout=10) as q:data=q.read();status=q.status;headers=dict(q.headers)
  (O/(name+'.json')).write_bytes(data);docs[name]=json.loads(data)
  r['requests'].append({'name':name,'path':path,'status':status,'headers':headers,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat()})
 a,b,p=docs['status-before'],docs['status-after'],docs['progress']
 r['http_generations']=[a['generation'],p['meta']['generation'],b['generation']]
 assert len(set(r['http_generations']))==1 and r['http_generations'][0]==gen,'Do not bind UI to a different generation'
 assert not a['problems'] and not b['problems'] and a['required'][0]=='progress'
 c=next(x for x in p['view']['progress']['categories'] if x['code']=='W')
 want=[x['key'] for x in c['items']]
 assert set(ids)==set(want),(ids,want)
 assert (c['accepted'],c['total'])==(690,831)
 r.update(reported_reader_stale=[a['reader_stale'],b['reader_stale']],category=c,
  view_status=p['view']['status'],progress=p['view']['progress'],status_keys=sorted(a),finished=True)
except BaseException as e:r['fatal']={'type':type(e).__name__,'reason':str(e)};raise
finally:(O/'raw.json').write_text(json.dumps(r,indent=2)+'\n')
print('BROWSER_GENERATION_BOUND',gen,'reader_stale',r['reported_reader_stale'],'16 displayed items; tab closed',flush=True)
