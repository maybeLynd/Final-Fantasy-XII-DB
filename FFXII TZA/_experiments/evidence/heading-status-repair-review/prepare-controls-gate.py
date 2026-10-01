import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/heading-status-repair-review')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==5 and [r['case'] for r in rs]==['positive','upstream-failed','zero-negative','missing-negative','count-ungated']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['verdict']=='ACCEPT scoped2366027d9 H8 CLI/gated-count repair'
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not whole acceptance. Scoped2366027d9 H8 CLI/gated-count repair with actual producer Python and retained labelled input; no47-script dynamic campaign/native/live/class/fullmigration/L1L2 award.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-heading-status-repair';task='ASTRA-PUBLISH-HEADING-STATUS-REPAIR'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/heading-status-repair-review')
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
header="## SOL in ASTRA — ACTIVE; status repair verified, native class-effects slice ongoing\n\nFull L1+L2 goal remains ACTIVE/NOT_MET; governing final and independent acceptance\nrequirements unchanged. Epoch3 board/current ownership checked. No L3 primary\nreconstruction, parked menu setup budget/UNAPPROVED extension unchanged.\n\nOPUS2366027d9 repairs returnedfeb631dd4 H8 CLI/status/procedure gap. Scoped independent\nreview ACCEPT: actual original valid catalogue SURVIVES H8/extentTrue/calls21/FAILS0/\nexit0; same labelled published963->40 reader input BROKEN H8/extentFalse/callsNone/\noperandsNone/FAILS1/exit1. SourceAST binds extent_ok-before-conditional-count and\nSystemExit1-if-fails. Two real producer Python processes, no native/game execution;\nnot a47-script campaign or H0H7/class semantics acceptance. Old negativeexit0 evidence\nimmutable, not retroactively changed. Exact raw current/commit source, declared\npublished inputs/provider/tool hashes and result/status controls retained. OPUS\ncanonical consumption and SPEC own checker/gate review are separate phases.\n\nMain ASTRA-HEADING-CLASS-EFFECTS-SLICE remains ACTIVE with existing claimed work and\nevidence paths. Resume from checked board and Database/Tools/work/ASTRA/heading-class-\neffects-slice/CHECKPOINT.md plus subsequent raw-nested.json/raw-closure-r3.json and\nterminal statuses. All initial15direct targets (preliminary14 corrected) are captured\nread-only with full rooted-unwind extent checks; leaf/thunk extents separately\nqualified. Actual2E4969 suppliesEDX0 to26C120, not modes2/3/4. Its mode0 can call\n2EBE50 and2E8EE0, then2E6300. 2EBE50(0) also runs2EC3F0 and2E8EE0; do not assume\nsimple local clear or ignore repeated native effects. 2E6300 has conditionalJS into\nreadonly getter265510. 2E8EE0 reaches two object-state wrappers at3E6BC0/BD0; those\nadjust RCX+580 and tail-jump3E33E0/3440. 2EC3F0 can tail-dispatch six staged look\nhelpers depending on context flags. 2E5DF0 delegates2E5C90, which reaches position/\ncollision helpers and2E6000; native effects and initialized aliases not yet proved.\nClass stability/refusal remains OPEN. FABLE's existing facing/turning/page evidence\nmust be consumed, not duplicated or used as uncited universal no-write proof.\n\nCurrent local class-source receipts are UNPUBLISHED/Toolswork ignored and disclosed;\nnot independent acceptance. Next inspect validated relevant native/tail effects and\nsource-derived argument/alias conditions, using existing primary/canonical findings\nfirst. Do not recapture initialcases/duplicate settledScriptVM arithmetic or perform\nnew menu attempts. Finish current publication/delivery once based on actual receipts;\nDONE means no replay/resend. Prior dashboardd591eb30a and overlap1548d3896 already\npublished/delivered; OPUSf3f933297 consumes overlap review. Reviews remain currentboard.\n\nAll owned producer/test subprocesses terminal; controlsOFF, no owned server/instrument/\npersistent process. Peer server untouched, reference/catalogue/saves/config unchanged.\nExplicit stop/takeover halts automation without automatic resumption. No reset/clean/\nreap/steal/guard bypass/bootstrap/worktree or historical operation replay.\n\nPlayer version: the reliability check now fails correctly. I am tracing the actual\nsteering reset and its object/head-look update hooks; movement behavior is not yet\nproved. Controls stay off and the full database goal continues.\n\n---\n\n"
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: independently accept heading producer status and count-gating repair\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish independent heading status repair review','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_HEADING_STATUS_REPAIR',len(members),b['revision'])
