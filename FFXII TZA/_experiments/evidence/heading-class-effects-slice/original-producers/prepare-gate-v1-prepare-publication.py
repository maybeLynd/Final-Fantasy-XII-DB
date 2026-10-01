import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/heading-class-effects-slice')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def controls_preflight(root):
 root=Path(root);rs=json.loads((root/'checks-effects-terminal.json').read_bytes())
 names=['positive','upstream-failed','missing-latest','empty-capture','drop-conditional','tail-as-call','fictional-closure','lea-read','store-read']
 assert len(rs)==len(names) and [r['case'] for r in rs]==names
 assert all(r['terminal'] is True and r['checker_sha256']==sha(root/'check-effects.py') for r in rs)
 assert rs[0]['returncode']==0 and not rs[0]['stderr'] and all(r['returncode']!=0 and r['stderr'] for r in rs[1:])
 result=json.loads((root/'result.json').read_bytes());assert result==json.loads(rs[0]['stdout']) and result['status']=='STATIC_EFFECT_BOUNDARIES_VALID_NOT_CLASS_CLOSURE' and result['class_stability']=='OPEN'
 # Execute the actual read-only checker; recorded PASS cannot suppress a failing prerequisite.
 q=subprocess.run([sys.executable,'-B',str(root/'check-effects.py')],capture_output=True,text=True)
 assert q.returncode==0 and not q.stderr and json.loads(q.stdout)==result, (q.returncode,q.stderr)
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
(P/'manifest.json').write_bytes((json.dumps({'schema':1,'members':members,'limits':'Integrity is not semantic/independent acceptance. MethodA/STATIC_ONLY retained source and validated producer correction; class stability/lifetime/normal live reachability OPEN. Four native dispatch tails unexamined. No new native/game execution, L3, migration or full L1L2 completion award.'},indent=2)+'\n').encode())
p=W/'publication';assert not p.exists();p.mkdir();old=W.parent/'transition-actual-write/publication'
for n in ('verify.py','manifest_closure.py'):shutil.copyfile(old/n,p/n)
sid='ASTRA-sol-20260929-heading-class-effects';task='ASTRA-PUBLISH-HEADING-CLASS-EFFECTS'
s=(W.parent/'heading-status-repair-review/publication/publish.py').read_text().replace('ASTRA-sol-20260929-heading-status-repair',sid).replace('ASTRA-PUBLISH-HEADING-STATUS-REPAIR',task).replace('evidence/heading-status-repair-review','evidence/heading-class-effects-slice')
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
header=(W/'handoff-header.txt').read_text()
(p/'reviewed-inbox-preimage.txt').write_text(normalized(text));(p/'reviewed-inbox-next.txt').write_text(header+text)
(p/'reviewed-inbox-body.txt').write_text(normalized(header+text));(p/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(p/'message.txt').write_text('ASTRA: retain movement native effect boundaries and conditional-tail producer correction\n')
assert not any(t['id']==task for t in b['tasks'])
b=team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{'id':task,'kind':'research','priority':'P1','target':'Publish bounded movement native effect source slice','scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only','completion':'Actual committed blobs/body/epoch/manifest verified; reservation released','dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_HEADING_CLASS_EFFECTS',len(members),b['revision'])
