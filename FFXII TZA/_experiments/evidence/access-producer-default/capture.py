import hashlib,importlib.util,json,subprocess
from pathlib import Path
import capstone
# The private producer uses the published bounded adapter by DEFAULT. The old
# published capture/source stays immutable; its two role errors are corrected
# additively in procedural-mode-cost. Raw provider flags remain diagnostic only.
adapter_path=Path('Database/FFXII TZA/_experiments/evidence/procedural-mode-cost/operand_direction.py')
assert hashlib.sha256(adapter_path.read_bytes()).hexdigest()=='9a25d0a958cae6506e994213b11898ac17c6edf7a8f3eb79d958f073df1cde36'
adapter_spec=importlib.util.spec_from_file_location('matrix_capture_role_adapter',adapter_path)
adapter=importlib.util.module_from_spec(adapter_spec);adapter_spec.loader.exec_module(adapter)
memory_role,POLICY_ID=adapter.memory_role,adapter.POLICY_ID
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
c='fcbffd545c30575039e80afc272680d6d71e9a38'
p='Database/FFXII TZA/_experiments/evidence/gs-coordinate-conversion'
assert subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],capture_output=True).returncode==0
manifest=json.loads(subprocess.check_output(['git','show',c+':'+p+'/manifest.json']))
entry=next(m for m in manifest['members'] if m['path']=='source.json')
b=subprocess.check_output(['git','show',c+':'+p+'/source.json'])
assert len(b)==entry['bytes'] and sha(b)==entry['sha256']
(R/'gs-source.json').write_bytes(b)
gs=json.loads(b)
assert gs['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
bodies=[];memory=[];calls=[]
for a,n in [(0x217060,235),(0x202B70,31)]:
 old=next(x for x in gs['bodies'] if int(x['entry'],16)==a)
 raw=bytes.fromhex(old['raw_hex']);assert len(raw)==n and sha(raw)==old['sha256']
 ii=list(cs.disasm(raw,a));assert sum(i.size for i in ii)==n and ii[-1].mnemonic=='ret'
 bodies.append(old)
 for i in ii:
  if i.mnemonic=='call':calls.append(dict(pc=hex(i.address),destination=hex(i.operands[0].imm)))
  for k,o in enumerate(i.operands):
   if o.type==capstone.CS_OP_MEM:
    memory.append(dict(pc=hex(i.address),op=i.mnemonic,operand=k,
     base=cs.reg_name(o.mem.base),index=cs.reg_name(o.mem.index),disp=o.mem.disp,width=o.size,
     access=memory_role(i,k),capstone_access_flag=o.access,bytes=i.bytes.hex()))
refs=[]
for pth in [Path('Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md'),
 Path('Database/FFXII TZA/_experiments/EXP-219-kind1C-catchall-emit-internals-exec.md'),
 Path('Database/FFXII TZA/17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md')]:
 bb=pth.read_bytes();(R/pth.name).write_bytes(bb);refs.append(dict(path=pth.as_posix(),retained='retained/'+pth.name,bytes=len(bb),sha256=sha(bb)))
s=dict(method='A verified committed original bytes / decoded operands; arithmetic conditional, no new B/C',
 reference_commit=c,reference_source=p+'/source.json',reference_bytes=len(b),reference_sha256=sha(b),
 exe_sha256=gs['exe_sha256'],image_base=gs['image_base'],capstone_version=capstone.__version__,
 bodies=bodies,memory_operands=memory,calls=calls,consumer_preimages=refs,role_policy=POLICY_ID,
 limits='Prior source B provenance retained; new alias conclusions derive from original ordering, NOT an executed alias fixture/native game/caller/ownership observation.')
(W/'source.json').write_text(json.dumps(s,indent=2)+'\n')
print('Retained exact235B leaf/31B wrapper and decoded memory/call ordering; method A, no execution.',flush=True)
