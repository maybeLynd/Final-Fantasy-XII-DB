"""Additive complete-copy twin for the returned field displacement defect.

Run only this affected control; do not repeat the pointer/member campaign.
"""
import hashlib, importlib.util, json, pathlib, shutil, sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py')
M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
out=W/'field-source-complete-twin-control-01';out.mkdir()
original=M.ROOT/'Database/FFXII TZA/_experiments/evidence/phyretext-softedges-field-extent/softedges-resource-source-01'
source=out/'source';shutil.copytree(original,source)
positive=out/'positive.json'
M.checked_run([sys.executable,str(W/'reduce-softedges-field-extent.py'),str(source),str(positive)],timeout=45,receipt_prefix=out/'positive-cli')
v=json.loads(positive.read_text())
if v.get('producer_complete') is not True or len(v['source_qualification'])!=4:raise ValueError('complete twin failed')
before=[];hits=0
for p in source.glob('*.json'):
    raw=json.loads(p.read_text())
    if 'ranges' not in raw:continue
    changed=False
    for q in raw['ranges']:
        for i in q['instructions']:
            if i['pc']=='0x1ea5c1':
                before.append(i.copy());b=bytes.fromhex(i['bytes']);i['bytes']=(b[:-4]+(0x9c8).to_bytes(4,'little')).hex();hits+=1;changed=True
        if changed:q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
    if changed:p.write_text(json.dumps(raw,indent=2),encoding='utf8')
if hits!=1:raise ValueError('exact mutation missing/ambiguous')
target=out/'must-not-exist.json';error=None
try:M.checked_run([sys.executable,str(W/'reduce-softedges-field-extent.py'),str(source),str(target)],timeout=45,receipt_prefix=out/'mutated-cli')
except RuntimeError as e:error=str(e)
if error is None or target.exists() or 'annotation disagrees' not in error:raise ValueError('intended changed-byte prerequisite did not refuse')
with (out/'result.json').open('x') as f:json.dump(dict(status='PASS_COMPLETE_SOURCE_TWIN_INDEPENDENT_PENDING',positive_exit=0,mutated_exit=1,mutated_result_exists=False,
    original_instruction=before[0],driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    reducer_sha256=hashlib.sha256((W/'reduce-softedges-field-extent.py').read_bytes()).hexdigest(),
    limits='One complete same-copy positive/changed-byte refusal; qualifies earlier partial gate fixture, no independent audit/native/live count.'),f,indent=2)
print('Complete field copy passes; same copy with only reviewed displacement bytes changed refuses')
