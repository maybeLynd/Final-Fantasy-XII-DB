import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+112+24)
ex=m.img_rd(raw,secs,m.IMG_LO+er,es);triples=[struct.unpack_from('<III',ex,i) for i in range(0,len(ex),12)]
bodies=[]
for entry,end,unwind in [(0x20F310,0x20F3D5,0x1D643C4),(0x1DB660,0x1DB7C6,0x1D52D78)]:
 assert (entry-m.IMG_LO,end-m.IMG_LO,unwind-m.IMG_LO) in triples
 b=m.img_rd(raw,secs,entry,end-entry);ins=list(cs.disasm(b,entry))
 assert sum(i.size for i in ins)==len(b) and ins[-1].mnemonic=='ret'
 bodies.append({'entry':hex(entry),'end':hex(end),'unwind':hex(unwind),'size':len(b),'sha256':sha(b),'raw_hex':b.hex(),
 'extent':'Exact PE RuntimeFunction; all bytes decoded through final RET, no first-RET truncation',
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
(HERE/'retained').mkdir(exist_ok=True);p=Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md');b=p.read_bytes()
(HERE/'retained'/p.name).write_bytes(b);(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A original static flow; no execution','exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),
 'reader_sha256':sha(rb),'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,
 'exception_directory':{'rva':hex(er),'bytes':es,'sha256':sha(ex)},'bodies':bodies,
 'consumer':{'path':p.as_posix(),'retained':'retained/'+p.name,'bytes':len(b),'sha256':sha(b)},
 'limits':'Static helper/caller arguments only. No original/native/guest/live execution, actual oversized packet, native allocator/memcpy effects, producer bounds, initialization or presentation observation.'},indent=2)+'\n')
for body in bodies:
 print('BODY',body['entry'],body['size'])
 for i in body['instructions']:print(i['pc'],i['op'],i['args'])
