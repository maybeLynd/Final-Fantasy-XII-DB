import hashlib,json,os,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';assert not R.exists();R.mkdir()
prior=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
sys.path.insert(0,str((prior/'python-deps').resolve()))
import capstone,pefile
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;b=json.loads(team.BOARD.read_bytes());t=next(t for t in b['tasks'] if t['id']=='ASTRA-HEADING-STATUS-REPAIR-REVIEW');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0 and not q.stderr;return q.stdout
source=Path('Database/Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py');catalog=Path('Database/Tools/work/graph/functions.tsv');exe=Path('Database/Tools/work/exe/FFXII_TZA.exe')
manifest={x['path']:x for x in json.loads((prior/'manifest.json').read_bytes())['members']}
needed=['h8-input-intervention.py','retained/functions.tsv','python-deps/pefile.py']+[p.relative_to(prior).as_posix() for p in (prior/'python-deps/ordlookup').rglob('*.py')]
for n in needed:assert sha(prior/n)==manifest[n]['sha256'] and (prior/n).stat().st_size==manifest[n]['bytes']
assert sha(catalog)==sha(prior/'retained/functions.tsv'),'Paired catalogue changed; preserve and revise rather than silently mix inputs'
ref=git('show','2366027d98e5c9016150e36437ee398d9472248b:'+source.as_posix());cur=source.read_bytes();assert cur.replace(b'\r\n',b'\n')==ref.replace(b'\r\n',b'\n')
(R/'producer-current.py').write_bytes(cur);(R/'producer-2366027d9.py').write_bytes(ref)
identity={'method':'A original producer Python/labelled catalogue reader; no native/game execution','driver_sha256':sha(Path(__file__)),'producer_commit':'2366027d98e5c9016150e36437ee398d9472248b','producer_sha256':sha(source),'commit_source_sha256':hashlib.sha256(ref).hexdigest(),'text_comparison':'Only CRLF->LF for equivalence, raw bothversions preserved','head':git('rev-parse','HEAD').decode().strip(),'dependencies':[{'path':str(prior/n),'sha256':sha(prior/n),'published_at':'feb631dd4755e77a1edfed3c9b20f7d629d30d70','member':n} for n in needed],'providers':[],'catalogue_sha256':sha(catalog),'exe_sha256':sha(exe)}
assert identity['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
for p in [Path(sys.executable),Path(capstone.__file__),Path(capstone.__file__).parent/'lib/capstone.dll',Path(pefile.__file__)]:identity['providers'].append({'path':str(p),'sha256':sha(p)})
identity['python']=sys.version;identity['loaded_pefile']=pefile.__file__
(W/'identity-before.json').write_text(json.dumps(identity,indent=2)+'\n')
receipts=[];env=os.environ.copy();env['PYTHONPATH']=str((prior/'python-deps').resolve())
for label,a in [('original',[sys.executable,'-B',str(source)]),('first-fragment-catalogue',[sys.executable,'-B',str(prior/'h8-input-intervention.py'),'--source',str(source),'--catalog',str(prior/'retained/functions.tsv')])]:
 q=subprocess.run(a,capture_output=True,text=True,env=env)
 receipts.append({'case':label,'argv':a,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True,'producer_sha256':sha(source),'wrapper_sha256':sha(prior/'h8-input-intervention.py') if label!='original' else None})
 (W/'producer-terminal.json').write_text(json.dumps(receipts,indent=2)+'\n')
 assert not q.stderr and q.returncode in [0,1],'Unexpected setup/process failure, no silent retry'
assert sha(source)==identity['producer_sha256'] and sha(catalog)==identity['catalogue_sha256'] and sha(exe)==identity['exe_sha256']
for x in identity['dependencies']:assert sha(x['path'])==x['sha256']
(W/'identity.json').write_text(json.dumps(identity,indent=2)+'\n');print('REPAIRED_H8_PAIRED_STATUS_CAPTURED')
