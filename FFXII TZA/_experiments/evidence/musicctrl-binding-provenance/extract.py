import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+112+24)
table=m.img_rd(raw,secs,m.IMG_LO+er,es)
entries=[struct.unpack_from('<III',table,i) for i in range(0,len(table),12)]
bodies=[]
for a,scope in [(0x3EAB60,'complete music binding'),(0x51ED10,'complete shared loader'),(0x379D20,'complete three-resource boot helper'),
 (0x17D000,'selected complete application initialization entry'),(0x17D4C0,'selected complete initialization burst'),(0x22A0B0,'selected complete boot fixer')]:
 e=next(x for x in entries if x[0]+m.IMG_LO==a);n=e[1]-e[0]
 assert n<1200,(hex(a),n)
 b=m.img_rd(raw,secs,a,n);ins=list(cs.disasm(b,a));assert sum(i.size for i in ins)==n and ins[-1].mnemonic in ('ret','jmp')
 bodies.append({'entry':hex(a),'size':n,'scope':scope,'sha256':sha(b),'raw_hex':b.hex(),
  'runtime_function':{'begin':hex(e[0]+m.IMG_LO),'end':hex(e[1]+m.IMG_LO),'unwind':hex(e[2]+m.IMG_LO)},
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
refs=['Database/FFXII TZA/18-Audio/the-music-control-file-and-the-bgm-stream.md',
 'Database/FFXII TZA/18-Audio/CONTRACT-music-control-file-and-bgm-stream.md',
 'Database/FFXII TZA/18-Audio/CONTRACT-field-music-selection.md',
 'Database/FFXII TZA/00-Engine-Core-Runtime/Application-Root/game-application.md']
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 b=Path(p).read_bytes();name=f'{i:02d}-'+Path(p).name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p,'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A bounded original control/data flow and current canonical claim preimages; no execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,'bodies':bodies,'refs':pins,
 'limits':'Selected direct startup chain only, no whole-image writer/caller census repeated; no framework invocation/reinitialization proof, heap5 teardown/release proof, normal startup frequency or live pointer-lifetime observation. No native/injected call.'},indent=2)+'\n')
for b in bodies:
 print(b['entry'],b['size'])
 if b['entry'] in ['0x3eab60','0x51ed10','0x379d20','0x17d000']:
  for i in b['instructions']:print(i['pc'],i['op'],i['args'])
 else:
  for i in b['instructions']:
   if i['op'] in ('call','jmp') and i['args'] in ('0x22a0b0','0x379d20'):print(i['pc'],i['op'],i['args'])
