import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('existing_image_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies=[]
for a,n in [(0x3EAB90,71),(0x3EAA70,229)]:
 b=m.img_rd(raw,secs,a,n);ins=list(cs.disasm(b,a));assert sum(i.size for i in ins)==n and ins[-1].mnemonic=='ret'
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
refs=['Database/FFXII TZA/18-Audio/the-music-control-file-and-the-bgm-stream.md',
 'Database/FFXII TZA/18-Audio/CONTRACT-music-control-file-and-bgm-stream.md',
 'Database/FFXII TZA/18-Audio/CONTRACT-field-music-selection.md',
 'Database/FFXII TZA/_experiments/evidence/field-music-selection-exec/check.py',
 'Database/FFXII TZA/_experiments/evidence/field-music-selection-exec/result.json']
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 b=Path(p).read_bytes();name=f'{i:02d}-'+Path(p).name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p,'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A original-code and retained EXP099 analysis; no new execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,'bodies':bodies,'refs':pins,
 'limits':'Nonnegative small maxFieldId witnesses. Exact write-loop extent and inclusive reader. No fresh execution, loader delivery, allocation placement, real table occurrence, game fault or lifetime claim.'},indent=2)+'\n')
print('Original callback/reader and retained producer-free fixture/result pinned; no EXP099 replay.')
