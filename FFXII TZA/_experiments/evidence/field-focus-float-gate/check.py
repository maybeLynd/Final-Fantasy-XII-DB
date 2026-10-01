import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference'];assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and r['architecture_sha256']==sha((W/'architecture.json').read_bytes())
for n,k in [('gate.bin','gate_sha256'),('zero.bin','zero_sha256'),('bit3-helper.bin','helper_sha256'),('shipping-reader.py','reader_sha256')]:assert sha((W/'retained'/n).read_bytes())==ref[k]
assert (W/'retained/zero.bin').read_bytes().hex()=='0f57ff'
assert (W/'retained/bit3-helper.bin').read_bytes().hex()=='0fb705ebfbf601c1e80383e001c3'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
raw=(W/'retained/gate.bin').read_bytes();ii={i.address:i for i in cs.disasm(raw,0x22AB68)}
assert len(raw)==sum(i.size for i in ii.values())==32 and len(ii)==9
expected=['e833d81200','85c0','7417','f30f1005479fe301','0f2ec7','7a12','7510','418bcf','e8385c0200']
assert [i.bytes.hex() for i in ii.values()]==expected
assert r['anchors']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()]
assert ii[0x22AB7C].mnemonic=='jp' and ii[0x22AB7E].mnemonic=='jne'
assert ii[0x22AB7C].operands[0].imm==ii[0x22AB7E].operands[0].imm==0x22AB90
assert ii[0x22AB6F].operands[0].imm==0x22AB88 and ii[0x22AB83].operands[0].imm==0x2507C0
assert ii[0x22AB71].address+ii[0x22AB71].size+ii[0x22AB71].operands[1].mem.disp==0x2064AC0
assert [ii[0x22AB79].reg_name(o.reg) for o in ii[0x22AB79].operands]==['xmm0','xmm7']
assert len(r['domains'])==4 and {x['relation'] for x in r['domains']}=={'unordered','greater','less','equal'}
for x in r['domains']:
 assert x['send']==(x['zf']==1 and x['pf']==0) and x['send_if_parity_guard_removed']==bool(x['zf'])
assert next(x for x in r['domains'] if x['relation']=='unordered')['send'] is False
assert next(x for x in r['domains'] if x['relation']=='unordered')['send_if_parity_guard_removed'] is True
assert [x['bits'] for x in r['cases']]==['00000000','80000000','3F800000','BF800000','7F800000','FF800000','7FC00001','7F800001','00000001','80000001']
for x in r['cases']:
 bits=int(x['bits'],16);zero=(bits&0x7FFFFFFF)==0;sub=(bits&0x7F800000)==0 and (bits&0x7FFFFF)!=0
 assert x['admitted_daz0_completed']==zero and x['admitted_daz1_completed']==(zero or sub)
assert len(r['producer_controls'])==2 and [x['name'] for x in r['producer_controls']]==['original','parity-branch-omitted-view']
for x in r['producer_controls']:assert x['exit']==0 and 'PASS O5' in x['stdout'] and 'FAILS 0' in x['stdout']
c=json.loads((W/'retained/cache-mutation.json').read_text());assert 'jp 0x22ab90' in c['before'] and 'nop' in c['after']
assert [x['cache_sha256'] for x in r['producer_controls']]==[c['original_cache_sha256'],c['mutant_cache_sha256']]
assert c['original_cache_sha256']!=c['mutant_cache_sha256'] and r['source_mutation']['source_obligation_rejected']
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_STATIC_GATE originalJP/JNE ordered-equality, conditional domains, actual checker-blindness control and source-mutant rejection; no original-code/live execution')
