"""Independent requested A16 controls through actual source/API/CLI, offline.

Disposable boards only. Every subprocess has a timeout and terminal receipt.
No producer test imports, shared edits, live writer invocation or host simulation.
"""
import ast,copy,csv,hashlib,json,os,pathlib,subprocess,sys

W=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
TOOLS=ROOT/'Database/Tools/analysis-kit/gfz-scripts';RUN=W/'actual-cases-02'
if RUN.exists():raise ValueError('immutable run exists')
RUN.mkdir();sys.dont_write_bytecode=True;sys.pycache_prefix=str(RUN/'fresh-unused-pyc')
sys.path.insert(0,str(TOOLS));import team,transitions
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={n:sha(TOOLS/n) for n in ('team.py','transitions.py')}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX=str(RUN/'cli-unused-pyc'))

def write(p,v):p.open('x',encoding='utf8').write(json.dumps(v,indent=2)+'\n')
def run(args,base):
 r=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,timeout=60)
 for suffix,data in [('.stdout',r.stdout),('.stderr',r.stderr),('.status.json',json.dumps(dict(argv=args,exit=r.returncode),indent=2).encode())]:pathlib.Path(str(base)+suffix).open('xb').write(data)
 return r

ok,why=team.board_status(team.BOARD)
if not ok:raise ValueError('current board incident: '+why)
live=json.loads(team.BOARD.read_text());team.validate(live)
live_before=dict(revision=live['revision'],sha256=sha(team.BOARD))
validation=run([sys.executable,'-B',str(TOOLS/'team.py'),'validate'],RUN/'live-read-validation')
if validation.returncode or not validation.stdout.strip() or validation.stderr.strip():raise ValueError('required live read validator failed')

# Pin assigned repair and current deployed source separately. Current source may
# contain later repairs; never imply that its entire file equals ed127d443.
for n in sources:
 r=run(['git','show','ed127d443:Database/Tools/analysis-kit/gfz-scripts/'+n],RUN/('assigned-'+n))
 if r.returncode or not r.stdout.strip():raise ValueError('assigned repair source unavailable')
 (RUN/('current-'+n)).open('xb').write((TOOLS/n).read_bytes())
 if n=='team.py':
  old=ast.parse(r.stdout.decode());new=ast.parse((TOOLS/n).read_text())
  a=next(q for q in old.body if isinstance(q,ast.FunctionDef) and q.name=='review_verdicts')
  b=next(q for q in new.body if isinstance(q,ast.FunctionDef) and q.name=='review_verdicts')
  if ast.dump(a,include_attributes=False)!=ast.dump(b,include_attributes=False):raise ValueError('assigned verdict parser changed; re-scope review')

invalid=[('missing',['receipt:fixture']),('trailing-lf',['verdict:ACCEPT\n']),('two-verdicts',['verdict:ACCEPT','verdict:REJECT']),('partial',['verdict:PARTIAL']),('lowercase',['verdict:accept'])]
valid=['ACCEPT','ACCEPT-WITH-NARROWING','REJECT','ESCALATE-FABLE','ESCALATE-OPUS','ESCALATE-ASTRA']
cases=[(label,refs,False,True) for label,refs in invalid]+[(v.lower(),['receipt:fixture','verdict:'+v],True,True) for v in valid]+[('plain-research',['receipt:plain'],True,False)]
rows=[]
for label,refs,accept,is_review in cases:
 case=RUN/label;case.mkdir();board_path=case/'TEAM.json'
 board={'schema_version':1,'phase':'DATABASE','revision':0,'agents':{},'tasks':[],'history':[]}
 for agent in team.AGENTS:board['agents'][agent]={'agent_id':agent,'primary_specialty':agent,'last_checkpoint':team.now()}
 team.refresh(board);team.validate(board)
 task=dict(id='FIXTURE-A16-'+label.upper(),kind='research',priority='P1',target='isolated requested finish gate',scope='disposable original supported CLI',completion='observed exact request outcome',dependencies=[],resources=[dict(key='fixture:a16/'+label)])
 if is_review:task['reviews']=dict(author='OPUS',commit='ed127d443',record='fixture:assigned-repair',incorporation_owner='FABLE')
 team.apply(board,'OPUS',dict(action='add',task=task),'astra-a16-private')
 team.apply(board,'ASTRA',dict(action='claim',task=task['id'],note='private fixture'),'astra-a16-private')
 team.validate(board);write(board_path,board)
 before=board_path.read_bytes();(case/'before.json').open('xb').write(before)
 op=case/'finish.json';write(op,dict(action='finish',task=task['id'],note='private requirement control',result_refs=refs))
 argv=[sys.executable,'-B',str(TOOLS/'team.py'),'apply','--board',str(board_path),'--agent','ASTRA','--session','astra-a16-private','--file',str(op)]
 actual=run(argv,case/'finish-invocation');after=board_path.read_bytes();(case/'after.json').open('xb').write(after)
 value=json.loads(after);team.validate(value);row=next(t for t in value['tasks'] if t['id']==task['id'])
 plans=[q for q in transitions.plan(value) if q[1]==task['id']]
 normalized=[dict(kind=q[0],review=q[1],detail=q[2],has_operation=q[3] is not None) for q in plans]
 record=dict(case=label,is_review=is_review,expected_accept=accept,exit=actual.returncode,status=row['status'],before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest(),result_refs=row.get('result_refs'),plan=normalized)
 if accept:
  if actual.returncode or row['status']!='DONE' or row.get('result_refs')!=refs or value['revision']!=board['revision']+1 or not actual.stdout.strip():raise ValueError('positive control failed '+label)
  if is_review:
   verdict=refs[-1].split(':',1)[1];kind={'ACCEPT':'INCORPORATE','REJECT':'REPAIR'}.get(verdict,'VERDICT-MANUAL')
   if len(plans)!=1 or plans[0][0]!=kind or (plans[0][3] is not None)!=(verdict in ('ACCEPT','REJECT')):raise ValueError('transition classification failed '+label)
  elif plans:raise ValueError('plain research unexpectedly transitioned')
 else:
  if not actual.returncode or before!=after or row['status']!='ACTIVE' or 'a review (task with a reviews field) finishes with exactly one' not in actual.stderr.decode(errors='replace'):raise ValueError('negative control failed '+label)
 write(case/'result.json',record);rows.append(record)
 if label=='accept-with-narrowing':
  native=run([sys.executable,'-B',str(TOOLS/'transitions.py'),'--board',str(board_path),'--json'],case/'transition-cli')
  if native.returncode:raise ValueError('required transition CLI failed')
  p=json.loads(native.stdout)
  if len(p)!=1 or p[0]['transition']!='VERDICT-MANUAL' or p[0]['review']!=task['id']:raise ValueError('actual transition CLI misclassified narrowing')

