"""A BMASK source request/reset pointer provenance; no machine-code execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,why=team.board_status(team.BOARD);assert ok,why;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-MASK-QUERY-RESET-BOUNDARY');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
p=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');pol=Path(roles.__file__);(R/'shipping-reader.py').write_bytes(p.read_bytes());(R/'reg_tracking.py').write_bytes(pol.read_bytes())
sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;bodies=[];ii={}
for a,n,name in [(0x3912E0,292,'query'),(0x861EC0,6,'memset-thunk')]:
    b=rd.img_rd(d,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n and seq[-1].mnemonic==('ret' if n==292 else 'jmp');(R/(name+'.bin')).write_bytes(b)
    records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    bodies.append(dict(name=name,entry=hex(a),bytes=n,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
pe=struct.unpack_from('<I',d,0x3C)[0];pr,ps=struct.unpack_from('<II',d,pe+24+112+24);pd=rd.img_rd(d,ss,rd.IMG_LO+pr,ps);ext=[]
for j in range(0,ps-11,12):
    a,e,u=struct.unpack_from('<III',pd,j)
    if a+rd.IMG_LO==0x3912E0:ext.append(dict(directory_rva=hex(pr),record_offset=j,record_hex=pd[j:j+12].hex(),entry=hex(a+rd.IMG_LO),end=hex(e+rd.IMG_LO)))
assert len(ext)==1 and ext[0]['end']=='0x391404'
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-allocation-return-boundary');pa=json.loads((parent/'result.json').read_text());assert pa['reference']['exe_sha256']==sha(d)
(R/'allocation-parent-result.json').write_bytes((parent/'result.json').read_bytes());(R/'allocation-parent-manifest.json').write_bytes((parent/'manifest.json').read_bytes());binding=pa['memset_import']
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
    b=bytes.fromhex(binding[bk]);assert rd.img_rd(d,ss,int(binding[ak],16),len(b))==b
raw=dict(reference=dict(exe_sha256=sha(d),base=hex(rd.IMG_LO),reader_sha256=sha(p.read_bytes()),policy_sha256=sha(pol.read_bytes()),parent_result_sha256=sha((R/'allocation-parent-result.json').read_bytes()),parent_manifest_sha256=sha((R/'allocation-parent-manifest.json').read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__),bodies=bodies,extent=ext[0],memset_import=binding)
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
def rip(pc):
    i=ii[pc];o=next(o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP);return i.address+i.size+o.mem.disp
assert rip(0x3912F9)==0x2AEE0B8 and rip(0x391302)==rip(0x3913B1)==rip(0x3913E8)==0x2AEE0B0
assert ii[0x3912F9].op_str.startswith('r8, dword ptr') and ii[0x391302].op_str.startswith('rcx, qword ptr') and ii[0x391309].op_str=='edx, edx' and ii[0x39130E].operands[0].imm==0x861EC0
before=[i for a,i in ii.items() if 0x3912E0<=a<=0x39130E];assert not any(i.mnemonic.startswith('j') or i.mnemonic=='call' for i in before[:-1])
# All query paths are local (returning opaque memset); the one call dominates
# every later local loop/return since there is no prior branch or alternate entry.
seq={a:i for a,i in ii.items() if 0x3912E0<=a<0x391404};edges={}
for a,i in seq.items():
    n=a+i.size
    if i.mnemonic=='ret':ds=[]
    elif i.mnemonic.startswith('j'):
        assert i.operands[0].type==capstone.CS_OP_IMM;ds=[i.operands[0].imm] if i.mnemonic=='jmp' else [n,i.operands[0].imm]
    else:ds=[n]
    assert all(x in seq for x in ds);edges[a]=ds
assert [hex(a) for a,i in seq.items() if i.mnemonic=='call']==['0x39130e']
orr=ii[0x3913C4];assert orr.mnemonic=='or' and orr.op_str=='byte ptr [rdx + rax - 1], cl' and roles.op_kind(orr,orr.operands[0],0)=='rw'
assert ii[0x3913B1].op_str.startswith('rdx, qword ptr') and ii[0x3913E8].op_str.startswith('rax, qword ptr')
code=(R/'query.bin').read_bytes()
def clear_binding(b):
    x={i.address:i for i in cs.disasm(b,0x3912E0)}
    return (x[0x391302].mnemonic=='mov' and x[0x391302].op_str.startswith('rcx, qword ptr') and x[0x391309].op_str=='edx, edx' and x[0x39130E].mnemonic=='call' and x[0x39130E].operands[0].imm==0x861EC0)
assert clear_binding(code)
mut=bytearray(code);off=0x391302-0x3912E0;assert mut[off:off+3]==bytes.fromhex('488b0d');mut[off+2]=0x15;assert not clear_binding(bytes(mut));(R/'labelled-wrong-clear-register.bin').write_bytes(mut)
omit=bytearray(code);off=0x39130E-0x3912E0;assert omit[off]==0xE8;omit[off:off+5]=b'\x90'*5;assert not clear_binding(bytes(omit));(R/'labelled-omitted-clear-call.bin').write_bytes(omit)
assert sha(mut)!=sha(code) and sha(omit)!=sha(code)
refs=[]
for name,path,kind in [('mask-field-preimage.tsv','Database/FFXII TZA/_types/fields.tsv','field'),('contract-preimage.md','Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-corridor-query-family.md','all')]:
    b=Path(path).read_bytes();lines=b.splitlines(keepends=True);kept=b if kind=='all' else lines[0]+b''.join(x for x in lines[1:] if x.startswith(b'NavGridParams\t0x050\t'))
    assert kept;(R/name).write_bytes(kept);refs.append(dict(path=path,full_source_sha256=sha(b),retained=name,retained_sha256=sha(kept)))
assert b'zeroed once' in (R/'mask-field-preimage.tsv').read_bytes() and b'rather than per query' in (R/'mask-field-preimage.tsv').read_bytes() and b'caller-supplied record mask' in (R/'contract-preimage.md').read_bytes()
result=dict(method='A source argument/flow/pointer provenance only; no FF12/native/emulator/live execution',reference=raw['reference'],driver_sha256=raw['driver_sha256'],bindings=dict(clear_pointer_cell=hex(rip(0x391302)),or_pointer_cell=hex(rip(0x3913B1)),returned_pointer_cell=hex(rip(0x3913E8)),clear_length_cell=hex(rip(0x3912F9)),call=hex(0x39130E),or_write=hex(0x3913C4)),flow=dict(clear_before_all_loops_on_normal_entry=True,no_early_branch_before_clear=True,call_pcs=['0x39130e'],opaque_call_assumption='Conforming memset returns; actual cleared bytes and loaded implementation unobserved'),controls=dict(original_entry_binding=True,private_wrong_register_rejected=not clear_binding(bytes(mut)),private_omitted_call_rejected=not clear_binding(bytes(omit)),original_binding_refuses_both=sha(mut)!=sha(code) and sha(omit)!=sha(code)),consumers=refs,interpretation='Each normal entry requests zeroing of the global-owned working mask with sign-extended cellBitsetBytes, before clamp/query loops; its OR accumulation and returned pointer are loaded from the same global cell. It is not a destination supplied through an incoming argument. Reset storage effect requires valid writable block/nonnegative appropriate size and conforming native memset, not a observed live clear.',limits='Normal entry only, arbitrary midfunction entry/intervention excluded. Repeated global loads do not prove atomic identity or stable pointer under reentrancy/concurrency; actual initialized storage/nativeclear/return effects and normalgame reachability remain unobserved. It is shared through a global, not proven thread-local/callerowned, but actual scheduling/singlethread/exclusiveuse not established here.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('CAPTURE_MASK_SOURCE entry requests shared mask reset before loops; sameglobal OR/return pointer source; wrongdest and omittedcall controls reject; native clear/identity stability unproved')
