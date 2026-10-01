import copy,hashlib,importlib.util,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01'
P=Path('Database/FFXII TZA/_experiments/evidence/board-stale-revision-writer')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr
 return p.stdout.strip()
def call(label,argv,env):
 p=subprocess.run(argv,capture_output=True,text=True,env=env,timeout=30)
 receipt={'label':label,'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'terminal':True}
 (R/(label+'-terminal.json')).write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
 assert p.returncode==0 and not p.stderr,(label,p.returncode,p.stderr)
 return receipt
def run():
 assert not R.exists(),'Write-once; retain failure and revise discriminator before retry'
 R.mkdir()
 manifest=json.loads((P/'manifest.json').read_bytes());seed=P/'run-01/initial-board.json'
 member=next(m for m in manifest['members'] if m['path']=='run-01/initial-board.json')
 assert sha(seed)==member['sha256'] and seed.stat().st_size==member['bytes']
 assert git('rev-parse','521f189be5d6bab445a7f7cccffa7a650c636afd:'+P.as_posix()+'/run-01/initial-board.json')==git('hash-object','--no-filters',str(seed))
 (R/'retained-empty-seed.json').write_bytes(seed.read_bytes())
 ident={'head':git('rev-parse','HEAD'),'python':sys.executable,'python_version':sys.version,'driver_sha256':sha(Path(__file__)),'parent_seed_commit':'521f189be5d6bab445a7f7cccffa7a650c636afd','seed_sha256':sha(seed),'source':[],'method':'Actual original repository CLI integration on one disposable board. Synthetic review declarations; no project review acceptance or live host execution.'}
 srcdir=R/'original/Database/Tools/analysis-kit/gfz-scripts'
 for name in ['transitions.py','team.py']:
  original=Path('Database/Tools/analysis-kit/gfz-scripts')/name;target=srcdir/name;target.parent.mkdir(parents=True,exist_ok=True)
  before=sha(original);shutil.copyfile(original,target);assert sha(original)==sha(target)==before
  ident['source'].append({'path':str(original),'copy':target.relative_to(R).as_posix(),'sha256':before,'commit':git('log','-1','--format=%H','--',original.as_posix()),'blob':git('hash-object','--no-filters',str(original))})
 sys.path.insert(0,str(srcdir.resolve()));spec=importlib.util.spec_from_file_location('team',srcdir/'team.py');team=importlib.util.module_from_spec(spec);sys.modules['team']=team;spec.loader.exec_module(team)
 board=json.loads(seed.read_bytes());assert board['revision']==0 and not board['tasks'] and not board['history'];team.validate(board)
 preparations=[]
 for name,verdict in [('ACCEPT','ACCEPT'),('REJECT','REJECT')]:
  tid='FIXTURE-REVIEW-'+name
  task={'id':tid,'kind':'research','priority':'P2','target':'Labelled synthetic review '+name,'scope':'Synthetic declarative review; no project semantic acceptance','completion':'Seed fixture only','dependencies':[],'resources':[{'key':'target:fixture/review-'+name.lower()}],'reviews':{'author':'OPUS','commit':ident['source'][0]['commit'],'record':'fixtures/SYNTHETIC-REVIEW.md','incorporation_owner':'SWE2-DATA'}}
  for agent,op in [('OPUS',{'action':'add','task':task}),('FABLE',{'action':'claim','task':tid,'note':'Synthetic reviewer identity in a disposable fixture'}),('FABLE',{'action':'finish','task':tid,'note':'Synthetic '+verdict+' declaration for writer integration only','result_refs':['verdict:'+verdict,'fixture:synthetic-receipt']})]:
   team.apply(board,agent,op,session='FIXTURE-SEED-PURE-APPLY');preparations.append({'agent':agent,'op':op,'method':'Original in-memory apply only; no journal write during fixture preparation'})
 (R/'preparation.json').write_bytes((json.dumps(preparations,indent=2)+'\n').encode())
 d=R/'private';d.mkdir();path=(d/'board.json').resolve();path.write_bytes((json.dumps(board,indent=2)+'\n').encode());before=path.read_bytes()
 (R/'before-board.json').write_bytes(before)
 ident.update(board_path=str(path),journal_path=str(team.journal_path(path)),loaded_team=str(Path(team.__file__).resolve()),seed_revision=board['revision'],seed_intervention='Two synthetic DONE reviews made with six original in-memory apply ops, then serialized before first native writer sighting; not real FABLE/OPUS communications.')
 (R/'identity.json').write_bytes((json.dumps(ident,indent=2)+'\n').encode())
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['TEAM_SESSION']='FIXTURE-ASTRA-TRANSITION-WRITE'
 original=str((srcdir/'transitions.py').resolve());argv=[sys.executable,'-B',original,'--board',str(path),'--agent','SWE2-FRONTIER','--apply','--json']
 first=call('first',argv,env);got=json.loads(first['stdout']);assert len(got)==2 and {x['transition'] for x in got}=={'REPAIR','INCORPORATE'} and all(x['status']=='created' for x in got),got
 after=path.read_bytes();journal=team.journal_path(path).read_bytes()
 (R/'after-first-board.json').write_bytes(after);(R/'after-first-journal.jsonl').write_bytes(journal)
 b=json.loads(after);team.validate(b);assert b['revision']==8 and len(b['tasks'])==4
 expected={'AUTO-INCORP-FIXTURE-REVIEW-ACCEPT':'SWE2-DATA','AUTO-REPAIR-FIXTURE-REVIEW-REJECT':'OPUS'}
 for tid,owner in expected.items():
  t=next(t for t in b['tasks'] if t['id']==tid);assert t['status']=='READY' and t['assigned_to']==owner and t['requester']=='SWE2-FRONTIER'
 assert b['tasks'][:2]==board['tasks'] and b['history'][:6]==board['history']
 health1=call('boardcheck-first',[sys.executable,'-B',str((srcdir/'team.py').resolve()),'boardcheck','--board',str(path)],env)
 second=call('second',argv,env);got2=json.loads(second['stdout']);assert len(got2)==2 and all(x['transition']=='DONE-ALREADY' and x['status']=='-' for x in got2),got2
 assert path.read_bytes()==after and team.journal_path(path).read_bytes()==journal
 (R/'after-second-board.json').write_bytes(path.read_bytes());(R/'after-second-journal.jsonl').write_bytes(team.journal_path(path).read_bytes())
 health2=call('boardcheck-second',[sys.executable,'-B',str((srcdir/'team.py').resolve()),'boardcheck','--board',str(path)],env)
 assert not path.with_suffix(path.suffix+'.lock').exists()
 for s in ident['source']:assert sha(Path(s['path']))==sha(R/s['copy'])==s['sha256']
 result={'first_status':'two actual writer creations','second_status':'two DONE-ALREADY, no writes','revision_before':6,'revision_after':8,'journal_kinds':[x['kind'] for x in team.journal_records(path)],'same_board_after_second':True,'same_journal_after_second':True,'private_lock_absent':True,'unchanged_sources':True,'parent_children_terminal':True,'limits':'Not concurrent dispatch, fairness, cancellation, quota, controller/native host, malformed/timeout behavior or full A14/A16/pilot acceptance.'}
 assert result['journal_kinds']==['genesis','intent','commit','intent','commit']
 (R/'summary.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:run()
 except BaseException:
  if R.exists():(R/'failure.txt').write_text(traceback.format_exc())
  raise
