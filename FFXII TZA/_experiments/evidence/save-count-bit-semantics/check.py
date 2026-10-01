import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());s=json.loads((W/'retained/source.json').read_text())
assert r['source_sha256']==sha((W/'retained/source.json').read_bytes()) and r['driver_sha256']==sha((W/'derive.py').read_bytes())
assert r['contract_sha256']==sha((W/'retained/contract.md').read_bytes())
raw=bytes.fromhex(next(x for x in s['bodies'] if x['name']=='save')['raw_hex']);assert len(raw)==89 and sha(raw)==r['body_sha256']=='ebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii={i.address:i for i in cs.disasm(raw,0x36D930)}
assert sum(i.size for i in ii.values())==89
expected=[(0x36D948,'85c9','test'),(0x36D94A,'7436','je'),(0x36D950,'448bd1','mov'),(0x36D97C,'4983ea01','sub'),(0x36D980,'75df','jne')]
assert len(r['anchors'])==len(expected)
for a,(pc,raw,mn) in zip(r['anchors'],expected):
 i=ii[pc];assert (i.bytes.hex(),i.mnemonic)==(raw,mn) and a==dict(pc=hex(pc),bytes=raw,mnemonic=mn,args=i.op_str)
assert ii[0x36D94A].operands[0].imm==0x36D982 and ii[0x36D980].operands[0].imm==0x36D961
assert ii[0x36D950].reg_name(ii[0x36D950].operands[0].reg)=='r10d' and ii[0x36D97C].reg_name(ii[0x36D97C].operands[0].reg)=='r10'
assert [c['ecx_hex'] for c in r['cases']]==['00000000','00000001','7FFFFFFF','80000000','FFFFFFFF']
for c in r['cases']:
 n=int(c['ecx_hex'],16);assert c['native_enters_first_iteration']==(n!=0) and c['native_zero_gate_takes_tail']==(n==0)
 assert c['r10_after_mov_r10d_ecx']==(n if n else None) and c['r10_after_first_sub']==(n-1 if n else None)
 assert c['signed_for_skips']==(c['signed_interpretation']<=0)
assert r['mutation']['rejected'] and all(c['native_enters_first_iteration'] and c['signed_for_skips'] for c in r['cases'][-2:])
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  raw=(W/x['path']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
print('PASS_STATIC_PREFIX count-zero gate, zero-extended32bit count/64bit countdown and signed-gate source control; no original execution/fault/completion claim')
