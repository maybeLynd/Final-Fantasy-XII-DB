import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/uc1-dependency-binding')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);q=json.loads((root/'controls-terminal.json').read_bytes())
 assert q['terminal'] is True and q['returncode']==0 and not q['stderr'], 'Required upstream control runner failed/missing'
 assert sha(root/'controls.py')==q['driver_sha256'] and sha(root/'check.py')==q['checker_sha256']
 raw=(root/'reducer-controls.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==q['output_sha256']
 controls=json.loads(raw)
 assert len(controls)==3 and {x['case'] for x in controls}=={'missing-manifest','nonzero-capture','changed-bound-table'} and all(x['refused'] is True for x in controls), 'Required controls incomplete/empty'
 assert json.loads(q['stdout'])==controls
 check=json.loads((root/'check-terminal.json').read_bytes())
 assert check['terminal'] is True and check['returncode']==0 and not check['stderr'] and sha(root/'check.py')==check['driver_sha256']
 assert json.loads(check['stdout'])['result']=='SCOPED_DEPENDENCY_BINDING_GAP'
if '--controls-root' in sys.argv:
 assert '--controls-preflight' in sys.argv
 gate_root=Path(sys.argv[sys.argv.index('--controls-root')+1])
else:gate_root=W
controls_preflight(gate_root)
if '--controls-preflight' in sys.argv:
 print('REQUIRED_CONTROLS_VERIFIED_NO_WRITES');sys.exit(0)
assert not P.exists()
shutil.copytree(W,P,ignore=shutil.ignore_patterns('prepare-publication.py','publication','deliver.py','__pycache__'))
shutil.copyfile(Path(__file__),P/'prepare-controls-gate.py')
(P/'.gitattributes').write_bytes(b'* -text\n')
terminal=json.loads((W/'check-terminal.json').read_bytes())
(P/'result.json').write_bytes((json.dumps(json.loads(terminal['stdout']),indent=2)+'\n').encode())
members=[]
for f in sorted(P.rglob('*')):
 if f.is_file():members.append({'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not independent acceptance. Selected retained manifest/output and static dependency path only; no full build, source-change drift/skip/export, loaded helper version or FF12 execution.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-uc1-dependency';task='ASTRA-PUBLISH-UC1-DEPENDENCY-BINDING'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/uc1-dependency-binding')
(p/'publish.py').write_text(s)
paths=[f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()];pay='\n'.join(paths)+'\n';got=[]
for flags in ([],['--no-filters']):
 q=subprocess.run(['git','hash-object','--stdin-paths',*flags],input=pay,capture_output=True,text=True)
 assert q.returncode==0 and not q.stderr and len(q.stdout.splitlines())==len(paths);got.append(q.stdout.splitlines())
assert got[0]==got[1] and len(paths)==len(members)+1
(p/'reviewed.json').write_text(json.dumps(dict(zip(paths,got[0])),indent=2)+'\n')
a=[sys.executable,'-B',str(W.parent/'migration-generation-independent/prepare-publication.py'),'--preflight-only','--preflight-pins',str(p/'reviewed.json')]
q=subprocess.run(a,capture_output=True,text=True)
(p/'path-preflight.json').write_text(json.dumps({'argv':a,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True},indent=2)+'\n')
assert q.returncode==0 and q.stdout.strip()=='PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES' and not q.stderr
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
sys.path.insert(0,str(p));from verify import normalized
ok,d=team.board_status(team.BOARD);assert ok,d;b=json.loads(team.BOARD.read_text())
inbox=Path('Database/FFXII TZA/_index/_inbox/ASTRA.md');text=inbox.read_text()
header='''## SOL in ASTRA — ACTIVE; UC1 helper-code binding gap packaged

The full FF12 L1+L2 goal stays ACTIVE until governing completion and required
independent reviews/final protocol are satisfied. Checkpoints, green checks,
all-MET labels, reports and ordinary publication/review waits do not end it.
Fresh supported board/claims and actual publications govern subsequent resumes.

Current bounded ASTRA-DASHBOARD-UC1-DEPENDENCY-BINDING: Method A selected retained
g20260929T135626Z-00f775 manifest/output and exact17d6 builder declarations. Builder
calls uc1_band.load/apply/describe; view names apply. All25 returned input keys
match selected manifest. Builder and two band-table snapshots positively bound,
generation verifier binds generation.py only; helper code path/hash absent.
Current helper bytes do not identify historical loaded helper. No full build,
source-change drift/skip/export, all-dependency/archive or A05/A23/M1 acceptance.
Initial extracted declaration failed at missing supplied __file__, INVALID.
Retained driver/terminal/raw; corrected actual pathname global, same retained
source/manifest/view bytes, no full module import or adapters executed. Read-only
reducer succeeds; missingmanifest/nonzerocapture/changedtable controls refuse.
Preparation and actual publication require complete successful bound controls.

Exact next: verify actual publication blobs/body/epoch/manifest, release, finish
bounded task, route OPUS canonical helper-binding repair and required SPEC review
once. While acceptance waits choose next eligible implementation discriminator
from checked current ownership; do not repeat settled samples or peer-owned work.

Prior c7f2f592f transition/writer package committed, verified, released, delivered
once39818: actual originald27 parent/bf000 path-keyed private writer creates exact
two follow-ups from labelled synthetic reviews, repeat unchanged dispatch no-write.
No actual host/controller/package cycle/races/cancellation/quota acceptance.
Preparation prerequisite defect/failure preserved, actual gate fixed and controls
validated; independent gate/evidence review pending. Prior0d9d9330c overlap package
delivered39809: triplefixture8unique/report12; retainedcensus1758/report1759 at
0032E040..0032E041. OPUS producer/definition/delta repair and SPEC review pending.
No UC1 adjudication/native extent or primary index regression claimed.
60618c109 navigation/18642d3c4 checkpoint and521f189b/afd0b823/6bc6d481 preserved.
FABLE canonical68d835b52 incorporates PoisonQ6 exact bounded scope; tick/live
limits remain, no whole-package closure. Current consumer/review board is authority.

PC/browser/game controls OFF. No own persistent instrument/server/test child.
Menu TWO attempts/TENminutes spent; extra6min350ms UNAPPROVED persists. No retry,
unchanged permission ask, board reset/replay/reap/steal, peer reset/clean, bootstrap
or reconstruction. Live-only gaps remain open. New user stop/takeover halts control;
ordinary authorized bounded live research remains subject to valid prepared state.

Player version: reproducing a database measurement requires exact helper code
as well as the data; we found one missing code binding in the existing receipt.
No game behavior changed or live test was run. Database work continues.

---

'''
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: expose executable-view UC1 helper source-binding gap\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish UC1 helper source-binding evidence','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_UC1_DEPENDENCY',len(members),b['revision'])
