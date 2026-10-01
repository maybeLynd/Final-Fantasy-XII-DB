"""Read-only original ordering and caller-argument reducer; no execution."""
import hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(root=W):
 root=Path(root);raw=json.loads((root/'raw.json').read_bytes());ident=raw['identity']
 receipt=json.loads((root/'capture-terminal.json').read_bytes())
 assert receipt['terminal'] is True and receipt['returncode']==0 and not receipt['stderr']
 assert sha(root/'capture.py')==receipt['driver_sha256']==ident['driver_sha256']
 assert ident['exe']['sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 for s in ident['sources']:assert sha(root/'retained'/s['copy'])==s['sha256']
 assert capstone.__version__==ident['capstone']
 policy=(root/'retained/reg_tracking.py').read_bytes();roles=types.ModuleType('roles')
 exec(compile(policy,'retained shared reviewed access-role adapter','exec'),roles.__dict__)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 expected=['f7aa75d3bcd5880f14d6ede40bb1e6638f08f0a608854bbc5aa4d90d1e1357d5','f739335670ae32f1bffe17b78e178d4ee4a009406894fd1f064a6cc76ea813e9','7935bf3b415aa31afbd91d68b8f4e530cbf32a51bb985605e5f30835d8d42136','bef9ef31cf27c89527cd3a858721dbf8901af34b5103f2f3ce175138fc4daa76']
 assert len(raw['bodies'])==4
 maps={}
 for b,digest in zip(raw['bodies'],expected):
  data=(root/'retained'/(b['name']+'.bin')).read_bytes()
  assert len(data)==b['bytes'] and sha(root/'retained'/(b['name']+'.bin'))==b['sha256']==digest
  ins=list(cs.disasm(data,int(b['pc'],16)));assert sum(i.size for i in ins)==len(data)
  rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
  assert rows==b['instructions'];maps[b['name']]={i.address:(i.mnemonic,i.op_str) for i in ins}
 d=maps['delta'];c=maps['caller']
 need={0x2e4389:('xor','eax, eax'),0x2e438b:('mov','r14, r9'),0x2e438e:('mov','qword ptr [rdx], rax'),0x2e4391:('mov','rbx, rdx'),0x2e4394:('mov','dword ptr [rdx + 8], eax'),0x2e439a:('movzx','eax, byte ptr [rcx + 3]'),0x2e43a2:('jne','0x2e45c9'),0x2e43b0:('mov','rdi, qword ptr [rcx + 0xb8]'),0x2e43b7:('test','r8d, r8d'),0x2e43ba:('je','0x2e4419'),0x2e43bc:('movss','xmm1, dword ptr [r9 + 4]'),0x2e43c2:('movss','xmm0, dword ptr [r9]'),0x2e43c7:('movss','xmm2, dword ptr [r9 + 8]'),0x2e43e1:('call','0x3a1d30'),0x2e43e6:('movss','dword ptr [rdi + 0xf8], xmm0'),0x2e43ee:('mov','eax, dword ptr [r14]'),0x2e43f9:('mov','dword ptr [rbx], eax'),0x2e43fb:('mov','eax, dword ptr [r14 + 4]'),0x2e43ff:('mov','dword ptr [rbx + 4], eax'),0x2e4402:('mov','eax, dword ptr [r14 + 8]'),0x2e4406:('mov','dword ptr [rbx + 8], eax'),0x2e4409:('mov','dword ptr [rbx + 0xc], 0x3f800000')}
 for pc,want in need.items():assert d[pc]==want,(hex(pc),d[pc],want)
 caller_need={0x2e504c:('mov','r14, r8'),0x2e504f:('mov','ebp, edx'),0x2e50bd:('mov','r9, r14'),0x2e50c0:('lea','rdx, [rsp + 0x30]'),0x2e50c5:('mov','r8d, ebp'),0x2e50c8:('mov','rcx, rbx'),0x2e50cb:('call','0x2e4380')}
 for pc,want in caller_need.items():assert c[pc]==want,(hex(pc),c[pc],want)
 wrapper=maps['sqrt-wrapper'];assert wrapper[0x3a1d42]==('jmp','0x861f14')
 assert maps['sqrt-thunk']=={0x861f14:('jmp','qword ptr [rip + 0x60c9e]')}
 # The first RUNTIME_FUNCTION range is not the complete intervening function.
 # Require the additive full-body evidence before accepting caller-proof scope.
 body=json.loads((root/'intervening-body.json').read_bytes())
 body_receipt=json.loads((root/'intervening-body-terminal.json').read_bytes())
 assert body_receipt['terminal'] is True and body_receipt['returncode']==0 and not body_receipt['stderr']
 assert sha(root/'capture-intervening-body.py')==body_receipt['driver_sha256']==body['driver_sha256']
 assert body['exe_sha256']==ident['exe']['sha256'] and body['adapter_sha256']==hashlib.sha256(policy).hexdigest()
 data=(root/'retained/intervening-body963.bin').read_bytes()
 assert len(data)==963 and hashlib.sha256(data).hexdigest()==body['sha256']
 ins=list(cs.disasm(data,0x2e45e0));assert sum(i.size for i in ins)==963
 rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'written':sorted(roles.written(i)),'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
 assert rows==body['instructions']
 entries=body['exception_directory']['selected_entries'];assert len(entries)==8
 cursor=0x2e45e0;runtime_records={}
 for e in entries:
  assert int(e['begin'],16)==cursor and int(e['end'],16)-cursor==e['bytes']
  start,end,uw=struct.unpack('<III',bytes.fromhex(e['raw_runtime_function']))
  assert (start+0x120000,end+0x120000,uw)==(cursor,int(e['end'],16),int(e['unwind_rva'],16))
  runtime_records[e['raw_runtime_function']]=e;cursor=end+0x120000
 assert cursor==0x2e49a3 and entries[0]['bytes']==40
 for e in entries:
  u=bytes.fromhex(e['raw_unwind_info']);assert u[0]>>3==e['flags'];trailer=((4+2*u[2]+3)//4)*4
  if e['flags']&4:assert len(u)==trailer+12 and u[trailer:].hex() in runtime_records
 assert body['catalog']['selected_line'].split('\t')[:3]==['002E45E0','Movement_UpdateSteeringTowardTarget','963']
 prefix=[i for i in ins if i.address<0x2e4608]
 assert sum(i.size for i in prefix)==40 and not any(i.mnemonic=='ret' for i in prefix)
 assert ins[-1].address==0x2e49a2 and ins[-1].mnemonic=='ret'
 calls=[hex(i.address) for i in ins if i.mnemonic=='call'];assert len(calls)==21 and '0x2e464a' in calls
 contract=(root/'retained/pages/CONTRACT-heading-speed-to-position-delta.md').read_text('utf-8')
 assert '40-byte leaf' in contract and 'no calls' in contract
 # Conditional BYTE calculations for the confirmed straight-line prefix only.
 # Source instruction ordering establishes these; this model is not replay proof.
 vec=struct.pack('<4f',3,4,12,99)
 source_before=list(struct.unpack('<3I',vec[:12]))
 same=bytearray(vec);same[:8]=b'\0'*8;same[8:12]=b'\0'*4
 same_reads=[struct.unpack_from('<I',same,i)[0] for i in (4,0,8)]
 distinct_reads=[struct.unpack_from('<I',vec,i)[0] for i in (4,0,8)]
 assert source_before==[0x40400000,0x40800000,0x41400000] and same_reads==[0,0,0] and distinct_reads==[0x40800000,0x40400000,0x41400000]
 assert same[12:]==vec[12:] # W isn't touched by the entry clearing.
 if '--fault-pointer-stages-values' in sys.argv:assert '[' in d[0x2e438b][1],'MOV R14,R9 preserves pointer, not the contents before zeroing'
 if '--fault-same-buffer-preserved' in sys.argv:assert same_reads==distinct_reads,'Entry clearing precedes source reads; exact same-buffer first reads see zero'
 if '--fault-caller-reuses-output' in sys.argv:assert c[0x2e50bd]==('lea','r9, [rsp + 0x30]'),'Caller forwards entry R8 via R14, while RDX is local rsp+30; no forced input=output construction'
 if '--fault-first-pdata-is-leaf' in sys.argv:assert any(i.mnemonic=='ret' for i in prefix) and not calls,'40B is the first of8unwind fragments; no return in first40B and full963B has21calls'
 return {'status':'SOURCE_ESTABLISHES_ALIAS_AND_REFUTES_LEAF_PROOF','method':'A exact original ordering/caller/body/unwind source and conditional prefix-byte calculation; no executed scenarios',
         'entry_zero_stores':['002E438E:qword[output]=0','002E4394:dword[output+8]=0'],
         'first_source_reads':['002E43BC:input+4','002E43C2:input','002E43C7:input+8'],
         'conditional_prefix':{'original_xyz_bits':[f'{v:08X}' for v in source_before],'distinct_first_reads_yxz':[f'{v:08X}' for v in distinct_reads],'same_buffer_first_reads_yxz':[f'{v:08X}' for v in same_reads],'original_W_unchanged_by_prefix':True},
         'caller_argument_construction':{'site':'002E50CB','output':'local [current RSP+0x30]','input':'R9 assigned R14; R14 initialized from entryR8 before intervening963Bcallee. Full preservation/closure not established here.','mode':'R8D assigned EBP; EBP initialized from entryEDX before interveningcallee; this is sourceconstruction, not an observed live value.'},
         'intervening_extent':{'current_catalog_bytes':963,'unwind_fragments':8,'first_fragment_bytes':40,'first_fragment_has_return':False,'full_body_direct_call_sites':21,'class_stability_from_40B_leaf_proof':'REFUTED_BASIS; actual class stability/refusal reachability remain unproved here'},
         'consumer_change':'Qualify pass-through alias precondition. Reopen/replace CONTRACT section14/15 first40B leaf/no-calls basis: current catalog already963B; do not edit correct primary index or infer class mutation/observed refusal. Add full-fragment/claimed-reachability prerequisite to existing producer/check; owner supplies full effect/preservation proof or narrows closure.',
         'limits':'Class3/r8d!=0/valid separate actor+movement state, sequential prefix analysis. Exact same-buffer hypothesis only, not general partial-overlap safety. No imported sqrtf execution or final F8 numeric/pointer effects proven here; wrapper/thunk/source identity only. Recorded sole caller not a new whole-image census. Fullintervening callclosure/class stability/livepointer separation not established. No actual caller execution, game initialization, timing/atomicity/reachability or live behavior.'}
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1]) if len(sys.argv)>1 and not sys.argv[1].startswith('--') else W),indent=2))
