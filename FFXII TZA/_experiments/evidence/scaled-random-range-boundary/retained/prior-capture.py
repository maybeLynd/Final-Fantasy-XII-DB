"""Bounded execution of original scaled-random arithmetic, no native calls/live game."""
import hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
parent=Path('Database/FFXII TZA/_experiments/evidence/procedural-mode-cost')
manifest=json.loads((parent/'manifest.json').read_text())
for m in manifest['members']:
 b=(parent/m['path']).read_bytes();assert len(b)==m['bytes'] and sha(b)==m['sha256']
pb=(parent/'source.json').read_bytes();s=json.loads(pb);body=bytes.fromhex(s['raw_hex'])
assert sha(body)=='32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a'
rp=Path(s['reader']['path']);assert sha(rp.read_bytes())==s['reader']['sha256']
spec=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
image,sections=reader.load_image();assert sha(image)==s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert reader.img_rd(image,sections,0x3D8E50,418)==body
one=reader.img_rd(image,sections,0x1EF93FC,4);assert one==bytes.fromhex('0000803f')
ENTRY,END=0x3D8F3F,0x3D8F79;code=body[ENTRY-0x3D8E50:END-0x3D8E50];assert len(code)==58
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
ii=list(cs.disasm(code,ENTRY));assert sum(i.size for i in ii)==len(code)
assert [(i.address,i.mnemonic) for i in ii if i.mnemonic in ('mulss','subss')]==[(0x3D8F52,'mulss'),(0x3D8F5D,'mulss'),(0x3D8F6D,'subss')]
for n,b in [('parent-source.json',pb),('parent-manifest.json',(parent/'manifest.json').read_bytes()),('shipping-reader.py',rp.read_bytes()),('window.bin',code),('one.bin',one)]:
 assert not (R/n).exists(),'capture once; do not replace historical evidence';(R/n).write_bytes(b)
page=Path('Database/FFXII TZA/21-RNG-And-Determinism/rng-streams.md');pagebytes=page.read_bytes();(R/'rng-streams.md').write_bytes(pagebytes)
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
floating=lambda x:struct.unpack('<f',struct.pack('<I',x))[0]
bits=lambda x:struct.unpack('<I',struct.pack('<f',x))[0]
SAMPLE=0x3F900001
def model(a,sample):
 a,v=floating(a),floating(sample)
 return dict(original_order=bits(f32(f32(a*v)-f32(a*1.0))),factored=bits(f32(a*f32(v-1.0))))
def run(name,a,mutant=False):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for p in (ENTRY&~4095,0x1EF9000,0x22D8000,0x22D9000,0x60001000):u.mem_map(p,4096)
 running=bytearray(code)
 if mutant:
  off=0x3D8F6D-ENTRY;assert running[off:off+4]==bytes.fromhex('f30f5cc8');running[off+2]=0x58 # ADDSS control instead of SUBSS
 u.mem_write(ENTRY,bytes(running));u.mem_write(0x1EF93FC,one)
 rsp=0x60001800;u.mem_write(rsp+0x30,a.to_bytes(4,'little'))
 for p,n in ((0x22D8F30,16),(0x22D91A0,16),(0x22D92E0,16)):u.mem_write(p,b'\xa5'*n)
 u.reg_write(UC_X86_REG_RSP,rsp);u.reg_write(UC_X86_REG_XMM1,SAMPLE);u.reg_write(UC_X86_REG_MXCSR,0x1F80)
 before={hex(p):bytes(u.mem_read(p,n)).hex() for p,n in ((0x22D8F30,16),(0x22D91A0,16),(0x22D92E0,16),(rsp+0x30,4),(0x1EF93FC,4))}
 visited=[];pending=[];writes=[];raw_writes=[];reads=[]
 def flush():
  if not pending:return
  pc=pending[0][0];assert all(p==pc for p,_,_ in pending)
  lo=min(a for _,a,n in pending);hi=max(a+n for _,a,n in pending)
  assert {j for _,a,n in pending for j in range(a,a+n)}==set(range(lo,hi))
  writes.append(dict(pc=hex(pc),address=hex(lo),bytes=bytes(u.mem_read(lo,hi-lo)).hex()));pending.clear()
 def oncode(uc,pc,n,_):flush();visited.append(pc)
 def onwrite(uc,t,addr,n,v,_):
  pc=uc.reg_read(UC_X86_REG_RIP);pending.append((pc,addr,n))
  raw_writes.append(dict(pc=hex(pc),address=hex(addr),size=n,provider_value=v))
 def onread(uc,t,addr,n,v,_):reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(addr),size=n))
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread)
 failure=None
 try:u.emu_start(ENTRY,END,count=64);flush()
 except Exception as e:failure=repr(e)
 out=u.reg_read(UC_X86_REG_XMM1)&0xFFFFFFFF
 return dict(name=name,intervention='Fixture branch patch SUBSS->ADDSS' if mutant else 'Injected arithmetic-window entry state; original instructions unchanged',
  mutated=mutant,input=dict(amplitude_bits=hex(a),sample_bits=hex(SAMPLE),entry=hex(ENTRY),stop=hex(END),rsp=hex(rsp),mxcsr='0x1f80'),
  running_code_sha256=sha(bytes(running)),before=before,visited=[hex(x) for x in visited],raw_writes=raw_writes,writes=writes,reads=reads,
  after={hex(p):bytes(u.mem_read(p,n)).hex() for p,n in ((0x22D8F30,16),(0x22D91A0,16),(0x22D92E0,16),(rsp+0x30,4),(0x1EF93FC,4))},
  output_bits=hex(out),model={k:hex(v) for k,v in model(a,SAMPLE).items()},
  stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp_after=hex(u.reg_read(UC_X86_REG_RSP)),mxcsr_after=hex(u.reg_read(UC_X86_REG_MXCSR)),failure=failure)
cases=[run('finite-amplitude-order-discriminator',0x3E99999A),run('power-of-two-nondiscriminating-control',0x3F000000),run('subtract-to-add-detection-control',0x3E99999A,True)]
receipt=dict(method='B isolated verified original58B arithmetic window; controlled state, no native calls/live game',
 reference=dict(exe_sha256=s['exe_sha256'],image_base=s['image_base'],parent_entry=s['entry'],parent_body_sha256=sha(body),parent_source_sha256=sha(pb),parent_manifest_sha256=sha((parent/'manifest.json').read_bytes()),window_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),one_va='0x1ef93fc',one_hex=one.hex()),
 tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,unicorn_module_sha256=sha(Path(unicorn.__file__).read_bytes())),
 driver_sha256=sha(Path(__file__).read_bytes()),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii],cases=cases,
 failed_discriminator=dict(amplitude_bits='0x3e99999a',sample_bits='0x3fb90003',prediction={k:hex(v) for k,v in model(0x3E99999A,0x3FB90003).items()},method='host-source prediction only, not new original recurrence execution'),
 consumer=dict(path=page.as_posix(),sha256=sha(pagebytes),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),
 limits='Injected finite sample and stack/scratch/MXCSR; entry skips branch/recurrence/native save and stops before second mode gate/restore/return. No real initialization, universal rounding mode, negative/subnormal amplitude, caller-flow or live rendering claim. Observed bits are emulator original-instruction evidence, not a reconstructed implementation fixture. No prior EXP070/071 rerun.',
 cleanup='Disposable emulator instances only. No PC/game/process attachment/save/config/reference writes; no live cleanup claimed.')
(W/'raw.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Preserved original-window observations and detection control; acceptance requires check.py.',flush=True)
