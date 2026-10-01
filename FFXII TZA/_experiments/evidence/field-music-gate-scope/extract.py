import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies=[]
for a,n,scope in [(0x265270,28,'complete getter'),(0x3EAA70,229,'complete music reader'),(0x266D10,0x229,'initializer prefix through five-slot loop, not complete function')]:
 b=m.img_rd(raw,secs,a,n);ins=list(cs.disasm(b,a));assert sum(i.size for i in ins)==n
 if scope.startswith('complete'):assert ins[-1].mnemonic=='ret'
 bodies.append({'entry':hex(a),'size':n,'scope':scope,'sha256':sha(b),'raw_hex':b.hex(),
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
refs=['Database/FFXII TZA/18-Audio/CONTRACT-field-music-selection.md',
 'Database/FFXII TZA/_experiments/EXP-099-field-music-selection-exec.md',
 'Database/FFXII TZA/_experiments/evidence/field-music-selection-exec/check.py',
 'Database/FFXII TZA/_experiments/evidence/field-music-selection-exec/result.json']
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 b=Path(p).read_bytes();name=f'{i:02d}-'+Path(p).name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p,'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
typepath=Path('Database/FFXII TZA/_types/types.tsv');typebytes=typepath.read_bytes()
line=next(x for x in typebytes.decode('utf-8-sig').splitlines() if x.startswith('ActorManagerSlot\t'))
(HERE/'retained'/'type-row.txt').write_text(line+'\n')
(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A original identity/control flow plus retained EXP099 fixture observations; no new execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,'bodies':bodies,'refs':pins,
 'type_source':{'path':typepath.as_posix(),'file_sha256':sha(typebytes),'selected_row_sha256':sha((HERE/'retained'/'type-row.txt').read_bytes())},
 'limits':'Complete getter/music reader but selected initializer prefix only. No native re-execution, actor health transition, normal death trigger, live game/field state or actual music presentation.'},indent=2)+'\n')
print('Getter/reader and aligned initializer prefix retained; no false266EDC anchor, no experiment replay.')
