"""Curate current conditional Method A evidence, preserving failed history."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
F=W/'uq147-native-relation-invariant-frozen-ready'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
need(not F.exists(),'existing immutable freeze: reconcile, do not overwrite')
for driver,tag,result in [('prove-native-relation-invariant.py','prove-native-relation-invariant-02','result-native-relation-invariant-02.json'),('check-native-relation-prerequisite.py','check-native-relation-prerequisite-01','result-native-relation-prerequisite-01.json')]:
    q=json.loads((P/(tag+'.status.json')).read_text());z=json.loads((P/result).read_text())
    need(q.get('terminal') is True and q.get('exit')==0 and q.get('exception') is None and q['driver_sha256']==sha(P/driver)==z['driver_sha256'] and z['producer_complete'] is True,'matching complete actual producer required')
selected=['capture-native-event-boundary.py','capture-relation-remove-leaf.py','qualify-ko-notify-retained.py','qualify-ko-notify-retained.v1.preimage.py',
 'prove-native-relation-invariant.py','prove-native-relation-invariant.v1.preimage.py','check-native-relation-prerequisite.py',
 'source-native-event-boundary-01.json','source-relation-remove-leaf-01.json','source-ko-notify-01.json',
 'lookup-native-event-preparation-01.json','lookup-notify-preparation-01.json','notify-physical-preparation-01.json',
 'result-native-relation-invariant-01.json','result-native-relation-invariant-02.json','result-native-relation-prerequisite-01.json',
 'reviewed-boundaries-failed-prerequisite-01.json','NATIVE-RELATION-INVARIANT-QUESTION.md','KO-NOTIFY-NEXT-QUESTION.md']
for tag in ['capture-native-event-boundary-01','capture-relation-remove-leaf-01','qualify-ko-notify-retained-01','qualify-ko-notify-retained-02',
            'prove-native-relation-invariant-01','prove-native-relation-invariant-02','prove-native-relation-refusal-01','check-native-relation-prerequisite-01']:
    selected += [tag+s for s in ['.status.json','.stdout','.stderr']]
need(len(selected)==len(set(selected)) and all((P/n).is_file() for n in selected),'curated input incomplete')
F.mkdir();(F/'.gitattributes').write_bytes(b'* -text\n')
for n in selected:shutil.copyfile(P/n,F/n)
shutil.copyfile(P/'NATIVE-RELATION-RESULT.md',F/'README.md')
dependencies={
 'validate-title-source-annotations.py':W/'validate-title-source-annotations.py',
 'capture-index-path.py':W/'ov42-gauge-callback-binding/capture-index-path.py',
 'reg_tracking.py':ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py',
 'run.py':W/'sd194-copier-limit/run.py',
 'locate-retained-span.py':W/'locate-retained-span.py'}
(F/'dependencies').mkdir()
for n,p in dependencies.items():shutil.copyfile(p,F/'dependencies'/n)
(F/'dependencies/identities.json').write_text(json.dumps(dict(dependencies=[dict(file=n,original_path=str(p.relative_to(ROOT)),sha256=sha(p)) for n,p in dependencies.items()],limits='Copies attest dependencies of actual invocation. Reproduction must resolve the original reviewed path, not silently substitute a different helper.'),indent=2)+'\n')
context=ROOT/'Database/FFXII TZA/_index/candidates/type-flow-census/README.md'
lines=context.read_text().splitlines();start=next(i for i,s in enumerate(lines) if 'embeddedBlock0650' in s)
(F/'existing-consumer-context.json').write_text(json.dumps(dict(path=str(context.relative_to(ROOT)),sha256=sha(context),first_line=start+1,lines=lines[start:start+2],limits='Prior DATA physical-access/layout credit only. No semantic recensus, exact current canonical type update, or independent acceptance is claimed.'),indent=2)+'\n')
shutil.copyfile(Path(__file__),F/'freeze-native-relation-1003.py')
members=[dict(path=p.relative_to(F).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps(dict(members=members,limits='Integrity only. Current proof/result02 and prerequisite control are producer-valid; independent review and canonical incorporation pending. Preserved failed/v1 history is not final credit.'),indent=2)+'\n')
print(json.dumps(dict(frozen=F.name,members=len(members),manifest_sha256=sha(F/'manifest.json'))),flush=True)
