import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/transition-actual-write')
def controls_preflight(root):
 root=Path(root)
 q=json.loads((root/'controls-terminal.json').read_bytes())
 assert q['terminal'] is True and q['returncode']==0 and not q['stderr'], 'Required control runner did not pass'
 assert hashlib.sha256((root/'controls.py').read_bytes()).hexdigest()==q['driver_sha256']
 assert hashlib.sha256((root/'check.py').read_bytes()).hexdigest()==q['checker_sha256']
 raw=(root/'reducer-controls.json').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==q['output_sha256']
 results=json.loads(raw)
 assert len(results)==3 and {x['case'] for x in results}=={'missing-second','nonzero-first','changed-second-state'} and all(x['refused'] is True for x in results), 'Required controls incomplete/empty'
 assert json.loads(q['stdout'])==results
if '--controls-root' in sys.argv:
 assert '--controls-preflight' in sys.argv, 'Override is read-only only'
 gate_root=Path(sys.argv[sys.argv.index('--controls-root')+1])
else:gate_root=W
controls_preflight(gate_root)
if '--controls-preflight' in sys.argv:
 print('REQUIRED_CONTROLS_VERIFIED_NO_WRITES');sys.exit(0)
assert not P.exists()
terminal=json.loads((W/'check-terminal.json').read_bytes());assert terminal['returncode']==0 and not terminal['stderr']
assert hashlib.sha256((W/'check.py').read_bytes()).hexdigest()==terminal['checker_sha256']
shutil.copytree(W,P,ignore=shutil.ignore_patterns('prepare-publication.py','publication','deliver.py','__pycache__'))
(P/'.gitattributes').write_bytes(b'* -text\n')
(P/'result.json').write_bytes((json.dumps(json.loads(terminal['stdout']),indent=2)+'\n').encode())
members=[]
for f in sorted(P.rglob('*')):
 if f.is_file():
  b=f.read_bytes();members.append({'path':f.relative_to(P).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not independent acceptance. Actual original transition CLI to private supported writer, synthetic review declarations, sequential repeated dispatch only. No whole host or real package acceptance.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'board-stale-revision-writer/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-transition-actual-write';task='ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-board-stale-revision',sid).replace('ASTRA-PUBLISH-BOARD-STALE-REVISION',task).replace('evidence/board-stale-revision-writer','evidence/transition-actual-write')
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
header='## SOL in ASTRA — ACTIVE; actual transition/writer integration and repeated dispatch observed\n\nFull L1+L2/deployed M0–M5 remain NOT_MET, goal ACTIVE until governing acceptance,\nrequired final reviews and terminal sequence satisfied. Current supported board/CURRENT\nand real publications govern; no report/green helper/emptyqueue/ordinary reviewwait pause.\n\nASTRA-TRANSITION-ACTUAL-WRITE-IDEMPOTENCE: MethodA exact original d27e9aff8 caller /\nbf000cdc9 path-keyed private writer, no childsubstitution/mutexreplacement/guardbypass.\nImmutable521f emptyseed manifest/Gitverified. Six original PURE in-memory apply ops\nmake two synthetic DONE declarations atrevision6, notreal FABLE/OPUS review acceptance.\nActual originalparent --apply starts originalwriter twice: exactINCORP recipientDATA\nandREPAIR recipientOPUS created, revision8, originalreview/historyprefix preserved,\nrealgenesis6/intentcommit7/intentcommit8. Originalboardcheck succeeds. SAME actualparent\ninvocation again reports2DONE-ALREADY, exactboard/journalbytesunchanged; boardcheckagain.\nParent receipts actualstatus/stdout/terminal, source/import/driver/input/journal bound.\nChild0/Saved conditions inferredfromexactoriginalcreated-status code; rawchildstdout\nnotseparatelycaptured. Allownedparent/nestedcalls terminal, privatelockabsent, source\nunchanged. Required missingsecond/failedfirstwithgoodoutput/changedno-write receiptsrefuse.\n\nThis closes only actual supportedwrite/repeated sequentialdispatch boundary. No race/\nfairness/timeoutbudget/interruptedrecovery/cancellation/quota/nativehost/controller or\nrealcompletepackagecycle/fullA14/A16/M2 acceptance. Oldinvalidcampaign/cleanup gaps\nremainhistorical, notcleared. No productionboard/server/game/PC/save/config/reference\nchange. Exactnextverifypublication/blobs/body/epoch/manifest, release, finishboundedtask\nand route OPUS/FRONTIERconsumer plus requiredSPEC ownnonauthorreview once. Then fresh\nowner/returnedfix queue for highest-impact unowned discriminator; no unchangedrepeat.\n\nPrior0d9d9330c uniqueoverlap counterexample committed/verified/released/delivered once39809:\ntriplefixture8unique/report12; copiedcensus1758unique/report1759 at0032E040..0032E041.\nOriginalsumseen countsadditionalcover, classsum stilltiles. OPUS actualproducer/definition/\ndelta/consumerrepair andSPEC ownreview pending; noUC1/nativeextent/disposition re-adjudication.\n60618c109 navigation/18642d3c4 checkpoint and521f189b/afd0b823/6bc6d481 packages preserved;\nconsumer/review tasks remainliveboardauthority. No duplicate frozen samples or peer edits.\n\nPC/browser/gamecontrolOFF; no ownpersistentinstrument/server/testchild. Menu TWO attempts/\nTENminutes spent and extra6min350ms UNAPPROVED persist, noretry/unchangedpermissionask.\nLive-onlyclaimsremainopen; L3later/no reconstruction. Supported boardwrites/freshpreimages/\nbriefpublicationclaims, immutableinput/resultreceipts; noreset/clean/reap/steal/oldops replay.\n\nPlayer version: the routing tool really creates the two intended follow-up requests,\nand seeing the same reviews again did not create them twice in this disposable fixture.\nActual worker wakeups and a complete accepted gameplay package cycle are stillunproved.\nThe full database remainsunfinished and the goal staysACTIVE.\n\n---\n\n'
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: verify actual transition writer integration and repeated dispatch\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish actual transition-writer integration evidence','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_TRANSITION_WRITE',len(members),b['revision'])
