import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'compare413.bin').read_bytes();assert len(code)==413 and sha(code)==raw['reference']['source_sha256'];assert sha((R/'executed-capture-before-checker-preflight.py').read_bytes())==raw['driver_sha256']
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'actual shared reviewed adapter','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;original={i.address:i for i in cs.disasm(code,0x25d740)};assert sum(i.size for i in original.values())==413
for x,i in zip(raw['instructions'],original.values()):
 assert (x['pc'],x['hex'],x['mnemonic'],x['args'])==(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)
 assert [m['kind'] for m in x['memory']]==[roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]
for pc,mn,op in [(0x25d74f,'mov','edi, 1'),(0x25d793,'movss','xmm7, dword ptr [rbx + rdx*4 + 0x184]'),(0x25d892,'movss','xmm6, dword ptr [rbx + rdx*4 + 0x184]'),(0x25d8b2,'ucomiss','xmm6, xmm7'),(0x25d8b5,'jp','0x25d8d0'),(0x25d8b7,'jne','0x25d8d0'),(0x25d8d3,'comiss','xmm7, xmm6'),(0x25d8d6,'cmova','edi, eax'),(0x25d8d9,'mov','eax, edi')]:assert (original[pc].mnemonic,original[pc].op_str)==(mn,op)
assert [i.address for i in original.values() if i.mnemonic=='ret']==[0x25d853,0x25d8cf]
expected=[('ordered-less','3F800000','40000000',-1),('ordered-equal','3F800000','3F800000',0),('ordered-greater','40000000','3F800000',1),('nan-left','7FC12345','3F800000',1),('nan-right','3F800000','7FC12345',1),('nan-self','7FC12345','7FC12345',1),('private-jp-nop','7FC12345','3F800000',0)]
assert len(raw['cases'])==len(expected)==7
for c,e in zip(raw['cases'],expected):
 assert (c['name'],c['left_bits'],c['right_bits'],c['result_signed'])==e
 a=c['initial'];b=c['final'];ram=bytes.fromhex(a['ram']);assert a['rcx']=='0x40000100' and a['rsp']=='0x60001808' and a['mxcsr']=='0x1f80' and a['eflags']=='0x2'
 assert struct.unpack_from('<i',ram,0x100)[0]==2 and ram[0x104:0x106]==b'\x02\x02' and [f'{v:08X}' for v in struct.unpack_from('<II',ram,0x284)]==[c['left_bits'],c['right_bits']]
 want=bytearray(ram);struct.pack_into('<i',want,0x100,0);assert bytes.fromhex(b['ram'])==bytes(want);assert b['pc']=='0x60000200' and b['rsp']=='0x60001810' and b['nonvolatile']==a['nonvolatile'] and b['code_sha256']==a['code_sha256']
 mutant=c['name']=='private-jp-nop';body=bytearray(code)
 if mutant:body[0x175:0x177]=b'\x90\x90'
 assert a['code_sha256']==sha(body);dd={i.address:i for i in cs.disasm(body,0x25d740)};vis=[int(v['pc'],16) for v in c['visits']];assert len(vis)<=128 and vis[0]==0x25d740 and vis[-1]==0x25d8cf and not any(dd[v].mnemonic=='call' for v in vis)
 for v in c['visits']:assert dd[int(v['pc'],16)].bytes.hex()==v['hex']
 assert [int.from_bytes(bytes.fromhex(w['hex']),'little') for w in c['writes'] if w['address']=='0x40000100']==[1,0]
 assert {r['address'] for r in c['reads']} >= {'0x40000100','0x40000104','0x40000105','0x40000284','0x40000288'}
 frame=bytearray.fromhex(a['frame']);frame_lo=0x60001808-0x48
 for w in c['writes']:
  addr=int(w['address'],16);size=w['size'];value=bytes.fromhex(w['hex']);assert len(value)==size
  if addr!=0x40000100:
   assert frame_lo<=addr and addr+size<=0x60001828;frame[addr-frame_lo:addr-frame_lo+size]=value
 assert bytes(frame)==bytes.fromhex(b['frame']) and struct.unpack_from('<Q',frame,0x48)[0]==0x60000200
 if c['name'].startswith('nan-'):
  assert 0x25d8d0 in vis and 0x25d8b9 not in vis
  for pc in [0x25d8b5,0x25d8d6]:assert int(next(v['eflags'] for v in c['visits'] if int(v['pc'],16)==pc),16)&0x45==0x45,'Guest unordered flags detection failed'
 if mutant:assert 0x25d8b9 in vis and 0x25d8d0 not in vis
 assert c['cleanup'].startswith('All three disposable guest mappings unmapped')
table=(R/'consumer-table24.bin').read_bytes();assert sha(table)==raw['reference']['table_sha256'];targets=[0x120000+n for n in struct.unpack('<6I',table)];assert targets==list(range(0x25ea18,0x25eaa8,24))
conditions=['sete','setne','setg','sets','setns','setle'];decisions=[]
for j,c in enumerate(raw['consumers']):
 p=R/f'consumer-{j+10:02x}.bin';b=p.read_bytes();assert len(b)==24 and sha(b)==c['sha256'];ii=list(cs.disasm(b,targets[j]));assert sum(i.size for i in ii)==24
 assert [i.mnemonic for i in ii]==['mov','call','xor','test','mov',conditions[j],'jmp']
 assert [(ii[0].op_str),(ii[1].op_str),(ii[3].op_str),(ii[5].op_str),(ii[6].op_str)]==['rcx, r10','0x25d740','eax, eax','cl','0x25e68f']
 assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ii]==[(x['pc'],x['hex'],x['mnemonic'],x['args']) for x in c['instructions']]
 decisions.append(dict(opcode=f'{j+10:02X}',condition=conditions[j],cl_from_result_plus_one=[0,1,1,0,1,0][j],method='A source TEST EAX/SETcc decision, not interpreter execution/shared push observation'))
if '--fault-unordered-is-equal' in sys.argv:assert all(c['result_signed']==0 for c in raw['cases'][3:6]),'Original masked qNaN compare returns +1, not equality'
if '--fault-unordered-is-negative' in sys.argv:assert all(c['result_signed']==-1 for c in raw['cases'][3:6]),'Original masked qNaN compare keeps EDI +1'
if '--fault-jp-control-unchanged' in sys.argv:assert raw['cases'][6]['result_signed']==raw['cases'][3]['result_signed'],'Private JP removal changes unordered result to zero'
result=dict(status='MASKED_QNAN_COMPARE_RETURNS_PLUS_ONE_WITH_SOURCE_BOOLEAN_CONSEQUENCES',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=[dict(name=c['name'],left_bits=c['left_bits'],right_bits=c['right_bits'],result=c['result_signed'],depth_after=0) for c in raw['cases']],source_consumer_decisions=decisions,interpretation='Original complete comparator on tested depth2/tag2/masked guest states returns -1/0/+1 for ordered finite controls and +1 for qNaN left/right/self, popping both operands. JP keeps unordered away from equality; COMISS unordered does not select CMOVA, EDI stays1. Six source boolean decision bytes for +1 are EQ0/NE1/GT1/LS0/GTE1/LSE0; common push/interpreter execution not observed.',consumer_change='Preserve ordered versus unordered behavior and masked/guest boundaries in comparator contract/spec; avoid substituting host IEEE relational operators whose NaN greater/ge results differ. Original same-qNaN comparison is not equality under these conditions; actual shipped NaNs/native flags/caller reachability remain open.',limits=raw['limits'])
if not any(x.startswith('--fault-') for x in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS77 retained original comparator returns/pops/guards/control plus STATIC_ONLY consumers',flush=True)
