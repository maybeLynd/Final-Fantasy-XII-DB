"""Method A: pin original argument/queue boundaries; no instructions executed."""
import hashlib,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
assert sha(raw)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24
base=struct.unpack_from('<Q',raw,opt+24)[0];assert base==0x120000
st=opt+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<IIII',raw,st+40*i+8) for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
    for _,r,z,f in sections:
        if r<=a-base and a-base+n<=r+z:return raw[f+a-base-r:f+a-base-r+n]
    raise AssertionError(hex(a))
sizes={0x3515b0:95,0x351020:173,0x3581b0:203,0x267f90:39,0x267e10:78,
       0x3e9bf0:22,0x3e9c10:275,0x3e9780:297,0x2df680:5,0x1dc280:58,
       0x2256f0:197,0x2257e0:76}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
insmap={};bodies={}
for a,n in sizes.items():
    code=read(a,n);ins=list(md.disasm(code,a))
    assert ins and sum(i.size for i in ins)==n
    insmap.update({i.address:i for i in ins})
    bodies[f'{a:08X}']=dict(bytes=n,sha256=sha(code),raw_hex=code.hex(),extent='complete catalog body',
        instructions=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins])
anchors={
 0x3515ca:('mov','edx, 0x40'),0x3515d8:('call','0x267f90'),
 0x3515dd:('mov','edx, 0x7f'),0x3515e5:('call','0x267f90'),0x35160a:('jmp','0x351020'),
 0x267f90:('movsxd','rax, dword ptr [rcx]'),0x267f93:('cmp','eax, 0x3f'),
 0x267f98:('mov','byte ptr [rax + rcx + 4], 1'),
 0x267fad:('mov','dword ptr [rcx + rax*4 + 0x184], edx'),0x267fb4:('inc','dword ptr [rcx]'),
 0x267e1a:('dec','eax'),0x267e1c:('movsxd','r8, eax'),0x267e1f:('mov','dword ptr [rcx], eax'),
 0x267e21:('movzx','edx, byte ptr [r8 + rcx + 4]'),0x267e27:('sub','edx, 1'),
 0x267e2a:('je','0x267e51'),0x267e51:('mov','eax, dword ptr [rcx + r8*4 + 0x184]'),
 0x35104d:('call','0x267e10'),0x351055:('mov','esi, eax'),
 0x351057:('call','0x267e10'),0x35105f:('mov','edi, eax'),
 0x351061:('call','0x267e10'),0x35106c:('mov','ebx, eax'),
 0x351066:('or','edx, 0xffffffff'),0x35106e:('call','0x267f90'),
 0x351073:('mov','edx, ebx'),0x351078:('call','0x267f90'),
 0x35107d:('mov','edx, edi'),0x351082:('call','0x267f90'),
 0x351087:('mov','edx, esi'),0x35108c:('call','0x267f90'),
 0x351091:('mov','edx, 1'),0x351099:('call','0x267f90'),0x3510c8:('jmp','0x3581b0'),
 0x3581d7:('call','0x267e10'),0x3581df:('mov','r12d, eax'),
 0x3581e2:('call','0x267e10'),0x3581ea:('mov','ebp, eax'),
 0x3581ec:('call','0x267e10'),0x3581f4:('mov','r14d, eax'),
 0x3581f7:('call','0x267e10'),0x3581ff:('mov','edi, eax'),
 0x358201:('call','0x267e10'),0x358206:('mov','esi, eax'),
 0x358238:('call','0x267310'),0x35823d:('test','eax, eax'),0x35823f:('jne','0x35825c'),
 0x358241:('mov','r9d, ebp'),0x358244:('mov','r8d, r14d'),
 0x35824b:('test','r12d, r12d'),0x358250:('call','0x3e9bf0'),
 0x3e9bf4:('mov','dword ptr [rsp + 0x20], 1'),0x3e9bfc:('call','0x3e9c10'),
 0x3e9c33:('mov','edi, r9d'),0x3e9c3b:('mov','r14d, r8d'),
 0x3e9c61:('cmp','byte ptr [rbx + 4], 3'),0x3e9c74:('cmp','dword ptr [r9 + 4], esi'),
 0x3e9cf9:('and','dword ptr [rbx + 8], 0x80ffffff'),
 0x3e9d00:('and','edi, 0x7f'),0x3e9d03:('shl','edi, 0x18'),
 0x3e9d06:('or','dword ptr [rbx + 8], edi'),0x3e9d09:('mov','byte ptr [rbx + 0xf], r14b'),
 0x3e981f:('movzx','r8d, byte ptr [rbx + rdi + 0xb]'),
 0x3e9825:('movzx','edx, byte ptr [rbx + rdi + 0xf]'),0x3e982a:('and','r8d, 0x7f'),
 0x3e9832:('call','0x2df680'),0x2df680:('jmp','0x1dc280'),
 0x1dc28f:('mov','ebx, r8d'),0x1dc292:('mov','edi, edx'),
 0x1dc29e:('mov','r9d, ebx'),0x1dc2a1:('mov','r8d, edi'),0x1dc2b5:('jmp','0x211230'),
 0x225709:('mov','esi, edx'),0x225743:('cmp','esi, 0x7f'),
 0x225750:('lea','edi, [rsi - 0x40]'),0x2257a2:('mov','dword ptr [rbp + 0x20], esi'),
 0x225811:('mov','dword ptr [rcx + 0x1c], eax'),0x225827:('jmp','0x7a81f0')}
