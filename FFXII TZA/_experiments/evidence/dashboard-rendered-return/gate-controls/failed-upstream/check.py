import ast, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def check(w):
 t=load(w/'preflight-terminal.json')
 if '--fault-upstream-failed' in sys.argv:t['returncode']=1
 assert t['terminal'] is True and t['returncode']==0 and not t['stderr'],'Required preflight failed'
 assert t['driver_sha256']==sha(w/'preflight.py')
 i=load(w/'identity.json');assert i==json.loads(t['stdout']) and i['driver_sha256']==sha(w/'preflight.py')
 assert sha(w/'server-source.py')==i['source_sha256']
 tree=ast.parse((w/'server-source.py').read_text('utf-8'))
 page=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='PAGE' for x in n.targets))
 assert ast.literal_eval(page).encode()==(w/'http-shell.bin').read_bytes()
 for x in i['HTTP']:assert x['status']==200 and x['bytes']>0 and sha(w/x['file'])==x['sha256'] and (w/x['file']).stat().st_size==x['bytes']
 status=load(w/'http-status.bin');assert status['generation']==i['status_generation']
 index=load(w/'raw-capture-index.json');assert len(index['members'])==7
 for x in index['members']:assert sha(w/x['path'])==x['sha256'] and (w/x['path']).stat().st_size==x['bytes']
 c=w/'capture-01';log=load(c/'control-log.json')
 assert log['method']=='HOST_BROWSER' and log['url']=='http://127.0.0.1:8765/' and log['ownedTab']=='3' and log['background'] is True
 assert len(log['actions'])==2 and all(a['toolDispatchReturned'] is True and 'error' not in a for a in log['actions'])
 setup,ret=log['actions'];prepared=log['returnPrepared']
 if '--fault-ambiguous-target' in sys.argv:prepared['count']=2
 assert setup['selector']=='button /^Agent Activity(?: |$)/' and setup['count']==1 and setup['visible'] is True
 assert prepared['selector']==ret['selector']=='button /^My Progress(?: |$)/' and prepared['count']==1 and prepared['visible'] is True
 assert setup['text']=='Agent Activity live' and prepared['text']=='My Progress PARTIAL'
 before=(c/'00-progress-dom.txt').read_text('utf-8');activity=(c/'02-activity-dom.txt').read_text('utf-8');after=(c/'04-return-dom.txt').read_text('utf-8')
 assert re.search(r'heading "My Progress [^"]+" \[level=2\]',before)
 assert 'button "My Progress STALE"' in before and 'button "My Progress PARTIAL"' in activity
 assert 'heading "Agent Activity" [level=2]' in activity and 'heading "My Progress' not in activity
 if '--fault-missing-return' in sys.argv:after=''
 assert 'heading "My Progress PARTIAL" [level=2]' in after and 'heading "Agent Activity" [level=2]' not in after, 'Required return destination absent'
 assert 'heading "Governing requirements accepted (L1+L2)" [level=3]' in after and 'generic: UNMEASURED' in after
 assert 'heading My Progress PARTIAL' in (c/'03-return-immediate-ax.txt').read_text('utf-8')
 assert 'metric MP-2' in after
 image=(c/'05-return.jpg').read_bytes();assert image[:2]==b'\xff\xd8' and image[-2:]==b'\xff\xd9' and len(image)==122916
 cleanup=log['cleanup']
 if '--fault-missing-cleanup' in sys.argv:cleanup={}
 assert cleanup.get('closeReturned') is True and cleanup.get('ownedTabListedAfter') is False
 assert not any(x['id']==log['ownedTab'] for x in cleanup['inventory'])
 assert log['result']=='RETURN_PROGRESS_PRESENTATION_OBSERVED'
 times=[log['observations'][0]['recordedAfter'],setup['started'],setup['observationAfter'],log['observations'][1]['recordedAfter'],prepared['observed'],ret['started'],ret['observationAfter'],log['observations'][2]['recordedAfter'],log['observations'][3]['recordedAfter'],cleanup['recordedAfter']]
 assert times==sorted(times)
 def generation(s):return re.search(r'g\d{8}T\d{6}Z-[0-9a-f]+',s).group()
 assert generation(activity)==generation(after)=='g20260929T154720Z-55ec16'
 assert generation(before)==i['status_generation']=='g20260929T154216Z-1827bc'
 return {'result':'BOUNDED_RENDERED_RETURN_ESTABLISHED','method':'HOST_BROWSER','transition':'Observed Activity -> click stable uniquely visible My Progress -> immediate AX heading / later DOM Progress content / screenshot','initial_generation':generation(before),'return_generation':generation(after),'status_changed_during_setup':'STALE -> PARTIAL; return selector omitted status','inputs':2,'cleanup':'owned tab3 closed and absent from inventory; controls off','limits':'One return on one local session. No forced label change at exact dispatch, event-handler trace or atomic DOM/screenshot/HTTP snapshot; no loaded server/PID/browser build, full A17/M3/allviews/totals/migration/FF12/database acceptance. Prior refused returns remain valid history.'}
if __name__=='__main__':print(json.dumps(check(Path(__file__).resolve().parent),indent=2))
