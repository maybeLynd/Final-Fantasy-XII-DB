import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
spec=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
raw,sections=reader.load_image();assert sha(raw)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
b=reader.img_rd(raw,sections,0x3977B0,349)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ii=list(cs.disasm(b,0x3977B0))
assert sum(i.size for i in ii)==349 and ii[-1].address==0x39790C and ii[-1].mnemonic=='ret'
page=Path('Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md')
pb=page.read_bytes();(R/page.name).write_bytes(pb)
s=dict(method='A complete shipping body and decoded source; conditional calculations only, no execution',exe_sha256=sha(raw),image_base='0x120000',entry='0x3977b0',bytes=len(b),sha256=sha(b),raw_hex=b.hex(),
 instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii],
 reader=dict(path=rp.as_posix(),sha256=sha(rp.read_bytes())),tools=dict(python=sys.version,capstone=capstone.__version__),
 consumer=dict(path=page.as_posix(),sha256=sha(pb),bytes=len(pb),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),
 cleanup='No game process, control/instrument/reference/save/config mutation. PC OFF.')
(W/'source.json').write_text(json.dumps(s,indent=2)+'\n')
print('Captured complete349B source, original identity and current consumer; A only.',flush=True)
