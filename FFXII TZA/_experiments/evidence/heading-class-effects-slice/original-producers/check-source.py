import hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
t=json.loads((W/'capture-terminal.json').read_bytes())
if '--fault-upstream-failed' in sys.argv:t['returncode']=1
assert t['terminal'] is True and t['returncode']==0 and not t['stderr'] and t['driver_sha256']==sha(W/'capture.py')
r=json.loads((W/'raw.json').read_bytes());i=json.loads((W/'identity.json').read_bytes());assert i['driver_sha256']==t['driver_sha256'] and r['status']=='SOURCE_ONLY_NOT_CLASS_PRESERVATION'
assert len(r['direct_call_sites'])==21 and len(r['unique_targets'])==15
if '--fault-cookie-omitted' in sys.argv:r['callees']=[f for f in r['callees'] if f['entry']!='0x808c40']
assert {int(f['entry'],16) for f in r['callees']}==set(r['unique_targets']), 'Every observed direct target, including cookie/failure helper, must be captured'
for f in r['callees']:
 data=(W/f['code_file']).read_bytes();assert len(data)==f['bytes']==f['decoded_bytes'] and hashlib.sha256(data).hexdigest()==f['code_sha256']
 assert b''.join(bytes.fromhex(x['bytes']) for x in f['instructions'])==data
 if f['extent_status']=='UNWIND_UNION_MATCH':assert f['unwind_contiguous'] is True and f['unwind_union']==f['bytes'] and f['fragments']
 elif f['extent_status']=='UNPROVED_CATALOGUE_ONLY':assert not f['fragments'] and f['unwind_union'] is None
 else:raise AssertionError('Unrecognized/missing extent status')
prior=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review');p=json.loads((prior/'raw.json').read_bytes());m={int(x['pc'],16):(x['mnemonic'],x['args']) for x in p['instructions']}
assert m[0x2e4964]==('xor','edx, edx') and m[0x2e4966]==('mov','rcx, rsi') and m[0x2e4969]==('call','0x26c120')
f=next(f for f in r['callees'] if f['entry']=='0x26c120');n={int(x['pc'],16):(x['mnemonic'],x['args']) for x in f['instructions']}
assert n[0x26c156]==('test','edx, edx') and n[0x26c158]==('je','0x26c244')
modezero=[x['target'] for x in f['call_sites'] if 0x26c244<=int(x['pc'],16)<=0x26c26d];assert modezero==['0x2ebe50','0x2e8ee0','0x2e6300']
if '--fault-mode-four' in sys.argv:assert m[0x2e4964]==('mov','edx, 4'),'Caller explicitly supplies mode0; do not test irrelevant mode4 to establish this call path'
print(json.dumps({'status':'SOURCE_CAPTURE_AND_ZERO_MODE_DISCRIMINATOR_VALID','normal_mode0_nested_targets':modezero,'scope':'Original static call argument/branch only. No class-preservation, initialized alias, nested effects or live reachability acceptance. Leaf extents remain separately unproved.'},indent=2))
