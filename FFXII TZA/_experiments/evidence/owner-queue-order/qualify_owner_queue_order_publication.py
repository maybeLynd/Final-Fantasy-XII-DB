"""Qualify the existing scientific packet for the standard publication map.

The first preparation refused a missing map, before any canonical writes.
Do not repeat original-code analysis or weaken that publication guard.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    original=HERE/'owner-queue-order-frozen-ready'
    out=HERE/'owner-queue-order-frozen-ready-02'
    if out.exists():raise ValueError('immutable qualified packet exists')
    if sha(original/'manifest.json')!='e1cd99c0727e019e051d57cdb3ded060ccbda6aa273c5d9ed96f71978849417f':raise ValueError('original packet changed')
    m=json.loads((original/'manifest.json').read_text())
    if len(m['members'])!=57 or {p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()}!={x['path'] for x in m['members']}|{'manifest.json'}:
        raise ValueError('original population changed')
    for x in m['members']:
        if sha(original/x['path'])!=x['sha256'] or (original/x['path']).stat().st_size!=x['bytes']:raise ValueError('original member changed')
    for prefix,driver in [('owner-queue-order-source-run-02','qualify_owner_queue_order_source.py'),
                          ('owner-queue-order-positive-01','prove_owner_queue_order.py'),
                          ('owner-queue-order-controls-run-01','control_owner_queue_order.py')]:
        s=json.loads((original/(prefix+'.status.json')).read_text())
        if s['exit']!=0 or s['driver_sha256']!=sha(original/driver):raise ValueError('required upstream failed/stale')
        if not(original/(prefix+'.stdout')).read_bytes().strip() or (original/(prefix+'.stderr')).read_bytes():raise ValueError('upstream missing/error output')
    result=json.loads((original/'owner-queue-order-result-01.json').read_text())
    controls=json.loads((original/'owner-queue-order-controls-01/result.json').read_text())
    if result['driver_sha256']!=sha(original/'prove_owner_queue_order.py') or result['source_sha256']!=sha(original/'owner-queue-order-source-02.json') or len(result['graphs'])!=6:
        raise ValueError('positive prerequisite incomplete')
    if len(controls['cases'])!=4 or not all(x['passed'] and x['result_absent'] and x['exit']!=0 for x in controls['cases']):raise ValueError('required refusals incomplete')
    # Import the already reviewed work helper, not the immutable packet: no
    # __pycache__ additions in the frozen source. Check its identity first.
    validator=HERE/'validate-title-source-annotations.py'
    if sha(validator)!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':raise ValueError('reviewed validator changed')
    spec=importlib.util.spec_from_file_location('queue_publication_roles',validator)
    roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
    annotation=roles.validate(json.loads((original/'owner-queue-order-source-02.json').read_text()))
    out.mkdir()
    for x in m['members']:
        p=out/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original/x['path'],p)
    shutil.copy2(original/'manifest.json',out/'original-frozen-manifest-01.json')
    shutil.copy2(Path(__file__),out/Path(__file__).name)
    qualification=dict(producer_complete=True,source_pins=[dict(path='owner-queue-order-source-02.json',sha256=sha(original/'owner-queue-order-source-02.json'))],
      driver_sha256=sha(Path(__file__)),annotation_receipt=annotation,original_manifest_sha256=sha(original/'manifest.json'),
      scientific_result_sha256=sha(original/'owner-queue-order-result-01.json'),
      status='CHECKED_PUBLICATION_PREREQUISITES_ONLY_INDEPENDENT_PENDING',
      original_preparation='Actual --deliver checkpoint37-owner-queue-order exited1: missing/incomplete source prerequisite map. No canonical destination/handoff/preparation directory or commit. Own publication released44952. This qualifies the existing map; no scientific rerun, guard change or old operation replay.')
    (out/'owner-queue-order-publication-qualification-01.json').write_text(json.dumps(qualification,indent=2)+'\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='conditional original queue order, publication map qualified02',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'),unchanged_scientific_members=57)))


if __name__=='__main__':main()
