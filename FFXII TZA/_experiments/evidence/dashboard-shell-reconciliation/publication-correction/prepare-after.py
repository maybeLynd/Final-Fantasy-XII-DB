import json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/migration-generation-independent')
# Publication lesson: raw ZIP fixtures inherit Database/*.zip ignores. Check the
# actual reviewed invocation paths before any claim/write, not only hash flags.
def check_ignored_paths(paths):
 payload=b'\0'.join(str(p).encode('utf-8') for p in paths)+b'\0'
 q=subprocess.run(['git','check-ignore','-q','--stdin','-z'],input=payload,capture_output=True)
 assert q.returncode in (0,1),q.stderr
 assert q.returncode==1,'Ignored reviewed publication path; preserve bytes/use package-local exception before claiming'
if '--preflight-only' in sys.argv:
 pinfile=W/'publication/reviewed.json'
 if '--preflight-pins' in sys.argv:pinfile=Path(sys.argv[sys.argv.index('--preflight-pins')+1])
 check_ignored_paths(json.loads(pinfile.read_text()))
 print('PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES',flush=True);sys.exit(0)
check_ignored_paths([f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()])
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
assert json.loads((P/'result.json').read_text())['verdict']=='REJECT'
ID='ASTRA-PUBLISH-MIGRATION-GENERATION-BOUNDARIES';SID='ASTRA-sol-20260929-generation-independent'
b=json.loads(team.BOARD.read_text())
if not any(t['id']==ID for t in b['tasks']):
 b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{
 'id':ID,'kind':'research','priority':'P1','target':'Publish independent generation export defects and valid interruption/input controls',
 'scope':'Own92 immutable members, ASTRA header and supportedTEAM only',
 'completion':'Actual committed blobs/body/epoch/all92 member SHA verified, short publication released; cause repair/evidence review separately routed',
 'dependencies':[],'resources':[{'key':'@publication'}]}},SID)
 print('ADDED_GENERATION_PUBLICATION',b['revision'],flush=True)
p=W/'publication';assert not p.exists(),'Inspect existing attempt, never overwrite/replay';p.mkdir()
old=W.parent/'migration-transitions-independent/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-admission',SID).replace('ASTRA-PUBLISH-MIGRATION-TRANSITION-ADMISSION',ID).replace('evidence/migration-transitions-independent','evidence/migration-generation-independent')
(p/'publish.py').write_text(s)
pins={f.as_posix():subprocess.check_output(['git','hash-object','--',f.as_posix()],text=True).strip() for f in sorted(P.rglob('*')) if f.is_file()}
assert len(pins)==93
(p/'reviewed.json').write_text(json.dumps(pins,indent=2)+'\n')
(p/'message.txt').write_text('ASTRA: reject ambiguous ZIP certification; verify generation interruption and input boundaries\n')
print('PREPARED_GENERATION_PUBLICATION',len(pins),flush=True)
