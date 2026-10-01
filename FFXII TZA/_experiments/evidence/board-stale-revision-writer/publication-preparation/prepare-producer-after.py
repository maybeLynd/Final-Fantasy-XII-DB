import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
P=Path('Database/FFXII TZA/_experiments/evidence/board-stale-revision-writer')
assert not P.exists()
assert json.loads((W/'check-terminal-r2.json').read_text())['returncode']==0
shutil.copytree(W,P,ignore=shutil.ignore_patterns('prepare-publication.py','publication'))
# Frozen receipts include literal Windows newlines. Preserve their exact bytes in
# Git rather than letting core.autocrlf change a cited result or its manifest.
(P/'.gitattributes').write_bytes(b'* -text\n')
for base in (P/'run-01',P/'run-02'):
 assert not (base/'private/TEAM.lock').exists()
meta={'root_capture_sha256':hashlib.sha256((P/'capture.py').read_bytes()).hexdigest(),
      'root_capture_status':'NOT_EXECUTED after wording-only overlap qualification; actual drivers retained separately at run-01/capture.py and run-02/capture.py',
      'checker_sha256':hashlib.sha256((P/'check.py').read_bytes()).hexdigest(),
      'checker_status':'EXECUTED, check-terminal-r2.json; independent acceptance separate',
      'raw_receipts_immutable':True,'full_A13':'NOT_ACCEPTED'}
(P/'producer-versions.json').write_text(json.dumps(meta,indent=2)+'\n')
result=json.loads(json.loads((P/'check-terminal-r2.json').read_text())['stdout'])
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n')
members=[]
for f in sorted(P.rglob('*')):
 if f.is_file():
  b=f.read_bytes();members.append({'path':f.relative_to(P).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(P/'manifest.json').write_text(json.dumps({'schema':1,'members':members,'limits':'Integrity is not independent semantic acceptance. Original invalid attempt and copy-state intervention retained.'},indent=2)+'\n')
p=W/'publication';assert not p.exists();p.mkdir()
old=W.parent/'migration-transitions-r3/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-board-stale-revision';task='ASTRA-PUBLISH-BOARD-STALE-REVISION'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transitions-r3',sid).replace('ASTRA-PUBLISH-TRANSITIONS-R3',task).replace('evidence/migration-transitions-r3','evidence/board-stale-revision-writer')
(p/'publish.py').write_text(s)
paths=[f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()]
q=subprocess.run(['git','hash-object','--stdin-paths'],input='\n'.join(paths)+'\n',capture_output=True,text=True)
assert q.returncode==0 and not q.stderr and len(q.stdout.splitlines())==len(paths)
pins=dict(zip(paths,q.stdout.splitlines()));assert len(pins)==len(members)+1
(p/'reviewed.json').write_text(json.dumps(pins,indent=2)+'\n')
a=[sys.executable,'-B',str(W.parent/'migration-generation-independent/prepare-publication.py'),'--preflight-only','--preflight-pins',str(p/'reviewed.json')]
q=subprocess.run(a,capture_output=True,text=True)
(p/'path-preflight.json').write_text(json.dumps({'argv':a,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True},indent=2)+'\n')
assert q.returncode==0 and q.stdout.strip()=='PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES' and not q.stderr
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
sys.path.insert(0,str(p));from verify import normalized
ok,d=team.board_status(team.BOARD);assert ok,d
b=json.loads(team.BOARD.read_text())
inbox=Path('Database/FFXII TZA/_index/_inbox/ASTRA.md');text=inbox.read_text()
header='''## SOL in ASTRA — ACTIVE; original private writer rejects stale revision

Full L1+L2 and deployed M0–M5 remain NOT_MET. The user reaffirmed that this goal stays
ACTIVE until full governing acceptance. Ordinary checkpoints/packages/review waits are
not completion or pause; genuine user stops/takeover and actual host/usage limits bind.
Fresh supported epoch3 boardcheck/CURRENT governs selection, not historical headers.

ASTRA-BOARD-STALE-REVISION-WRITER: Method A actual unmodified bf000cdc96d3ca9ec7fb461d0e066572d6657041
repository CLI/transaction on a synthetic private fixture; path-keyed mutex source is the
meaningful change from old shared-namespace failure. Fresh expected0 -> revision1;
stale0 -> exit1 with board/journal byte-identical; two independently launched expected1
callers -> one revision2 commit, one exit1/refusal; fresh2 -> revision3. Original CLI
boardcheck succeeds after positive/pair/follow-on; own processes terminal, private lock
absent, source unchanged. No production board replacement/recovery, lock substitution,
original FF12 code/live execution, save/config/reference or PC/browser controls.

Run01 INVALID: writer succeeded, our driver wrongly demanded LF against WindowsCRLF.
Original source/raw/state retained; corrected actual default keeps raw bytes and compares
exact splitlines, extra output refuses. Run02 validates/copies exact successful private
board+journal and reuses positive; only still-unrun stale/pair/follow-on executed. Copy
is an explicit fixture intervention, not proof of same-path lifetime. First child was
nonterminal BEFORE second launch, both spawned before collection; simultaneous child
execution/contention not proved. Raw overlap wording qualified by corrected producer
default/normalized checker/prose; wording-only producer-after NOT_EXECUTED. Final checker
source-hash-bound, missing-case/hidden-exit/extra-output receipt controls refuse.

Exactnext: verify actual publication blobs/body/epoch/manifest and release, finish bounded
task and route OPUS canonical scope/required SPEC evidence review once. Then read checked
current source/review returns and take next implementation-relevant discriminator.
Do not repeat this settled gate or claim wholeA13, fairness, interrupted intent/commit,
removed-lock/epoch-recovery, taskidempotence, controller/deployment or old descendant cleanup.

Previous transitions5eaabddf/activity8380c611/baseline9e84de62 committed and routed once;
OPUS incorporation and own nonauthor reviews pending as current board records. q0 count
already corrected to59 by dafa690954d147ac94cf5bd088dec193c4e357e0 and acknowledged;
do not reopen stale61 request. DATA consumer tasks still separate. Serverc466fc47 scoped
consumption7c14ecf56 preserved; supplied restart/PID is not independent loaded-module proof.

PC/game control OFF; no own persistent instrument/server/test child remains. Live-only
questions stay open. Menu TWO attempts/TEN minutes spent and extra6min350ms UNAPPROVED
persist across sessions/tasks/epochs; no retry/unchanged approval ask. Shared publication
uses hold_set/overlap, fresh preimages, brief supported claims; no reset/clean/reap/steal
or old-operation replay. Inputs/results immutable; successful producer controls and sent
review requests are not independent acceptance or full database completion.

---

'''
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text))
(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text))
(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: verify real private writer stale-revision arbitration\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish bounded original board writer evidence','scope':'Explicit frozen own evidence and refreshed ASTRA header; supported board writes only','completion':'Logged actual commit/allmemberSHA/body/epoch verified, reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_BOARD_WRITER',len(members),b['revision'])
