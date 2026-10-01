import hashlib,json,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['access_adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def decode(b,pc):return [dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,reads=sorted(set(roles.canon(i.reg_name(r)) for r in i.regs_access()[0])),writes=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in cs.disasm(b,pc)]
for name,key,pc,n in [('lookup32.bin','lookup',0x32f240,32),('caller30.bin','caller',0x267f1e,30),('store-prefix23.bin','store_prefix',0x26d530,23)]:
 b=(R/name).read_bytes();assert len(b)==n and sha(b)==raw['reference'][key]['sha256'] and decode(b,pc)==raw[key]
look=(R/'lookup32.bin').read_bytes();ll={i.address:i for i in cs.disasm(look,0x32f240)};todo=[0x32f240];seen=set();rets=[]
while todo:
 pc=todo.pop()
 if pc in seen:continue
 assert pc in ll;seen.add(pc);i=ll[pc]
 if i.mnemonic=='ret':rets.append(pc);continue
 assert i.mnemonic not in ['call','jmp'],'Closed original lookup has no callback/indirect boundary'
 if i.mnemonic.startswith('j'):assert i.operands[0].type==capstone.CS_OP_IMM;todo.append(i.operands[0].imm)
 todo.append(pc+i.size)
assert seen==set(ll) and sorted(rets)==[0x32f25b,0x32f25f] and sum(i.size for i in ll.values())==32
assert ll[0x32f240].op_str=='rax, ecx' and ll[0x32f243].address+ll[0x32f243].size+ll[0x32f243].operands[1].mem.disp==0x120000
assert ll[0x32f24a].mnemonic=='cmp' and ll[0x32f24a].operands[0].mem.disp==0x21a6d18 and ll[0x32f252].operands[0].imm==0x32f25c
assert ll[0x32f254].mnemonic=='mov' and ll[0x32f254].op_str=='eax, dword ptr [rcx + rax*4 + 0x21a6d28]' and ll[0x32f25c].op_str=='eax, 0xffffffff'
touch=[x for x in raw['lookup'] if x['memory'] and x['mnemonic']!='lea'];assert len(touch)==2 and all(x['memory'][0]['kind']=='r' for x in touch)
cc={i.address:i for i in cs.disasm((R/'caller30.bin').read_bytes(),0x267f1e)}
for pc,m,a in [(0x267f1e,'mov','ecx, dword ptr [rdi + 0x28]'),(0x267f21,'lea','eax, [rcx - 1]'),(0x267f24,'cmp','eax, 2'),(0x267f27,'ja','0x267f32'),(0x267f29,'test','esi, esi'),(0x267f2b,'jne','0x267f32'),(0x267f2d,'call','0x32f240'),(0x267f32,'lea','rcx, [rsp + 0x30]'),(0x267f37,'call','0x26d530')]:assert (cc[pc].mnemonic,cc[pc].op_str)==(m,a)
prefix=(R/'store-prefix23.bin').read_bytes();st=list(cs.disasm(prefix,0x26d530));assert st[3].address==0x26d53b and st[3].op_str=='eax, dword ptr [r9 + 0x18]'
def incoming_read_before_overwrite(instructions):
 for i in instructions:
  rr={roles.canon(i.reg_name(r)) for r in i.regs_access()[0]}
  if 'rax' in rr:return True
  if 'rax' in roles.written(i):return False
 raise AssertionError('No discriminating RAX boundary')
assert not incoming_read_before_overwrite(st) and 'rax' not in raw['caller'][-2]['reads'],'Returned EAX unused before original full EAX overwrite'
# Private decoded-only witnesses make the negative-source detectors observable.
mut=bytearray(look);mut[0x32f254-0x32f240]=0x89;mi=next(cs.disasm(bytes(mut[0x32f254-0x32f240:]),0x32f254));assert mi.mnemonic=='mov' and mi.operands[0].type==capstone.CS_OP_MEM and roles.op_kind(mi,mi.operands[0],0)=='w'
z=bytearray(prefix);z[0x26d53b-0x26d530:0x26d53f-0x26d530]=b'\x90'*4;assert incoming_read_before_overwrite(list(cs.disasm(z,0x26d530)))
if '--fault-lookup-emits-write' in sys.argv:assert any(x['memory'][0]['kind'] in ['w','rw'] for x in touch),'Read-only original lookup has no event write'
if '--fault-return-used' in sys.argv:assert incoming_read_before_overwrite(st),'Original store overwrites lookup return before use'
if '--fault-disable-write-detector' in sys.argv:assert roles.op_kind(mi,mi.operands[0],0)=='r','Private load-to-store is detected as a write'
result=dict(status='POPV_LOOKUP_READ_ONLY_RETURN_DISCARDED',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=dict(lookup_closed_pcs=[hex(p) for p in sorted(seen)],returns=[hex(p) for p in sorted(rets)],tables=dict(registered_byte='0x22c6d18+i',id_dword='0x22c6d28+4*i'),source_writes=0,source_calls=0,registered_result='selected table id',unregistered_result='FFFFFFFF',caller_gate='uint32(slot_index-1)<=2 and ESI==0',continuation='LEA RCX record thenCALL26D530; no returnedEAXread',store_clobber='26D53B MOV EAX,record.descriptor before anyRAXread',controls=dict(decoded_private_load_to_store='w',decoded_private_store_firstclobberNOP='incoming RAXread becomesvisible'),effects='Two ordinary globalreads/return, no source event dispatch/write/call. ReturnunusedonthisPOPV path; may fault if required memoryinvalid, notobservedhere'),interpretation='For this exact shipping local source path, notification helper is a registration/id query, not an emitting callback, and its returned id is discarded before storing. Narrow70 former omitted-helper uncertainty accordingly via additive evidence, not rawrewrite. Preserve actual data validity/other notification systems andlivegaps.',limits='STATIC_ONLY. No original-code/guest/native/live execution, actual tablevalues/writer/globalvalidity/nativefaults/normalreachability/othercallbacks/lifetime. Claims conditioned validordinarymemory andcorrect32B/sourceidentity; no no-fault guarantee. Consumer incorporation/independentacceptance pending. PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS71 original read-only lookup and discarded return; static only',flush=True)
