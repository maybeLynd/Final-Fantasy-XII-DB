"""Reduce actual original guest writes; arithmetic predictions aren't execution."""
import hashlib,importlib.util,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());ref=raw['reference'];code=(R/'original194.bin').read_bytes();table=(R/'original-table24.bin').read_bytes();assert len(code)==194 and sha(code)==ref['body_sha256'] and len(table)==24 and sha(table)==ref['table_sha256']
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==ref['access_policy_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'retained reviewed source adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii={i.address:i for i in cs.disasm(code,0x26d530)};assert len(ii)==len(raw['instructions']) and all(ii[int(r['pc'],16)].bytes.hex()==r['hex'] and ii[int(r['pc'],16)].mnemonic==r['mnemonic'] for r in raw['instructions']);assert not any(i.mnemonic=='call' for i in ii.values());assert [hex(0x120000+x) for x in struct.unpack('<6I',table)]==ref['targets']
for r in raw['instructions']:
 i=ii[int(r['pc'],16)];mem=[dict(kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp,size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM];assert mem==r['memory'],'Actual shared-policy decoding differs'
assert len(raw['cases'])==22
extra=json.loads((W/'extra-s16-boundary.json').read_text());assert extra['parent_raw_sha256']==sha((W/'raw.json').read_bytes()) and extra['runner_source_sha256']==raw['driver_sha256']==sha((R/'runner-source-used-for-extra.py').read_bytes());assert len(extra['cases'])==3 and [c['signed_input'] for c in extra['cases']]==[-32767,-32766,32769]
assert ii[0x26d5c7].mnemonic=='mov' and ii[0x26d5c7].operands[1].imm & 0xffffffff == 0xffff8001 and ii[0x26d5d4].mnemonic=='mov' and ii[0x26d5d4].operands[1].imm==0x8000,'Original width3 bound constants are not standard signed16 limits'
if '--fault-standard-s16-bounds' in sys.argv:assert ii[0x26d5c7].operands[1].imm & 0xffffffff == 0xffff8000,'Conventional signed16 clamp contradicts original lower bound'
out=[];sizes=[1,1,2,2,4,4];bounds=[(0,255),(-128,127),(0,65535),(-32767,32768)]
for c in raw['cases']+extra['cases']:
 w=c['width'];v=c['signed_input'];a=c['after'];assert c['error'] is None and a['pc']=='0x60000200' and a['rsp']==hex(0x60001808+8) and 0<len(c['visits'])<64 and c['visits'][-1] in ref['returns'] and c['reads']
 assert a['record']==c['initial']['record'] and a['code']==c['running_hex'] and a['table']==table.hex() and a['stack']==struct.pack('<Q',0x60000200).hex()
 running=bytes.fromhex(c['running_hex']);expected_code=bytearray(code)
 if c['mutated']:expected_code[0x26d577-0x26d530+1]=0x4c
 assert running==bytes(expected_code) and (sha(running)==ref['body_sha256'])!=c['mutated']
 before=bytes.fromhex(c['initial']['guard_memory']);after=bytes.fromhex(a['guard_memory']);expected=bytearray(before)
 if w<=5:
  size=sizes[w];address=0x40000100+c['index']*size
  value=max(bounds[w][0],min(bounds[w][1],v)) if w<4 else int(c['input_bits'],16)
  if c['mutated']:assert w==0 and v==256;value=256 # private CMOVL changes clamp branch; low byte becomes00
  expected_bits=value&((1<<(size*8))-1);expected_bytes=expected_bits.to_bytes(size,'little');writes=c['writes'];assert len(writes)==1 and writes[0]['address']==hex(address) and writes[0]['size']==size and writes[0]['hex']==expected_bytes.hex(),'Original effect/width/address or detector mismatch'
  offset=address-(0x40000100-32);expected[offset:offset+size]=expected_bytes;assert after==bytes(expected),'Unexpected surrounding memory changes'
  wrapped=int(c['input_bits'],16)&((1<<(size*8))-1)
  if '--fault-narrowing-wrap' in sys.argv and w<4 and not c['mutated']:assert expected_bits==wrapped,'Wrapping cast disagrees with original saturating write'
  out.append(dict(width=w,input_bits=c['input_bits'],signed_input=v,index=c['index'],private_opcode=c['mutated'],lower_descriptor_bits=c['lowbits'],address=hex(address),write_hex=expected_bytes.hex(),wrap_prediction_hex=wrapped.to_bytes(size,'little').hex(),wrap_agrees=expected_bits==wrapped,signed16_view_prediction=struct.unpack('<h',expected_bytes)[0] if w==3 else None))
 else:
  assert w==6 and not c['writes'] and after==before and '0x26d545' in c['visits'] and c['visits'][-1]=='0x26d5f1'
  if '--fault-no-write-as-undetected' in sys.argv:assert not any(x['width']==5 and x['writes'] for x in raw['cases']),'No-write claim must retain positive width5 write detector'
  out.append(dict(width=w,input_bits=c['input_bits'],no_write=True,positive_detector='Original width5 case writes4B; source width compare/JA then complete RET observed'))
original=next(c for c in raw['cases'] if c['width']==0 and c['signed_input']==256 and not c['mutated'] and c['lowbits']=='0x0');private=next(c for c in raw['cases'] if c['mutated']);assert original['writes'][0]['hex']=='ff' and private['writes'][0]['hex']=='00'
if '--fault-accept-clamp-mutation' in sys.argv:assert original['writes'][0]['hex']==private['writes'][0]['hex'],'Original clamp opcode matters to observed write'
result=dict(status='ORIGINAL_RESOLVED_STORE_SATURATION_SUPPORTED',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),extra_raw_sha256=sha((W/'extra-s16-boundary.json').read_bytes()),observations=out,interpretation='Verified complete original call-free leaf/table writes width0u8 and2u16 by signed-input clamp [0,MAX], width1s8 by signed MIN/MAX clamp; width3 clamps signed input to[-32767,+32768] then stores low16 bits (unusual asymmetric bounds, intent unknown). Not C narrowing/wrap: negativeu8->00 and256->FF. Original width3 -32768 stores8001 and +32768/+32769 stores8000; signed16 reinterpretation prediction differs from normal signed-limit clamp, not an executed PUSHV read. Width4/5 store raw supplied dword bits with stride4; width5 NaN payload7FC00000 copied, not float arithmetic/conversion. Width3 index-1 writes base-2; supplied signed index is scaled here, no new index clamp in this leaf. Width6 returns without destination write with positive observer/fullRET controls. Lower28 descriptor bits ignored by this leaf selector in tested supplied record. This leaf performs resolved value stores; no call/free/release occurs in its verified closed source graph, refuting canonical release-block wording for0026D530.',controls=dict(private_clamp_opcode_changes_ff_to_00=True,original_provider_source_and_table_verified=True,all_guests_complete_ret=True,guards_record_code_table_stack_preserved=True,no_write_negative_has_positive_detector=True),limits='Isolated supplied already-resolved ABI record/state, not original POPV/caller conversion/execution/notification, actual bank initialization/lifetime/scheduling/normal gameplay or caller-guaranteed value/index domain. No universal malformed/alias safety; signed index-1 writes intentionally within bounded guard. Emulator not native CPU/game and no MXCSR status parity claim. Source-derived closed code/table graph, not whole module or unwind extent proof. Consumer correction/independent acceptance pending, PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';encoded=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==encoded,'Frozen result differs'
else:p.write_bytes(encoded)
print('PASS67 original narrow signed-input saturation, raw wide stores and bounded negative/control writes; no caller/native-game proof',flush=True)
