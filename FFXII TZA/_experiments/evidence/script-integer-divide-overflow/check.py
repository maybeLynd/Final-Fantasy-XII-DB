import sys
sys.dont_write_bytecode=True
import hashlib,json,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'original5.bin').read_bytes();guard=(R/'guard8.bin').read_bytes();assert code.hex()=='99f7fb8bc8' and guard.hex()=='85db0f84a9f5ffff';assert sha(code)==raw['reference']['code_sha256'] and sha(guard)==raw['reference']['guard_sha256']
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
for f in raw['reference']['parent_files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
parent=json.loads((R/'parent79-raw.json').read_text());manifest=json.loads((R/'parent79-manifest.json').read_text());members={m['path']:m for m in manifest['members']}
for f in raw['reference']['parent_files']:
 if f['path']!='manifest.json':assert members[f['path']]['sha256']==f['sha256']
assert parent['reference']['exe_sha256']==raw['reference']['exe_sha256'] and parent['reference']['opcode']=='0x15' and parent['reference']['name']=='OPDIV';full=(R/'parent79-opdiv298.bin').read_bytes();assert len(full)==298 and full[45:50]==code and full[37:45]==guard
assert 0x120000+int.from_bytes((R/'parent79-dispatch4.bin').read_bytes(),'little')==0x25f0ac and (R/'parent79-name32.bin').read_bytes().split(b'\0')[0]==b'OPDIV'
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'actual shared adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
for b,pc,rows in [(code,0x25f0d9,raw['instructions']),(guard,0x25f0d1,raw['guard'])]:
 ii=list(cs.disasm(b,pc));assert sum(i.size for i in ii)==len(b);assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ii]==[(x['pc'],x['hex'],x['mnemonic'],x['args']) for x in rows]
 for i,x in zip(ii,rows):assert sorted(roles.written(i))==x['written'] and x['memory']==[]
# Private adapter regressions are not shipping execution controls.
for b,index,want in [('8900',0,'w'),('8d00',1,'addr'),('830001',0,'rw')]:
 i=next(cs.disasm(bytes.fromhex(b),0));assert roles.op_kind(i,i.operands[index],index)==want
c=raw['cases'];assert [x['name'] for x in c]==['positive','negative','min-valid','quotient-overflow','zero-bypass-detection','private-idiv-nop']
expected=[(6,2),(-6,-2),(-2147483648,0),None,None,(-2147483648,-1)]
for x,want in zip(c,expected):
 body=bytes.fromhex('9990908bc8') if x['name']=='private-idiv-nop' else code;page=bytearray(b'\xcc'*4096);page[0xd9:0xde]=body;assert x['initial']['code_hex']==body.hex() and x['initial']['page_sha256']==sha(page) and x['final']['code_hex']==body.hex()
 a=x['initial'];z=x['final'];assert a['pc']=='0x25f0d9' and int(a['eax'],16)==x['dividend']&0xffffffff and int(a['ebx'],16)==x['divisor']&0xffffffff and a['edx']=='A5A5A5A5' and a['ecx']=='12345678';assert z['nv']==a['nv'] and z['ebx']==a['ebx'] and z['page_sha256']==a['page_sha256'] and x['memory']==[] and 'unmapped' in x['cleanup']
 if want is None:
  assert x['error']['errno']==21 and z['pc']=='0x25f0da' and z['ecx']==a['ecx'] and [v['pc'] for v in x['visits']]==['0x25f0d9','0x25f0da'];assert x['visits'][-1]['hex']=='f7fb'
 else:
  assert x['error'] is None and z['pc']=='0x25f0de' and (int(z['eax'],16),int(z['edx'],16),int(z['ecx'],16))==(want[0]&0xffffffff,want[1]&0xffffffff,want[0]&0xffffffff)
  assert [v['pc'] for v in x['visits']]==(['0x25f0d9','0x25f0da','0x25f0db','0x25f0dc'] if x['name']=='private-idiv-nop' else ['0x25f0d9','0x25f0da','0x25f0dc'])
 assert int(x['visits'][-1 if want is None else 1]['before']['edx'],16)==(0xffffffff if x['dividend']<0 else 0)
if '--fault-wraps' in sys.argv:assert c[3]['error'] is None,'Original guest IDIV overflows before quotient reaches MOV'
if '--fault-saturates' in sys.argv:assert c[3]['final']['ecx']=='7FFFFFFF','No saturated quotient is delivered by original guest slice'
if '--fault-private-also-fails' in sys.argv:assert c[5]['error'] is not None,'Private IDIV-NOP control reaches stop; setup does not cause the exception'
result=dict(status='ORIGINAL_GUEST_IDIV_QUOTIENT_OVERFLOW_BEFORE_RESULT',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=[dict(name=x['name'],dividend=x['dividend'],divisor=x['divisor'],final=x['final'],error=x['error'],cleanup=x['cleanup']) for x in c],interpretation='Three original positive controls reach MOV/stop with quotient/remainder; signedMIN/-1 reaches original IDIV then UC_ERR_EXCEPTION before MOV, same detector handles explicit zero-guard bypass. PrivateIDIVNOP same MIN/-1 reaches stop. Source original TESTEBX/JE only protects zero, so nonzero quotient-overflow register state is not intercepted by that guard. This is isolated guest evidence, not native OS exception/game crash proof.',consumer_change='Specify quotient-overflow boundary separately from zero-divisor guard; do not silently model wrap/saturation as observed original result. Preserve original instruction/entry and detector/private intervention limits; native handler/caller/authored inputs remain open.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS80 original guest positive/exception/private controls, no native/live claim',flush=True)
