import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'admission-01';assert not D.exists(),'Keep prior phase immutable';D.mkdir()
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
root=D/'source';dash=root/'Database/Tools/dashboard';gs=root/'Database/Tools/analysis-kit/gfz-scripts';dash.mkdir(parents=True);gs.mkdir(parents=True)
rels=['Database/Tools/dashboard/'+n for n in ('requirements.py','build_views.py','server.py')]+['Database/Tools/analysis-kit/gfz-scripts/generation.py',
 'Database/FFXII TZA/_index/workflow/MY-PROGRESS-METRICS.md','Database/FFXII TZA/_index/workflow/my-progress/category-map.tsv',
 'Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md','Database/FFXII TZA/_index/completion-packages/README.md',
 'Database/FFXII TZA/_index/progress/progress_report.py','Database/FFXII TZA/_index/FINAL-AUDIT-PROTOCOL.md']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
sources={}
for rel in rels:
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);data=subprocess.check_output(['git','show',commit+':'+rel]);p.write_bytes(data)
 sources[rel]={'sha256':sha(p),'blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip(),
 'last_commit':subprocess.check_output(['git','log','-1','--format=%H',commit,'--',rel],text=True).strip()}
assert (dash/'requirements.py').read_bytes()==(W/'core-01/requirements.py').read_bytes(),'Changed measure source; re-evaluate, do not silently combine'
sys.path.insert(0,str(gs));sys.path.insert(0,str(dash))
import generation as G, requirements as R, build_views as B, server as S
base=json.loads((W/'core-01/all-accepted-final30-input.json').read_text())
raw={'method':'A original Python producer v_progress + original generation store + original State/check_view; labelled pre-resolved fixtures/composed path',
 'source_tree_commit':commit,'sources':sources,'driver_sha256':sha(__file__),'python':sys.version,
 'cases':[],'finished':False,'normal_emitter_limit':'Copied reporter source hardcodes required_consecutive30; invalid0 is an explicit input intervention, not demonstrated normal output/reachability',
 'composition_limit':'Actual v_progress/store/State methods called; full _build_once collection, other adapters, CLI main producer and network/browser omitted'}
for name in ('valid-final30','invalid-terminal0','partial29-not-met','inconsistent-headline','ready-with-open-Q'):
 d=D/name;d.mkdir();inp=d/'inputs';inp.mkdir();f=copy.deepcopy(base['facts_doc']);rep=copy.deepcopy(base['reporter']);gate=copy.deepcopy(base['gate'])
 if name=='invalid-terminal0':rep['levels']['terminal_certification'].update(required_consecutive=0,final_audits_declared=0)
 elif name=='partial29-not-met':rep['levels']['terminal_certification']['final_audits_declared']=29;gate.update(verdict='NOT_MET',detail=['acceptance: UNMET labelled incomplete streak'],remaining='labelled incomplete final audit')
 elif name=='ready-with-open-Q':next(x for x in f['facts'] if x['f']=='Q').update(ok=False,st='OPEN')
 for n,val in (('requirement_facts',f),('team',base['board']),('progress_snapshot',rep),('goal_gate',gate)):(inp/n).write_text(json.dumps(val,indent=2)+'\n')
 (inp/'category_map').write_bytes((root/'Database/FFXII TZA/_index/workflow/my-progress/category-map.tsv').read_bytes())
 (inp/'subsystems').write_bytes((W/'core-01/subsystems.tsv').read_bytes())
 inputs={n:{'path':str(inp/n)} for n in ('requirement_facts','team','progress_snapshot','goal_gate','category_map','subsystems')}
 store=G.Store(str(d/'store'));b=store.begin(inputs,{'name':'labelled ASTRA composition of original tooling'})
 snap={n:str(Path(b.dir)/'inputs'/n) for n in inputs}
 v=B.v_progress(snap,'2026-09-29T07:40:00Z');original=copy.deepcopy(v)
 if name=='inconsistent-headline':v['progress']['scopes']['union']['accepted']-=1
 elif name=='ready-with-open-Q':v['progress']['reconstruction']['state']='DATABASE READY - labelled invalid field intervention'
 (d/'producer-original.json').write_text(json.dumps(original,indent=2)+'\n')
 (d/'view-input.json').write_text(json.dumps(v,indent=2)+'\n')
 why=S.check_view(v,S.load_vocabulary());Path(b.output_path('view-progress.json')).write_text(json.dumps(v,indent=2)+'\n')
 gid=store.commit(b,['view-progress.json']);state=S.State(store.root)
 status=state.status();served=state.view('progress');admitted='view' in served
 if name in ('valid-final30','invalid-terminal0'):assert why is None and admitted and status['views']['progress']=='OK' and v['progress']['reconstruction']['state'].startswith('DATABASE READY')
 elif name=='partial29-not-met':assert why is None and admitted and not v['progress']['reconstruction']['state'].startswith('DATABASE READY') and v['progress']['terminal']=={'accepted':29,'required':30}
 else:assert why and not admitted and status['views']['progress']=='MALFORMED'
 assert status['reader_stale'] is False and not status['problems']
 receipt={'name':name,'view_sha256':sha(d/'view-input.json'),'original_producer_sha256':sha(d/'producer-original.json'),
 'intervention':'pre-resolved reporter/gate/facts fixture; '+('extra post-producer view field mutation' if name in ('inconsistent-headline','ready-with-open-Q') else 'no post-producer view mutation'),
 'check_view_reason':why,'generation':gid,'status':status,'served':served,'admitted':admitted}
 raw['cases'].append(receipt);(d/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert all(sha(root/p)==v['sha256'] for p,v in sources.items());raw['sources_unchanged']=True;raw['finished']=True
(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('ORIGINAL_PRODUCER_AND_STATE_ADMISSION_COMPLETE',[(c['name'],c['admitted']) for c in raw['cases']],flush=True)
