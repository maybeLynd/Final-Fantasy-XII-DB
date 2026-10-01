"""Retained exact source/constant/graph/control replay; no original-code execution."""
import hashlib,importlib.util,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained'
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference']
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
raw=(R/'source.bin').read_bytes()
assert ref['entry']=='0x339630' and ref['bytes']==len(raw)==1061 and sha(raw)==ref['body_sha256']=='8a75e847cb7520bb1e19c64607ac094482fb0ad6ba8c825c7a8f8c363478d1f6'
assert sha((W/'derive.py').read_bytes())==r['driver_sha256']
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
assert sha((R/'reg_tracking.py').read_bytes())==ref['policy_sha256']
sp=importlib.util.spec_from_file_location('retained_reviewed_policy',R/'reg_tracking.py');policy=importlib.util.module_from_spec(sp);sp.loader.exec_module(policy)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii={i.address:i for i in cs.disasm(raw,0x339630)}
assert sum(i.size for i in ii.values())==1061 and ii[0x339A54].mnemonic=='ret'
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()]
expected={0x339723:'f3440f100d0c9a5b00',0x339735:'f3440f101512259b01',0x339871:'6bc35a',0x339874:'660f6ec0',0x339878:'0f5bc0',0x33987B:'f3410f59c2',0x339880:'f3410f5ec1',0x339885:'e8e6320000'}
for pc,h in expected.items():assert ii[pc].bytes.hex()==h
assert ii[0x339885].operands[0].imm==0x33CB70
edges={}
for pc,i in ii.items():
    if i.mnemonic=='ret':dest=[]
    elif i.mnemonic.startswith('j'):
        assert i.operands[0].type==capstone.CS_OP_IMM
        dest=[i.operands[0].imm] if i.mnemonic=='jmp' else [pc+i.size,i.operands[0].imm]
    else:dest=[pc+i.size]
    assert all(d in ii for d in dest)
    edges[pc]=dest
assert r['edges']=={hex(pc):[hex(d) for d in dest] for pc,dest in edges.items()}
def reaches(blocked=()):
    seen=set();todo=[0x339630]
    while todo:
        pc=todo.pop()
        if pc in seen or pc in blocked:continue
        seen.add(pc);todo.extend(edges[pc])
    return 0x339880 in seen
assert reaches() and not reaches((0x339723,)) and not reaches((0x339735,)) and reaches((0x339A02,))
assert [pc for pc,i in ii.items() if 'xmm9' in policy.written(i)]==[0x339723,0x339A02]
assert [pc for pc,i in ii.items() if 'xmm10' in policy.written(i)]==[0x339735,0x3399F9]
assert edges[0x339958]==[0x33995E,0x339781]
observed=[]
for pc in (0x33971A,0x339723,0x339735,0x339A02):
    i=ii[pc]
    for k,o in enumerate(i.operands):
        if o.type==capstone.CS_OP_MEM:observed.append(dict(pc=hex(pc),operand=k,kind=policy.op_kind(i,o,k),width=o.size,base=i.reg_name(o.mem.base),disp=o.mem.disp))
assert observed==r['focused_memory_roles'] and [x['kind'] for x in observed]==['w','r','r','r']
for c,name,want in zip(r['constants'],('degrees.bin','pi.bin'),(0x8F3138,0x1CEBC50)):
    i=ii[int(c['load'],16)]
    assert i.address+i.size+i.operands[1].mem.disp==want==int(c['address'],16)
    assert (R/name).read_bytes().hex()==c['bytes_hex']
assert r['constants'][0]['bytes_hex']=='00003443' and r['constants'][0]['f32']==180.0 and r['constants'][1]['bytes_hex']=='db0f4940' and 3<r['constants'][1]['f32']<4
m=r['mutation_control'];mut=bytearray(raw)
assert m['offset']==0x339723-0x339630+4 and m['original_byte']==0x0D and m['mutant_byte']==5
mut[m['offset']]=m['mutant_byte'];mi={i.address:i for i in cs.disasm(mut,0x339630)}
assert mi[0x339723].op_str.startswith('xmm8,') and mi[0x339723].size==9 and mi[0x339723].address+mi[0x339723].size+mi[0x339723].operands[1].mem.disp==0x8F3138
assert [pc for pc,i in mi.items() if 'xmm9' in policy.written(i)]==[0x339A02]
assert sha(mut)==m['mutant_body_sha256'] and sha(mut)!=sha(raw) and m['constant_reaching_definition_missing'] and m['original_body_binding_rejected']
assert r['abi']['source']=='https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170' and 'assumption' in r['abi']
assert sha((R/'maths-preimage.md').read_bytes())==r['consumer']['sha256']
assert json.loads((R/'catalog-identity.json').read_text())['row']['body_bytes']=='1061'
if (W/'manifest.json').exists():
    members=json.loads((W/'manifest.json').read_text())['members'];assert members
    for x in members:
        data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_SOURCE_APPROACH_DIVISOR original180/pi/localdominance/loop/save-restore/actualsharedpolicy/source-destination-control, conformingcalleeABI explicit; no native/live/allangle-domain proof')
