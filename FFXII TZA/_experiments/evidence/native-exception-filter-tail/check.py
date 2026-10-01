import sys
sys.dont_write_bytecode=True
import hashlib,json,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'filter240.bin').read_bytes();assert len(code)==240 and sha(code)==raw['reference']['code_sha256']
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
assert sha((R/'consumer-primary.md').read_bytes())==raw['reference']['consumer_sha256']
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed access policy','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x79ad50));assert sum(i.size for i in ii)==240 and ii[-1].address==0x79ae3f and ii[-1].mnemonic=='ret'
for i,row in zip(ii,raw['instructions']):
 assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(row['pc'],row['hex'],row['mnemonic'],row['args'])
 assert sorted(roles.written(i))==row['written'] and [roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]==row['memory']
assert len(ii)==len(raw['instructions'])
for b,index,want in [('8900',0,'w'),('8d00',1,'addr'),('830001',0,'rw')]:
 i=next(cs.disasm(bytes.fromhex(b),0));assert roles.op_kind(i,i.operands[index],index)==want
by={i.address:i for i in ii};branches={i.address:i.operands[0].imm for i in ii if i.mnemonic.startswith('j')};assert branches=={0x79ad77:0x79ae35,0x79adf7:0x79ae09}
assert code[0x79ae35-0x79ad50:0x79ae3a-0x79ad50].hex()=='b801000000'
imports={int(r['slot'],16):r for r in raw['imports']};slots={i.address+i.size+i.operands[0].mem.disp for i in ii if i.mnemonic=='call' and i.operands[0].type==capstone.CS_OP_MEM};assert set(imports)==slots and len(imports)==8
for slot,dll,symbol,ordinal in [(0x8c21b8,'KERNEL32.dll','GetCurrentProcess',None),(0x8c21d8,'KERNEL32.dll','GetCurrentThreadId',None),(0x8c2278,'KERNEL32.dll','GetProcessId',None),(0x8c23e0,'KERNEL32.dll','CloseHandle',None),(0x8c28c0,'USER32.dll','ShowCursor',None),(0x8c29c0,'USER32.dll','MessageBoxW',None),(0x8c27c8,'OLEAUT32.dll',None,6),(0x8c27d0,'OLEAUT32.dll',None,4)]:
 r=imports[slot];assert (r['dll'],r['symbol'],r['ordinal'])==(dll,symbol,ordinal)
 v=int.from_bytes(bytes.fromhex(r['lookup_hex']),'little');assert ((v>>63)!=0)==(ordinal is not None)
 if ordinal is not None:assert v==0x8000000000000000|ordinal
 assert bytes.fromhex(r['dll_hex']).decode('ascii')==dll+'\0'
# Calls/arguments from exact instructions, no API or interpreter simulation.
for pc,want in [(0x79ade0,'b937780000'),(0x79adf9,'0fb710'),(0x79adfc,'488d4802'),(0x79ae09,'b901000000'),(0x79ae14,'41b910000000'),(0x79ae21,'488bd3'),(0x79ae24,'33c9'),(0x79ae2c,'488bcb')]:assert by[pc].bytes.hex()==want
assert by[0x79ade5].operands[0].imm==0x19a510
assert by[0x79ae1a].address+by[0x79ae1a].size+by[0x79ae1a].operands[1].mem.disp==0x8f3dc0
caption=(R/'caption.bin').read_bytes();assert caption.hex()==raw['caption']['hex'] and caption[-2:]==b'\0\0' and caption[:-2].decode('utf-16le')==raw['caption']['utf16']
paths=[]
for supplied in raw['local_paths']:
 pc=0x79ad50;visits=[];calls=[]
 while True:
  assert pc in by and len(visits)<100;i=by[pc];visits.append(hex(pc))
  if i.mnemonic=='call':calls.append(hex(pc))
  if i.mnemonic=='ret':break
  pc=branches[pc] if pc in branches and supplied['branches'][hex(pc)] else pc+i.size
 assert '0x79ae35' in visits and visits[-1]=='0x79ae3f'
 paths.append(dict(condition=supplied['condition'],visits=visits,calls=calls,local_return=1,assumption='Each encountered call returns normally; branch inputs supplied for source calculation, no execution'))
assert paths[0]['calls']==['0x79ad59']
assert '0x79ae00' not in paths[1]['calls'] and '0x79ae00' in paths[2]['calls']
assert all(p['calls'].index('0x79ade5')<p['calls'].index('0x79ae0e')<p['calls'].index('0x79ae26')<p['calls'].index('0x79ae2f') for p in paths[1:])
if '--fault-return-zero' in sys.argv:assert all(p['local_return']==0 for p in paths),'Original local RET is preceded by MOV EAX,1'
if '--fault-cursor-before-text' in sys.argv:assert paths[2]['calls'].index('0x79ae0e')<paths[2]['calls'].index('0x79ade5'),'Original text request precedes cursor call'
if '--fault-name-ordinal' in sys.argv:assert imports[0x8c27c8]['symbol'] is not None,'Ordinal identity is not a captured import-by-name'
result=dict(status='STATIC_FILTER_TAIL_RETURN_ONE_WITH_CONDITIONAL_MESSAGEBOX',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),paths=paths,caption=raw['caption'],interpretation='Original local gate-zero path skips dump/message tail; enabled returning paths request text7837 before ShowCursor1, then call MessageBoxW(HWND0, RBXtext, caption8F3DC0, flags0x10), then OLEAUT32 ordinal6 with RBX and converge on MOV EAX1/RET. Nonnull text sends its leading u16 and pointer+2 to ordinal4; returned pointer becomes RBX. Null text path retains RBXzero. DLL/ordinal identity is source evidence, callback names/effects unproved.',consumer_change='Replace unread CV3 tail with exact source order/ABI/conditional return1. Do not infer actual message rendering, OS dispatch, universal gate state, native termination or EXP127 cause.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS81 static local CFG/import/ABI/order controls; callbacks/native/live unexecuted',flush=True)
