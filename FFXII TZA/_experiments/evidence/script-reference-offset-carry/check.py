import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());code=(R/'pushp164.bin').read_bytes();table=(R/'scale-table24.bin').read_bytes();assert len(code)==164 and sha(code)==raw['reference']['source_sha256'];assert len(table)==24 and sha(table)==raw['reference']['table_sha256'];assert sha((R/'consumer-before.md').read_bytes())==raw['consumer']['sha256']
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'actual shared reviewed adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x268100));d={i.address:i for i in ii};assert sum(i.size for i in ii)==164 and d[0x2681a3].mnemonic=='ret'
assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ii]==[(x['pc'],x['hex'],x['mnemonic'],x['args']) for x in raw['instructions']]
expected={0x268118:('mov','r9d, dword ptr [rsp + 0x48]'),0x268120:('mov','edx, dword ptr [rsp + 0x4c]'),0x268124:('shr','r8d, 0x1c'),0x268128:('cmp','r8d, 5'),0x26812c:('ja','0x26814d'),0x26812e:('lea','r10, [rip - 0x148135]'),0x268135:('mov','ecx, dword ptr [r10 + r8*4 + 0x1481a4]'),0x26813d:('add','rcx, r10'),0x268140:('jmp','rcx'),0x268142:('add','edx, edx'),0x268144:('jmp','0x26814d'),0x268146:('lea','edx, [rdx*4]'),0x268155:('mov','r8d, r9d'),0x268158:('and','r8d, 0xffffff'),0x26815f:('and','r9d, 0x7000000'),0x268166:('add','r8d, edx'),0x268169:('or','r8d, r9d'),0x26816c:('or','r8d, 0x70000000'),0x268173:('cmp','eax, 0x3f'),0x268176:('jge','0x26819e'),0x268194:('mov','dword ptr [rbx + rcx*4 + 0x184], r8d')}
for pc,pair in expected.items():assert (d[pc].mnemonic,d[pc].op_str)==pair,(hex(pc),pair)
targets=[0x120000+n for n in struct.unpack('<6I',table)];assert targets==[0x26814d,0x26814d,0x268142,0x268142,0x268146,0x268146];assert [hex(x) for x in targets]==raw['table_targets']
assert [(i.address,i.operands[0].imm) for i in ii if i.mnemonic=='call']==[(0x268113,0x262440)]
# Closed local branches/table paths end in the single normal epilogue. The call
# is source only and deliberately not replaced with a stub or executed.
for i in ii:
 if i.mnemonic.startswith('j') and i.operands[0].type==capstone.CS_OP_IMM:assert i.operands[0].imm in d
assert [i.address for i in ii if i.mnemonic=='ret']==[0x2681a3]
assert [i.address for i in ii if 0x268155<=i.address<=0x268194 and 'r8' in roles.written(i)]==[0x268155,0x268158,0x268166,0x268169,0x26816c]
payload=d[0x268194];assert roles.op_kind(payload,payload.operands[0],0)=='w'
lea=d[0x268146];assert roles.op_kind(lea,lea.operands[1],1)=='addr'
stackread=d[0x268120];assert roles.op_kind(stackread,stackread.operands[1],1)=='r'
for x,i in zip(raw['instructions'],ii):
 assert x['written']==sorted(roles.written(i))
 assert [m['kind'] for m in x['memory']]==[roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]
assert raw['import_control']['getfile_callable'] and raw['import_control']['own_shadow_module_absent']
u32=lambda x:x&0xffffffff
def calc(desc,index,mask_after=False,force7=False):
 width=desc>>28;assert 0<=width<=5
 stride=[1,1,2,2,4,4][width]
 scaled=u32(index*stride);summed=u32((desc&0xffffff)+scaled)
 packed=(summed&0xffffff if mask_after else summed)|(desc&0x7000000)|0x70000000
 if force7:packed=(packed&0x0fffffff)|0x70000000
 return dict(descriptor=f'{desc:08X}',index=index,stride=stride,scaled_u32=f'{scaled:08X}',sum_u32=f'{summed:08X}',packed=f'{packed:08X}',decoded_class=(packed>>24)&7,decoded_width=packed>>28,float_bit=(packed>>27)&1)
cases=[calc(0x02fffffe,1),calc(0x02ffffff,1),calc(0x02000000,-1),calc(0x42000000,-1)]
assert [x['packed'] for x in cases]==['72FFFFFF','73000000','FFFFFFFF','FFFFFFFC']
assert [(x['decoded_class'],x['decoded_width'],x['float_bit']) for x in cases]==[(2,7,0),(3,7,0),(7,15,1),(7,15,1)]
alternatives=dict(final_offset_mask=calc(0x02ffffff,1,mask_after=True),force_width_exact7=calc(0x42000000,-1,force7=True))
assert alternatives['final_offset_mask']['packed']=='72000000' and alternatives['force_width_exact7']['packed']=='7FFFFFFC'
if '--fault-final-offset-mask' in sys.argv:assert cases[1]['packed']==alternatives['final_offset_mask']['packed'],'No final offset mask occurs after the ADD'
if '--fault-class-always-preserved' in sys.argv:assert all(x['decoded_class']==2 for x in cases),'Upper arithmetic bits can change the OR-combined class'
if '--fault-width-always-seven' in sys.argv:assert all(x['decoded_width']==7 for x in cases),'OR70000000 sets three bits, not exact width when bit31 arrives'
result=dict(status='PACKED_REFERENCE_CLASS_WIDTH_REQUIRE_ARITHMETIC_DOMAIN',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),conditional_calculations=cases,distinguishing_alternatives=alternatives,interpretation='PUSHP retains original class bits via OR but does not clear upper bits contributed by low32 offset+scaled index. Within24bit computed sum yields original class and width7; positive carry can set class bits, negative sum can set class/float/bit31 so width15. Calculations are not actual game references or original instruction execution.',consumer_change='Qualify class preserved and width forced7 with computed-sum domain; model literal low32ADD/OR instruction order, do not invent final24mask or exact-width replacement. Original descriptor aux-width source is separate; tag1 remains source path. Keep actual shipped input/validity/native fault/live unknowns open.',limits=raw['limits'])
if not any(x.startswith('--fault-') for x in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS76 original source/adapter/packing conditional controls; STATIC_ONLY',flush=True)
