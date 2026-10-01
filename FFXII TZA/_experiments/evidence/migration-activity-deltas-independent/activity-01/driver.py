"""Original in-memory board operations distinguish lane writes from assignment dates."""
import copy,hashlib,importlib.util,json,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];D=W/'activity-01';assert not D.exists();D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
    q=subprocess.run(['git',*args],cwd=ROOT,capture_output=True);assert q.returncode==0,q.stderr
    return q.stdout
commit=git('rev-parse','8ddc8c7e8').decode().strip();here=D/'source';here.mkdir()
sources={}
for n,rel in [('activity.py','Database/Tools/dashboard/activity.py'),('requirements.py','Database/Tools/dashboard/requirements.py'),('team.py','Database/Tools/analysis-kit/gfz-scripts/team.py')]:
    b=git('show',commit+':'+rel);(here/n).write_bytes(b)
    sources[n]={'path':rel,'commit':commit,'bytes':len(b),'sha256':sha(b),'blob':git('rev-parse',commit+':'+rel).decode().strip(),
                'current_disk_equal':(ROOT/rel).read_bytes()==b}
sys.path.insert(0,str(here))
import activity as A, team as T
now=1800000000.0
from datetime import datetime,timezone
stamp=lambda t:datetime.fromtimestamp(t,timezone.utc).isoformat(timespec='seconds')
old=stamp(now-7200);fresh=stamp(now-30)
base={'schema_version':1,'phase':'DATABASE','revision':0,'recovery_epoch':0,'agents':{n:{'agent_id':n,'primary_specialty':'labelled fixture only','current_task':[],'claimed_scope':[],'dependencies':[],'blockers':[],'last_checkpoint':old,'status':'READY'} for n in T.AGENTS},'tasks':[],'history':[],'checkpoints':[]}
task={'id':'LABELLED-OPUS-OLD-CLAIM','kind':'research','priority':'P1','target':'07-Combat-Action labelled fixture','scope':'activity classification only','completion':'fixture only','dependencies':[],'resources':[{'key':'request:fixture/old-claim'}]}
T.now=lambda:old  # labelled clock boundary; no production writer or mutex invoked
T.apply(base,'OPUS',{'action':'add','task':task});T.apply(base,'OPUS',{'action':'claim','task':task['id']})
T.validate(base)
foreign=copy.deepcopy(base);T.now=lambda:fresh
new={'id':'LABELLED-VERIFY-QUEUED','kind':'request','requester':'FABLE','assigned_to':'OPUS','priority':'P1',
     'target':'07-Combat-Action labelled review','scope':'foreign assignment fixture','completion':'fixture only',
     'question':'labelled review','known_evidence':'fixture','missing_information':'fixture','why_it_matters':'fixture',
     'what_is_blocked':'fixture','dependencies':[],'resources':[{'key':'request:fixture/queued'}]}
T.apply(foreign,'FABLE',{'action':'add','task':new});T.validate(foreign)
own=copy.deepcopy(base);T.apply(own,'OPUS',{'action':'note','note':'labelled genuine lane write, no task update'});T.validate(own)
placer=A.Placer({'folder':{'07':['C']}},{'facts':[]},{})
decls=[('old-claim-no-feed',base,None,None,'UNKNOWN','claimed'),
 ('foreign-review-no-feed',foreign,None,None,'UNKNOWN','claimed'),
 ('foreign-review-explicit-unknown',foreign,None,{'OPUS':{'classification':'UNKNOWN'}},'UNKNOWN','claimed'),
 ('own-note-no-feed',own,None,None,'recent','working'),
 ('busy-control',base,{'ts':stamp(now),'lane_state':{'OPUS':'busy-test'}},None,'active','working'),
 ('idle-control',foreign,{'ts':stamp(now),'lane_state':{'OPUS':'free'}},None,'idle','claimed')]
raw={'method':'A original repository Python activity.compute and supported in-memory team.apply, labelled fixture clock boundary',
     'source_commit':commit,'sources':sources,'driver_sha256':sha(Path(__file__).read_bytes()),'clock':now,
     'clock_intervention':'team.now replaced by explicit old/fresh timestamp for disposable in-memory operations only; no transaction/journal/real writer',
     'cases':[],'finished':False,'limits':'Not FF12/native/host execution; deployed effect separate; no producer tests executed; scope does not certify deltas/timer/presentation'}
try:
    for name,b,poll,claude,expected_live,expected_kind in decls:
        d=D/name;d.mkdir();inp={'board':b,'poll':poll,'claude':claude,'now':now}
        (d/'input.json').write_text(json.dumps(inp,indent=2)+'\n')
        result=A.compute(copy.deepcopy(b),poll,claude,placer,now)
        mine=next(x for x in result['by_agent'] if x['lane']=='OPUS')
        item=next(x for x in result['categories'] if x['code']=='C')
        claim=next(x for x in mine['working'] if x['task']==task['id'])
        c={'name':name,'expected_liveness':expected_live,'expected_claim_kind':expected_kind,
           'observed_liveness':mine['liveness'],'observed_claim_kind':claim['kind'],
           'combat_colored_lanes':item['working'],'combat_muted_lanes':item['muted'],
           'actual_recent_writers':sorted({x['agent'] for x in b['history'] if now-datetime.fromisoformat(x['at']).timestamp()<=3600}),
           'input_sha256':sha((d/'input.json').read_bytes()),'result':result,'exception':None}
        (d/'receipt.json').write_text(json.dumps(c,indent=2)+'\n');raw['cases'].append(c)
    raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('ACTIVITY_CONTROLS',[(c['name'],c['expected_liveness'],c['observed_liveness'],c['actual_recent_writers']) for c in raw['cases']])
