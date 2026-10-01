import hashlib,json,struct
from pathlib import Path
import capstone
from unicorn.x86_const import UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_RSP,UC_X86_REG_RBX,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_MXCSR
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest();r=json.loads((W/'raw.json').read_text());ref=r['reference'];code=(W/'retained/source.bin').read_bytes()
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and ref['entry']=='0x866a00' and ref['bytes']==len(code)==116 and ref['body_sha256']==sha(code)
assert r['driver_sha256']==sha((W/'capture.py').read_bytes()) and ref['reader_sha256']==sha((W/'retained/shipping-reader.py').read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x866A00));assert sum(i.size for i in ins)==116 and not any(i.mnemonic=='call' for i in ins)
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins]
ii={i.address:i for i in ins}
for pc,b in [(0x866A3D,'418b09'),(0x866A44,'7316'),(0x866A4D,'4188143a'),(0x866A54,'41ff01'),(0x866A5A,'7cd4'),(0x866A64,'0f94c3')]:assert ii[pc].bytes.hex()==b
for pc,addr in [(0x866A30,0x1F44D48),(0x866A36,0x1F44D40)]:assert pc+ii[pc].size+ii[pc].operands[-1].mem.disp==addr
assert [c['name'] for c in r['cases']]==['one-byte-disjoint-control','one-byte-cursor-alias','two-byte-disjoint-control','two-byte-cursor-alias-feedback','zero-count-alias-no-copy-control']
assert len(r['tools']['binaries'])==2 and {x['name'] for x in r['tools']['binaries']}=={'capstone','unicorn'} and all(x['bytes']>0 and len(x['sha256'])==64 for x in r['tools']['binaries'])
for c in r['cases']:
 n=c['count'];alias=c['alias'];target=0x40002000 if alias else 0x40003000;a=c['after'];s=c['initial'];copied=min(n,1) if alias else n
 regs=[(UC_X86_REG_RCX,0x40002000),(UC_X86_REG_RDX,target),(UC_X86_REG_R8,n),(UC_X86_REG_RSP,0x60001808),(UC_X86_REG_RBX,0x1122334455667788),(UC_X86_REG_RSI,0x2233445566778899),(UC_X86_REG_RDI,0x33445566778899AA),(UC_X86_REG_MXCSR,0x1F80)]
 assert s['registers']=={str(k):hex(v) for k,v in regs} and s['cursor']=='00000000' and s['destination']==('00000000' if alias else 'a5'*4) and s['disjoint_destination']=='a5'*8 and s['source']=='0a14283c' and s['global_vector']==struct.pack('<QQ',0x40004000,0x40004004).hex()
 assert s['stack']==(b'\0'*8+struct.pack('<Q',0x70000000)+b'\0'*24).hex()
 assert c['error'] is None and a['rip']=='0x70000000' and a['rsp']=='0x60001810' and c['visited'][0]=='0x866a00' and c['visited'][-1]=='0x866a6f' and 0<len(c['visited'])<128 and all(int(p,16) in ii for p in c['visited'])
 assert a['nonvolatile']=={str(k):hex(v) for k,v in regs if k in (UC_X86_REG_RBX,UC_X86_REG_RSI,UC_X86_REG_RDI)} and a['source']==s['source'] and a['global_vector']==s['global_vector']
 expected_cursor=11 if alias and n else n;assert a['cursor']==struct.pack('<I',expected_cursor).hex() and a['eax']==(0 if alias and n==2 else 1)
 expected=[dict(pc='0x866a00',address='0x60001800',bytes=struct.pack('<Q',0x33445566778899AA).hex()),dict(pc='0x866a12',address='0x60001810',bytes=struct.pack('<Q',0x1122334455667788).hex()),dict(pc='0x866a19',address='0x60001818',bytes=struct.pack('<Q',0x2233445566778899).hex())]
 for j in range(copied):expected += [dict(pc='0x866a4d',address=hex(target+j),bytes=['0a','14'][j]),dict(pc='0x866a54',address='0x40002000',bytes=struct.pack('<I',11 if alias else j+1).hex())]
 assert c['writes']==expected and len(c['raw_writes'])==len(expected)
 for x,y in zip(c['raw_writes'],expected):assert x['pc']==y['pc'] and x['address']==y['address'] and x['size']==len(bytes.fromhex(y['bytes'])) and isinstance(x['provider_value'],int)
 cursor_reads=[x['bytes'] for x in c['reads'] if x['pc']=='0x866a3d'];assert cursor_reads==(['00000000','0b000000'] if alias and n==2 else (['00000000','01000000'] if n==2 else ['00000000'] if n==1 else []))
 source_reads=[x for x in c['reads'] if x['pc']=='0x866a46'];assert source_reads==[dict(pc='0x866a46',address=hex(0x40004000+j),bytes=['0a','14'][j]) for j in range(copied)]
 if alias:assert a['destination']==a['cursor'] and a['disjoint_destination']==s['disjoint_destination']
 else:assert a['destination']==bytes.fromhex('0a14283c')[:n].hex()+'a5'*(4-n) and a['disjoint_destination']==a['destination']+'a5'*4
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_ORIGINAL_LEAF alias-count1 returns1/cursor11/dest0B; alias-count2 reloads11/shortreturns0; disjoint1/2 and zero control; exact state/ABI/source/read/write/stop; no save/native/live corruption proof')
