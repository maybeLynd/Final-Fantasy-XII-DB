"""Verify concrete prerequisite refusal, then freeze the ownership discriminator."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
F=W/'uq147-relation-reset-effects-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
need(not F.exists(),'existing freeze: reconcile, do not overwrite')
driver=P/'prove-relation-reset-effects.py';dh=sha(driver)
positive=json.loads((P/'prove-relation-reset-effects-01.status.json').read_text());result=json.loads((P/'result-relation-reset-effects-01.json').read_text())
need(positive.get('terminal') is True and positive.get('exit')==0 and positive.get('exception') is None and positive['driver_sha256']==dh==result['driver_sha256'] and result.get('producer_complete') is True,'actual current positive required')
stem='prove-relation-reset-refusal-01';failed=P/'reviewed-boundaries-failed-prerequisite-01.json';st=json.loads((P/(stem+'.status.json')).read_text())
need(json.loads(failed.read_text())==dict(terminal=True,exit=1,exception=None,label='Synthetic failed qualification receipt'),'labelled failed receipt changed')
need(st.get('terminal') is True and st.get('exit')==1 and st.get('exception') is None and st.get('driver_sha256')==dh and st['argv'][2:]==[str(driver),'result-relation-reset-refused-01.json',failed.name],'actual specific current CLI refusal required')
need(b'successful upstream qualification required' in (P/(stem+'.stderr')).read_bytes() and not (P/'result-relation-reset-refused-01.json').exists(),'required upstream rejection/output absence failed')
selected=['RELATION-RESET-NEXT-QUESTION.md','capture-relation-reset-leaves.py','source-relation-reset-leaves-01.json','prove-relation-reset-effects.py',
 'result-relation-reset-effects-01.json','reviewed-boundaries-failed-prerequisite-01.json','source-relation-remove-leaf-01.json']
for tag in ['capture-relation-reset-leaves-01','prove-relation-reset-effects-01','prove-relation-reset-refusal-01']:
    selected += [tag+s for s in ['.status.json','.stdout','.stderr']]
need(all((P/n).is_file() for n in selected),'curated input missing')
F.mkdir();(F/'.gitattributes').write_bytes(b'* -text\n')
for n in selected:shutil.copyfile(P/n,F/n)
shutil.copyfile(P/'RELATION-RESET-RESULT.md',F/'README.md')
(F/'actual-prerequisite-control.json').write_text(json.dumps(dict(status='VERIFIED',tested_producer_sha256=dh,positive_status_sha256=sha(P/'prove-relation-reset-effects-01.status.json'),positive_result_sha256=sha(P/'result-relation-reset-effects-01.json'),failure_status_sha256=sha(P/(stem+'.status.json')),failed_input_sha256=sha(failed),actual_child_exit=1,exception=None,required_marker=True,result_absent=True,limits='Synthetic prerequisite, actual producer invocation/status. Not independent review/native/game evidence.'),indent=2)+'\n')
deps={'validate-title-source-annotations.py':W/'validate-title-source-annotations.py','capture-index-path.py':W/'ov42-gauge-callback-binding/capture-index-path.py','run.py':W/'sd194-copier-limit/run.py'}
(F/'dependencies').mkdir()
for n,p in deps.items():shutil.copyfile(p,F/'dependencies'/n)
(F/'dependencies/identities.json').write_text(json.dumps([dict(file=n,original_path=str(p),sha256=sha(p)) for n,p in deps.items()],indent=2)+'\n')
shutil.copyfile(Path(__file__),F/'freeze-relation-reset-1003.py')
members=[dict(path=p.relative_to(F).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps(dict(members=members,limits='Integrity/current producer controls only; independent scientific acceptance/canonical consumption pending.'),indent=2)+'\n')
print(json.dumps(dict(frozen=F.name,members=len(members),manifest_sha256=sha(F/'manifest.json'))),flush=True)
