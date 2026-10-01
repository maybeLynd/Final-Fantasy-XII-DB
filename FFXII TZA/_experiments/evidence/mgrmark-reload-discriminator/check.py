"""A only: verify the shipping indexed clear and its relation to the mark getter."""
import hashlib,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86 import X86_OP_MEM,X86_OP_REG,X86_OP_IMM,X86_REG_RIP
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();assert sha(raw)==EXE
pe=struct.unpack_from('<I',raw,0x3c)[0];opt=pe+24
base=struct.unpack_from('<Q',raw,opt+24)[0];assert base==0x120000
table=opt+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<IIII',raw,table+i*40+8) for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(va,n):
    for _,rva,size,offset in sections:
        if rva<=va-base and va-base+n<=rva+size:return raw[offset+va-base-rva:offset+va-base-rva+n]
    raise AssertionError(hex(va))
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
bodies=[];decoded={};by_addr={}
for va,n in [(0x32ED80,1001),(0x32F6E0,15),(0x332190,69)]:
    b=read(va,n);ins=list(md.disasm(b,va));assert ins and sum(i.size for i in ins)==n
    decoded[va]=ins;by_addr.update({i.address:i for i in ins})
    bodies.append(dict(address=hex(va),bytes=n,sha256=sha(b),raw=b.hex(),instructions=[
        dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]))
assert bodies[0]['sha256']=='6a3873e214cfd4ead700d942008aac232a402fde9850a9445ecdb8812d76d88f'
anchors={
 0x32ED9A:('movsxd','rdi, ecx'),0x32EDBB:('lea','r14, [rip - 0x20edc2]'),
 0x32EDC2:('xor','ebp, ebp'),0x32F107:('cmp','rdi, 5'),0x32F10B:('jae','0x32f164'),
 0x32F14B:('mov','byte ptr [rdi + r14 + 0x21a6d20], bpl'),
 0x32F153:('mov','rbp, qword ptr [rsp + 0x38]'),0x32F163:('ret',''),
 0x32F6E0:('movsxd','rax, ecx'),0x32F6E3:('lea','rcx, [rip + 0x1f97636]'),
 0x32F6EA:('movsx','eax, byte ptr [rax + rcx]'),
 0x3321BD:('mov','byte ptr [rbx + rdx], 1')}
for a,expected in anchors.items():
    i=by_addr[a];assert (i.mnemonic,i.op_str)==expected,(hex(a),i.op_str)
lea=by_addr[0x32EDBB];assert lea.operands[1].mem.base==X86_REG_RIP
image_base=lea.address+lea.size+lea.operands[1].mem.disp;assert image_base==base
getter=by_addr[0x32F6E3]
table_base=getter.address+getter.size+getter.operands[1].mem.disp;assert table_base==0x22C6D20

# Deliberately bounded to this verified body, not a general register census.
# Normal x64 callees preserve r14/rdi/rbp; native callee success is not asserted.
families={'source_zero':{'rbp','ebp','bp','bpl'},'image_base':{'r14','r14d','r14w','r14b'},'manager_index':{'rdi','edi','di','dil'}}
writes={k:[] for k in families}
for i in decoded[0x32ED80]:
    names={i.reg_name(r) for r in i.regs_access()[1]}
    for k,regs in families.items():
        if names&regs:writes[k].append(i.address)
assert [a for a in writes['source_zero'] if a<=0x32F14B]==[0x32EDC2]
assert [a for a in writes['image_base'] if a<=0x32F14B]==[0x32EDBB]
assert [a for a in writes['manager_index'] if a<=0x32F14B]==[0x32ED9A]

def target(i,m):
    assert i.mnemonic=='mov' and i.operands[0].type==X86_OP_MEM
    op=i.operands[0];mem=op.mem
    regs={'r14':image_base,'rdi':m}
    return regs[i.reg_name(mem.base)]+regs[i.reg_name(mem.index)]*mem.scale+mem.disp,op.size
def require_mark(i):
    assert i.operands[1].type==X86_OP_REG and i.reg_name(i.operands[1].reg)=='bpl'
    for m in range(5):assert target(i,m)==(table_base+m,1)
require_mark(by_addr[0x32F14B])
neg=[]
for a,label in [(0x32F10D,'neighbor byte table22C6D18'),(0x32F0FF,'qword pending masks22C6E48')]:
    try:require_mark(by_addr[a])
    except AssertionError:neg.append(label)
    else:raise AssertionError('wrong target accepted')
