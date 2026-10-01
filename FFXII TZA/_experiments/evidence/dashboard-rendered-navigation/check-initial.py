import ast, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
def check(w):
 c=w/'capture-01'; log=json.loads((c/'control-log.json').read_bytes()); ident=json.loads((w/'identity.json').read_bytes())
 assert log['ownedTab']=='2' and log['browser']['id']=='1'
 assert log['cleanup']=={'closeReturned':True,'ownedTabListedAfter':False}
 assert json.loads((c/'07-tabs-after-close.json').read_bytes())==[]
 assert len(log['actions'])==4 and [a['status'] for a in log['actions']]==['REFUSED_STALE_IDENTIFIER','OVERVIEW_HEADING_OBSERVED','AX_INTERMEDIATE_THEN_ACTIVITY_DOM_OBSERVED','NO_MATCHES_REFUSED']
 assert 'heading My Progress PARTIAL' in (c/'00-progress-ax.txt').read_text()
 assert 'heading Overview - where the whole database stands OK' in (c/'03-overview-ax.txt').read_text()
 assert 'heading "Agent Activity" [level=2]' in (c/'05-activity-dom.txt').read_text()
 assert 'ASTRA-DASHBOARD-RENDERED-NAVIGATION' in (c/'05-activity-dom.txt').read_text()
 assert 'My Progress STALE' in (c/'05-activity-dom.txt').read_text()
 final=(c/'06-final-dom.txt').read_text()
 assert 'My Progress PARTIAL' in final and 'heading "Agent Activity" [level=2]' in final
 for n in ('01-input-failure.txt','06-return-input-failure.txt'): assert (c/n).stat().st_size>100
 for n in ('00-progress.png','03-overview.png','05-activity.png','06-final.png'):
  assert (c/n).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
 source=(w/'server-source.py').read_bytes()
 assert hashlib.sha256(source).hexdigest()==ident['source_sha256']
 page=next(ast.literal_eval(n.value) for n in ast.parse(source.decode('utf-8-sig')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAGE' for t in n.targets))
 assert (w/'root-after-browser.raw').read_bytes()==page.encode() and ident['page_matches_later_http']
 for receipt,stem in zip(ident['http_after_browser'],('root','status'),strict=True):
  data=(w/(stem+'-after-browser.raw')).read_bytes()
  assert receipt['status']==200 and receipt['bytes']==len(data) and receipt['sha256']==hashlib.sha256(data).hexdigest()
 return {'result':'SCOPED_OBSERVATIONS_SUPPORTED_RETURN_TRANSITION_UNPROVED','navigation':'Progress baseline -> Overview -> Activity observed','refused_inputs':2,'cleanup':'owned tab closed; absent from inventory','source':'later HTTP PAGE byte match only','limits':'No full A17/M3, totals, taxonomy, adapters, deployment or FF12 acceptance. Evidence author review pending.'}
if __name__=='__main__': print(json.dumps(check(Path(__file__).resolve().parent),indent=2))
