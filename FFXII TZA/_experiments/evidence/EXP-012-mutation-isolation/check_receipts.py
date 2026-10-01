"""Verify this experiment's preserved inputs, generated candidates and raw comparisons."""
from pathlib import Path
import hashlib
import importlib.util
import json

base = Path(__file__).resolve().parent
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
spec = importlib.util.spec_from_file_location('historical_mutation',base/'mutation_test-full-campaign.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
checked = 0
for name in ['group-campaign','limited-control','return-control']:
    run = base/name
    campaign = read(run/'campaign.json')
    instrument = base/('final-instruments/mutation_test.py' if name=='return-control' else 'mutation_test-full-campaign.py')
    assert sha(instrument)==campaign['instrument_sha256']
    assert campaign['production_inputs_stable']
    assert campaign['baseline']['status']=='PASS' and campaign['baseline']['case_removed']
    for rel,digest in campaign['input_hashes'].items():
        assert sha(run/'inputs'/rel)==digest
    generated=[]
    for rel in ['Game/Spawn/group_completion.c','Game/Spawn/group_completion.h']:
        source=(run/'inputs'/rel).read_bytes().decode('utf-8')
        generated.extend((rel,desc,text.encode('utf-8')) for desc,text in m.mutations(source))
    assert campaign['manifest']==[dict(target=rel,description=desc) for rel,desc,_ in generated]
    assert len(generated)==campaign['total_generated']==87
    assert len(campaign['results'])==campaign['selected']
    assert m.campaign_verdict(87,campaign['selected'],campaign['results'])[0]==campaign['status']
    for result in campaign['results']:
        case=run/('case-%05d'%result['index'])
        raw=read(case/'case.json')
        assert raw=={k:v for k,v in result.items() if k not in {'index','description'}}
        rel,desc,data=generated[result['index']]
        assert result['target']==rel and result['description']==desc
        assert (case/'mutated-source.txt').read_bytes()==data
        assert hashlib.sha256(data).hexdigest()==result['input_hashes'][rel]
        assert result['case_removed']
        build=read(case/'build.json')
        assert build['exit_code']==0 and not build['timed_out']
        if result['status']=='EQUIVALENT':
            assert result['driver_sha256']==campaign['baseline']['driver_sha256']
            assert not (case/'harness.json').exists()
            continue
        harness=read(case/'harness.json')
        assert m.harness_verdict(harness)==result['status']
        diff=case/'differential'
        receipt=read(diff/'receipt.json')
        assert result['driver_sha256'] in receipt['identities'].values()
        for digest in result['input_hashes'].values():
            assert digest in receipt['identities'].values()
        if result['status']=='INVALID':
            assert name=='group-campaign' and result['index']==72
            assert receipt['status']=='INVALID'
            continue
        original=read(diff/'original-records.json')
        lines=(diff/'driver-stdout.txt').read_text().splitlines()
        assert lines[0]=='SCHEMA GROUP_COMPLETION_V2' and lines[-1].startswith('DIGEST ')
        candidate=[json.loads(line) for line in lines[1:-1]]
        assert len(candidate)==len(original)==receipt['cases']==100
        mismatch=[i for i in range(100) if candidate[i]!=original[i]]
        assert mismatch==receipt['mismatched_cases']
        same=(diff/'driver-post.bin').read_bytes()==(diff/'original-post.bin').read_bytes()
        assert same==receipt['final_bytes_equal']
        assert (not mismatch and same)==(result['status']=='PASS')
        checked+=1
old=read(base/'group-campaign/case-00072/case.json')
new=read(base/'return-control/case-00072/case.json')
assert old['driver_sha256']==new['driver_sha256']
assert old['input_hashes']['Game/Spawn/group_completion.c']==new['input_hashes']['Game/Spawn/group_completion.c']
assert read(base/'return-control-process.json')['exit_code']==3
vm=base.parent/'EXP-013-vm-pop-boundaries'
v=read(vm/'observations.json')
assert sha(vm/'probe.py')==v['probe_sha256'] and sha(vm/'reader-snapshot.py')==v['reader_sha256']
assert len(v['cases'])==14 and v['status']=='OBSERVED_MATCHING_BOUNDARIES'
for c in v['cases']:
    assert c['return_boundary'] and c['return_bits']==c['expected_return_bits']
    assert len(c['errors'])==c['expected_error_count']
    assert bytes.fromhex(c['before_hex'])[4:]==bytes.fromhex(c['after_hex'])[4:]
print('Receipt checks passed:',checked,'raw behavioral comparisons, 3 campaign manifests, 14 VM observations.')
