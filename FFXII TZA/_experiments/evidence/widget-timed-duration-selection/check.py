import hashlib,json,struct
from fractions import Fraction
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest();r=json.loads((W/'result.json').read_text());ref=r['reference'];code=(W/'retained/source.bin').read_bytes()
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']=='0x244e9c' and ref['end_exclusive']=='0x244edf' and len(code)==67 and sha(code)==ref['body_sha256']
assert r['driver_sha256']==sha((W/'derive.py').read_bytes()) and sha((W/'retained/shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x244E9C));assert sum(i.size for i in ins)==67
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins];ii={i.address:i for i in ins}
expected={0x244E9C:'0fb77902',0x244EA0:'e8ebcdf3ff',0x244EA5:'33c9',0x244EA7:'83f801',0x244EAA:'8b437c',0x244EAD:'0f44f9',0x244EB0:'0fbae00b',0x244EB4:'730c',0x244EB6:'8bf8',0x244EB8:'0fbaf70b',0x244EBC:'897b7c',0x244EBF:'c1ef16',0x244EC2:'6bcf3c',0x244EC5:'b8d34d6210',0x244ECF:'f7e1',0x244ED1:'c1ea06',0x244ED4:'895370',0x244ED7:'83637cf4',0x244EDB:'834b7c04'}
for pc,b in expected.items():assert ii[pc].bytes.hex()==b
assert ii[0x244E9C].operands[-1].size==2 and ii[0x244EA0].operands[0].imm==0x181C90 and ii[0x244EB4].operands[0].imm==0x244EC2
assert not any(i.mnemonic in ('cmp','test','bt','btr') for i in ins if 0x244EA7<i.address<0x244EAD),'MOV flags read must preserve CMP return flags for CMOVE'
mut=bytearray(code);mut[0x244EBF-0x244E9C+2]=0x15;assert bytes(mut)==(W/'retained/changed-shift-source.bin').read_bytes() and r['detector']['raw_hex']==bytes(mut).hex() and r['detector']['original_binding_rejected']
assert next(i for i in cs.disasm(mut,0x244E9C) if i.address==0x244EBF).operands[1].imm==21
proof=r['domain_proof'];assert proof['max_record_ms']==65535 and proof['max_override_ms']==1023 and proof['max_product']==3932100 and proof['magic']==0x10624DD3 and proof['shift']==38 and proof['magic_excess_times1000']==56
error=Fraction(proof['max_error_numerator'],proof['max_error_denominator']);assert error==Fraction(3932100*56,1000*(1<<38)) and 0<=error<Fraction(20,1000)
assert 60%20==1000%20==0 and (0x10624DD3*1000)-(1<<38)==56 and 3932100<2**31
assert [c['frames'] for c in r['cases']]==[60,0,1,3932,0,1,0,61,0]
def casecheck(c,shift):
 flags=int(c['flags_before'],16);record=c['record_ms'];assert 0<=record<=65535 and 0<=flags<=0xFFFFFFFF
 override=bool(flags&0x800);cleared=flags&~0x800 if override else flags;chosen=(cleared>>shift) if override else (0 if c['callee_return']==1 else record)
 assert c['override']==override and c['selected_ms']==chosen and c['flags_after_override']==f'{cleared:08X}' and c['flags_after_local_state']==f'{((cleared&0xFFFFFFF4)|4):08X}'
 x=chosen*60;assert c['product']==x and c['frames']==((x*0x10624DD3)>>38)==c['ordinary_division']==x//1000
for c in r['cases']:casecheck(c,22);assert c['selected_ms']<=65535 and (not c['override'] or c['selected_ms']<=1023)
assert r['cases'][4]['callee_return']==r['cases'][5]['callee_return']==r['cases'][6]['callee_return']==1 and [r['cases'][k]['selected_ms'] for k in (4,5,6)]==[0,17,0]
casecheck(r['detector']['calculation'],21);assert r['detector']['calculation']['selected_ms']==2047 and r['detector']['calculation']['frames']==122
rows=json.loads((W/'retained/field-preimages.json').read_text());assert len(rows['rows'])==2 and {x.split('\t')[1] for x in rows['rows']}=={'0x070','0x07C'}
assert (W/'retained/getter-context.bin').read_bytes().hex()=='4883ec28e8a79d06008b80800200004883c428c3'
assert r['tools']['capstone_dll']['bytes']>0 and len(r['tools']['capstone_dll']['sha256'])==64
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_SOURCE_SELECTION post-zero bit11 override/high10bits/consumption; u16 or10bit bounded exact reciprocal floor; source-model controls and changedSHIFT rejected; no original/native/emulator/live tests')
