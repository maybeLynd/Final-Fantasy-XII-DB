"""Readonly host-invocation evidence checker; does not rerun the producer."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference'];spec=json.loads((W/'invocation.json').read_text())
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert sha((W/'capture.py').read_bytes())==r['driver_sha256']
source=(R/'producer.py').read_bytes();text=source.decode()
assert sha(source)==ref['producer_sha256']==spec['producer_sha256']
assert r['invocation']==spec and sha((W/'invoke_private.py').read_bytes())==spec['wrapper_sha256']
needle=spec['needle'];assert text.count(needle)==1 and needle=='FI = os.path.join(DB, "_types", "fields.tsv")'
def tags(output):
    rows=[l.split() for l in output.splitlines()]
    pairs=[(l[1],l[0]) for l in rows if len(l)>=3 and l[0] in ('PASS','FAIL')]
    assert len(pairs)==4 and {a for a,b in pairs}=={'R1','R2','M','S'}
    return dict(pairs)
assert [x['name'] for x in r['receipts']]==['current-positive','legacy-patch','generated-check']
assert [x['returncode'] for x in r['receipts']]==[0,0,1]
for x in r['receipts']:
    out=(R/(x['name']+'.stdout')).read_bytes();err=(R/(x['name']+'.stderr')).read_bytes()
    assert sha(out)==x['stdout_sha256'] and sha(err)==x['stderr_sha256'] and not err
    fixture=Path(spec['private_fixture_root'])/x['fixture']
    transformed=text.replace(needle,'FI = '+repr(str(fixture)))
    assert sha(transformed.encode())==x['transformed_source_sha256']
assert tags((R/'current-positive.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='PASS')
assert tags((R/'generated-check.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='FAIL')
assert 'patched' in (R/'legacy-patch.stdout').read_text() and 'FAILS 1' in (R/'generated-check.stdout').read_text()
before=(R/'legacy-before.tsv').read_bytes();after=(R/'legacy-generated.tsv').read_bytes();current=(R/'current-control.tsv').read_bytes()
assert sha(current)==r['receipts'][0]['before_sha256']==r['receipts'][0]['after_sha256']
assert sha(before)==r['receipts'][1]['before_sha256'] and sha(after)==r['receipts'][1]['after_sha256']==r['receipts'][2]['before_sha256']==r['receipts'][2]['after_sha256'] and before!=after
assert before.decode().rstrip('\r\n')==json.loads((R/'legacy-input-identity.json').read_text())['row']
old=before.decode().rstrip('\r\n').split('\t');new=after.decode().rstrip('\r\n').split('\t')
assert old[:2]==new[:2]==['Widget','0x0B8'] and old[5].startswith('1.0f on every widget in the game') and 'BY DEFAULT' in new[5]
assert 'COMPLETED comparison' not in new[5] and 'DAZ' not in new[5] and 'COMPLETED comparison' in current.decode() and 'DAZ' in current.decode()
F=W/'initial-parser-failure';f=json.loads((F/'failure.json').read_text())
assert f['status']=='INVALID_NORMALIZATION' and (F/'additive-source-provenance.json').exists()
assert tags((F/'retained/current-positive.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='PASS') and tags((F/'retained/generated-check.stdout').read_text())==dict(R1='PASS',R2='PASS',M='PASS',S='FAIL')
try:tags('')
except AssertionError:pass
else:raise AssertionError('Zero-case output accepted')
assert r['normalized']['generated_S']=='FAIL' and r['normalized']['current_positive_S']=='PASS' and r['normalized']['generated_failure_count']==1
if (W/'manifest.json').exists():
    m=json.loads((W/'manifest.json').read_text())['members'];assert m
    for x in m:
        data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_HOST_TEMPLATE_REPLAY currentpositive/guard-preservingFIonly/freshpatch/generatedSFAIL/exactraw/nonemptyparsercontrols; no FF12/native/live proof')