legacy=ROOT/'Database/FFXII TZA/_index/candidates/a16-finish-verdict-gate-0929/legacy-verdictless-reviews.tsv'
lines=[q for q in legacy.read_text().splitlines() if not q.startswith('#')]
listed=list(csv.DictReader(lines,delimiter='\t'));ids={t['id']:t for t in live['tasks']}
legacy_status=[dict(task=q['task'],present=q['task'] in ids,status=ids.get(q['task'],{}).get('status'),retired=ids.get(q['task'],{}).get('retired',False)) for q in listed]
if len(listed)!=55 or any(not q['present'] for q in legacy_status):raise ValueError('historical legacy inventory missing/incomplete')
if any(sha(TOOLS/n)!=pin for n,pin in sources.items()):raise ValueError('source moved during controls; result incomplete')
ok,why=team.board_status(team.BOARD)
if not ok:raise ValueError('post-run current board incident: '+why)
result=dict(status='VALID_SCOPED_NONAUTHOR_GATE_REVIEW',verdict='ACCEPT',request='OPUS-REQ-ASTRA-VERIFY-A16-FINISH-GATE-0929',source_sha256=sources,assigned_repair='ed127d443',assigned_parser_ast_matches_current=True,live_read=live_before,live_validator_exit=validation.returncode,legacy_list_sha256=sha(legacy),legacy_rows=legacy_status,cases=rows,counts=dict(required_invalid=5,policy_valid=6,plain=1),checker_sha256=sha(pathlib.Path(__file__)),
 established=['All five required invalid forms refused by actual finish CLI, task ACTIVE and exact board bytes unchanged','All six policy verdicts admitted with exact refs; plain research remains admitted','Narrowing recognized as VERDICT-MANUAL without a next operation, independently through imported plan and actual CLI','Current read-only live validation passes; all55 named historical rows retained; no history rewritten'],
 limits=['Assigned repair parser matches current AST; current whole source also includes later changes, pinned separately','Offline real supported CLI/API on disposable boards; no production review->incorporation transaction or deployed host/wholeA16/M2 acceptance','Peer board writes can occur concurrently; this test does not assert whole live board unchanged. All writer argv explicitly target private fixtures','Old ASTRA reproduction7068c250a reused as prior defect evidence, not rerun or counted as a new control; OPUS campaign not counted as ours'],
 cleanup='All foreground child invocations terminal/timeout-bounded; private fixture locks/journals retained as evidence; no shared source/live board writer/PC/game/process/instrument/save/config/reference mutation')
write(RUN/'result.json',result)
print('SCOPED ACCEPT: actual CLI5 refusal/6 policy/1 plain controls; narrowing manual; live read validation and55 legacy identities retained')

if not rows:raise ValueError('invalid zero-case run')
