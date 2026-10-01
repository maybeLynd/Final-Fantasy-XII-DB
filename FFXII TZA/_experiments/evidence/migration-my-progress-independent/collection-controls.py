import copy, hashlib, importlib.util, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'collection-02';assert not D.exists(),'Preserve prior collection';D.mkdir()
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();root=D/'source'
prior=json.loads((W/'author-622-01/raw.json').read_text());sources={}
for rel in prior['sources']:
 data=subprocess.check_output(['git','show',commit+':'+rel]);p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 sources[rel]={'sha256':hashlib.sha256(data).hexdigest(),'blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip()}
dash=root/'Database/Tools/dashboard';gs=root/'Database/Tools/analysis-kit/gfz-scripts';sys.path.insert(0,str(gs));sys.path.insert(0,str(dash));import requirements as R
assert (dash/'requirements.py').read_bytes()==(W/'core-01/requirements.py').read_bytes()
db=D/'fixture-db';idx=db/'_index';(idx/'_inbox').mkdir(parents=True);(idx/'candidates/register-triage').mkdir(parents=True);pages=db/'04-Actor-Entity';pages.mkdir()
(idx/'OPEN-QUESTIONS.md').write_text('''# Labelled independent fixture
## W. Fixture
| ID | Question | Status |
|---|---|---|
| W-901 | carrier obligation | **NOT A QUESTION 2026-09-26** - carrier task |
| W-902 | answered [page](../04-Actor-Entity/answered.md) | **ANSWERED** - labelled closure |
| W-903 | open [page](../04-Actor-Entity/answered.md) | **OPEN** - still live |
| W-904 | excluded | **WITHDRAWN** - labelled exclusion |
| ~~W-905~~ | struck | **CLOSED** |
''')
(idx/'candidates/register-triage/batch-K-scope-rulings.md').write_text('''# Labelled independent fixture
## Class 2: NOT A QUESTION, with a carrier
| row | carrier |
|---|---|
| W-901 | `ASTRA-FIX-CARRIER-0001` |
''')
(pages/'answered.md').write_text('''---
status: DOCUMENTED
---
# Labelled answered page
- [ ] **W-903.** live register obligation, not a second requirement
- [ ] **W-902.** open page against answered row, retain residue
- [ ] independent idless obligation
''')
(pages/'dispositioned.md').write_text('''---
status: DOCUMENTED - SUPERSEDED accepted-disposition residue W-901
---
# Labelled dispositioned page
''')
(pages/'partial.md').write_text('''---
status: PARTIAL
readiness: BEHAVIORALLY UNDERSTOOD
---
# Labelled partial coverage despite understood mechanism
''')
fn=D/'functions.tsv';fn.write_text('entry\tname\tbody_bytes\towner\tfinal_no_owner\tthunk\tnoreturn\tcomment_len\ttags\n')
raw={'method':'A actual collect/measure with independent private corpus/board fixtures; no production writer or FF12/native/live claim',
 'source_tree_commit':commit,'sources':sources,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':[],'finished':False}
def retain_failure(kind,value,tb):
 raw['fatal']={'type':kind.__name__,'reason':str(value)}
 (D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
 sys.__excepthook__(kind,value,tb)
sys.excepthook=retain_failure
observed={}
for state in ('READY','DONE'):
 # Independently labelled input boards, not a hand transition on the production TEAM.
 bp=D/('input-board-'+state+'.json');bp.write_text(json.dumps({'tasks':[{'id':'ASTRA-FIX-CARRIER-0001','status':state,'assigned_to':'ASTRA'}]},indent=2)+'\n')
 f=R.collect(str(db),functions_path=str(fn),board_path=str(bp));observed[state]=f
 (D/('facts-'+state+'.json')).write_text(json.dumps(f,indent=2)+'\n')
 q=next(x for x in f['facts'] if x['k']=='Q:W-901');assert q['ok']==(state=='DONE')
 dd={x['k']:x for x in f['facts'] if x['f']=='DD'}
 assert dd['DD:04-Actor-Entity/answered.md']['ok'] and dd['DD:04-Actor-Entity/answered.md']['st']=='documented, all answered'
 assert dd['DD:04-Actor-Entity/dispositioned.md']['ok'] and dd['DD:04-Actor-Entity/dispositioned.md']['st']=='documented with a dispositioned residue'
 assert not dd['DD:04-Actor-Entity/partial.md']['ok']
 ps=[x for x in f['facts'] if x['f']=='P'];assert len(ps)==2,'Retain idless/closed-row page residue, dedup live register obligation'
 assert not any(x['k'] in ('Q:W-904','Q:W-905') for x in f['facts'])
 raw['cases'].append({'name':'collect-carrier-'+state,'carrier':q,'documents':dd,'page_residue':ps,'failed_families':f['failed'],'excluded':f['excluded']})
base=json.loads((W/'core-01/all-accepted-final30-input.json').read_text());cmap=R.load_map(str(root/'Database/FFXII TZA/_index/workflow/my-progress/category-map.tsv'))
for name in ('conflicting-duplicate-key','reopen-required-row','DD-split-current'):
 f=copy.deepcopy(base['facts_doc']);board=base['board']
 if name=='conflicting-duplicate-key':duplicate=copy.deepcopy(next(x for x in f['facts'] if x['f']=='Q'));duplicate.update(ok=False,st='OPEN');f['facts'].append(duplicate)
 elif name=='reopen-required-row':next(x for x in f['facts'] if x['f']=='Q').update(ok=False,st='OPEN')
 else:f=copy.deepcopy(observed['DONE'])
 out=R.measure(f,cmap,board,base['reporter'],base['gate'],str(W/'core-01/subsystems.tsv'))
 (D/(name+'-input.json')).write_text(json.dumps(f,indent=2)+'\n');(D/(name+'-output.json')).write_text(json.dumps(out,indent=2)+'\n')
 if name=='conflicting-duplicate-key':assert out['duplicates_merged']==1 and out['families']['Q']=={'accepted':0,'total':1} and not out['ready'] and out['scopes']['union']['total']==45
 elif name=='reopen-required-row':assert out['families']['Q']=={'accepted':0,'total':1} and not out['ready']
 else:assert out['q_split']['dd_answered']==1 and out['q_split']['dd_dispositioned']==1 and out['families']['DD']=={'accepted':2,'total':3}
 # A 04 obligation lives in both E and P while its global key remains one object.
 if name!='DD-split-current':assert out['categories']['E']['total']==out['categories']['P']['total'] and len(out['remaining']['E'])==len(out['remaining']['P'])==1
 raw['cases'].append({'name':name,'ready':out['ready'],'measured':out['measured'],'scopes':out['scopes'],'q_split':out['q_split'],'duplicates_merged':out['duplicates_merged']})
raw['sources_unchanged']=all(hashlib.sha256((root/p).read_bytes()).hexdigest()==s['sha256'] for p,s in sources.items());assert raw['sources_unchanged']
raw['finished']=True;raw['limits']='Corpus intentionally lacks registry/format/contradiction/function populations: failed families preserved, never a complete healthy database or native semantic proof. A DOCUMENTED page may still carry P residue; separate axes remain visible.'
(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('INDEPENDENT_COLLECTION_AND_CURRENT_DD_CONTROLS_COMPLETE',len(raw['cases']),flush=True)
