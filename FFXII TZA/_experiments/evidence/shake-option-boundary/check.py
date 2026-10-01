"""Method A: pin the Screen Shake option's actual output-copy boundary."""
import hashlib,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86 import X86_OP_MEM,X86_OP_IMM,X86_REG_RIP
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
sizes={0x2de200:34,0x2ddd60:16,0x37ddc0:7,0x37d7f0:158,
       0x37d970:245,0x237420:13,0x358320:8,0x37d4c0:808,
       0x37db70:7,0x3dd220:5,0x37d1f0:712,0x3dcfb0:285,0x314370:85}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
bodies={};instructions={};decoded={}
for va,n in sizes.items():
    b=read(va,n);ins=list(md.disasm(b,va));assert ins and sum(i.size for i in ins)==n
    decoded[va]=ins;instructions.update({i.address:i for i in ins})
    bodies[f'{va:08X}']=dict(bytes=n,sha256=sha(b),raw_hex=b.hex(),
                           disassembly=[f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins])
def anchor(a,mn,op):
    i=instructions[a];assert (i.mnemonic,i.op_str)==(mn,op),(hex(a),i.op_str)
def rip(a,operand=0):
    i=instructions[a];m=i.operands[operand];assert m.type==X86_OP_MEM and m.mem.base==X86_REG_RIP
    return i.address+i.size+m.mem.disp
anchor(0x2de207,'and','ecx, 1');anchor(0x2de20a,'shl','ecx, 0xe')
anchor(0x2de21d,'jmp','0x37ddc0');anchor(0x37ddc0,'mov','dword ptr [rip + 0x2b415fe], ecx')
assert rip(0x2de200,1)==rip(0x2ddd60,1)==0x215e6e0
flag=rip(0x37ddc0);assert flag==0x2ebf3c4
assert rip(0x37d80a)==rip(0x37d9ff)==flag
anchor(0x37d80a,'mov','dword ptr [rip + 0x2b41bb0], 1')
anchor(0x37d989,'call','0x237420');anchor(0x37d98e,'mov','ebx, eax')
anchor(0x237420,'xor','eax, eax');anchor(0x237429,'setne','al')
override_pointer=rip(0x237422);assert override_pointer==0x2089350
anchor(0x37d9f6,'call','0x3d83a0')
anchor(0x37d9fb,'test','ebx, ebx');anchor(0x37d9fd,'jne','0x37da0f')
anchor(0x37d9ff,'cmp','dword ptr [rip + 0x2b419bf], ebx')
anchor(0x37da05,'je','0x37da4a');anchor(0x37da0d,'je','0x37da4a')
other=rip(0x37da07);assert other==0x2ebf3c0 and other!=flag
assert rip(0x37db70)==other;anchor(0x3dd220,'jmp','0x37db70')
outbase=rip(0x37da15,1);assert outbase==0x2ebf380
anchor(0x37da1f,'shl','rax, 5')
anchor(0x37da23,'movss','dword ptr [rax + rcx], xmm0')
anchor(0x37da45,'movups','xmmword ptr [rax + rcx + 0xc], xmm0')
anchor(0x37d4f1,'call','0x37d970')
assert rip(0x37d75c)==other
anchor(0x37d763,'je','0x37d7bc');assert rip(0x37d769,1)==outbase
anchor(0x37d7c4,'call','0x382b70')
# Full recorded bodies agree with the already-published camera primary. No rerun
# of its isolated sampler or live session, and no new execution count is claimed.
priorpath=ROOT/'Database/FFXII TZA/_experiments/evidence/camera-rng-discriminator/original-code.json'
prior=json.loads(priorpath.read_text())
for a in (0x37d1f0,0x3dcfb0,0x314370):
    key=f'{a:08X}';assert bodies[key]['raw_hex']==prior['bodies'][key]['raw_hex']
refs=[]
for va,ins in decoded.items():
    for i in ins:
        for n,op in enumerate(i.operands):
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP and rip(i.address,n)==flag:
                refs.append(i.address)
assert sorted(refs)==[0x37d80a,0x37d9ff,0x37ddc0]
# This is a LOCAL positive source boundary, not whole-image alias/indirect proof.
assert sum(i.mnemonic=='call' and i.operands[0].type==X86_OP_IMM and i.operands[0].imm==0x379ce0 for i in decoded[0x37d1f0])==9
anchor(0x3dd06b,'call','0x37d1f0')
result=dict(method='A: verified shipping instructions, no execution',executable_sha256=EXE,
            capstone_version=capstone.__version__,python_version=sys.version,bodies=bodies,
            normalized=dict(option_flag=hex(flag),other_enable=hex(other),override_pointer=hex(override_pointer),
                            output_base=hex(outbase),output_stride=32,
                            own_copy_condition='override_pointer != 0 OR (option_flag != 0 AND other_enable != 0)',
                            compute_call_before_option_branch='0037D9F6 ->003D83A0',
                            own_copy_bytes=28,own_copy_skipped_not_zeroed=True,
                            gather_gate_uses_other_enable_not_option=True),
            controls=dict(option_setter_getter_same_record=True,init_and_setter_and_reader_same_flag=True,
                          neighbor_gate_distinguished=True,retained_camera_bodies_identical=True,
                          local_option_rip_sites=[f'{a:08X}' for a in refs]),
            prior_primary=dict(path=str(priorpath.relative_to(ROOT)),sha256=sha(priorpath.read_bytes())),
            limitations=['No live setting state, call rate, effect visibility or RNG attribution observed.',
                         'Output condition assumes normally returning callees and valid caller state.',
                         'Skipping this copy does not establish what other routines do to the output row.',
                         'Local branch inspection and positive xrefs do not prove absence of indirect aliases.',
                         'The authored driver/sampler entry path is separate from this output gate; global scheduling remains open.'])
target=HERE/'observation.json'
if '--write' in sys.argv:
    assert not target.exists(),'retain original evidence; do not overwrite'
    target.write_text(json.dumps(result,indent=2)+'\n')
else:assert json.loads(target.read_text())==result,'retained primary changed'
print('PASS: option bit14 ->02EBF3C4; distinct02EBF3C0 gate; override pointer02089350.')
print('PASS: evaluator called before conditional28-byte output copy; skip is not a local row clear.')
print('PASS: retained driver/sampler bytes match; no new execution or global scheduling claim.')
