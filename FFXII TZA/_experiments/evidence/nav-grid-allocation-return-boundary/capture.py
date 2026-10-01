"""A focused source/return-boundary controls; never executes FF12 instructions."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
policy=Path('Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py')
(R/'shipping-reader.py').write_bytes(reader.read_bytes());(R/'reg_tracking.py').write_bytes(policy.read_bytes())
sys.path.insert(0,str(policy.parent));import reg_tracking as roles
assert Path(roles.__file__).resolve()==policy.resolve()
sp=importlib.util.spec_from_file_location('original_reader',reader);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd)
d,ss=rd.load_image();exe_sha=sha(d);assert exe_sha=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-quantization');ps=json.loads((parent/'source.json').read_text());pb=next(b for b in ps['bodies'] if b['entry']=='0x3924b0')
(R/'parent-source.json').write_bytes((parent/'source.json').read_bytes());(R/'parent-manifest.json').write_bytes((parent/'manifest.json').read_bytes())
assert pb['sha256']=='0a7ec1000ef3d48a471ff9200675b11ef90717fedcb53b50afa84a4281e236f5'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
bodies=[];ii={}
for a,n,name in [(0x3924B0,607,'builder'),(0x384580,104,'wrapper'),(0x861EC0,6,'memset-thunk')]:
    b=rd.img_rd(d,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n
    assert seq[-1].mnemonic==('jmp' if n==6 else 'ret')
    if name=='builder':assert b==bytes.fromhex(pb['raw_hex']) and sha(b)==pb['sha256']
    (R/(name+'.bin')).write_bytes(b)
    records=[]
    for i in seq:
        mem=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=mem,written=sorted(roles.written(i))))
    bodies.append(dict(name=name,entry=hex(a),bytes=n,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
# Save source reduction before semantic assertions; actual shared adapter is called above.
raw=dict(bodies=bodies,reference=dict(exe_sha256=exe_sha,base=hex(rd.IMG_LO),reader_sha256=sha(reader.read_bytes()),policy_sha256=sha(policy.read_bytes())),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__),driver_sha256=sha(Path(__file__).read_bytes()))
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
def imm(pc):
    i=ii[pc];assert i.operands[0].type==capstone.CS_OP_IMM;return i.operands[0].imm
assert imm(0x39266A)==0x384580 and imm(0x3845B0)==0x36A190
assert ii[0x3845B5].op_str=='rbx, rax' and ii[0x3845B8].op_str=='rax, rax'
assert ii[0x3845BB].mnemonic=='je' and imm(0x3845BB)==0x3845CB
assert imm(0x3845C6)==0x36C660 and ii[0x3845DA].op_str=='rax, rbx'
wrapper=[i for i in ii.values() if 0x3845B5<=i.address<0x3845E8]
assert not any('rbx' in roles.written(i) for i in wrapper if i.address not in (0x3845B5,0x3845DD))
# Focused branch path calculation from the TEST and branch, with opaque calls
# returning/preserving RBX. It is a conditional CFG calculation, not execution.
def path(code,null):
    seq={i.address:i for i in cs.disasm(code,0x384580)};pc=0x3845B5;visited=[];calls=[]
    for _ in range(32):
        i=seq[pc];visited.append(hex(pc));op=i.mnemonic
        if op=='ret':return dict(visited=visited,calls=calls,initializer=hex(0x36C660) in calls,returned='zero' if null else 'same allocator pointer')
        if op in ('je','jne'):
            assert pc==0x3845BB;take=null if op=='je' else not null;pc=i.operands[0].imm if take else pc+i.size;continue
        if op=='call':calls.append(hex(i.operands[0].imm))
        pc+=i.size
    raise AssertionError('bounded local path did not reach RET')
wb=(R/'wrapper.bin').read_bytes();cases=[dict(name='returning-zero',path=path(wb,True)),dict(name='returning-nonzero',path=path(wb,False))]
assert not cases[0]['path']['initializer'] and cases[1]['path']['initializer']
mut=bytearray(wb);off=0x3845BB-0x384580;assert mut[off]==0x74;mut[off]=0x75
mutcase=path(bytes(mut),True);assert mutcase['initializer'] and sha(mut)!=sha(wb)
(R/'labelled-je-to-jne.bin').write_bytes(mut)
# Exact caller interval after wrapper returns, through the memset call.
caller=[i for i in ii.values() if 0x39266F<=i.address<=0x39267E]
assert [i.address for i in caller]==[0x39266F,0x392672,0x392674,0x392677,0x39267E]
assert [i.mnemonic for i in caller]==['movsxd','xor','mov','mov','call']
assert ii[0x39266F].op_str=='r8, ebx' and ii[0x392672].op_str=='edx, edx' and ii[0x392674].op_str=='rcx, rax' and imm(0x39267E)==0x861EC0
store=ii[0x392677];o=store.operands[0];assert o.type==capstone.CS_OP_MEM and roles.op_kind(store,o,0)=='w' and store.operands[1].type==capstone.CS_OP_REG and store.reg_name(store.operands[1].reg)=='rax'
cell=store.address+store.size+o.mem.disp;assert cell==0x2AEE0A0
bb=(R/'builder.bin').read_bytes();destmut=bytearray(bb);p=0x392674-0x3924B0;assert destmut[p:p+3]==bytes.fromhex('488bc8');destmut[p+2]=0xCB
mi=next(cs.disasm(bytes(destmut[p:p+3]),0x392674));assert mi.op_str=='rcx, rbx' and mi.op_str!=ii[0x392674].op_str
(R/'labelled-clear-destination.bin').write_bytes(destmut)
# Resolve the original thunk's IAT through the actual import descriptor.
th=ii[0x861EC0];o=th.operands[0];iat=th.address+th.size+o.mem.disp
pe=struct.unpack_from('<I',d,0x3C)[0];ir,size=struct.unpack_from('<II',d,pe+24+112+8)
rva=lambda a,n:rd.img_rd(d,ss,rd.IMG_LO+a,n)
bind=[]
for off in range(0,size,20):
    desc=rva(ir+off,20);oft,_,_,dn,ft=struct.unpack('<IIIII',desc)
    if not ft:break
    for k in range(1000):
        lookup=rva(oft+8*k,8);v=struct.unpack('<Q',lookup)[0]
        if not v:break
        if rd.IMG_LO+ft+8*k==iat:
            assert not v>>63;dll=rva(dn,80).split(b'\0')[0];fn=rva(v+2,80).split(b'\0')[0]
            bind.append(dict(iat=hex(iat),descriptor_va=hex(rd.IMG_LO+ir+off),descriptor_hex=desc.hex(),lookup_va=hex(rd.IMG_LO+oft+8*k),lookup_hex=lookup.hex(),name_va=hex(rd.IMG_LO+v),name_hex=rva(v,2+len(fn)+1).hex(),dll_va=hex(rd.IMG_LO+dn),dll_hex=(dll+b'\0').hex(),dll=dll.decode(),name=fn.decode()))
assert len(bind)==1 and bind[0]['name']=='memset'
consumers=[]
for name,path,selection in [('corridor-preimage.md','Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-corridor-query-family.md','all'),('rebuild-preimage.md','Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md','rebuild'),('nav-fields-preimage.tsv','Database/FFXII TZA/_types/fields.tsv','fields')]:
    b=Path(path).read_bytes();lines=b.splitlines(keepends=True)
    kept=b if selection=='all' else b''.join(x for x in lines if (b'| grid rebuild |' in x if selection=='rebuild' else x==lines[0] or x.startswith(b'NavGridParams\t')))
    assert kept;(R/name).write_bytes(kept);consumers.append(dict(path=path,full_source_sha256=sha(b),retained=name,retained_sha256=sha(kept),scope=selection))
assert sha(reader.read_bytes())==raw['reference']['reader_sha256'] and sha(policy.read_bytes())==raw['reference']['policy_sha256']
result=dict(method='A source/conditional CFG/ABI boundary only; zero FF12/native/emulator/live instructions',reference=raw['reference'],driver_sha256=raw['driver_sha256'],cases=cases,source_controls=dict(branch=dict(site=hex(0x3845BB),original='je',private='jne',null_path=mutcase,original_binding_rejects=True),destination=dict(site=hex(0x392674),original='rcx, rax',private='rcx, rbx',original_binding_rejects=True)),memset_import=bind[0],caller=dict(pcs=[hex(i.address) for i in caller],base_store=hex(cell),store_before_call=True,conditional_guard=False,destination='wrapper-return RAX',fill='zero',length='sign-extension of original low32 total in EBX',allocator_input='ECX low32 total, zero-extended register; downstream allocator interpretation not proved'),consumers=consumers,limits='Conditional on opaque allocator/initializer/synchronizers returning conformingly and preserving nonvolatile RBX. No actual null return/OOM/fault/loaded CRT/lock semantics/lifetime/leak/global readiness/normal reachability/whole malformed safety. Caller partial published base and dimensions are source-order facts; actual callback or cross-thread effects unknown.',cleanup='Reference and peer source readback unchanged; no process/game/input/memory/hook/save/config writes; private changed bytes data only.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('CAPTURE_STATIC_RETURN_BOUNDARY returning-zero skips init then caller publishes base/calls clear; nonzero initializes; source branch/destination controls discriminate; no runtime/OOM proof')
