"""One bounded read-only HTTP observation of the deployed dashboard."""
import hashlib, json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
R=W/'raw-http'
assert not R.exists(), 'Preserve prior HTTP capture; inspect before another run'
R.mkdir()
paths=[('/api/status','status-before'),('/','root'),('/api/view/progress','progress'),
       ('/api/view/overview','overview'),('/api/status','status-after')]
observed=[]
for path,name in paths:
    url='http://127.0.0.1:8765'+path
    start=datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(url,timeout=8) as reply:
            body=reply.read();status=reply.status;headers=dict(reply.headers.items())
        (R/(name+'.body')).write_bytes(body)
        observed.append({'name':name,'path':path,'utc_start':start,'status':status,
                         'headers':headers,'bytes':len(body),
                         'sha256':hashlib.sha256(body).hexdigest(),
                         'body_file':'raw-http/'+name+'.body','error':None})
    except Exception as e:
        observed.append({'name':name,'path':path,'utc_start':start,'status':None,
                         'error':type(e).__name__+': '+str(e)})
        break
result={'method':'actual deployed HTTP GET; no server/store mutation',
        'base_url':'http://127.0.0.1:8765','observed':observed,'complete':len(observed)==len(paths)}
if result['complete'] and all(x['status']==200 for x in observed):
    before=json.loads((R/'status-before.body').read_bytes())
    after=json.loads((R/'status-after.body').read_bytes())
    result['generation_before']=before.get('generation')
    result['generation_after']=after.get('generation')
    result['same_generation']=before.get('generation')==after.get('generation')
    result['reader_stale_before']=before.get('reader_stale')
    result['reader_stale_after']=after.get('reader_stale')
    result['problems_before']=before.get('problems')
    result['problems_after']=after.get('problems')
    result['view_states_after']=after.get('views')
else:
    result['same_generation']=False
(W/'capture.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['complete'] and all(x['status']==200 for x in observed),result
assert result['same_generation'],'Generation changed during the bounded HTTP observation'
print(json.dumps({'status':'BOUNDED_HTTP_CAPTURE','generation':result['generation_after'],
                  'views':list(result['view_states_after']),'reader_stale':result['reader_stale_after'],
                  'problems':result['problems_after']}))
