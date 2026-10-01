"""Bounded B counterexample: unchanged deposits can accompany real instruction execution.

Reuses EXP-115 World and verified shipping instructions; no live process and no
reconstructed implementation. Does not run or overwrite EXP-115's campaign.
"""
import hashlib, importlib.util, json, struct
from pathlib import Path
import capstone, unicorn
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP, UC_X86_REG_RSP

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
source=HERE/'sources/exp115-check.py'
spec=importlib.util.spec_from_file_location('exp115_reuse',source)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
h.EXE=str(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe')
raw,sections=h.load_image()
body=h.img_rd(raw,sections,h.TPT,377)
assert sha(body)=='1965049e479872fa5d23d2688a53f733287f98bb0e63c9843e86f2f17be2eb26'
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
ins=list(md.disasm(body,h.TPT));assert len(ins)==68 and sum(i.size for i in ins)==377
starts=[i.address for i in ins]
assert ins[-1].mnemonic=='ret' and not any(i.mnemonic.startswith('call') for i in ins)
case={'entry':h.TPT}
world=h.World(case,raw,sections)
uc,gm=world.uc,world.gm
slots=[h.SCR,h.INCPY,h.OUTCPY,h.OUTG]
trace=[];writes=[]
def code(uc,addr,size,unused):
    assert addr in starts,'unexpected executed address '+hex(addr)
    trace.append(addr)
def write(uc,access,addr,size,value,unused):
    if any(addr < s+16 and s < addr+size for s in slots):
        writes.append({'pc':hex(uc.reg_read(UC_X86_REG_RIP)),
                       'address':hex(addr),'bytes':size,'before':gm.r(addr,size).hex()})
uc.hook_add(UC_HOOK_CODE,code)
uc.hook_add(UC_HOOK_MEM_WRITE,write)
def snapshot():return {hex(s):gm.r(s,16).hex() for s in slots}
results=[]
for label in ('seed','same-input-repeat','changed-input-control'):
    if label=='changed-input-control':h.vec_w(gm,h.INBUF,[4.0,-2.0,0.5,7.0])
    before=snapshot();trace.clear();writes.clear()
    assert gm.r(h.TPT,377)==body
    # Microsoft x64 function entry: return address, rsp % 16 == 8, mapped
    # shadow space and stack. Both argument buffers are aligned and disjoint.
    rsp=h.STACK+0x80008;gm.w(rsp,h.qw(h.RETQ))
    uc.reg_write(UC_X86_REG_RSP,rsp)
    uc.reg_write(UC_X86_REG_RCX,h.INBUF);uc.reg_write(UC_X86_REG_RDX,h.OUTBUF)
    input_raw=gm.r(h.INBUF,16).hex();matrix_raw=gm.r(h.M,64).hex()
    leaf_raw=gm.r(h.LEAF_G,16).hex()
    uc.emu_start(h.TPT,h.RETQ,count=100)
    assert uc.reg_read(UC_X86_REG_RIP)==h.RETQ and uc.reg_read(UC_X86_REG_RSP)==rsp+8
    assert not world.faults and trace==starts
    assert gm.r(h.TPT,377)==body and gm.r(h.M,64).hex()==matrix_raw
    assert gm.r(h.LEAF_G,16).hex()==leaf_raw
    covered=set()
    for w in writes:covered.update(range(int(w['address'],16),int(w['address'],16)+w['bytes']))
    assert all(set(range(s,s+16))<=covered for s in slots)
    after=snapshot()
    changed={s:sum(a!=b for a,b in zip(bytes.fromhex(before[s]),bytes.fromhex(after[s]))) for s in before}
    assert (not any(changed.values())) if label=='same-input-repeat' else all(changed.values())
    assert gm.r(h.OUTBUF,16).hex()==after[hex(h.OUTG)]==after[hex(h.OUTCPY)]
    results.append(dict(label=label,input=input_raw,matrix=matrix_raw,leaf=leaf_raw,
                        before=before,after=after,changed_bytes=changed,
                        instruction_trace=[hex(a) for a in trace],deposit_writes=list(writes),
                        returned=True,output=gm.r(h.OUTBUF,16).hex()))
assert len(results)==3 and results[0]['after']==results[1]['before']==results[1]['after']
out=dict(status='COUNTEREXAMPLE_VALID_ISOLATED_ORIGINAL_CODE',method='B',live_game=False,
         executable_sha256=sha(raw),source_sha256=sha(source.read_bytes()),
         unicorn_version=unicorn.__version__,capstone_version=capstone.__version__,
         body=dict(address=hex(h.TPT),bytes=377,sha256=sha(body),raw=body.hex(),
                   instructions=[dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]),
         cases=results,stubs_reached=[],faults=world.faults,
         limits=['Controlled matrix/input/vf00 and direct entry; no live initialization, callers or scheduling.',
                 'Same-value execution falsifies the no-execution inference, not the historical unchanged-value report.',
                 'Original EXP115 World maps other code/boundaries, but only the 68 leaf instructions execute here.'])
(HERE/'transform-counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
print('Three isolated original-body calls returned; each executed all68 instructions and wrote all64 deposit bytes.')
print('Same-input repeat changed0 deposit bytes; seed and changed-input controls changed every slot.')
