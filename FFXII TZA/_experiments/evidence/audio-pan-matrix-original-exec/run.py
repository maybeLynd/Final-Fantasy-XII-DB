"""Bounded original pan-matrix execution. No FF12 process, OS audio, or native calls.

Reuse the image/guest-memory pattern already used by EXP115. No function is stubbed.
The shipping pan/trig instructions and normal cookie-check path execute in Unicorn.
All inputs and stack/output objects are controlled fixtures, not live initialization.
"""
import argparse,ctypes,hashlib,json,math,platform,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn import Uc,UC_ARCH_X86,UC_MODE_64,UC_PROT_ALL,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.x86_const import *

E=Path(__file__).resolve().parent;R=E.parents[4]
sys.path.insert(0,str(R/'Database/Tools/analysis-kit/gfz-scripts'))
from disasm_fn import Image
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
PAN=0x7B8430;COOKIE=0x808C40;SENTINEL=0x62000000;STACK=0x61000000;OUT=0x40000100
BODIES=[(PAN,1895),(0x7B8BA0,217),(0x7B8C80,192),(COOKIE,33)]
pack=lambda f:struct.pack('<f',f)
fbits=lambda f:struct.unpack('<I',pack(f))[0]
sha=lambda b:hashlib.sha256(b).hexdigest()
NONVOL=[UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15]

class Guest:
    # Windows Unicorn mem_map_ptr pattern from EXP115; buffers stay alive with the Uc.
    def __init__(self,u):self.u=u;self.buffers=[];self.regions=[]
    def map(self,a,n,data=b''):
        buf=ctypes.create_string_buffer(n);self.buffers.append(buf)
        if data:ctypes.memmove(buf,data,len(data))
        self.u.mem_map_ptr(a,n,UC_PROT_ALL,ctypes.addressof(buf))
        self.regions.append((a,n,ctypes.addressof(buf)))
    def ptr(self,a,n):
        for base,size,p in self.regions:
            if base<=a and a+n<=base+size:return p+a-base
        raise ValueError(f'unmapped fixture access {a:X}/{n}')
    def write(self,a,b):ctypes.memmove(self.ptr(a,len(b)),b,len(b))
    def read(self,a,n):return ctypes.string_at(self.ptr(a,n),n)

def provenance(im):
    assert sha(im.d)==SHA and im.base==0x120000
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);rows=[]
    for a,n in BODIES:
        raw=im.read(a,n);ins=list(md.disasm(raw,a))
        assert sum(i.size for i in ins)==n
        rows.append(dict(address=f'{a:08X}',size=n,raw=raw.hex(),sha256=sha(raw),instructions=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]))
    return dict(executable_sha256=SHA,image_base=f'{im.base:08X}',bodies=rows,
                python=sys.version,unicorn=unicorn.__version__,capstone=capstone.__version__,host=platform.platform(),
                entry_abi='XMM0 pan, XMM1 frpan, XMM2 udpan, XMM3 center; entry RSP+28 lfe, +30 source count, +38 source index, +40 output count, +48 output pointer, +50 spread',
                limits=['Supplied ABI, file-backed shipping data, synthetic stack/output and register state.',
                        'No stubs. Normal original cookie check executes; its failure destination is forbidden.',
                        'No Sound/MaterialTrack initialization, parent combiner, real cue waveform, hardware mapping, scheduling or audible output.',
                        'MXCSR=0x1F80; not a claim about live thread FP control. Only finite tested arguments.'])

