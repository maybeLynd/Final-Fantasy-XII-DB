import hashlib,importlib.util,json,struct,sys
from datetime import datetime,timezone
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
pe=struct.unpack_from('<I',raw,60)[0];er,es=struct.unpack_from('<II',raw,pe+24+112+24);table=m.img_rd(raw,secs,m.IMG_LO+er,es)
e=next(x for x in [struct.unpack_from('<III',table,i) for i in range(0,len(table),12)] if x[0]+m.IMG_LO<=0x31E241<x[1]+m.IMG_LO)
start=e[0]+m.IMG_LO;end=0x31E250;b=m.img_rd(raw,secs,start,end-start);ii=list(cs.disasm(b,start))
known=next(i for i in ii if i.address==0x31E241);assert known.mnemonic=='movzx' and known.op_str=='eax, byte ptr [rbp + 0x13]'
assert known.size==4 and next(i for i in ii if i.address==0x31E245).mnemonic=='mov'
refs=[Path('Database/FFXII TZA/_index/candidates/status-sparse-slot-watch-preparation.md'),
 Path('Database/FFXII TZA/_experiments/evidence/status-watch-preflight/source.json'),
 Path('Database/FFXII TZA/_experiments/evidence/status-watch-preflight/observer.json'),
 Path('Database/FFXII TZA/_experiments/evidence/status-watch-preflight/status-table.bin')]
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 data=p.read_bytes();name=f'{i:02d}-'+p.name;(HERE/'retained'/name).write_bytes(data)
 pins.append({'path':p.as_posix(),'retained':'retained/'+name,'bytes':len(data),'sha256':sha(data)})
(HERE/'retained'/'image-reader.py').write_bytes(rb)
docs={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'class':'Primary published ISA/debugger documentation, not a native detector receipt; remote PDF not hashed',
 'intel':{'url':'https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-3b-part-2-manual.pdf',
 'identity':'Intel SDM Volume3B,253669-060US,September2016','section':'17.3.1.2, PDF page120, printed17-9',
 'excerpt':'The processor generates the exception after it executes the instruction that made the access',
 'interpretation':'Data watch conditions produce trap-class events after access; execute conditions fault before. Source-access PC and raw context PC must be separated. No generic RIP-minus-fixed-length for unknown branches/string access.'},
 'microsoft':{'url':'https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/ba--break-on-access-',
 'section':'Access/Size','interpretation':'r means read or write, w means write, e means instruction execution. x64 sizes1/2/4/8 describe watched memory windows, not the width of the triggering instruction.'}}
(HERE/'documentation.json').write_text(json.dumps(docs,indent=2)+'\n')
(HERE/'primary.json').write_text(json.dumps({'method':'A original known-read alignment plus retained preparation/resource/observer and primary ISA documentation; no live/native run',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,
 'aligned_prefix':{'start':hex(start),'end':hex(end),'size':len(b),'raw_hex':b.hex(),'sha256':sha(b),
 'containing_runtime_function':{'begin':hex(e[0]+m.IMG_LO),'end':hex(e[1]+m.IMG_LO),'unwind':hex(e[2]+m.IMG_LO)},
 'scope':'Selected aligned prefix, not complete containing dispatcher or scheduling proof'},
 'selected_instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii if i.address>=0x31E1B4],
 'refs':pins,'documentation_sha256':sha((HERE/'documentation.json').read_bytes()),
 'limits':'No current row binding/save/action/expiry/removal, qualified native read detector, actual data-watch event/PC/width/value, causal actor consequence, corpus re-extraction or old observer qualification rerun.'},indent=2)+'\n')
print('Original known read',known.bytes.hex(),'access PC31E241/next PC31E245; future detector still requires native positive control.')
