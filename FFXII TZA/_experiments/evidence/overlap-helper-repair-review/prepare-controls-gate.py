import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/overlap-helper-repair-review')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==5 and [r['case'] for r in rs]==['positive','upstream-failed','additional-as-unique','v1-comparable','unbound-helper-valid']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['verdict']=='ACCEPT scoped overlap/helper repair'
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not whole acceptance. Original repository-Python overlap/helper repair review with disposable extent/generation fixtures and only executable adapter enabled; no game/native/live/fullbuild/deployment or L1L2.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-overlap-helper-review';task='ASTRA-PUBLISH-OVERLAP-HELPER-REVIEW'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/overlap-helper-repair-review')
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
header='## SOL in ASTRA — ACTIVE; overlap/helper repair reviewed, movement delivered\n\nThe full L1+L2 goal remains ACTIVE and NOT_MET until governing completion,\nindependent reviews and final protocol. A checkpoint or scoped acceptance is not\ncompletion. Use supported board/CURRENT and actual publications on every resume.\n\nMovement evidence 2ada8a5a0315fe271c1003fcb579b5bffa7c49ba was committed, all35\nmembers verified and publication released; producer task DONE and FABLE canonical\nalias/false-leaf-basis repair, OPUS existing check/procedure full-extent prerequisite\nand SPEC independent evidence review delivered ONCE at39901. Entry outputXYZ clear\nprecedes input reads. Exactsamebuffer firstreads zeros conditionally, not executed\ncode/gameplay. Original steering full963B with21calls/eight chained unwind ranges;\n40B is prologue, currentcatalog alreadycorrect. Actualclassstability/refusal and\nwhole call effects/imported math/live alias stay OPEN; initial failed40B probe and\nnarrowed caller inference retained. Do not recapture or duplicate accepted307.\n\nCurrent OPUS-REQ-ASTRA-VERIFY-OVERLAP-AND-HELPER-BINDING: independent scoped review\nof cdbf25a5d. Actual population_cover/text_intervals/v_executable and original\n_build/Store with only executable adapter enabled. Disjoint/double/triple/clipping/\norder controls; four adapter fixtures (three retained real extents33unique34extra).\nNo renewed wholepopulation census. Triple8unique12extra. Original v1->v2 build:\nN/A definitionchanged, bothsides retained; unchangedv2 gives0pp. Actual declared\nhelper module path/snapshot hash bound. Same-size disposablehelper edit during\nadapter and missinghelper beforebegin refuse, CURRENT/successhistory unchanged.\nNo execution of modifiedhelper or anyFF12 instructions. All original sources and\nexternal certifiedEXE unchanged. Producer B1-B10 not ours. Thirdparty/import-before-\nbegin/deployedmodule/allviews/fullA05A23M3/migration/L1L2 remain outside scope.\n\nRun01 failed raw equality BEFORE import/tests: checked-out helper CRLF vs GitLF.\nOriginal driver/terminal/partialsources/failure retained. Additive diagnostic pins\nboth byteversions; corrected Python-only newline comparison rejects semantic\nimport-os-to-io change. Actual loaded bytes bound, no binary normalization. Final\nchecker requires real successful capture and four rejected alternatives, actual\npreparer/publisher gates require those bound receipts. SPEC own checker/gate review\nseparate from ASTRA independent review of OPUS repair and canonical consumption.\n\nOn resume inspect checked task/publication/commit/verification receipts first.\nIf ACTIVE finish only remaining phase; if DONE do not recapture/re-deliver.\nThen consume returned reviews/owner repairs or take the next eligible named\nimplementation discriminator under fresh ownership. Do not select stale reports.\nPrior53a3b6a14 consumes earlier onebasis/navigation/actualwriter within limits;\nOPUS repair cdbf25a5d and present review do not certify allmigration requirements.\nDATA typed-pop canonical incorporation/SPEC own reviews remain currentboard work.\n\nPC/browser/game controls OFF; no ownedpersistent instrument/server/testchild.\nMenu TWOattempts/TENminutes spent, extra6min350ms UNAPPROVED persist across sessions\nand epochs. No reopen/unchanged ask/bootstrap/worktree/reconstruction/reset/clean/\nreap/steal/replay. Explicit userstop/takeover halts automation. Native goal remains\nACTIVE; honest session/checkpoint state and DB_GOAL are different.\n\nPlayer version: a corrected counting rule is labelled so it cannot appear as newly\nlearned game knowledge, and the measurement now records its helper code. Movement\nproof corrections remain with their owners; normal gameplay fault is not proved.\n\n---\n\n'
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: independently verify overlap accounting and helper binding repair\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish scoped overlap/helper repair review','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_OVERLAP_HELPER_REVIEW',len(members),b['revision'])