for a,want in anchors.items():
    i=insmap[a];assert (i.mnemonic,i.op_str)==want,(hex(a),i.mnemonic,i.op_str)
for a,expected in [(0x225783,1/128),(0x22581f,127.0)]:
    i=insmap[a];op=i.operands[1]
    assert op.type==capstone.x86.X86_OP_MEM and op.mem.base==capstone.x86.X86_REG_RIP
    constant=i.address+i.size+op.mem.disp
    assert struct.unpack('<f',read(constant,4))[0]==expected
# The exact native calls and their intervening moves, not a name-only argument list.
default_literals=[insmap[a].operands[1].imm for a in (0x3515ca,0x3515dd)]
assert default_literals==[64,127] and default_literals!=[127,64]
# Documented static LIFO reduction under the verified typed integer push/pop path.
stack=['cue']+default_literals
esi,edi,ebx=stack.pop(),stack.pop(),stack.pop()
stack.extend([-1,ebx,edi,esi,1])
r12,rbp,r14,cue,speaker=[stack.pop() for _ in range(5)]
assert not stack and (r12,rbp,r14,cue,speaker)==(1,127,64,'cue',-1)
assert (r14,rbp)==(64,127) # R8 and R9 at00358244/241; NOT a machine execution.
# The existing execution package already pins the identical VM pop body. Reuse it.
prior=ROOT/'Database/FFXII TZA/_experiments/evidence/sound-request-exec/bodies.json'
catalog=json.loads(prior.read_text())
pop=next(b for b in catalog['real'] if int(b['va'],16)==0x267e10)
assert pop['sha256']==bodies['00267E10']['sha256'] and pop['size']==78
out=dict(method='A: original instruction inspection and static LIFO reduction; no native/isolated/live execution',
 executable_sha256=sha(raw),capstone_version=capstone.__version__,bodies=bodies,
 normalized=dict(default_push_order=default_literals,pushes_in_three_arg_adapter=[-1,'cue',64,127,1],
 common_pop_values=dict(r12d_flag=1,ebp_volume=127,r14d_pan=64,edi_cue='cue',esi_speaker=-1),
 setter=dict(r8d_pan=64,r9d_volume=127,pan_store='003E9D09 -> cue+0F',volume_store='003E9D06 -> cue+08 bits24..30'),
 pump=dict(pan='003E9825 EDX from cue+0F',volume='003E981F R8D from cue+0B masked7F',call='003E9832 ->002DF680')),
 reused_pop_identity=dict(source=str(prior.relative_to(ROOT)).replace('\\','/'),sha256=sha(prior.read_bytes()),same_original_body=True),
 limits=['Well-formed typed cue argument and adequate VM stack capacity; invalid/overflowed frames excluded.',
 'The mute predicate, valid loaded cue table, selected language and request-pump readiness gate native progress.',
 'ABI-preserved nonvolatile temporaries and normally returning calls are required.',
 'Stored request parameters are not voice initialization, realized gain, acoustic centering or normal reachability.',
 'No downstream00211230/controller/native voice execution or audibility observation.'])
dest=HERE/'observation.json'
if '--write' in sys.argv:
    assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n')
else:assert json.loads(dest.read_text())==out
print('PASS: complete original bodies and argument/queue anchors match reference; no code executed.')
print('voiceplay request: pan64 to cue+0F; volume127 to cue+08 bits24..30; pump preserves order.')
print('Existing EXP096 pop body identity reused; audible/native voice results remain open.')
