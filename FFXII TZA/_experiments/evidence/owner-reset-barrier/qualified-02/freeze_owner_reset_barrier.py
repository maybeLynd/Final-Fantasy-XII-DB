"""Explicit immutable source/control receipts; no board or peer mutations."""
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for prefix,driver in [('owner-reset-barrier-capture-01','capture-owner-reset-barrier.py'),
                          ('owner-reset-barrier-positive-04','prove_owner_reset_barrier.py'),
                          ('owner-reset-barrier-controls-run-01','control_owner_reset_barrier.py')]:
        s=json.loads((HERE/(prefix+'.status.json')).read_text())
        if s['exit']!=0 or s['driver_sha256']!=sha(HERE/driver):raise ValueError('upstream failed/stale')
        if not(HERE/(prefix+'.stdout')).read_bytes().strip() or (HERE/(prefix+'.stderr')).read_bytes():raise ValueError('upstream output missing/error')
    result=json.loads((HERE/'owner-reset-barrier-result-04.json').read_text())
    controls=json.loads((HERE/'owner-reset-barrier-controls-01/result.json').read_text())
    if result['driver_sha256']!=sha(HERE/'prove_owner_reset_barrier.py') or len(result['fst_dependency']['members'])!=12:raise ValueError('scientific result incomplete')
    if controls['status']!='PASS_ACTUAL_OWNER_RESET_PREREQUISITE_REFUSALS' or len(controls['cases'])!=4 or not all(x['passed'] for x in controls['cases']):raise ValueError('actual controls incomplete')
    files=['capture-owner-reset-barrier.py','prove_owner_reset_barrier.py','control_owner_reset_barrier.py',
           'freeze_owner_reset_barrier.py','validate-title-source-annotations.py','OWNER-RESET-METHOD-1001.md']
    files += [p.relative_to(HERE).as_posix() for p in HERE.glob('prove_owner_reset_barrier-before-*.py')]
    files += [p.relative_to(HERE).as_posix() for p in HERE.glob('owner-reset-barrier-*') if p.is_file()]
    files += [p.relative_to(HERE).as_posix() for p in (HERE/'owner-reset-barrier-controls-01').rglob('*') if p.is_file()]
    # The first publication refused three derived interpreter caches. Preserve
    # the original frozen candidate; fix the actual producer's selection path.
    def transient(name):return '__pycache__' in Path(name).parts or Path(name).suffix in ['.pyc','.pyo']
    discarded=sorted(name for name in files if transient(name))
    if len(discarded)!=3:raise ValueError('known cache boundary changed; review actual selection')
    old=HERE/'owner-reset-barrier-frozen-ready'
    original=json.loads((old/'manifest.json').read_text())
    if sha(old/'manifest.json')!='82077c82933d31278d0bf5fa066ff0401ff3f32f5ffb6f47376edc45a332575b':raise ValueError('original frozen manifest changed')
    if any(sha(old/m['path'])!=m['sha256'] for m in original['members']):raise ValueError('original frozen member changed')
    files=[name for name in files if not transient(name)]
    files.append('freeze_owner_reset_barrier-before-cache-selection-01.py')
    out=HERE/'owner-reset-barrier-frozen-ready-02'
    if out.exists():raise ValueError('immutable packet exists')
    out.mkdir()
    for file in sorted(set(files)):
        dst=out/file;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/file,dst)
    shutil.copy2(HERE/'OWNER-RESET-README-1001.md',out/'README.md')
    with (out/'README.md').open('a') as f:
        f.write('\n## Delivery qualification02\n\nThe initial uncommitted publication failed on three generated .pyc caches.\nThe actual freezer now excludes only interpreter-cache artifacts; original\n70-member frozen candidate and failed publication receipts remain unchanged.\nAll primary bytes/results/controls are retained; no scientific rerun or new\nacceptance. This qualified02 packet is the committed delivery.\n')
    qualification=dict(original_manifest_sha256=sha(old/'manifest.json'),
                       original_members_verified=len(original['members']),
                       excluded_derived_caches=[dict(path=n,sha256=sha(HERE/n)) for n in discarded],
                       source_preimage_sha256=sha(HERE/'freeze_owner_reset_barrier-before-cache-selection-01.py'),
                       current_producer_sha256=sha(Path(__file__)),
                       conclusion='Only interpreter-cache packaging changed; primary scientific evidence unchanged')
    (out/'DELIVERY-QUALIFICATION-02.json').write_text(json.dumps(qualification,indent=2)+'\n')
    failed=HERE/'publication-owner-reset-barrier-01'
    for source,dest in [('automated-publication-attempt-01.json','FAILED-PUBLICATION-01.json'),
                        ('automated-publisher-stderr-01.txt','FAILED-PUBLICATION-01.stderr'),
                        ('automated-publisher-stdout-01.txt','FAILED-PUBLICATION-01.stdout')]:
        shutil.copy2(failed/source,out/dest)
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='conditional original owner-reset barrier',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))


if __name__=='__main__':main()
