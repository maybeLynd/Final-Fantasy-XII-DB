import hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists(),'Retained run exists; no replay/overwrite';R.mkdir()
helper=Path('Database/Tools/analysis-kit/gfz-scripts/prereq.py').resolve();retained=R/'prereq.py';shutil.copyfile(helper,retained)
base=Path(sys._base_executable);assert base.is_file()
raw=dict(method='A labelled synthetic controls through actual composer subprocesses',driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),helper_commit=subprocess.check_output(['git','log','-1','--format=%H','--',str(helper)],text=True).strip(),python=sys.version,venv_executable=sys.executable,child_executable=str(base),cases=[])
composer=R/'composer.py'
composer.write_text('''import importlib.util,json,re,sys
spec=importlib.util.spec_from_file_location('subject',sys.argv[1]);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
c=json.load(open(sys.argv[3]));kw=dict(names=('obj',),exits=tuple(c['exits']))
if c['mode']=='tagged':
 kw['tags']=c['tags']
 if c.get('separator')=='tab':kw['line']=re.compile(r'^(PASS|FAIL)\\t(\\S+)(?:\\t|$)')
else:
 def validate(m):
  x=m.obj
  return None if isinstance(x,dict) and x.get('complete') is True and x.get('rows')==[7,9] else 'incomplete required data object'
 kw['validate']=validate
m,why=p.run(sys.argv[2],[sys.argv[2]],**kw)
if why:
 print('COMPOSER_FAIL',why);sys.exit(1)
print('COMPOSER_PASS',json.dumps(m.obj));sys.exit(0)
''')
obj="obj={'complete':True,'rows':[7,9]}\n"
good="print('PASS  A required')\nprint('PASS  B required')\nprint('FAILS 0')\nsys.exit(0)\n"
tag=dict(mode='tagged',tags=['A','B'],exits=[0])
data=dict(mode='data',exits=[0,1])
tab=dict(mode='tagged',tags=['A'],exits=[0],separator='tab')
cases=[
 ('valid-tagged',obj+good,tag,True),
 ('fail-with-zero-exit',obj+good.replace('PASS  B','FAIL  B'),tag,False),
 ('nonzero-exit',obj+good.replace('sys.exit(0)','sys.exit(1)'),tag,False),
 ('missing-file',None,tag,False),
 ('upstream-exception',obj+"raise RuntimeError('deliberate required failure')\n",tag,False),
 ('malformed-output',obj+"print('unrecognized output')\n"+good,tag,False),
 ('same-count-changed-tags',obj+good.replace('PASS  B','PASS  C'),tag,False),
 ('missing-object',good,tag,False),
 ('missing-footer',obj+good.replace("print('FAILS 0')\n",''),tag,False),
 ('data-declared-findings',obj+"print('FAIL findings-only not a required verdict')\nsys.exit(1)\n",data,True),
 ('data-exit-two',obj+"sys.exit(2)\n",data,False),
 ('data-half-built',"obj={'complete':False,'rows':None}\nsys.exit(1)\n",data,False),
 ('default-tab-fail',obj+"print('FAIL\\tA\\trequired failure')\nprint('FAILS 0')\nsys.exit(0)\n",dict(mode='tagged',tags=['A'],exits=[0]),False),
 ('custom-tab-pass',obj+"print('PASS\\tA\\trequired success')\nprint('FAILS 0')\nsys.exit(0)\n",tab,True),
 ('custom-tab-fail',obj+"print('FAIL\\tA\\trequired failure')\nprint('FAILS 0')\nsys.exit(0)\n",tab,False),
 ('bounded-timeout',obj+"import time\ntime.sleep(3)\n"+good,tag,False),
]
for name,body,declaration,expected in cases:
 d=R/name;d.mkdir();up=d/'upstream.py';decl=d/'declaration.json';decl.write_text(json.dumps(declaration))
 if body is not None:up.write_text('import sys\n'+body)
 args=[str(base),'-B',str(composer),str(retained),str(up),str(decl)];timeout=1 if name=='bounded-timeout' else 5
 try:
  r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
  obs=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
 except subprocess.TimeoutExpired as e:
  obs=dict(returncode=None,stdout=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '',stderr=(e.stderr or b'').decode() if isinstance(e.stderr,bytes) else e.stderr or '',timed_out=True)
 accepted=obs['returncode']==0 and obs['stdout'].startswith('COMPOSER_PASS ')
 raw['cases'].append(dict(name=name,expected_accepted=expected,actually_accepted=accepted,expectation_met=accepted==expected,invocation=args,declaration=declaration,upstream_sha256=hashlib.sha256(up.read_bytes()).hexdigest() if up.exists() else None,**obs))
 (d/'receipt.json').write_text(json.dumps(raw['cases'][-1],indent=2)+'\n')
# First adopter: authored suite executed separately, no silent missing dependency PASS.
t=Path('Database/FFXII TZA/_index/candidates/sn1-layouts/test_sn1_prereq.py').resolve()
raw['first_adopter']={'path':str(t),'available':t.is_file()}
if t.is_file():
 shutil.copyfile(t,R/'first-adopter-test.py');raw['first_adopter']['sha256']=hashlib.sha256(t.read_bytes()).hexdigest()
 try:
  r=subprocess.run([sys.executable,'-B',str(t)],capture_output=True,text=True,timeout=30)
  raw['first_adopter'].update(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
 except subprocess.TimeoutExpired as e:raw['first_adopter'].update(returncode=None,timed_out=True,stdout=str(e.stdout),stderr=str(e.stderr))
raw['helper_unchanged']=hashlib.sha256(helper.read_bytes()).hexdigest()==raw['helper_sha256']
raw['finished']=True
(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('PREREQ_CAPTURE',len(raw['cases']),'UNEXPECTED',[x['name'] for x in raw['cases'] if not x['expectation_met']], 'FIRST_ADOPTER',raw['first_adopter'].get('returncode'))
