"""Validate the retained three admission controls without rerunning native code."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
need=lambda ok,msg: None if ok else (_ for _ in ()).throw(RuntimeError(msg))
r=json.loads((P/'result-01.json').read_text())
up=json.loads((P/'review-01.status.json').read_text())
need(up.get('terminal') is True and up.get('exit')==0 and up.get('exception') is None,'incomplete actual review invocation')
need(up.get('driver_sha256')==sha(P/'review.py')==r.get('driver_sha256'),'actual review driver identity')
need(r.get('complete') is True and r.get('verdict')=='ACCEPT_SCOPED_UPSTREAM_ADMISSION_REPAIR','missing scoped result')
need(len(r.get('cases',[]))==3 and [x['case'] for x in r['cases']]==['positive','reported-fail','raised-failure'],'required case cardinality/identity')
need(r.get('scientific_native_runs')==0 and r.get('game_runs')==0,'evidence-method scope changed')
for n,name in enumerate(['check.py','upstream_guard.py','test_upstream_guard.py'],1):
 g=json.loads((P/f'git-source-{n:02}.status.json').read_text())
 need(g.get('terminal') is True and g.get('exit')==0 and g.get('exception') is None,'Git source acquisition failed')
 need(sha(P/f'git-source-{n:02}.stdout')==sha(P/'retained'/name)==r['inputs'][name]['git_sha256'],'committed source identity')
need(sha(P/'retained'/'historical-result.json')==r['inputs']['historical-result.json']['sha256'],'historical result identity')
for x in r['cases']:
 label=x['case'];tag='case-'+label
 z=json.loads((P/(tag+'.status.json')).read_text());out=(P/(tag+'.stdout')).read_bytes();err=(P/(tag+'.stderr')).read_bytes()
 need(z==x['receipt'] and z.get('terminal') is True and z.get('exception') is None and not err,'incomplete case invocation')
 need(z['driver_sha256']==r['driver_sha256'] and z['stdout_sha256']==sha(P/(tag+'.stdout')) and z['stderr_sha256']==sha(P/(tag+'.stderr')),'case receipt/raw identity')
 base=P/'cases'/label;current=base/'s33-opus-replay-op1-real';fixture=base/'s21-opus-replay-applier-stub-free'/'check.py'
 need(sha(fixture)==x['fixture_sha256'],'fixture input identity')
 for name,key in [('check.py','tested_check_sha256'),('upstream_guard.py','tested_guard_sha256')]:
  need(sha(current/name)==x[key]==r['inputs'][name]['git_sha256'],'actual invocation uses retained unmodified code')
 need(not (current/'result.json').exists() and not (fixture.parent/'result.json').exists(),'unexpected result at admission boundary')
 if label=='positive':
  need(z['exit']==0 and out.strip()==b'ASTRA_DOWNSTREAM_STATE_BOUNDARY' and x['downstream_state_reached'] is True,'positive admission boundary missing')
 elif label=='reported-fail':
  need(z['exit']==2 and b'REFUSED: upstream allok is False, not True' in out and b'ASTRA_DOWNSTREAM_STATE_BOUNDARY' not in out and x['downstream_state_reached'] is False,'false verdict not refused before downstream')
 else:
  need(z['exit']==2 and b'REFUSED: upstream check raised RuntimeError: qualified upstream failure' in out and b'ASTRA_DOWNSTREAM_STATE_BOUNDARY' not in out and x['downstream_state_reached'] is False,'exception not refused before downstream')
 need(x['required_observation'] is True and x['no_result'] is True,'normalized admission observation incomplete')
print('VERIFIED scoped S33 admission repair: three actual whole-driver host fixtures; no native/game execution')
