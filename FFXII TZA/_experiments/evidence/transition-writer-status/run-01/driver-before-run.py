import ast,copy,hashlib,importlib.util,json,os,subprocess,sys,traceback
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();H=R/'source/Database/Tools/analysis-kit/gfz-scripts';H.mkdir(parents=True);sha=lambda b:hashlib.sha256(b).hexdigest();C='f21fe80440fc9d24df09fc19172753394fe61773';OLD=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-r2');OC='117f85ab6889eb7915d01e2a8f7596e762bbf25f'
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0,q.stderr;return q.stdout
r={'method':'A actual original transition CLI and labelled child-entry writer substitution; not supportedwriter execution/game/productionwrites','source_commit':C,'prior_commit':OC,'driver_sha256':sha(Path(__file__).read_bytes()),'sources':{},'cases':[],'terminal':False,'exception':None,'python':{'version':sys.version,'base':sys._base_executable,'base_sha256':sha(Path(sys._base_executable).read_bytes())}};(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
try:
 mbytes=(OLD/'manifest.json').read_bytes();assert git('show',OC+':'+(OLD/'manifest.json').as_posix())==mbytes
 m=next(x for x in json.loads(mbytes)['members'] if x['path']=='run-01/valid-reject/TEAM.json');data=(OLD/m['path']).read_bytes();assert sha(data)==m['sha256'] and git('show',OC+':'+(OLD/m['path']).as_posix())==data;(R/'original-fixture.json').write_bytes(data);r['prior_manifest_sha256']=sha(mbytes);r['fixture_sha256']=sha(data)
 for n in ['transitions.py','team.py']:
  rel='Database/Tools/analysis-kit/gfz-scripts/'+n;b=git('show',C+':'+rel);(H/n).write_bytes(b);r['sources'][n]={'path':rel,'sha256':sha(b),'blob':git('rev-parse',C+':'+rel).decode().strip()}
 original=(H/'team.py').read_bytes();(R/'original-team.py').write_bytes(original)
 guard='''# ASTRA labelled child-entry substitution: original imported definitions below are unchanged.
if __name__ == '__main__':
    import json,os,sys
    receipt={'argv':sys.argv,'exit_code':int(os.environ['ASTRA_WRITER_CONTROL_EXIT']),'stdout':os.environ['ASTRA_WRITER_CONTROL_STDOUT'],'real_writer_executed':False}
    fp=sys.argv[sys.argv.index('--file')+1]
    receipt['received_op']=json.load(open(fp,encoding='utf-8'))
    json.dump(receipt,open(os.environ['ASTRA_WRITER_CONTROL_RECEIPT'],'w',encoding='utf-8'),indent=2)
    sys.stdout.write(receipt['stdout'])
    sys.exit(receipt['exit_code'])
'''.encode();(R/'labelled-child-entry-guard.py').write_bytes(guard);(H/'team.py').write_bytes(guard+original);r['private_team_with_guard_sha256']=sha(guard+original)
 sys.path.insert(0,str(H));sp=importlib.util.spec_from_file_location('original_transition',H/'transitions.py');T=importlib.util.module_from_spec(sp);sp.loader.exec_module(T);assert Path(T.team.__file__).resolve()==(H/'team.py').resolve();r['module_paths']={'transition':T.__file__,'team':T.team.__file__};b=json.loads(data);T.team.validate(b);plans=T.plan(copy.deepcopy(b));assert len(plans)==1 and plans[0][0]=='REPAIR' and plans[0][3] is not None;r['original_plan']=plans
 current=Path(r['sources']['transitions.py']['path']).read_bytes();(R/'current-parent-preimage.py').write_bytes(current)
 def status_assignment(text):
  return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='status' for t in n.targets) and 'Saved revision' in ast.unparse(n)]
 old= status_assignment((H/'transitions.py').read_text());new=status_assignment(current.decode());assert len(old)==len(new)==1 and old==new;r['current_status_assignment_equal']=True;r['current_parent_sha256']=sha(current)
 controls=[('zero-marker',0,'Saved revision 1\n'),('nonzero-marker',1,'Saved revision 1\n'),('nonzero-error',1,'Labelled writer failed before success\n')]
 for name,code,text in controls:
  bp=R/(name+'-board.json');bp.write_bytes(data);rp=R/(name+'-child.json');env=os.environ.copy();env.update(ASTRA_WRITER_CONTROL_EXIT=str(code),ASTRA_WRITER_CONTROL_STDOUT=text,ASTRA_WRITER_CONTROL_RECEIPT=str(rp.resolve()))
  argv=[sys._base_executable,'-B',str(H/'transitions.py'),'--board',str(bp),'--agent','SWE2-FRONTIER','--apply','--json'];q=subprocess.run(argv,capture_output=True,text=True,env=env,timeout=5);rows=json.loads(q.stdout);assert len(rows)==1 and rp.exists() and sha(bp.read_bytes())==sha(data);child=json.loads(rp.read_text());assert child['exit_code']==code and child['stdout']==text and not child['real_writer_executed'] and child['received_op']==plans[0][3]|{'task':plans[0][3]['task']|{'requester':'SWE2-FRONTIER'}}
  r['cases'].append({'name':name,'argv':argv,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'report':rows,'child':child,'board_unchanged':True,'terminal':True})
 assert sha((H/'transitions.py').read_bytes())==r['sources']['transitions.py']['sha256'] and sha((H/'team.py').read_bytes())==r['private_team_with_guard_sha256']
 r['verdict']='REJECT_NONZERO_REQUIRED_WRITER_SUPPRESSED_BY_MARKER'
except BaseException as e:r['exception']={'type':type(e).__name__,'text':str(e),'traceback':traceback.format_exc()};r['verdict']='INVALID'
finally:r['terminal']=True;(R/'raw.json').write_text(json.dumps(r,indent=2)+'\n');print(r['verdict'],r['exception']);sys.exit(1 if r['exception'] else 0)