def execute(im,case,budget=12000,mutation=None):
    u=Uc(UC_ARCH_X86,UC_MODE_64);g=Guest(u);ranges=[]
    for name,va,vs,ra,rs in im.secs:
        if rs:
            g.map(im.base+va,(rs+4095)&~4095,im.d[ra:ra+rs]);ranges.append((im.base+va,im.base+va+rs))
    g.map(STACK,0x20000);g.map(OUT&~4095,4096,b'\xA5'*4096);g.map(SENTINEL,4096,b'\xCC')
    if mutation=='suppress-rear-half-turn':
        assert g.read(0x7B8769,4)==bytes.fromhex('f30f58f0');g.write(0x7B8769,b'\x90'*4)
    rsp=STACK+0x10008
    g.write(rsp,struct.pack('<Q',SENTINEL))
    for off,raw in [(0x28,pack(case.get('lfe',0.0))),(0x30,struct.pack('<i',case['sources'])),
                    (0x38,struct.pack('<i',case['channel'])),(0x40,struct.pack('<i',2)),
                    (0x48,struct.pack('<Q',OUT)),(0x50,pack(case.get('spread',0.0)))]:g.write(rsp+off,raw)
    u.reg_write(UC_X86_REG_RSP,rsp);u.reg_write(UC_X86_REG_EFLAGS,0x202);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
    for reg,value in zip([UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3],[case['pan'],case['frpan'],case.get('udpan',0.0),case.get('center',0.0)]):u.reg_write(reg,fbits(value))
    saved={reg:0xAA00000000000000+reg for reg in NONVOL}
    for reg,value in saved.items():u.reg_write(reg,value)
    saved_xmm={getattr(sys.modules[__name__],f'UC_X86_REG_XMM{i}'):int.from_bytes(bytes([i])*16,'little') for i in range(6,16)}
    for reg,value in saved_xmm.items():u.reg_write(reg,value)
    state=dict(instructions=0,reached_return=False,errors=[],calls=[],trace=[],writes=[],image_reads=set())
    def code(uc,a,size,data):
        if a==SENTINEL:state['reached_return']=True;uc.emu_stop();return
        if not any(lo<=a and a+size<=lo+n for lo,n in BODIES):
            state['errors'].append(f'code escape {a:08X}');uc.emu_stop();return
        state['instructions']+=1;state['trace'].append(f'{a:08X}')
        if a in [lo for lo,n in BODIES]:state['calls'].append(f'{a:08X}')
        if a==COOKIE:
            wanted=struct.unpack('<Q',g.read(0x1F44830,8))[0]
            if uc.reg_read(UC_X86_REG_RCX)!=wanted:state['errors'].append('cookie mismatch');uc.emu_stop()
    def write(uc,access,a,size,value,data):
        if OUT<=a and a+size<=OUT+8:
            state['writes'].append(dict(pc=f'{uc.reg_read(UC_X86_REG_RIP):08X}',address=f'{a:08X}',size=size,value=value & ((1<<(size*8))-1)))
        elif not (STACK<=a and a+size<=STACK+0x20000):state['errors'].append(f'unexpected write {a:08X}/{size}');uc.emu_stop()
    def read(uc,access,a,size,value,data):
        if any(lo<=a and a+size<=hi for lo,hi in ranges):state['image_reads'].add((a,size))
        elif not ((STACK<=a and a+size<=STACK+0x20000) or (OUT<=a and a+size<=OUT+8)):
            state['errors'].append(f'read outside original/fixture state {a:08X}/{size}');uc.emu_stop()
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write);u.hook_add(UC_HOOK_MEM_READ,read)
    try:u.emu_start(PAN,SENTINEL+1,count=budget)
    except unicorn.UcError as ex:state['errors'].append(str(ex))
    state['stack_restored']=u.reg_read(UC_X86_REG_RSP)==rsp+8
    state['nonvolatile_restored']=all(u.reg_read(reg)==v for reg,v in {**saved,**saved_xmm}.items())
    state['canaries_intact']=g.read(OUT-32,32)==b'\xA5'*32 and g.read(OUT+8,32)==b'\xA5'*32
    state['return_value']=u.reg_read(UC_X86_REG_RAX)&0xFFFFFFFF
    state['gain_bits']=[f'{v:08X}' for v in struct.unpack('<2I',g.read(OUT,8))]
    state['gains']=list(struct.unpack('<2f',g.read(OUT,8)))
    state['image_reads']=[dict(address=f'{a:08X}',size=n,raw=g.read(a,n).hex()) for a,n in sorted(state['image_reads'])]
    state['case']=case;state['budget']=budget;state['mutation']=mutation
    state['valid']=bool(state['reached_return'] and not state['errors'] and state['stack_restored'] and state['nonvolatile_restored'] and state['canaries_intact'] and state['return_value']==0 and state['writes'] and f'{COOKIE:08X}' in state['calls'] and all(math.isfinite(v) for v in state['gains']))
    return state

def cases():
    result=[]
    def c(name,pan,frpan,sources=1,channel=0,spread=0,**kw):
        result.append(dict(id=name,pan=pan,frpan=frpan,sources=sources,channel=channel,spread=spread,**kw))
    c('mono-front-center',0,1);c('mono-output1-control',.5,1);c('mono-output0-control',-.5,1)
    c('mono-at-listener-control',.31,0);c('mono-udpan-control',0,1,udpan=1)
    for byte in [127,128,191,215,240,250,255]:
        pan=(byte-64)/128 if byte<128 else (191-byte)/128;fr=1 if byte<128 else -1
        c(f'mono-byte-{byte}',pan,fr,byte=byte)
    c('mono-byte-240-mirror-input',49/128,-1)
    for spread in [-1,0,.5,1,2]:
        for ch in [0,1]:c(f'stereo-byte-240-spread-{spread}-ch-{ch}',-49/128,-1,2,ch,spread,byte=240)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['feasibility','full'],required=True);a=p.parse_args()
    path=E/(a.phase+'.json');assert not path.exists(),'Preserve prior raw run; choose a new explicit campaign after inspecting failure.'
    im=Image(R/'Database/Tools/work/exe/FFXII_TZA.exe');identity=provenance(im)
    chosen=cases()[:3] if a.phase=='feasibility' else cases()
    result=[execute(im,c) for c in chosen]
    controls=[]
    if a.phase=='full':
        controls=[execute(im,cases()[0],budget=1),execute(im,next(c for c in cases() if c['id']=='mono-byte-240'),mutation='suppress-rear-half-turn')]
    raw=dict(identity=identity,method='B: isolated original machine code with supplied inputs; no game/audio output',rows=result,controls=controls)
    path.write_text(json.dumps(raw,indent=2)+'\n')
    for r in result:print(r['case']['id'],r['valid'],r['gain_bits'],r['gains'],r['errors'])
    assert result and all(r['valid'] for r in result),'Invalid execution retained; stop and diagnose before further cases.'
if __name__=='__main__':main()
