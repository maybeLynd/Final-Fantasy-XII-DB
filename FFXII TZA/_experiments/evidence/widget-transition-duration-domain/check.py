import hashlib,json,struct
from pathlib import Path
import capstone
from capstone.x86_const import X86_OP_MEM,X86_REG_RSP
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest();r=json.loads((W/'result.json').read_text());ref=r['reference'];code=(W/'retained/source.bin').read_bytes()
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']=='0x2468a0' and ref['end_exclusive']=='0x246a0c' and len(code)==364 and sha(code)==ref['body_sha256']
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and sha((W/'retained/shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x2468A0));assert sum(i.size for i in ins)==364
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins];ii={i.address:i for i in ins}
for pc,b in {0x2468A0:'4053',0x2468A2:'4883ec40',0x2468C9:'4885c9',0x2468CC:'7456',0x2468CE:'f681800000000e',0x2468D5:'754d',0x2468E0:'7557',0x2468EC:'754b',0x246971:'6b4c24703c',0x246995:'b8d34d6210',0x24699A:'f7e9',0x2469A6:'c1fa06',0x2469A9:'8bc2',0x2469AB:'c1e81f',0x2469AE:'03d0',0x2469B0:'899390000000'}.items():assert ii[pc].bytes.hex()==b
assert ii[0x2468E0].operands[0].imm==ii[0x2468EC].operands[0].imm==0x246939
duration_access=[(i.address,o.size) for i in ins for o in i.operands if o.type==X86_OP_MEM and o.mem.base==X86_REG_RSP and o.mem.disp==0x70];assert duration_access==[(0x246971,4)]
assert not any(i.mnemonic=='call' for i in ins if 0x246939<=i.address<=0x2469B0)
mut=bytearray(code);mut[0x24699A-0x2468A0+1]=0xE1;assert bytes(mut)==(W/'retained/changed-multiply-source.bin').read_bytes() and r['detector']['raw_hex']==bytes(mut).hex() and r['detector']['original_binding_rejected']
assert next(i for i in cs.disasm(mut,0x2468A0) if i.address==0x24699A).mnemonic=='mul'
s32=lambda x:struct.unpack('<i',int(x).to_bytes(4,'little'))[0]
def casecheck(c,unsigned=False):
 ms=int(c['input_dword_bits'],16);low=(ms*60)&0xFFFFFFFF;s=s32(low);full=((low if unsigned else s)*0x10624DD3)&0xFFFFFFFFFFFFFFFF;hi=(full>>32)&0xFFFFFFFF;shift=(s32(hi)>>6)&0xFFFFFFFF;adj=shift>>31;out=(shift+adj)&0xFFFFFFFF
 assert c['input_signed']==s32(ms) and c['low32_product_bits']==f'{low:08X}' and c['product_signed']==s and c['full_product_bits']==f'{full:016X}' and c['high32_product_bits']==f'{hi:08X}' and c['shifted_bits']==f'{shift:08X}' and c['sign_adjustment']==adj and c['stored_bits']==f'{out:08X}' and c['stored_signed']==s32(out)
 assert c['signed_division_trunc0']==(abs(s)//1000)*(-1 if s<0 else 1)
assert len(r['cases'])==5 and [c['stored_signed'] for c in r['cases']]==[60,1,-1,2147483,-2147483]
for c in r['cases']:casecheck(c);assert c['stored_signed']==c['signed_division_trunc0']
assert r['cases'][2]['input_signed']==-17 and r['cases'][2]['product_signed']==-1020 and r['cases'][2]['stored_bits']=='FFFFFFFF' and r['host_predictions']['negative17_floor']==-2
assert r['cases'][3]['input_signed']==35791394 and r['cases'][3]['low32_product_bits']=='7FFFFFF8' and r['cases'][4]['input_signed']==35791395 and r['cases'][4]['low32_product_bits']=='80000034' and r['host_predictions']['positive_overflow_unbounded_trunc0']==2147483
casecheck(r['detector']['calculation'],True);assert r['detector']['calculation']['stored_bits']!=r['cases'][2]['stored_bits']
p=r['input_path'];assert p['entry_rsp_to_local_rsp_delta']==-0x48 and p['local_duration_offset']==0x70 and p['entry_duration_offset']==0x28 and p['argument_width']==4
assert sha((W/'retained/prior37-manifest.json').read_bytes())==ref['prior37_manifest_sha256']
prior=(W/'retained/prior37-source.bin').read_bytes();priorii={i.address:i for i in cs.disasm(prior,0x244E9C)};assert len(prior)==67 and priorii[0x244ECF].bytes.hex()=='f7e1' and priorii[0x244ED1].bytes.hex()=='c1ea06'
rows=json.loads((W/'retained/field-preimages.json').read_text());assert len(rows['rows'])==2 and {x.split('\t')[1] for x in rows['rows']}=={'0x070','0x090'}
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_SOURCE_SIGNED_DURATION low32 product, signed reciprocal/SAR/sign correction; negative17 trunc-1 vsfloor-2, firstpositiveoverflow flips sign; bounded+70 source distinction, no native/original/live calls')
