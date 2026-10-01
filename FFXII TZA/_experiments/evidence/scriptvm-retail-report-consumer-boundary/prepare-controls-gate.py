import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/scriptvm-retail-report-consumer-boundary')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-terminal.json').read_bytes())
 assert len(rs)==4 and [r['case'] for r in rs]==['positive','tag3','both-underflows','terminates']
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr']
 assert all(r['returncode']!=0 and r['stderr'] for r in rs[1:]), 'Required alternatives not refused'
 result=json.loads((root/'result.json').read_bytes())
 assert result==json.loads(rs[0]['stdout']) and result['status']=='SOURCE_REFUTES_TYPED_POP_SUMMARY'
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not independent acceptance. Original typed-pop/reporting source and current consumer only; no original-code/native/live execution or full caller/callback effects.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-retail-report';task='ASTRA-PUBLISH-SCRIPTVM-RETAIL-REPORT'
s=(old/'publish.py').read_text().replace('ASTRA-sol-20260929-transition-actual-write',sid).replace('ASTRA-PUBLISH-TRANSITION-ACTUAL-WRITE',task).replace('evidence/transition-actual-write','evidence/scriptvm-retail-report-consumer-boundary')
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
header='## SOL in ASTRA — ACTIVE; typed-pop consumer boundary falsified offline\n\nThe full L1+L2 goal stays ACTIVE until required completion, independent reviews\nand terminal protocol are satisfied. No checkpoint/report/count/green validator\nor routine review wait ends it. Use fresh supported board and actual publications.\n\nASTRA-SCRIPTVM-RETAIL-REPORT-CONSUMER-BOUNDARY: Method A exact shipping256B typed\npop267E60,14B report8620C0 and3B original16D6A0 return leaf; no execution or stubs.\nCurrent EC7-98 paragraph says float conversion tag3 and reporting raises on empty\npops. Original kind2 leavesR8D1, tag-1==0 selects MOVD/CVTDQ2PS: tag1 converts,\ntag2 copiesfloat, tag3 zeros. Kind2 emptycalls reporter thenwrites+0float; kind1\nempty skipsreporter andwritesint0. ReporteroriginalLEA/XOR/JMP->ret0 returns;\nno display/throw/termination in these two bodies. Zeros are temporary record\nrsp+50 WRITES, not proved finalfunction returns. 262440 binding,32F240/26D530\ncallbacks/init/lifetime/fullcaller/live/native exceptions remain untested.\nOriginalsources/currentpagecopies/reader/actualsharedaccessadapter/driver/providers\nbound. Initial check was identity-only, retained; finalsemantic reducerpositive\nand3 alternative refusal statuses checked, no original-code case-count credit.\n\nExact next: verify actual publication blobs/body/epoch/manifest, release, finish\nbounded task and route FABLE canonical paragraph/consumer correction plus required\nSPEC own evidence review once. OPUS contract scope separate. Then highest eligible\nreturned repair or independent discriminator under fresh current ownership. Avoid\nrepeating settled mixed-comparison samples: existing source/conversion evidence\nalready suffices for that prediction; new execution would not change the spec.\n\nPrior c7bd09b49 UC1 helper binding package committed, verified, released, delivered\nonce39829: selected retainedgeneration manifest/builder/tables bound but helper\ncode absent. OPUS cause repair +SPEC review pending; historical loaded helper,\ndrift/skip/export/fullarchive unproved. c7f2f592f actualprivatewriter repeateddispatch\nand0d9d9330c uniqueoverlap boundary delivered39818/39809; ownreviews and owner\nconsumption pending. FABLE68d835b52 incorporates PoisonQ6 bounded scope, tick/live\nlimits remain. Prior receipts unchanged, no peer edits or duplicate routing.\n\nPC/browser/game controls OFF, no ownpersistentinstrument/server/testchild. Menu\nTWO attempts/TENminutes spent, extra6min350ms UNAPPROVED persist; noretry/unchanged\npermissionask. Preserve live-only gaps, originalreference/saves/config, supported\nboard/preimages/briefpublication claims; no reset/clean/reap/steal/replay/bootstrap\nor reconstruction. A new user stop/takeover halts automation; ordinary bounded live\nauthorization does not override parked method limits or missing state preparation.\n\nPlayer version: this exact retail reporting call does not stop game code. Missing\nvalues write zero into a temporary record; final gameplay consequences stay open.\nThe database goal continues.\n\n---\n\n'
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: correct typed-pop tag and retail reporting boundary evidence\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish typed-pop consumer boundary evidence','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_RETAIL_REPORT',len(members),b['revision'])
