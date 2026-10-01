"""Original writer discriminator, not a replay of the settled predicate samples.

Preconditions: bf000cdc path-keyed fixture mutex; exact parent postwrite board and
journal. Preserve CRLF stdout, compare exact splitlines; never rebuild live state.
The prefix is constructed by omitting a copied commit, not by crashing a process.
"""
import copy,hashlib,json,os,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;RUN=W/'run-01';assert not RUN.exists()
ROOT=Path.cwd().resolve();SOURCE=ROOT/'Database/Tools/analysis-kit/gfz-scripts/team.py'
sys.path.insert(0,str(SOURCE.parent));import team
P=ROOT/'Database/FFXII TZA/_experiments/evidence/board-stale-revision-writer'
COMMIT='521f189be5d6bab445a7f7cccffa7a650c636afd'
source=SOURCE.read_bytes();assert hashlib.sha256(source).hexdigest()=='240bb9c88c0b5dcae8b52216af97f6ec4ae727a791e108bb802fb748d79fc480'
assert Path(team.__file__).resolve()==SOURCE and W.is_relative_to(ROOT/'Database/Tools/work/ASTRA')

def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
 assert not p.exists(),str(p)
 p.write_bytes(b)
def js(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0 and not q.stderr
 return q.stdout

manifest=json.loads((P/'manifest.json').read_bytes())
names=['run-01/private/TEAM.json','run-01/private/TEAM.json.journal.jsonl','run-01/team.py']
inputs={}
for n in names:
 row=next(r for r in manifest['members'] if r['path']==n);b=(P/n).read_bytes()
 assert len(b)==row['bytes'] and sha(b)==row['sha256']
 assert git('show',COMMIT+':'+(P/ n).relative_to(ROOT).as_posix())==b
 inputs[n]=b
assert inputs[names[2]]==source
RUN.mkdir();(RUN/'parent').mkdir()
for n,target in zip(names,['board.json','journal.jsonl','team.py']):put(RUN/'parent'/target,inputs[n])
put(RUN/'team.py',source);put(RUN/'capture.py',Path(__file__).read_bytes())
board=inputs[names[0]];journal=inputs[names[1]]
records=[json.loads(x) for x in journal.decode().splitlines()]
assert [r['kind'] for r in records]==['genesis','intent','commit']
assert records[-1]['rev']==1 and records[-1]['board_sha']==sha(board)
prefix=b''.join(journal.splitlines(keepends=True)[:-1])
raw={'method':'A: unmodified original repository Python CLI/transaction; not FF12 native/live',
 'question':'Does pending-write healing bind complete written state, or only revision/last operation?',
 'hypotheses':['H1 complete-state mismatch refuses','H2 matching last operation promotes changed checkpoint state'],
 'identity':{'source_sha256':sha(source),'source_path':str(SOURCE),'module_path':team.__file__,
 'source_commit':'bf000cdc96d3ca9ec7fb461d0e066572d6657041','parent_commit':COMMIT,
 'head':git('rev-parse','HEAD').decode().strip(),'driver_sha256':sha(Path(__file__).read_bytes()),
 'python':sys.version,'python_executable':sys.executable,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'python_base_executable':sys._base_executable,'python_base_sha256':sha(Path(sys._base_executable).read_bytes())},
 'interventions':['Copy exact observed postwrite board/journal, omit copied final commit to construct pending prefix',
 'Change one copied checkpoint note without changing last operation; change last operation in negative control'],
 'cases':[],'state':'INCOMPLETE','limits':'Constructed private states, no real crash/production recovery/controller/deployment or game observation.'}
owned=[]

def cli(args):
 start=time.monotonic();p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});owned.append(p)
 timed=False
 try:out,err=p.communicate(timeout=5)
 except subprocess.TimeoutExpired:
  timed=True;p.terminate();out,err=p.communicate(timeout=5)
 receipt={'argv':args,'pid':p.pid,'returncode':p.returncode,'stdout':out.decode(),'stderr':err.decode(),
 'terminal':p.poll() is not None,'timed_out':timed,'elapsed_seconds':time.monotonic()-start}
 assert not timed and receipt['terminal'],receipt
 return receipt

try:
 for name in ['healthy-prefix','changed-checkpoint','different-last-operation']:
  d=RUN/name;d.mkdir();fixture=d/'TEAM.json';assert fixture.resolve()!=team.BOARD.resolve()
  assert fixture.resolve().is_relative_to(RUN.resolve())
  b=json.loads(board)
  if name=='changed-checkpoint':b['checkpoints'][0]['note']='different retained checkpoint value'
  elif name=='different-last-operation':b['history'][-1]['operation']['note']='different last operation value'
  team.validate(b)
  initial=board if name=='healthy-prefix' else js(b)
  put(fixture,initial);put(team.journal_path(fixture),prefix)
  put(d/'before-board.json',initial);put(d/'before-journal.jsonl',prefix)
  op={'action':'note','note':'fresh follow-on after '+name};put(d/'operation.json',js(op))
  case={'name':name,'schema_valid_before':True,'before_board_sha256':sha(initial),
  'before_journal_sha256':sha(prefix),'matches_observed_parent_commit':sha(initial)==records[-1]['board_sha']}
  raw['cases'].append(case)
  args=[sys.executable,'-B',str(SOURCE),'apply','--board',str(fixture),'--agent','ASTRA',
        '--session',name,'--expect-revision','1','--file',str(d/'operation.json')]
  case['writer']=cli(args)
  after=fixture.read_bytes();jafter=team.journal_path(fixture).read_bytes()
  put(d/'after-board.json',after);put(d/'after-journal.jsonl',jafter)
  case.update(after_board_sha256=sha(after),after_journal_sha256=sha(jafter),
  private_lock_absent=not fixture.with_suffix('.lock').exists())
  team.validate(json.loads(after))
  if case['writer']['returncode']==0:
   case['health']=cli([sys.executable,'-B',str(SOURCE),'boardcheck','--board',str(fixture)])
  else:case['health']=None
  assert SOURCE.read_bytes()==source
 assert all(p.poll() is not None for p in owned)
 raw['cleanup']={'owned_processes_terminal':True,'source_unchanged':True,
 'all_private_locks_absent':all(c['private_lock_absent'] for c in raw['cases']),
 'original_parent_bytes_unchanged':all((P/n).read_bytes()==inputs[n] for n in names),
 'production_board_not_a_fixture':True,'normal_game_or_production_host_health':'NOT_OBSERVED'}
 raw['state']='OBSERVED'
except BaseException as e:
 raw['state']='INVALID';raw['exception']={'type':type(e).__name__,'message':str(e)};raise
finally:
 for p in owned:
  if p.poll() is None:p.terminate();p.communicate(timeout=5)
 put(RUN/'raw.json',js(raw))
print('PENDING_WRITER_OBSERVED; reducer acceptance required')
