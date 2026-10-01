import hashlib,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;s=json.loads((W/'source.json').read_text());body=s['body'];raw=bytes.fromhex(body['raw_hex'])
assert len(raw)==542 and hashlib.sha256(raw).hexdigest()==body['sha256']=='03d069e5f80b0ca4064fe36f11683df4110a494a96d7f920e1d43c19e1bef773'
assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert hashlib.sha256((W/'retained/query-source.json').read_bytes()).hexdigest()==s['reference_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(raw,0x383F10));assert sum(i.size for i in ii)==542
d={i.address:i for i in ii}
for p,args in [(0x383F64,'edx, word ptr [rbx + 4]'),(0x383F7D,'r8d, word ptr [rbx + 6]'),(0x383FDB,'ecx, word ptr [rbx + 6]'),(0x38400E,'ecx, word ptr [rbx + 4]')]:assert d[p].mnemonic=='movsx' and d[p].op_str==args
for p,args in [(0x383F99,'ecx, byte ptr [rbx + 2]'),(0x383F9D,'eax, byte ptr [rbx]'),(0x383FB5,'ecx, byte ptr [rbx + 3]'),(0x383FB9,'eax, byte ptr [rbx + 1]'),(0x383FEC,'ecx, byte ptr [rbx + 1]'),(0x384016,'ecx, byte ptr [rbx]')]:assert d[p].mnemonic=='movzx' and d[p].op_str==args
guards=[0x383F77,0x383F93,0x383FAF,0x383FCD]
for p in guards:assert d[p].mnemonic=='ja' and d[p].operands[0].imm==0x384120
for p,args in [(0x383F74,'xmm0, xmm1'),(0x383F90,'xmm0, xmm2'),(0x383FAC,'xmm1, xmm0'),(0x383FCA,'xmm2, xmm0')]:assert d[p].mnemonic=='comiss' and d[p].op_str==args
for p,args in [(0x383FA0,'ecx, eax'),(0x383FBD,'ecx, eax')]:assert d[p].mnemonic=='imul' and d[p].op_str==args
for p,args in [(0x383FA3,'ecx, edx'),(0x383FC0,'ecx, r8d')]:assert d[p].mnemonic=='add' and d[p].op_str==args
assert max(guards)<0x383FF7<0x384020
for p in (0x383FF3,0x38401C):assert d[p].mnemonic=='subss'
for p in (0x383FF7,0x384020):assert d[p].mnemonic=='cvttss2si' and d[p].op_str=='eax, xmm1'
for p in (0x384001,0x384025):assert d[p].mnemonic=='idiv' and d[p].op_str=='ecx'
assert d[0x384027].mnemonic=='add' and d[0x384027].op_str=='eax, r8d'
assert d[0x38402A].mnemonic=='cdqe' and d[0x38402C].mnemonic=='movzx' and d[0x38402C].op_str=='ecx, word ptr [r9 + rax*2]'
assert not any(i.mnemonic.startswith('j') for i in ii if 0x383FF7<=i.address<0x38402C)
for p in (0x383F44,0x383F5A):assert d[p].mnemonic=='cmp' and d[p].op_str=='ax, 2'
for p in (0x383F48,0x383F5E):assert d[p].mnemonic=='je' and d[p].operands[0].imm==0x384120
assert d[0x384120].mnemonic=='mov' and d[0x384120].op_str=='eax, 0xff'
fd=next(x for x in s['imports'] if x['iat']=='0x8c2c10');assert fd['name']=='_fdclass'
for p in (0x383F3E,0x383F54):
 i=d[p];assert i.mnemonic=='call' and i.address+i.size+i.operands[0].mem.disp==0x8C2C10
# Range proof, not an executed fixture: lower <= finite point <= lower+span,
# stable narrow fields. Endpoints are exactly representable binary32 integers;
# any ordinary binary32 rounding keeps a finite subtraction in [0,span].
origin=(-2**15,2**15-1);spanmax=(2**8-1)**2;uppermax=origin[1]+spanmax
assert spanmax==65025 and uppermax==97792 and uppermax<2**24
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
for x in (*origin,spanmax,uppermax,0):assert f32(x)==x
assert 0<=spanmax<2**31
maxlinear=255*255+255;assert maxlinear==65280 and maxlinear<2**31
# Dependency controls: narrowing and ALL four bound checks matter. Widened
# unsigned16 extent product exceeds INT32, so that substitute layout cannot
# support this proof. Removing a guard invalidates its own axis inequality.
assert 65535*65535>2**31-1
obligations={hex(p):why for p,why in zip(guards,['X>=originX','Z>=originZ','X<=originX+cw*cols','Z<=originZ+ch*rows'])}
assert len(obligations)==4
v=dict(status='PASS_STATIC_ONLY',method='A finite stable-domain proof from original source',new_original_code_executions=0,live_cases=0,
 origin_range=origin,span_range=[0,spanmax],upper_range=[origin[0],uppermax],converted_displacement_range=[0,spanmax],linear_index_upper_bound=maxlinear,
 original_guard_obligations=obligations,conversion_pcs=['0x383ff7','0x384020'],table_read_pc='0x38402c',postconversion_index_range_guard=False,
 classifier='Only original returnedAX==2 ->FF source branch; parent finite host-stub/import witness is NOT native classifier behavior.',
 rejected_consumer_inference='Stable admitted finite point cannot produce negative/indefinite conversion here. Out-of-grid finite coordinates exit by earlier bounds, not downstream cell-index guard.',
 limits='Stable finite point/header/bindings required; native classifier/MXCSR/initialization/atomicity unobserved. Nonzero divisor required to complete IDIV. Nonnegative/int32-safe index does NOT imply in-table; equality/rounding hazards retained in parent evidence.')
if (W/'manifest.json').exists():assert json.loads((W/'validation.json').read_text())==json.loads(json.dumps(v))
else:(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS A domain: four original guards/narrow fields => finite CVTT0..65025; no postconversion rangeguard. No B/C rerun.',flush=True)
