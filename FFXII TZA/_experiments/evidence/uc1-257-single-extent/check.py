"""Read-only source/control/projection validation and retained-result normalization."""
import copy,csv,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';ROOT=Path.cwd().resolve();sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,str(W));from normalize import normalize
raw=json.loads((W/'raw.json').read_text());diag=json.loads((R/'invalid-normalization/diagnostic.json').read_text())
assert diag['status']=='INVALID_NORMALIZATION' and diag['raw_sha256']==sha((W/'raw.json').read_bytes())
assert (R/'invalid-normalization/raw-before.json').read_bytes()==(W/'raw.json').read_bytes()
assert raw['driver_sha256']==sha((R/'driver-before-run.py').read_bytes())==sha((R/'invalid-normalization/review-before.py').read_bytes())
payload={x['name']:(R/x['name']).read_bytes() for x in raw['inputs']}
for x in raw['inputs']:assert len(payload[x['name']])==x['bytes'] and sha(payload[x['name']])==x['sha256']
def table(data):return list(csv.DictReader([l for l in data.decode('utf-8-sig').splitlines() if l and not l.startswith('#')],delimiter='\t'))
old=payload['old-flow.py'].decode();prefix=old[:old.index('adm = table(ADM)')]
assert sha(prefix.encode())==raw['reference']['flow_prefix_sha256'] and sha(payload['old-flow.py'])==raw['reference']['full_flow_sha256']
# Only the original reader/flow definitions are evaluated, never the old bulk sweep.
ns={'__file__':str(ROOT/'Database/Tools/work/ASTRA/uc1-band-ruling/review.py')};exec(compile(prefix,'unchanged retained flow prefix','exec'),ns)
assert sha(ns['raw'])==raw['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
obs=raw['observation'];entry,length=int(obs['entry'],16),obs['bytes'];assert length==353
code=bytes.fromhex(obs['raw_hex']);assert code==ns['bytes_at'](entry,length) and sha(code)==obs['sha256']
assert ns['flow'](entry,length,code)==obs['flow']
assert bytes.fromhex(obs['short352']['raw_hex'])==code[:-1] and ns['flow'](entry,length-1,code[:-1])==obs['short352']['flow']
for control in raw['controls'].values():
    data=bytes.fromhex(control['raw_hex']);a=int(control['entry'],16)
    assert data==ns['bytes_at'](a,control['bytes']) and ns['flow'](a,control['bytes'],data)==control['flow']
assert ns['flow'](0x1000,5,bytes.fromhex('750189c8c3'))['problems'], 'Disposable mid-instruction-target detector control must fail'
assert obs['candidate']==next(x for x in table(payload['band.tsv']) if x['start_va']=='00712180')
assert obs['admission']==next(x for x in table(payload['admissions.tsv']) if x['start_va']=='00712180')==json.loads((R/'admission-row.json').read_text())
assert obs['candidate']['bytes']=='353' and obs['candidate']['outcome']=='clean' and obs['admission']['verdict']=='body'
ref=obs['reference_thunk'];assert ref['row']==next(x for x in table(payload['applied1.tsv']) if x['start']=='006DAA30')
assert ref['row']['kind']=='admit-frontier' and ref['row']['end']=='006DAA35'
b=bytes.fromhex(ref['raw_hex']);ins=list(ns['md'].disasm(b,0x6DAA30));assert b==ns['bytes_at'](0x6DAA30,5) and len(ins)==1 and ins[0].mnemonic=='jmp' and ins[0].operands[0].imm==entry
listed=table(payload['functions.tsv']);parent=json.loads(payload['functions-parent.json'])
assert parent['executable_sha256']==raw['reference']['exe_sha256'] and len(listed)==parent['function_count']
sizes={int(x['entry'],16):int(x['body_bytes']) for x in listed if x['body_bytes'].isdigit() and not x['name'].startswith(('Unwind@','Catch_All@'))};assert sizes
applied=[]
for x in table(payload['errata.tsv']):
    if x['verdict']=='merge' and x['corrected_end'].strip():
        a,end=int(x['entry'],16),int(x['corrected_end'],16)
        if a in sizes and a<end<a+sizes[a]:applied.append(dict(source='errata',row=x));sizes[a]=end-a
for name in ['applied1.tsv','applied65.tsv']:
    for x in table(payload[name]):
        if x['kind']=='held':continue
        a,e=int(x['start'],16),int(x['end'],16);assert a<e
        if x['kind']=='remove-listed':assert a in sizes;sizes.pop(a)
        elif x['kind']=='extend-listed':assert a in sizes;sizes[a]=e-a
        elif x['kind'] in ['admit-frontier','split-part']:assert a not in sizes or sizes[a]==e-a;sizes[a]=e-a
        else:raise AssertionError(('Unknown applied kind',x))
        applied.append(dict(source=name,row=x))
projection=('entry\tbytes\n'+''.join(f'{v:08X}\t{sizes[v]}\n' for v in sorted(sizes))).encode()
# Initial Windows write_text produced CRLF; compare text and separately hash original bytes.
assert (R/'listed-span-projection.tsv').read_text()==projection.decode()
assert sha((R/'listed-span-projection.tsv').read_bytes())==raw['projection']['projection_sha256']
assert len(sizes)==raw['projection']['filtered_numeric_spans'] and applied==raw['projection']['applied_current_rows']
assert obs['listed_entries']==[hex(v) for v in sorted(sizes) if entry<=v<entry+length]
assert obs['numeric_span_overlaps']==[dict(entry=hex(v),bytes=z) for v,z in sorted(sizes.items()) if v<entry+length and entry<v+z]
# Exercise the actual producer with the old ambient shadow present; normalization binds from observation.
n='ruling.md';result=normalize(raw);assert result['bytes']==353 and result['end']=='0x7122e1'
for bad_length in ('ruling.md',352,0):
    bad=copy.deepcopy(raw);bad['observation']['bytes']=bad_length
    try:normalize(bad)
    except AssertionError:pass
    else:raise AssertionError(('Invalid bound accepted',bad_length))
bad=copy.deepcopy(raw);bad['observation']['end']='0x7122e0'
try:normalize(bad)
except AssertionError:pass
else:raise AssertionError('Truncated end accepted')
assert 'from normalize import normalize' in (W/'review.py').read_text() and "runpy.run_path(str(W/'check.py')" in (W/'review.py').read_text()
for x in raw['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256']
if (W/'result.json').exists():assert json.loads((W/'result.json').read_text())==result
else:(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
    for x in json.loads((W/'manifest.json').read_text())['members']:
        b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_BOUNDARY_54 retained353B/82reachable/352negative/known48negative57positive/current-at-capture collision projection; INVALID_NORMALIZATION preserved, actual default producer fixed; no admission/ABI/live proof')
