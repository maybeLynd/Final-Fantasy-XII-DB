"""Check actual pre-copy producer path, not only its documented helper."""
import hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];D=W/'run-01';assert not D.exists();D.mkdir()
producer=ROOT/'Database/Tools/work/ASTRA/migration-my-progress-independent/freeze.py'
E=ROOT/'Database/FFXII TZA/_experiments/evidence/migration-my-progress-independent'
def sha(b):return hashlib.sha256(b).hexdigest()
def pins():return {f.relative_to(E).as_posix():sha(f.read_bytes()) for f in E.rglob('*') if f.is_file()}
before=pins();manifest=json.loads((E/'manifest.json').read_text());members={m['path']:m for m in manifest['members']}
fixture=[m for m in manifest['members'] if '/fixture-db/' in m['path']];assert len(fixture)==10
for m in fixture:
 b=(E/m['path']).read_bytes();assert sha(b)==m['sha256'] and len(b)==m['bytes']
clean=D/'clean';clean.mkdir();(clean/'safe-receipt.txt').write_text('A labelled inert source, not an empty run.\n')
decls=[('actual-default',[str(producer)],1,'NESTED_FIXTURE_DATABASE_NEEDS_INERT_CAPSULE'),
 ('same-source-preflight',[str(producer),'--preflight-only'],1,'NESTED_FIXTURE_DATABASE_NEEDS_INERT_CAPSULE'),
 ('clean-source',[str(producer),'--preflight-only','--preflight-source',str(clean)],0,'FIXTURE_PLACEMENT_PREFLIGHT_ONLY_NO_WRITES'),
 ('missing-source',[str(producer),'--preflight-only','--preflight-source',str(D/'absent')],1,'Missing preparation source')]
raw={'method':'A actual owned freezer invocation and original current question reader on private labelled root',
     'driver_sha256':sha(Path(__file__).read_bytes()),'producer_path':str(producer),'producer_sha256':sha(producer.read_bytes()),
     'original_publication':'037557884af3ed9b687b6bb8b2a34855c0703cdd','fixture_members':fixture,'cases':[],'finished':False}
try:
 for n,args,rc,marker in decls:
  cmd=[sys.executable,'-B',*args];q=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
  assert q.returncode==rc and marker in q.stdout+q.stderr
  c={'name':n,'args':cmd,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'expected_marker':marker,'terminal':True}
  (D/(n+'-receipt.json')).write_text(json.dumps(c,indent=2)+'\n');raw['cases'].append(c)
 # Current OPUS reader's actual walk excludes the nested database but retains a
 # real-root control. The copy stays in private work/, never the canonical DB.
 root=D/'reader-root';(root/'04-Actor-Entity').mkdir(parents=True)
 (root/'04-Actor-Entity/control.md').write_text('- [ ] **W-999.** labelled retained-root control\n')
 shutil.copytree(E/'collection-01/fixture-db',root/'archived-fixture')
 reader=ROOT/'Database/Tools/analysis-kit/gfz-scripts/check_questions.py'
 data=reader.read_bytes();(D/'reader-source.py').write_bytes(data)
 spec=importlib.util.spec_from_file_location('current_original_question_reader',reader)
 Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q)
 boxes=Q.read_boxes(str(root))
 assert len(boxes)==1 and boxes[0]['file']=='04-Actor-Entity/control.md',boxes
 raw['reader']={'source_path':str(reader),'sha256':sha(data),'result':boxes,'private_root':str(root),
                'claim':'one original nested-reader path; not sixty scanners or whole gate'}
 assert before==pins(),'Published byte mutation'
 raw['published_members_unchanged']=True;raw['finished']=True
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
(W/'freeze-after.py').write_bytes(producer.read_bytes())
print('FIXTURE_PRODUCER_GUARD_CONTROLS',len(raw['cases']),'ORIGINAL_READER_ONE_RETAINED',raw['published_members_unchanged'])
