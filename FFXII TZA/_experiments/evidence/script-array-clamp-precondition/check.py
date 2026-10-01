import hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'resolver591.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes()
assert len(code)==591 and sha(code)==raw['reference']['body_sha256'] and sha(policy)==raw['reference']['access_adapter_sha256']
roles=types.ModuleType('roles');exec(compile(policy,'retained shared reviewed access adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x262440)};assert sum(i.size for i in ii.values())==591
rows=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp,size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii.values()];assert rows==raw['instructions'],'Actual source adapter invocation/disassembly'
def exact(pc,h,m,a):
 i=ii[pc];assert (i.bytes.hex(),i.mnemonic,i.op_str)==(h,m,a),(hex(pc),i.mnemonic,i.op_str)
for args in [
 (0x26245d,'33db','xor','ebx, ebx'),(0x2624b3,'0fb74104','movzx','eax, word ptr [rcx + 4]'),
 (0x2624ba,'412bc5','sub','eax, r13d'),(0x2624bd,'4c63e8','movsxd','r13, eax'),
 (0x2624c0,'0f8880000000','js','0x262546'),(0x2624cd,'4a8d6cad00','lea','rbp, [rbp + r13*4]'),
 (0x2624d5,'8b7500','mov','esi, dword ptr [rbp]'),(0x2624da,'7e2e','jle','0x26250a'),
 (0x26250a,'8bc3','mov','eax, ebx'),(0x26250c,'85c0','test','eax, eax'),
 (0x26250e,'8bcb','mov','ecx, ebx'),(0x262510,'0f49c8','cmovns','ecx, eax'),
 (0x262513,'8d46ff','lea','eax, [rsi - 1]'),(0x262516,'3bce','cmp','ecx, esi'),
 (0x262518,'0f4cc1','cmovl','eax, ecx'),(0x26251f,'410fafc0','imul','eax, r8d'),
 (0x262523,'440fafc6','imul','r8d, esi'),(0x262527,'4403d0','add','r10d, eax'),
 (0x26257d,'418b849684010000','mov','eax, dword ptr [r14 + rdx*4 + 0x184]'),
 (0x262585,'eb85','jmp','0x26250c')]:exact(*args)
assert ii[0x262478].mnemonic=='lea' and ii[0x262478].op_str=='r13d, [rbx + 1]'
# In the selected integer/empty-stack paths, EBX remains the original zero. The
# bad-tag call and later bank selection are outside the proved input routes.
assert all('rbx' not in roles.written(i) for pc,i in ii.items() if 0x26245f<=pc<0x26252a)
assert all('rbx' not in roles.written(ii[pc]) for pc in [0x26257d,0x262585])
assert ii[0x2624ed].mnemonic=='je' and ii[0x2624ed].operands[0].imm==0x26257d
assert ii[0x2624ca].op_str=='r15d, r8d' and ii[0x2624ad].op_str=='r8d, r13d'
assert ii[0x2624ea].op_str=='ecx, r15d' # tag1 when rank initial product is 1
def kinds(pc):return [roles.op_kind(ii[pc],o,j) for j,o in enumerate(ii[pc].operands) if o.type==capstone.CS_OP_MEM]
assert kinds(0x2624e1)==['w'] and kinds(0x2624d5)==['r'] and kinds(0x262513)==['addr'],'Actual original store/read/LEA path roles'
# Counterfactual decoded private bytes, never executed: upper <= instead of <
# would change the predicate identity. Keep original input immutable.
z=bytearray(code);z[0x262518-0x262440+1]=0x4e;mut=next(cs.disasm(bytes(z[0x262518-0x262440:]),0x262518));assert mut.mnemonic=='cmovle' and mut.bytes.hex()=='0f4ec1'
if '--fault-upper-inclusive' in sys.argv:assert mut.mnemonic==ii[0x262518].mnemonic,'Changed upper predicate rejected'
# No native instructions are executed below. These are literal consequences of
# the verified TEST/CMOVNS/LEA/CMP/CMOVL sequence for signed32 inputs with EBX=0.
signed=lambda n:struct.unpack('<i',struct.pack('<I',n&0xffffffff))[0]
def calc(index,dim):
 assert -(1<<31)<=index<(1<<31) and -(1<<31)<=dim<(1<<31)
 lower=index if index>=0 else 0;upper=signed(dim-1);return lower if lower<dim else upper
cases=[dict(index=i,dimension=d,predicted_signed_clamped=calc(i,d),kind='CONDITIONAL_STATIC_CALCULATION_NOT_EXECUTION') for d,inds in [(5,[-1,0,4,5,6]),(1,[-1,0,1]),(0,[-1,0,1])] for i in inds]
assert [x['predicted_signed_clamped'] for x in cases[:5]]==[0,0,4,4,4] and [x['predicted_signed_clamped'] for x in cases[5:8]]==[0,0,0]
assert all(x['predicted_signed_clamped']==-1 for x in cases[8:]),'Zero dimension does not select an existing edge'
if '--fault-zero-dimension-is-edge' in sys.argv:assert all(x['predicted_signed_clamped']==0 for x in cases[8:]),'Zero-dimension edge assumption rejected'
rank0=signed(0-1);rank1=signed(1-1);assert rank0<0 and rank1==0
if '--fault-rank-is-dimension' in sys.argv:assert rank1<0,'Zero dimension is not zero rank'
result=dict(status='EDGE_CLAMP_REQUIRES_POSITIVE_SIGNED_DIMENSION',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),static_observations=dict(rank='u16 header+4 minus1, MOVSXD then JS to262546; rank0 skips entire loop, rank1 enters',dimension='Each iteration loads signed32 ESI from [RBP]; no positivity guard in selected clamp26250C..262527',zero_lower='Original XOR EBX,EBX preserved on selected integer/empty-stack routes',clamp='ECX=index if signedindex>=0 else0; EAX=low32(dim-1); CMOVL chooses ECX iff signedECX<signedESI',zero_dimension='For rank>=1 and selected stage with dim0/EBX0, predictedclamp=-1. With initialR8D=1/R10D=0 the decoded multiply/add predicts contribution=-1, nextproduct0; not executed here',memory_roles=dict(stack_depth_store='w',dimension_read='r',upper_LEA='addr'),private_decoded_control='Upper CMOVL->CMOVLE changes decoded predicate; no execution'),conditional_calculations=cases,implication='Qualify edge-clamp/silent-index behavior with strictly positive signed32 dimension and otherwise valid storage/state. Rank/count0 guard is not dimension-value0 validation. Do not promise no fault or universal malformed safety from this stage.',limits='Static source and calculations, not original execution. No original dimension validity census, actual zero array, native bank read/write/fault, caller acceptance, initialization/lifetime/scheduling/reachability or rank0 complete resolver outcome. Positive dimensions also do not prove product/offset overflow or storage validity. Parent65 publication correction required. Owner consumers/independent acceptance pending; PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS69 original rank/dimension signed clamp identity; conditional calculations only',flush=True)
