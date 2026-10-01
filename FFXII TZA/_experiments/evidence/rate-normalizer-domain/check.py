import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();r=json.loads((W/'result.json').read_text());ref=r['reference'];code=(R/'source.bin').read_bytes();isa=json.loads((W/'isa.json').read_text())
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']=='0x229e70' and ref['bytes']==len(code)==37 and sha(code)==ref['body_sha256']
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32' and sha((W/'isa.json').read_bytes())==ref['isa_sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x229E70)};assert sum(i.size for i in ii.values())==37
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()]
for a,h in {0x229E70:'f30f100da889bd01',0x229E78:'0f57c0',0x229E7B:'0f2fc1',0x229E7E:'7211',0x229E80:'f30f1005201dac01',0x229E88:'f30f11059089bd01',0x229E90:'c3',0x229E91:'0f28c1',0x229E94:'c3'}.items():assert ii[a].bytes.hex()==h
assert ii[0x229E7E].operands[0].imm==0x229E91 and not any(i.mnemonic=='call' for i in ii.values())
for a,n,target in [(0x229E70,1,0x1E02820),(0x229E88,0,0x1E02820),(0x229E80,1,0x1CEBBA8)]:i=ii[a];assert i.address+i.size+i.operands[n].mem.disp==target
assert (R/'one.bin').read_bytes()==bytes.fromhex('0000803f') and isa['completed_flags_zf_pf_cf']==dict(unordered='111',greater='000',less='001',equal='100')
cases=r['cases'];assert len(cases)==6 and [c['input_bits'] for c in cases]==['3F000000','40000000','00000000','80000000','BF800000','7FC00001'] and [c['return_bits'] for c in cases]==['3F000000','40000000','3F800000','3F800000','3F800000','7FC00001']
for c in cases:
 flags=isa['completed_flags_zf_pf_cf'][c['completed_relation']];assert c['zf_pf_cf']==flags and c['branch_taken']==(flags[2]=='1') and c['store_default']==(flags[2]!='1') and c['global_after_bits']==c['return_bits'] and c['return_bits']==(c['input_bits'] if flags[2]=='1' else '3F800000')
assert [c['store_default'] for c in r['daz_conditional']]==[False,True] and [c['return_bits'] for c in r['daz_conditional']]==['00000001','3F800000']
assert len(r['controls'])==2
for c in r['controls']:
 raw=bytes.fromhex(c['mutant_hex']);delta=[j for j,(a,b) in enumerate(zip(code,raw)) if a!=b];assert len(raw)==37 and len(delta)==1 and c['binding_rejected'] and c['baseline']['return_bits']!=c['private_source_model']['return_bits']
 if c['name']=='zero-reset-JB-to-JBE':assert delta==[14] and raw[14]==0x76 and c['private_source_model']['return_bits']=='00000000'
 else:assert c['name']=='fraction-comparison-operands-swapped' and delta==[13] and raw[13]==0xC8 and c['private_source_model']['return_bits']=='3F800000'
for x in r['consumer_preimages']:assert sha((R/x['retained_name']).read_bytes())==x['sha256']
assert json.loads((R/'catalog-identity.json').read_text())['row']['body_bytes']=='37' and json.loads((R/'field-preimage.json').read_text())['row'].split('\t')[:2]==['Widget','0x0B8']
assert {x['site'] for x in json.loads((R/'caller-identities.json').read_text())}=={'0x244dfe','0x2469c9'}
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  d=(W/x['path']).read_bytes();assert len(d)==x['bytes'] and sha(d)==x['sha256']
print('PASS_SOURCE_RATE_DOMAIN positivefraction retained, negative reset, completedunordered bypasses default; exact branch/constant/write/source controls, no original/native/live or universal-positive proof')
