import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+136)
ed=m.img_rd(raw,secs,m.IMG_LO+er,es);rfs=[struct.unpack_from('<III',ed,i) for i in range(0,len(ed),12)]
selected=[r for r in rfs if 0x210320<=r[0]+m.IMG_LO<0x2104C8]
assert [(a+m.IMG_LO,b+m.IMG_LO) for a,b,c in selected]==[(0x210320,0x21033C),(0x21033C,0x2104C1),(0x2104C1,0x2104C8)]
fragments=[]
for i,(a,b,c) in enumerate(selected):
 hdr=m.img_rd(raw,secs,c+m.IMG_LO,4);flags=hdr[0]>>3;codes=hdr[2];offset=(4+2*codes+3)&~3
 assert hdr[0]&7==1
 uw=m.img_rd(raw,secs,c+m.IMG_LO,offset+(12 if flags&4 else 0))
 parent=None
 if i:
  assert flags==4;parent=struct.unpack_from('<III',uw,offset);assert parent==selected[0]
 else:assert flags==0
 fragments.append({'start':hex(a+m.IMG_LO),'end':hex(b+m.IMG_LO),'unwind':hex(c+m.IMG_LO),
  'flags':flags,'unwind_raw_hex':uw.hex(),'chain_parent':list(map(hex,(v+m.IMG_LO for v in parent))) if parent else None})
body=m.img_rd(raw,secs,0x210320,424);ins=list(cs.disasm(body,0x210320))
assert sum(i.size for i in ins)==424 and ins[-1].address==0x2104C7 and ins[-1].mnemonic=='ret'
assert m.img_rd(raw,secs,0x2104C8,8)==b'\xcc'*8
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for p in [Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md'),
 Path('Database/FFXII TZA/_experiments/evidence/gif-size-copy-boundary/primary.json')]:
 b=p.read_bytes();name=p.name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p.as_posix(),'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A complete static original mode/loop flow','exe_path':m.EXE,'exe_sha256':sha(raw),
 'image_base':hex(m.IMG_LO),'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),
 'capstone_version':capstone.__version__,'reader_sha256':sha(rb),'exception_directory':{'rva':hex(er),'bytes':es,'sha256':sha(ed)},
 'body':{'entry':hex(0x210320),'size':424,'sha256':sha(body),'raw_hex':body.hex(),'fragments':fragments,
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]},
 'refs':pins,'limits':'Local original dispatcher branches only. No callee/native effects, source-resource census, real initialization/normal caller path, scheduling, rendering or live/emulated execution.'},indent=2)+'\n')
print('Complete424B dispatcher verified across three chained PE fragments.',flush=True)
