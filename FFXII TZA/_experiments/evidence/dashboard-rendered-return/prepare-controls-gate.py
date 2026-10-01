import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/dashboard-rendered-return')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==5 and [r['case'] for r in rs]==['positive','upstream-failed','ambiguous-target','missing-return','missing-cleanup']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['result']=='BOUNDED_RENDERED_RETURN_ESTABLISHED'
 capture=json.loads((root/'preflight-terminal.json').read_bytes())
 assert capture['terminal'] is True and capture['returncode']==0 and not capture['stderr'] and capture['driver_sha256']==sha(root/'preflight.py')
 assert json.loads(capture['stdout'])==json.loads((root/'identity.json').read_bytes())
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not semantic acceptance. One HOST_BROWSER rendered Activity to Progress return; non-atomic raw DOM/AX/JPEG/HTTP, no event-handler trace, loaded-module identity, totals/allviews/A17/M3/migration/FF12/L1L2 acceptance.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-rendered-return';task='ASTRA-PUBLISH-DASHBOARD-RENDERED-RETURN'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/dashboard-rendered-return')
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
header="## SOL in ASTRA — active goal; safe delivered stopping point\n\nThe full L1+L2 goal remains ACTIVE and NOT_MET. This is the user's requested\nrecoverable stopping point, not goal achievement or a permanent pause. Preserve\nidentity, history and governing completion/review/final-audit requirements. L3 is\nlater; no primary reconstruction phase is authorized.\n\nCurrent dashboard-rendered-return package: HOST_BROWSER only, one observed\nActivity -> My Progress return. Stable role/name matched one visible target and\nexcluded mutable status text. Two input actions; immediate AX, later DOM and JPEG\nshow the destination. Status changed during setup, not proven at exact dispatch.\nOriginal HTTP/source/raw identities, successful upstream status and four rejected\nreducer alternatives retained. Seven immutable raw captures; ordered non-atomic\nobservations, interactive CUA calls rather than a standalone browser driver.\nNo proof of input registration/event-handler internals, every polling race, loaded\nserver module/PID/build, progress numbers, all views, full A17/M3/migration or FF12.\nOld60618c109 refused returns remain valid; no retroactive credit or repeated game\nsample. OPUS scoped canonical consumption and SPEC non-author raw/check/gate review\nmust remain separate from producer checks and publication integrity.\n\nBrowser tab3 closed and absent from inventory. PC/browser/game controls OFF; no\nowned persistent observer/server/instrument/test child or process handle. Peer\nserver untouched; no game/save/config/reference/source changes. Menu TWO attempts/\nTEN minutes spent and extra6min350ms UNAPPROVED persist across sessions/epochs.\nNo reopen, unchanged permission question, bootstrap, worktree, guard bypass,\nreset/clean/reap/claim stealing or old-operation replay. Explicit stop/takeover\nhalts automation; do not automatically resume after it.\n\nResume with supported fresh boardcheck/CURRENT, current ownership and actual\npublication/review receipts. Finish any current incomplete publication/delivery\nphase once; a DONE task must not be recaptured or resent. Consume returned evidence\nand owner repairs first. The movement2ada8a5a0 corrections and independent OPUS\nrepair review1548d3896 are already committed/delivered; prior checkpoint184bcf4b8\npreserves their exact scope. Independent review/canonical acceptance remains\npending as recorded by current tasks; do not duplicate FABLE's assigned EXP curve\nreview or edit a peer consumer. Next select the highest-impact eligible independent\nimplementation discriminator from checked records, respecting scarce runtime\nbudget and explicit live-only gaps. Missing live evidence blocks affected claims,\nnot independent database work. Checkpoint is not database completion.\n\nPlayer version: the dashboard returned from the agent view correctly using its\nstable button name. Its progress numbers were not validated. Controls are off and\nthe evidence and next steps are preserved for continued database work.\n\n---\n\n"
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: preserve one observed dashboard return and safe stopping checkpoint\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish bounded rendered return and safe stopping checkpoint','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_RENDERED_RETURN',len(members),b['revision'])
