import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/heading-passthrough-alias-boundary')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==5 and [r['case'] for r in rs]==['positive','pointer-staging','same-buffer','caller-forces-alias','first-pdata-leaf']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['status']=='SOURCE_ESTABLISHES_ALIAS_AND_REFUTES_LEAF_PROOF'
 missing=json.loads((root/'missing-extent-prerequisite-control.json').read_bytes())
 assert missing['terminal'] is True and missing['returncode']!=0 and 'intervening-body.json' in missing['stderr'] and missing['checker_sha256']==sha(root/'check.py')
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not independent acceptance. Original movement order/caller/full963B extent and unwind fragments only; no original execution or whole callclosure/class stability/live effects.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-heading-alias';task='ASTRA-PUBLISH-HEADING-ALIAS-EXTENT'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/heading-passthrough-alias-boundary')
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
header='## SOL in ASTRA — ACTIVE; heading alias and false40B-leaf proof\n\nFull L1+L2 remains NOT_MET; goal ACTIVE until governing completion, independent\nreviews and final protocol. Source evidence/commit/request/green checks are not\nwhole acceptance. Fresh supported board/CURRENT/actual publications govern.\n\nASTRA-HEADING-PASSTHROUGH-ALIAS-BOUNDARY, Method A: original601B delta clears12\noutputbytes before reading inputXYZ; MOVR14,R9 savespointer notcontents. Exact\nsame-buffer prefixreads0, distincthypothetical3/4/12 preserved: conditionalbyte\ncalculations, not executed cases or finalimportedmath/F8 outcomes. Caller uses\nlocaloutputrsp+30 and R9=R14 / modeR8D=EBP, registers initializedfromentryR8/EDX;\nfull intervening preservation/livepointers notproved. Generaloverlap unknown.\n\nRequired caller investigation refuted CONTRACT§14/15 40Bleaf/no-calls basis:\ncurrent PRIMARY CATALOG ALREADY963B correct. Original8 contiguous/chained unwind\nfragments sum963; first40B onlyprologue/noRET, fullsource21calls/RET2E49A2.\nNo index regression, no observed classmutation/refusal or whole callclosure proof.\nInitial40B/no-nonvolatile-write probe FAILED before rawsave, INVALID; driver/status\npreserved. Correctedsource capture rawbeforeacceptance +originalmetadata. Old\nalias/check/result/status preserved; caller-forwarding inference narrowed.\nFinalchecker requiresactualfullbody/prerequisites; four wronginterpretations and\nmissingrequiredextent refuse. ExistingOPUS H0-H7 source read, not rerun/credited.\nNew independentSPEC review and FABLE/OPUS canonicalconsumer/proof repair required.\n\nOn resume: check task/publication states and actual verification/commit receipts\nbefore choosing any action. If DONE, do not recapture or repeat claim/delivery.\nIf a reservation is ACTIVE, inspect owned process/receipt and finish only required\nremaining phase. Then consume actual returned repairs/reviews or select another\neligible named discriminator under fresh ownership. Consumer/review waits do not\npause goal. Correct existing producer/procedure for full-function prerequisites,\nnot only result wording; leave class-stability/refusal closure open until owner\nsupplies adequate proof. Do not duplicate accepted OPUS307 worlds/F8 corrections.\n\nPrior ff62e59d5 typed-pop tag/reporting evidence delivered39855: DATA onlynewtag/\nreportscope andSPEC review, separate OPUS DATA store-notrelease request preserved.\nc7bd09b49 helperbinding/c7f2f592f actualwriter/0d9d9330c overlap delivered; owner\nincorporation/independentreview pending per liveboard. FABLE68d835b52 PoisonQ6\nincorporated with boundedlimits. Do not resend legacy READY superseded requests.\n\nPC/browser/game controls OFF; no own persistentinstrument/server/testchild. Menu\nTWOattempts/TENminutes spent /extra6min350ms UNAPPROVED persist, noretry/unchanged\npermissionask. Supportedboard/preimages/briefpublication; no reset/clean/reap/steal/\noldops replay/bootstrap/reconstruction. Live-only gaps stayopen; explicitstop/\ntakeover halts automation. Checkpoints and sessionlimits are not database success.\n\nPlayer version: reusing one movementvector as input/output losesXYZ before reads.\nAn old never-happens proof treated a prologue as a full steering routine. Neither\nestablishes a fault in normal gameplay; database correction/acceptance continues.\n\n---\n\n'
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: expose movement alias and incomplete steering leaf proof\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish heading alias and steering extent proof evidence','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_HEADING_ALIAS_EXTENT',len(members),b['revision'])
