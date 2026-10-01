import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import capstone
from operand_direction import memory_role,POLICY_ID
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
spec=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
raw,sections=reader.load_image();assert sha(raw)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
b=reader.img_rd(raw,sections,0x3D8E50,418)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(b,0x3D8E50))
assert sum(i.size for i in ii)==418 and ii[-1].address==0x3D8FF1 and ii[-1].mnemonic=='ret'
refs=[];calls=[]
for i in ii:
 if i.mnemonic=='call':calls.append(dict(pc=hex(i.address),target=hex(i.operands[0].imm)))
 for k,o in enumerate(i.operands):
  if o.type==capstone.CS_OP_MEM and cs.reg_name(o.mem.base)=='rip':
   refs.append(dict(pc=hex(i.address),op=i.mnemonic,target=hex(i.address+i.size+o.mem.disp),width=o.size,capstone_access_flag=o.access,access=memory_role(i,k),operand=k))
page=Path('Database/FFXII TZA/21-RNG-And-Determinism/rng-streams.md');pb=page.read_bytes();(R/page.name).write_bytes(pb)
s=dict(method='A shipping original418B and mode/amplitude control-flow; no new execution',exe_sha256=sha(raw),image_base='0x120000',entry='0x3d8e50',bytes=len(b),sha256=sha(b),raw_hex=b.hex(),
 instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii],rip_references=refs,calls=calls,role_policy=POLICY_ID,
 reader=dict(path=rp.as_posix(),sha256=sha(rp.read_bytes())),tools=dict(python=sys.version,capstone=capstone.__version__),
 consumer=dict(path=page.as_posix(),sha256=sha(pb),bytes=len(pb),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),
 failed_hypothesis='NaN is same as zero at initial compare: REFUTED by JP3D8E60 before JNE. Candidate stopped, no new NaN run.',
 limits='Direct body mode-conditioned recurrence sites only; native scratch/copy calls not executed and not assumed inert. No whole-invocation/lifecycle/caller guarantee; PC OFF.')
(W/'source.json').write_text(json.dumps(s,indent=2)+'\n')
print('Retained complete418B/source/hash/current consumer; A only, native calls not executed.',flush=True)
