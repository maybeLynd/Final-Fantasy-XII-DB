"""Read-only primary-byte reducer; conditional source results are not execution."""
import hashlib,json,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
def check(root=W):
 root=Path(root);raw=json.loads((root/'raw.json').read_bytes());ident=raw['identity']
 terminal=json.loads((root/'capture-terminal.json').read_bytes())
 assert terminal['terminal'] is True and terminal['returncode']==0 and not terminal['stderr']
 assert hashlib.sha256((root/'capture.py').read_bytes()).hexdigest()==terminal['driver_sha256']==ident['driver_sha256']
 assert ident['exe']['sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 for s in ident['sources']:assert hashlib.sha256((root/'retained'/s['copy']).read_bytes()).hexdigest()==s['sha256']
 assert capstone.__version__==ident['capstone']
 policy=(root/'retained/reg_tracking.py').read_bytes();roles=types.ModuleType('roles')
 exec(compile(policy,'retained shared reviewed access-role adapter','exec'),roles.__dict__)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 expected=['545b50d980b78413b91c682306944d64c9cbf6d8009734fc6ee9ac46ebc8c844','0d21a1f5d20ef0ba8d7d3e91c612aeb506cbd465779fd79134051c832e1ae95e','b6cbececf1b07e74f37d57710c68c31f0b92cb08d51093252b321b07542e177b']
 decoded={}
 for b,digest in zip(raw['bodies'],expected):
  data=(root/'retained'/(b['name']+'.bin')).read_bytes()
  assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256']==digest
  assert b''.join(bytes.fromhex(x['bytes']) for x in b['instructions'])==data
  ins=list(cs.disasm(data,int(b['pc'],16)));assert sum(i.size for i in ins)==len(data)
  rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
  assert rows==b['instructions'];decoded[b['name']]={i.address:(i.mnemonic,i.op_str) for i in ins}
 assert len(raw['bodies'])==3
 a=decoded['typed-pop']
 requirements={0x267e7f:('call','0x262440'),0x267e84:('movsx','r8d, word ptr [rsp + 0x34]'),0x267e8c:('sub','r8d, 1'),0x267e90:('je','0x267ef2'),0x267e92:('cmp','r8d, 1'),0x267e96:('jne','0x267f1e'),0x267e9e:('test','ecx, ecx'),0x267ea0:('jle','0x267edd'),0x267ea7:('mov','dword ptr [rbx], ecx'),0x267ea9:('movzx','ecx, byte ptr [rdx + rbx + 4]'),0x267eae:('sub','ecx, r8d'),0x267eb1:('je','0x267ec9'),0x267eb3:('cmp','ecx, r8d'),0x267eb6:('jne','0x267ee7'),0x267eb8:('movss','xmm0, dword ptr [rbx + rdx*4 + 0x184]'),0x267ec9:('movd','xmm0, dword ptr [rbx + rdx*4 + 0x184]'),0x267ed2:('cvtdq2ps','xmm0, xmm0'),0x267ed5:('movss','dword ptr [rsp + 0x50], xmm0'),0x267edd:('mov','ecx, 1'),0x267ee2:('call','0x8620c0'),0x267ee7:('xorps','xmm0, xmm0'),0x267eea:('movss','dword ptr [rsp + 0x50], xmm0'),0x267ef4:('test','eax, eax'),0x267ef6:('jle','0x267f18'),0x267efd:('mov','dword ptr [rbx], eax'),0x267f04:('sub','ecx, 1'),0x267f07:('je','0x267f57'),0x267f09:('cmp','ecx, 1'),0x267f0c:('je','0x267f4c'),0x267f13:('call','0x8620c0'),0x267f18:('xor','eax, eax'),0x267f1a:('mov','dword ptr [rsp + 0x50], eax'),0x267f2d:('call','0x32f240'),0x267f37:('call','0x26d530'),0x267f4c:('cvttss2si','eax, dword ptr [rbx + rdx*4 + 0x184]'),0x267f57:('mov','eax, dword ptr [rbx + rdx*4 + 0x184]')}
 for pc,want in requirements.items():assert a[pc]==want,(hex(pc),a[pc],want)
 assert decoded['report-wrapper'][0x8620c7]==('xor','ecx, ecx') and decoded['report-wrapper'][0x8620c9]==('jmp','0x16d6a0')
 assert len(decoded['report-wrapper'])==3 and decoded['report-wrapper'][0x8620c0][0]=='lea'
 assert decoded['folded-return']=={0x16d6a0:('ret','0')}
 # Exact normalized tag branch calculation, after original kind==2 selection:
 # r8d=kind-1=1, then ecx=tag-r8d; zero -> conversion, ==1 -> copy.
 actions={tag:('convert_signed_int' if tag-1==0 else 'copy_float_bits' if tag-1==1 else 'write_zero_float') for tag in [1,2,3]}
 assert actions=={1:'convert_signed_int',2:'copy_float_bits',3:'write_zero_float'}
 page=(root/'retained/pages/scriptvm-verb-dispatch-and-parameter-encoding.md').read_text('utf-8')
 assert 'tag 3' in page and '`008620C0` raises on empty pops' in page
 if '--fault-tag3-converts' in sys.argv:assert actions[3]=='convert_signed_int','Kind2 normalizes r8d to1: only tag1 converts; tag3 zeros'
 if '--fault-both-underflow-report' in sys.argv:assert a[0x267ef6][1]=='0x267f0e','Kind1 underflow skips reporting call to267F18'
 if '--fault-report-terminates' in sys.argv:assert decoded['folded-return'][0x16d6a0][0]!='ret','Original report wrapper tails to exact original return leaf'
 return {'status':'SOURCE_REFUTES_TYPED_POP_SUMMARY', 'method':'A original source/control flow plus conditional tag branch calculation, not executed cases',
         'kind2_tag_actions':actions,'underflow':{'kind2':'Call original8620C0 returning leaf; write +0.0 at temporary rsp+0x50; no depth decrement on this arm','kind1':'Skip reporter; write integer0 at temporary rsp+0x50; no depth decrement on this arm'},
         'report_chain':'Original 14B wrapper stages a string and zeroes ECX then tails to original C2 00 00 (ret0). No memory write, raise, abort or display in these instructions.',
         'consumer_change':'Correct current EC7-98 paragraph tag3->tag1 and qualify asymmetric underflow/reporting no-op; keep authored state/reachability and later callbacks unproved.',
         'limits':'Kind and value branches after00262440 supplies the temporary record. Values written into that record, NOT established final function returns. Actual00262440/0032F240/0026D530 effects, initialization, lifetime, caller reachability, native execution/exception/presentation and live behavior not tested.'}
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1]) if len(sys.argv)>1 else W),indent=2))
