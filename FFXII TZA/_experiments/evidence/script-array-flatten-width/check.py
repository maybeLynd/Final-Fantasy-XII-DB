import hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'resolver591.bin').read_bytes();store=(R/'store194.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes();ref=raw['reference'];assert sha(code)==ref['resolver_sha256'] and sha(store)==ref['store_sha256'] and sha(policy)==ref['adapter_sha256']
roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x262440)};si={i.address:i for i in cs.disasm(store,0x26d530)}
for pc,m,a in [(0x26245d,'xor','ebx, ebx'),(0x262478,'lea','r13d, [rbx + 1]'),(0x262487,'mov','r10d, ebx'),(0x2624ad,'mov','r8d, r13d'),(0x2624b3,'movzx','eax, word ptr [rcx + 4]'),(0x2624ba,'sub','eax, r13d'),(0x2624bd,'movsxd','r13, eax'),(0x2624cd,'lea','rbp, [rbp + r13*4]'),(0x26251b,'sub','rbp, 4'),(0x26251f,'imul','eax, r8d'),(0x262523,'imul','r8d, esi'),(0x262527,'add','r10d, eax'),(0x26252a,'sub','r13, r15'),(0x26252d,'mov','dword ptr [rsp + 0x78], r10d'),(0x262532,'mov','dword ptr [rsp + 0x60], r8d'),(0x262537,'jns','0x2624d2'),(0x262672,'mov','dword ptr [r15 + 0x1c], r10d')]:assert (ii[pc].mnemonic,ii[pc].op_str)==(m,a),(hex(pc),ii[pc].op_str)
assert ii[0x2624ca].op_str=='r15d, r8d' and ii[0x2624c6].op_str=='rbp, [rcx + 8]'
assert all(ii[pc].operands[0].size==4 for pc in [0x26251f,0x262523,0x262527])
assert si[0x26d537].mnemonic=='movsxd' and si[0x26d537].op_str=='rcx, dword ptr [rcx + 0x1c]' and si[0x26d537].operands[1].size==4
assert roles.op_kind(ii[0x262672],ii[0x262672].operands[0],0)=='w' and roles.op_kind(si[0x26d537],si[0x26d537].operands[1],1)=='r'
assert all('r10' not in roles.written(i) for pc,i in ii.items() if 0x262546<=pc<0x262672 and pc not in [0x2625b1,0x26261d])
for pc in [0x2625b1,0x26261d]:assert ii[pc].mnemonic=='mov' and ii[pc].op_str=='r10d, dword ptr [rsp + 0x78]'
# The selected loop does not branch on multiply/add overflow; its loop-control
# SUB overwrites flags before the JNS, with only MOVs between them.
assert [ii[p].mnemonic for p in [0x26251f,0x262523,0x262527,0x26252a,0x26252d,0x262532,0x262537]]==['imul','imul','add','sub','mov','mov','jns']
signed=lambda n:struct.unpack('<i',struct.pack('<I',n&0xffffffff))[0]
cases=[]
for dims,idx in [([2,3],[1,0]),([2,3],[1,2]),([65536,65536],[0,0]),([65536,65536],[32768,0]),([65536,65536],[65535,65535])]:
 product,total=1,0;steps=[];unbounded=0;unbounded_product=1
 for d,i in zip(reversed(dims),reversed(idx)):
  assert d>0 and 0<=i<d;contribution=(i*product)&0xffffffff;total=(total+contribution)&0xffffffff;product=(product*d)&0xffffffff;unbounded+=i*unbounded_product;unbounded_product*=d;steps.append(dict(dimension=d,injected_popped_index=i,contribution_bits=f'{contribution:08x}',sum_bits=f'{total:08x}',next_product_bits=f'{product:08x}'))
 c=dict(dimensions_in_header_order=dims,indices_in_corresponding_axis_order=idx,pop_order=list(reversed(idx)),steps=steps,predicted_record1C_bits=f'{total:08x}',predicted_signed_handler_index=signed(total),unbounded_rowmajor=unbounded,predicted_product_bits=f'{product:08x}',kind='CONDITIONAL_STATIC_CALCULATION_NOT_EXECUTION');cases.append(c)
 if '--fault-unbounded-index' in sys.argv:assert c['predicted_signed_handler_index']==unbounded,'Originallow32 field is signed at handler, not unboundedrowmajor'
 if '--fault-saturating-index' in sys.argv:assert c['predicted_signed_handler_index']==min(unbounded,0x7fffffff),'Originalflatten wraps instead of saturating'
 if '--fault-forward-dimensions' in sys.argv and dims==[2,3] and idx==[1,0]:assert total==1,'Originalreverse dimension/pop order is distinguishable'
assert cases[0]['predicted_signed_handler_index']==3 and cases[1]['predicted_signed_handler_index']==5 and cases[2]['predicted_product_bits']=='00000000' and cases[3]['predicted_record1C_bits']=='80000000' and cases[3]['predicted_signed_handler_index']==-2147483648 and cases[4]['predicted_record1C_bits']=='ffffffff' and cases[4]['predicted_signed_handler_index']==-1
result=dict(status='FLATTEN_PRODUCTS_SUM_LOW32_THEN_SIGNED_HANDLER_INDEX',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),conditional_cases=cases,interpretation='Originalseeds product1/sum0, consumes dimensions lastfirst; IMUL/ADD low32 anddwordindex store followedbyMOVSXD, no multiplyoverflow branchinselectedloop. Rowmajorformula requires mod2^32 products/sum then signed32 handler scaling. Positiveper-axisclamp alone doesnotprove nonnegative flatindex or storage safety; conditional65536² produces80000000/signMIN orFFFFFFFF/sign-1. Not actualoccurrence.',consumer_change='Preserve wordwidth/reversepoporder/modulo32/indexsignextension informula/contract/spec, withsmallordercontrol andconditionalpositive-large examples. No overflowrejection/saturation invented, no shippedlargearray/fault claim.',limits=raw['limits']+' Consumer incorporation/independentacceptance pending; originalpublishedinputs/resultsimmutable.')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS74 exactoriginal32bitflatten/signedhandler; conditionalcalculations only',flush=True)
