"""Typed code/data publication map; retain the original scientific packet."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    original=W/'filecache-key-preprocessing-frozen-ready'
    out=W/'filecache-key-preprocessing-frozen-ready-02'
    if out.exists():raise ValueError('immutable qualified packet exists')
    if sha(original/'manifest.json')!='9047a360d0e92017e32c9d9bd570d0ad70cd610f639e5960ceb6284247be6ff9':
        raise ValueError('scientific manifest changed')
    m=json.loads((original/'manifest.json').read_text())
    if len(m['members'])!=53:raise ValueError('scientific packet incomplete')
    actual={p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()}
    if actual!={x['path'] for x in m['members']}|{'manifest.json'}:
        raise ValueError('scientific population changed')
    for x in m['members']:
        if sha(original/x['path'])!=x['sha256']:raise ValueError('scientific preimage changed')
    r=json.loads((original/'filecache-key-preprocessing-result-02.json').read_text())
    if r.get('producer_complete') is not True:raise ValueError('scientific result incomplete')
    for name,pin in r['source_pins'].items():
        if sha(original/name)!=pin:raise ValueError('scientific dependency moved')
    validator=W/'validate-title-source-annotations.py'
    if sha(validator)!='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13':
        raise ValueError('reviewed byte validator changed')
    spec=importlib.util.spec_from_file_location('existing_key_publication_adapter',validator)
    V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    code=['filecache-key-boundaries-source-01.json','filecache-key-boundaries-source-02.json',
          'filecache-hash-loop-source-01.json']
    receipts=[{'path':n,'agreement':V.validate(json.loads((original/n).read_text()))} for n in code]
    data='filecache-import-declarations-01.json'
    d=json.loads((original/data).read_text())
    if d.get('complete') is not True or {x['iat_va']:x['name'] for x in d['imports']}!={'0x8c2ff0':'toupper','0x8c2ff8':'strncmp'}:
        raise ValueError('import-data prerequisite incomplete')
    out.mkdir()
    for x in m['members']:
        dst=out/x['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original/x['path'],dst)
    shutil.copy2(original/'manifest.json',out/'original-frozen-manifest-01.json')
    shutil.copy2(Path(__file__),out/Path(__file__).name)
    mapping={'producer_complete':True,'source_pins':[{'path':n,'sha256':sha(original/n)} for n in code],
             'data_pins':[{'path':data,'sha256':sha(original/data),'role':'static import declarations, not instruction ranges'}],
             'scientific_result_sha256':sha(original/'filecache-key-preprocessing-result-02.json'),
             'driver_sha256':sha(Path(__file__)),'annotation_receipts':receipts,
             'status':'PUBLICATION_MAP_ONLY_INDEPENDENT_PENDING',
             'limits':'Original53 members unchanged. Import declarations are typed data, not sent as fake code ranges. No scientific rerun, guard change, whole E2 or live/native acceptance.'}
    (out/'filecache-key-publication-map-01.json').write_text(json.dumps(mapping,indent=2)+'\n')
    members=[{'path':p.relative_to(out).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps({'kind':'qualified original cache-key preprocessing','members':members},indent=2)+'\n')
    print(json.dumps({'members':len(members),'unchanged_scientific_members':53,'manifest_sha256':sha(out/'manifest.json')}))


if __name__=='__main__':main()
