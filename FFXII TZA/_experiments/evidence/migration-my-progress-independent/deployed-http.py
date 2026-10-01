import hashlib, json, sys, urllib.request
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'deployed-01';assert not D.exists(),'Keep original deployed sample';D.mkdir()
raw={'method':'A read-only actual deployed HTTP sample, no restart/write/controller/game control','base':'http://127.0.0.1:8765',
 'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'requests':[],'finished':False,
 'limits':'Bracketed same-generation observations are not an atomic snapshot or loaded-module/PID proof; browser presentation separate'}
try:
 payload={}
 for name,path in (('status-before','/api/status'),('progress','/api/view/progress'),('page','/'),('status-after','/api/status')):
  req=urllib.request.Request(raw['base']+path,method='GET')
  with urllib.request.urlopen(req,timeout=10) as r:data=r.read();status=r.status;headers=dict(r.headers)
  (D/(name+('.html' if name=='page' else '.json'))).write_bytes(data)
  raw['requests'].append({'name':name,'path':path,'status':status,'headers':headers,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  payload[name]=data if name=='page' else json.loads(data)
 a=payload['status-before'];b=payload['status-after'];p=payload['progress'];v=p.get('view');assert v,'No view delivered; not a valid empty progress sample'
 g=[a['generation'],p['meta']['generation'],b['generation']];assert len(set(g))==1,'Generation moved during sample; mixed sample cannot pass'
 m={x['id']:x for x in v['measures']};sc=v['progress']['scopes'];checks=[]
 for k,s in sc.items():
  key='union-exf' if k=='union_exF' else k
  assert key in m and (s['accepted'],s['total'])==(m[key]['numerator'],m[key]['denominator']);checks.append(key)
 for c in v['progress']['categories']:
  key='cat-'+c['code'];assert (c['accepted'],c['total'])==(m[key]['numerator'],m[key]['denominator']);checks.append(key)
 assert a['required'][0]==b['required'][0]=='progress' and not a['problems'] and not b['problems']
 raw.update(generation=g[0],view_status=v['status'],reported_reader_stale=[a['reader_stale'],b['reader_stale']],
  verified_projection=checks,headline=sc,progress_measured=v['progress']['measured'],gaps=v['progress']['gaps'],reconstruction=v['progress']['reconstruction'],
  required=a['required'],server_progress_status=[a['views']['progress'],b['views']['progress']],
  selected_drilldown=next(c for c in v['progress']['categories'] if c['total'] and c.get('items')),
  served_page_limit='Raw HTML retained, not rendered screenshot/browser interaction',finished=True)
except BaseException as e:raw['fatal']={'type':type(e).__name__,'reason':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('DEPLOYED_PROGRESS_HTTP_SAMPLE',raw['generation'],raw['server_progress_status'],raw['progress_measured'],'reader_stale',raw['reported_reader_stale'],flush=True)
