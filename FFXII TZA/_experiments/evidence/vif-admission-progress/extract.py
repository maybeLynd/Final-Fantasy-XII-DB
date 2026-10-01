import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
rb=reader.read_bytes();sp=importlib.util.spec_from_file_location('existing_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies=[]
for a,n in [(0x22C940,43),(0x22C970,533),(0x22BFF0,2268)]:
 b=m.img_rd(raw,secs,a,n);ins=list(cs.disasm(b,a));assert sum(i.size for i in ins)==n and ins[-1].mnemonic=='ret'
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
(HERE/'retained').mkdir(exist_ok=True)
(HERE/'retained'/'existing-reader.py').write_bytes(rb)
p=Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md');pb=p.read_bytes();(HERE/'retained'/'consumer-preimage.md').write_bytes(pb)
(HERE/'primary.json').write_text(json.dumps({'method':'A exact shipping instructions and bounded control-flow derivation; no execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,'bodies':bodies,
 'consumer':{'path':p.as_posix(),'sha256':sha(pb)},'limits':'Supplied positive lengths/NUM and zero/one WL comparison. No live occurrence, authored invalid packet, actual exception or presentation.'},indent=2)+'\n')
print('Three original bodies preserved. No original-code or live run.')
