"""Retain exact original source and consumer preimages. Static, not execution."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
readerpath=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
assert sha(readerpath.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
spec=importlib.util.spec_from_file_location('shipping_reader',readerpath);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
image,sections=reader.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_module_sha256=sha(Path(capstone.__file__).read_bytes()),dll_path=str(capstone._cs._name),dll_sha256=sha(Path(capstone._cs._name).read_bytes()))
bodies=[]
for name,va,n,expected in [('save',0x36D930,89,'ebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda'),('restore',0x36D8E0,66,'5bb9d143a12bf8959ae1c75d5f7245c4b1081d9ae3432095ebfd253953ec253b')]:
 raw=reader.img_rd(image,sections,va,n);assert sha(raw)==expected
 ii=list(cs.disasm(raw,va));assert sum(i.size for i in ii)==n and ii[-1].mnemonic=='ret'
 rows=[]
 for i in ii:
  rip=[i.address+i.size+o.mem.disp for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86.X86_REG_RIP]
  rows.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,rip_targets=[hex(x) for x in rip]))
 bodies.append(dict(name=name,entry=hex(va),size=n,sha256=sha(raw),raw_hex=raw.hex(),instructions=rows))
consumers=[]
for src,name in [(readerpath,'shipping-reader.py'),(Path('Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md'),'contract.md'),(Path('Reconstruction/Tests/Differential/diff_workbench_save.py'),'existing-differential.py'),(Path('Database/FFXII TZA/_index/candidates/s05-runtime-what-has-run.md'),'prior-runtime-summary.md')]:
 raw=src.read_bytes();assert not (R/name).exists(),'Do not replace retained preimages';(R/name).write_bytes(raw)
 try:headraw=subprocess.check_output(['git','show','HEAD:'+src.as_posix()],stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError:headraw=None
 consumers.append(dict(path=src.as_posix(),retained=name,sha256=sha(raw),head_sha256=sha(headraw) if headraw is not None else None,working_matches_head=headraw is not None and raw.replace(b'\r\n',b'\n')==headraw.replace(b'\r\n',b'\n')))
source=dict(method='A original-source static proof; no new B/C run',reference=dict(exe_sha256=sha(image),image_base='0x120000',reader_path=readerpath.as_posix(),reader_sha256=sha(readerpath.read_bytes())),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),bodies=bodies,consumers=consumers,limits='Complete original leaves read, no execution/caller census/live state or universal alias characterization. Existing differential source retained but not rerun. Source predictions are conditional, not captured original runtime outcomes.',cleanup='No game/PC/attachment/save/config/reference writes; no live cleanup claimed.')
assert not (W/'source.json').exists();(W/'source.json').write_text(json.dumps(source,indent=2)+'\n')
print('Retained exact89/66B and primary consumer/old-harness preimages; method A.',flush=True)
