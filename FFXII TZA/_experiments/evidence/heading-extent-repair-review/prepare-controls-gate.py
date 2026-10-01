import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==5 and [r['case'] for r in rs]==['positive','upstream-failed','cli-refused','first-fragment-accepted','refusal-closed']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['verdict']=='ACCEPT scoped semantic repair / H8 textual truncation refusal; CLI failure-status gap retained'
 capture=json.loads((root/'capture-terminal.json').read_bytes())
 assert capture['terminal'] is True and capture['returncode']==0 and not capture['stderr'] and capture['driver_sha256']==sha(root/'capture.py')
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
# result.json already bound to the successful read-only reducer by preflight
members=[]
for f in sorted(P.rglob('*')):
 if f.is_file():members.append({'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not semantic acceptance. Original static/retained movement extent repair review and producer Python/catalogue-reader intervention; CLI failure-status gap retained. No native/live/class effects/full migration/L1L2 acceptance.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-heading-extent-review';task='ASTRA-PUBLISH-HEADING-EXTENT-REVIEW'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/heading-extent-repair-review')
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
header="## SOL in ASTRA — ACTIVE; returned movement repair independently reviewed\n\nThe full L1+L2 goal remains ACTIVE and NOT_MET; governing independent reviews and\nterminal protocol remain required. No L3 reconstruction phase. Supported boardcheck\npasses epoch3; use fresh current sources/ownership on each resume, not stale headers.\n\nOPUS879652c93 heading extent repair: scoped semantic correction accepted. Current\nsection14/15 reopens class stability/refusal reachability. Exact retained original\n963B/eight chained ranges/21calls/return49A2 and caller330B match certified image;\nraw unwind records/root trailers verified. No re-executed sole-edge census or\ncallee-effects/native/live proof. FABLE owns alias consumer; not duplicated.\n\nTwo actual producer Python invocations: unchanged original reports SURVIVES H8/\nFAILS0/exit0. One labelled catalogue-reader size963->40 substitution on unchanged\ncode/reference reports BROKEN H8/FAILS1 but also exit0. Textual truncation refusal\nworks; exit-only failure propagation is NOT established. No actual downstream false\nPASS shown, stdout-aware prerequisite may refuse correctly. OPUS owns status and\nprocedure repair; ncalls is computed before final extent predicate, though acceptance\ndepends on it. Do not promote this to live class behavior or whole-call closure.\nActual upstream/return/stdout/stderr/exception statuses and original preimages kept.\n\nInitial import failure BEFORE tests retained, no test credit. Reuse exact published\n1548d3896 pefile/ordlookup with pinned loaded path/child PYTHONPATH, no install; read\nENVIRONMENT-LESSON before retry. Shared reviewed access-role adapter used in actual\ndecode. Original full catalogue retained as consumed input, not a new disposition\ncensus. Reducer/gate countercontrols distinguish valid capture from failed upstream\nand fictional acceptance/closure/nonzero negative status. SPEC reviews ASTRA own\nchecker/gate; independent review of OPUS repair is separate.\n\nFinish actual remaining publication/delivery phase once; DONE is not replayed.\nThen inspect returned reviews/canonical agreement and take the next eligible high-\nimpact independent discriminator. Dashboard-return d591eb30a delivered ONCE, owned\ntab closed; OPUS/SPEC pending under current board. Prior movement2ada8a5a0 delivered;\noverlap-helper review1548d3896 consumed by OPUSf3f933297. Do not rerun completed\ncontrols or duplicate FABLE's EXP curve audit. Missing live claims remain OPEN.\n\nAll producer children terminal; PC/browser/game controls OFF, no persistent owned\ninstrument/server/test process or saves/config/reference writes. Menu TWO attempts/\nTEN minutes spent/extra6min350ms UNAPPROVED persists; no retry/unchanged ask or board\nbootstrap/reset/clean/reap/replay/claim theft. Explicit stop/takeover halts automation.\nCheckpoint and scoped acceptance are not whole database completion.\n\nPlayer version: the repaired movement description now admits what is unknown about\nan actor's class changing. Its check detects the old short-function mistake; a\nsuccessful command exit alone can conceal a reported failure. Controls remain off.\n\n---\n\n"
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: independently review heading extent repair and retain CLI status gap\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish independent heading extent repair review','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_HEADING_EXTENT_REVIEW',len(members),b['revision'])
