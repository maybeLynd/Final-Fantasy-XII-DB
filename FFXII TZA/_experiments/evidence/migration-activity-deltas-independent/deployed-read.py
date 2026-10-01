"""Bounded observation of existing service; no restart, state changes or UI controls."""
import gzip,hashlib,json,sys,time,urllib.request
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];D=W/'deployed-01';assert not D.exists();D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
raw={'method':'A existing deployed repository HTTP/file read observation, not FF12 live evidence','base':'http://127.0.0.1:8765',
     'driver_sha256':sha(Path(__file__).read_bytes()),'requests':[],'files':[],'finished':False,
     'limits':'No atomic snapshot, loaded module/PID certification or browser presentation; activity cache may predate bracketed board. Source fixtures establish discrimination separately.'}
def snapshot(label,path,compress=False):
    t=time.time();data=Path(path).read_bytes();out=D/(label+('.json.gz' if compress else '.json'))
    out.write_bytes(gzip.compress(data,mtime=0) if compress else data)
    raw['files'].append({'label':label,'source_path':str(Path(path).resolve()),'observed_at':t,'bytes':len(data),'sha256':sha(data),'stored':out.name,'compressed':compress})
    return json.loads(data)
try:
    board=ROOT/'Database/FFXII TZA/_index/_inbox/TEAM.json'
    fleet=Path.home()/'.swe2-fleet/watchdog-state.json'
    raw['board_before_revision']=snapshot('board-before',board,True)['revision']
    snapshot('controller-before',fleet)
    for name,path in [('status-before','/api/status'),('activity','/api/activity'),('live','/api/live'),('page','/'),('status-after','/api/status')]:
        t=time.time()
        with urllib.request.urlopen(urllib.request.Request(raw['base']+path,method='GET'),timeout=10) as response:
            data=response.read();status=response.status;headers=dict(response.headers)
        (D/(name+('.html' if name=='page' else '.json'))).write_bytes(data)
        raw['requests'].append({'name':name,'path':path,'before':t,'after':time.time(),'status':status,'headers':headers,'bytes':len(data),'sha256':sha(data)})
    raw['board_after_revision']=snapshot('board-after',board,True)['revision']
    snapshot('controller-after',fleet)
    raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
a=json.loads((D/'activity.json').read_text());s=json.loads((D/'status-before.json').read_text());s2=json.loads((D/'status-after.json').read_text())
print('DEPLOYED_READ_FINISHED','activity',a.get('status'),'generation_bracket',[s.get('generation'),a.get('generation'),s2.get('generation')],
      'reader_stale',[s.get('reader_stale'),s2.get('reader_stale')],'board',[raw['board_before_revision'],a.get('feed',{}).get('board_revision'),raw['board_after_revision']])