assert len(neg)==2
destinations=[dict(manager=m,address=hex(target(by_addr[0x32F14B],m)[0]),bytes=1,source=0) for m in range(5)]
assert destinations[1]['address']!=hex(table_base+8)

# Local CFG: calls return to their following instruction. The range-failure call
# at the catalog end has no successor in this body; no native failure is executed.
insmap={i.address:i for i in decoded[0x32ED80]}
edges={}
for a,i in insmap.items():
    nxt=a+i.size
    if i.mnemonic=='ret':edges[a]=[]
    elif i.group(capstone.CS_GRP_JUMP):
        assert i.operands[0].type==X86_OP_IMM
        edges[a]=[i.operands[0].imm]+([] if i.mnemonic=='jmp' else [nxt])
    else:edges[a]=[nxt] if nxt in insmap else []
def reachable_without(skip):
    seen=set();todo=[0x32ED80]
    while todo:
        a=todo.pop()
        if a==skip or a in seen:continue
        assert a in insmap;seen.add(a);todo.extend(edges[a])
    return sorted(seen)
ret=0x32F163
assert [a for a,i in insmap.items() if i.mnemonic=='ret']==[ret]
assert ret in reachable_without(None)
assert ret not in reachable_without(0x32F14B)
assert ret in reachable_without(0x32F139) # nullable resource: optional clear
for a in (0x32ED9A,0x32EDBB,0x32EDC2,0x32F107,0x32F10B):
    assert ret not in reachable_without(a),hex(a)

prior_path=ROOT/'Database/FFXII TZA/_experiments/evidence/spawn-pending-latch/primary.json'
prior=json.loads(prior_path.read_text());old=next(b for b in prior['bodies'] if int(b['address'],16)==0x32ED80)
assert old['sha256']==bodies[0]['sha256'] and ''.join(i['bytes'] for i in old['instructions'])==bodies[0]['raw']
source=HERE/'sources/opus-blockclear.py'
assert source.is_file()
out=dict(status='POSITIVE_STATIC_COUNTEREXAMPLE_PENDING_CONSUMERS',method='A',live_game=False,
         executable_sha256=EXE,capstone_version=capstone.__version__,bodies=bodies,
         checker_sha256=sha(Path(__file__).read_bytes()),python_version=sys.version,
         store=hex(0x32F14B),table_base=hex(table_base),image_base=hex(image_base),width=1,
         index='sign-extended ecx; normal tail guarded by unsigned rdi <5',destinations=destinations,
         local_register_writers={k:[hex(a) for a in v] for k,v in writes.items()},
         cfg=dict(edges={hex(a):[hex(b) for b in v] for a,v in edges.items()},
                  explicit_normal_return=hex(ret),baseline_reaches_return=True,
                  without_clear_reaches_return=False,without_optional_resource_clear_reaches_return=True,
                  setup_and_guard_dominate_return=[hex(a) for a in (0x32ED9A,0x32EDBB,0x32EDC2,0x32F107,0x32F10B)],
                  assumption='Direct local CFG with returning callees; no proof that cleanup succeeds'),
         rejected_wrong_targets=neg,
         prior_primary=dict(path=str(prior_path.relative_to(ROOT)),sha256=sha(prior_path.read_bytes()),same_original_body=True),
         historical_bulk_filter=dict(source='Database/Tools/work/OPUS/blockclear.py',retained='sources/opus-blockclear.py',sha256=sha(source.read_bytes()),
                                     scope='RIP-based bulk rep-stos or3argument fills; scalar image-base indexed byte stores excluded'),
         limits=['No native or live execution; no lifetime, scheduling or loaded-state observation.',
                 'Nonvolatile-register preservation and returning cleanup callees are preconditions of normal-return analysis.',
                 'The valid-index guard is late and does not protect earlier indexed accesses.',
                 'Counterexample refutes the universal absence/sticky premise, not every narrow search result.',
                 'The gate fixture does not gain coverage of a reset it does not execute.'])
(HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: original0032F14B clears mark022C6D20+m; getter confirms base/byte-width/stride.')
print('All5valid index addresses;2wrong-table controls rejected; clear dominates explicit normal return under stated ABI/call-return limits.')
print('Same1001-byte reset body already retained in spawn-pending-latch; no B/C run.')
