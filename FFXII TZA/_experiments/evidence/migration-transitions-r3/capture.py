import copy,hashlib,importlib.util,json,os,subprocess,sys,traceback
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();H=R/'source/Database/Tools/analysis-kit/gfz-scripts';H.mkdir(parents=True);sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):
 q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(args,q.stderr);return q.stdout
C=git('rev-parse','d27e9aff8').decode().strip();OLD=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-r2');OC='117f85ab6889eb7915d01e2a8f7596e762bbf25f'
raw=dict(method='A original repository CLI/plan; apply callers use explicit child-entry substitution/private board intervention, not real journal writer/game',source_commit=C,prior_commit=OC,driver_sha256=sha(Path(__file__).read_bytes()),sources={},regression=[],fields=[],writer=[],terminal=False,exception=None,python=dict(version=sys.version,base=sys._base_executable,base_sha256=sha(Path(sys._base_executable).read_bytes())));(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
try:
 mb=(OLD/'manifest.json').read_bytes();assert git('show',OC+':'+(OLD/'manifest.json').as_posix())==mb;members={x['path']:x for x in json.loads(mb)['members']};raw['prior_manifest_sha256']=sha(mb)
 def prior(rel):
  b=(OLD/rel).read_bytes();assert sha(b)==members[rel]['sha256'] and len(b)==members[rel]['bytes'] and git('show',OC+':'+(OLD/rel).as_posix())==b;return b
 oldraw=prior('run-01/raw.json');(R/'prior-raw.json').write_bytes(oldraw);raw['prior_raw_sha256']=sha(oldraw);rows=json.loads(oldraw)['cases'];assert len(rows)==13
 for n in ['transitions.py','team.py']:
  rel='Database/Tools/analysis-kit/gfz-scripts/'+n;b=git('show',C+':'+rel);(H/n).write_bytes(b);raw['sources'][n]=dict(path=rel,sha256=sha(b),blob=git('rev-parse',C+':'+rel).decode().strip())
 sys.path.insert(0,str(H));sp=importlib.util.spec_from_file_location('original_transition_r3',H/'transitions.py');T=importlib.util.module_from_spec(sp);sp.loader.exec_module(T);assert Path(T.team.__file__).resolve()==(H/'team.py').resolve();raw['module_paths']=dict(transition=T.__file__,team=T.team.__file__)
 def dryrun(group,name,b,expected):
  d=R/group/name;d.mkdir(parents=True);f=d/'TEAM.json';f.write_bytes(b);x=json.loads(b);T.team.validate(x);plans=T.plan(copy.deepcopy(x));args=[sys._base_executable,'-B',str(H/'transitions.py'),'--board',str(f),'--json'];q=subprocess.run(args,capture_output=True,text=True,timeout=5)
  row=dict(name=name,input_sha256=sha(b),argv=args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,report=json.loads(q.stdout),original_plan=plans,board_unchanged=sha(f.read_bytes())==sha(b),writer_invoked=False,expected=expected);(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');raw[group].append(row)
  assert q.returncode==0 and not q.stderr and len(row['report'])==len(plans)==1 and row['report'][0]['transition']==expected and row['board_unchanged']
  return row
 for old in rows:dryrun('regression',old['name'],prior('run-01/'+old['name']+'/TEAM.json'),old['expected'])
 valid=json.loads(prior('run-01/valid-accept/TEAM.json'));valid['tasks'][0]['reviews']['commit']=C
 for name,change,expect in [('valid-full40',None,'INCORPORATE'),('commit-full40-lf','commitLF','MALFORMED'),('commit-full40-crlf','commitCRLF','MALFORMED'),('verdict-lf','verdictLF','VERDICT-MISSING')]:
  x=copy.deepcopy(valid)
  if change=='commitLF':x['tasks'][0]['reviews']['commit']+='\n'
  elif change=='commitCRLF':x['tasks'][0]['reviews']['commit']+='\r\n'
  elif change=='verdictLF':x['tasks'][0]['result_refs'][0]+='\n'
  row=dryrun('fields',name,(json.dumps(x,indent=2)+'\n').encode(),expect);op=row['original_plan'][0][3]
  if change is None:assert op['task']['transition_of']['commit']==C and row['report'][0]['status']=='planned'
  else:assert op is None and row['report'][0]['status']=='-'
 original=(H/'team.py').read_bytes();(R/'original-team.py').write_bytes(original)
 guard=b'''# ASTRA labelled child-entry control: normal imported original definitions below unchanged.
if __name__ == '__main__':
    import hashlib,json,os,sys
    from pathlib import Path
    op=json.load(open(sys.argv[sys.argv.index('--file')+1],encoding='utf-8'))
    bp=Path(sys.argv[sys.argv.index('--board')+1]);before=bp.read_bytes();mode=os.environ['ASTRA_PRIVATE_BOARD_CONTROL']
    if mode != 'none':
        import copy,team
        b=json.loads(before);added=copy.deepcopy(op)
        if mode == 'other': added['task']['id']+='-OTHER'
        team.apply(b,sys.argv[sys.argv.index('--agent')+1],added);team.validate(b)
        bp.write_text(json.dumps(b,indent=2)+'\\n',encoding='utf-8')
    receipt={'argv':sys.argv,'received_op':op,'exit_code':int(os.environ['ASTRA_WRITER_CONTROL_EXIT']),'stdout':os.environ['ASTRA_WRITER_CONTROL_STDOUT'],'real_writer_executed':False,'private_intervention':mode,'board_before_sha256':hashlib.sha256(before).hexdigest(),'board_after_sha256':hashlib.sha256(bp.read_bytes()).hexdigest()}
    json.dump(receipt,open(os.environ['ASTRA_WRITER_CONTROL_RECEIPT'],'w',encoding='utf-8'),indent=2)
    sys.stdout.write(receipt['stdout']);sys.exit(receipt['exit_code'])
''';(R/'labelled-child-entry-guard.py').write_bytes(guard);(H/'team.py').write_bytes(guard+original);raw['guarded_team_sha256']=sha(guard+original)
 b=prior('run-01/valid-reject/TEAM.json');plans=T.plan(json.loads(b));assert len(plans)==1 and plans[0][0]=='REPAIR';raw['writer_plan']=plans;expected_op=plans[0][3]|{'task':plans[0][3]['task']|{'requester':'SWE2-FRONTIER'}}
 cases=[('zero-marker',0,'Saved revision 1\n','none','created',0),('nonzero-marker',1,'Saved revision 1\n','none','FAILED:',1),('nonzero-error',1,'Labelled writer failed before success\n','none','FAILED:',1),('zero-no-marker',0,'No Saved revision marker\n','none','FAILED:',1),('exists-absent',1,'task already exists\n','none','FAILED:',1),('exists-derived-id',1,'task already exists\n','derived','exists',0),('exists-other-id',1,'task already exists\n','other','FAILED:',1)]
 for name,code,text,mode,status,parent_code in cases:
  d=R/'writer'/name;d.mkdir(parents=True);bp=d/'TEAM.json';bp.write_bytes(b);rp=d/'child.json';env=os.environ.copy();env.update(ASTRA_WRITER_CONTROL_EXIT=str(code),ASTRA_WRITER_CONTROL_STDOUT=text,ASTRA_WRITER_CONTROL_RECEIPT=str(rp.resolve()),ASTRA_PRIVATE_BOARD_CONTROL=mode)
  args=[sys._base_executable,'-B',str(H/'transitions.py'),'--board',str(bp),'--agent','SWE2-FRONTIER','--apply','--json'];q=subprocess.run(args,capture_output=True,text=True,env=env,timeout=5);child=json.loads(rp.read_text());report=json.loads(q.stdout);after=bp.read_bytes();optemp=Path(child['argv'][child['argv'].index('--file')+1]);row=dict(name=name,argv=args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True,report=report,child=child,input_sha256=sha(b),after_sha256=sha(after),expected_status=status,expected_parent_code=parent_code,temp_op_removed=not optemp.exists());(d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');raw['writer'].append(row)
  assert q.returncode==parent_code and not q.stderr and len(report)==1 and report[0]['status'].startswith(status) and child['received_op']==expected_op and child['exit_code']==code and child['stdout']==text and not child['real_writer_executed'] and row['temp_op_removed']
  T.team.validate(json.loads(after));ids={t['id'] for t in json.loads(after)['tasks']};nid=expected_op['task']['id'];assert (nid in ids)==(mode=='derived') and (nid+'-OTHER' in ids)==(mode=='other') and child['board_before_sha256']==sha(b) and child['board_after_sha256']==sha(after)
  if mode=='none':assert after==b
 for n,z in raw['sources'].items():assert sha((H/n).read_bytes())==(raw['guarded_team_sha256'] if n=='team.py' else z['sha256'])
 raw['verdict']='ACCEPT_SCOPED_EXACT_FIELDS_AND_CALLER_STATUS_R3'
except BaseException as e:raw['exception']=dict(type=type(e).__name__,text=str(e),traceback=traceback.format_exc());raw['verdict']='INVALID'
finally:raw['terminal']=True;(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print(raw['verdict'],raw['exception']);sys.exit(1 if raw['exception'] else 0)
