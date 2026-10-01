"""A: validate the owner/pool identity before designing a register-reuse test."""
import hashlib,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86 import X86_OP_MEM,X86_REG_RIP
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();assert sha(raw)==EXE
pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24
assert raw[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',raw,opt)[0]==0x20b
base=struct.unpack_from('<Q',raw,opt+24)[0];assert base==0x120000
table=opt+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<IIII',raw,table+40*i+8) for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(va,n):
    assert n>0
    for _,v,z,f in sections:
        if v<=va-base and va-base+n<=v+z:return raw[f+va-base-v:f+va-base-v+n]
    raise AssertionError(hex(va))
sizes={0x2679f0:436,0x26ce60:1332,0x358940:30,0x2628b0:1689,
       0x25b070:473,0x3697f0:13,0x369860:1009,0x25df00:1228,0x25e4c0:55}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
bodies={};insmap={};decoded={}
for a,n in sizes.items():
    r=read(a,n);ins=list(md.disasm(r,a));assert ins and sum(i.size for i in ins)==n
    decoded[a]=ins;insmap.update({i.address:i for i in ins})
    bodies[f'{a:08X}']=dict(bytes=n,sha256=sha(r),raw_hex=r.hex(),
      extent='entry prefix only; full interpreter is14646bytes' if a==0x25e4c0 else 'complete catalog body',
      instructions=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins])
anchors={
 0x267a79:('call','qword ptr [r15 + 0x88]'),0x267a83:('xor','edx, edx'),
 0x267a88:('mov','r14, rax'),0x267a8b:('call','0x861ec0'),
 0x267aa8:('mov','qword ptr [r15 + 0x1f0], rcx'),
 0x267af5:('mov','qword ptr [r14 + rax*8 + 8], rdx'),
 0x267b79:('call','0x266530'),0x267b89:('mov','rax, r14'),
 0x26ce7e:('imul','rbx, r12, 0x288'),0x26ceb0:('call','0x2679f0'),
 0x26ceb8:('mov','qword ptr [rbx + 8], rax'),
 0x358940:('mov','r8, qword ptr [rcx + 8]'),0x358955:('mov','rax, qword ptr [r8 + rax*8 + 8]'),
 0x2628dd:('imul','rbx, rdi, 0x288'),0x262d34:('call','0x25b070'),
 0x262d96:('mov','rcx, qword ptr [rbx + 8]'),0x262d9d:('je','0x262da8'),
 0x262d9f:('call','0x3697f0'),0x262da4:('mov','qword ptr [rbx + 8], rbp'),
 0x262da8:('and','byte ptr [rbx + 0x10], 0xfe'),
 0x3697f5:('xor','edx, edx'),0x3697f7:('jmp','0x369860'),
 0x3698c1:('lea','rbx, [rcx - 0x40]'),0x3698d5:('cmp','word ptr [rbx], ax'),
 0x25e0cd:('mov','rdx, rdi'),0x25e0d0:('mov','rcx, r15'),
 0x25e0d3:('call','0x25e4c0'),0x25e4d5:('mov','r15, rdx')}
for a,want in anchors.items():
    i=insmap[a];assert (i.mnemonic,i.op_str)==want,(hex(a),i.op_str)
def rip(a,n):
    i=insmap[a];op=i.operands[n];assert op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP
    return i.address+i.size+op.mem.disp
assert rip(0x26ce74,1)==rip(0x2628d6,1)==0x2098e10
# Do not assume the zero-source from a symbolic name: verify its local writers.
writes=[i for i in decoded[0x2628b0] if i.address<=0x262da4 and
        {'rbp','ebp','bp','bpl'} & {i.reg_name(r) for r in i.regs_access()[1]}]
assert len(writes)==1 and writes[0].mnemonic=='xor' and writes[0].op_str=='ebp, ebp'
assert insmap[0x262da4].operands[0].size==8
owner_writes=[i.address for i in decoded[0x2628b0] if i.address<=0x262da4 and
              {'rbx','ebx','bx','bl','bh'} & {i.reg_name(r) for r in i.regs_access()[1]}]
assert owner_writes==[0x2628dd,0x2628e9]
# Local CFG with returning calls: the zero source cannot be bypassed on a path
# to this store. This is not a claim that arbitrary native cleanup calls return.
bodymap={i.address:i for i in decoded[0x2628b0]}
def reaches_store(skip):
    todo=[0x2628b0];seen=set()
    while todo:
        a=todo.pop()
        if a==skip or a in seen:continue
        assert a in bodymap;seen.add(a)
        if a==0x262da4:return True
        i=bodymap[a];nxt=a+i.size
        if i.mnemonic=='ret':continue
        if i.group(capstone.CS_GRP_JUMP):
            todo.append(i.operands[0].imm)
            if i.mnemonic=='jmp':continue
        if nxt in bodymap:todo.append(nxt)
    return False
assert reaches_store(None) and not reaches_store(writes[0].address)
# Wrong-root controls: +1F0 is a derived pointer; record->secondaryContext is not
# the owner->recordPool. The real getter and release both use owner+08.
assert insmap[0x267aa8].operands[0].mem.disp!=insmap[0x262d96].operands[1].mem.disp
assert insmap[0x358940].operands[1].mem.disp==insmap[0x262d96].operands[1].mem.disp==8
out=dict(method='A, shipping instructions; no execution or live observation',executable_sha256=EXE,
         capstone_version=capstone.__version__,bodies=bodies,
         normalized=dict(manager_base='02098E10',manager_stride='288',owner_pool_offset='08',
                         table_header=8,record_pointer_stride=8,derived_region_offset='1F0',
                         owner_pool_publish='0026CEB8',owner_pool_release_call='00262D9F',
                         owner_pool_null_store='00262DA4',zero_source_instruction=hex(writes[0].address),
                         release_thunk='003697F0 ->00369860',interpreter_record_argument='RDX -> R15',
                         cleanup_and_allocation_release_are_separate=True),
         controls=dict(same_manager_array_in_producer_and_unload=True,
                       getter_and_release_same_owner_offset=True,derived_pointer_rejected_as_root=True,
                       zero_source_verified_locally=True),
         limits=['Valid native state and normally returning callees are required; no allocator success or session health is asserted.',
                 'No in-pool logical actor reuse, register inheritance or first-read timing observed.',
                 'Equal endpoint addresses cannot rule out release/reallocation between samples.',
                 'The 55-byte interpreter prefix proves argument placement only, not all interpreter accesses.',
                 '0025B070 can remain a semantic cleanup/dtor entry; it is not the separate owner allocation-release site.'])
p=HERE/'observation.json'
if '--write' in sys.argv:
    assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n')
else:assert json.loads(p.read_text())==out
print('PASS: allocation result, table getter and unload all agree on manager+08 root.')
print('PASS: unload sends that root through003697F0->00369860 and then nulls it; +1F0 is not the root.')
print('PASS: interpreter record argument anchored; no actual register-reuse/lifetime observation claimed.')
print('PASS: owner base has only its setup writes; zero source dominates the null store under local returning-call analysis.')
