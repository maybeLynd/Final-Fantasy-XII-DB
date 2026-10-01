import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
sp=importlib.util.spec_from_file_location('verified_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies=[]
for a,n in [(0x300530,880),(0x239820,27)]:
 b=m.img_rd(raw,secs,a,n);ii=list(cs.disasm(b,a));assert sum(i.size for i in ii)==n and ii[-1].mnemonic=='ret'
 bodies.append({'entry':hex(a),'size':n,'sha256':sha(b),'raw_hex':b.hex(),
  'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]})
assert bodies[0]['sha256']=='ebad5845dd8a1c8a9bc10da6c3aecb10c473f5651f780a83726687924fb35a94'
ret=HERE/'retained';ret.mkdir(exist_ok=True);refs=[]
for p in [reader,Path('Database/FFXII TZA/08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md'),
 Path('Database/FFXII TZA/08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md'),
 Path('Database/FFXII TZA/_experiments/EXP-093-hp-write-execution.md'),
 Path('Database/FFXII TZA/_experiments/evidence/hp-write-execution/bodies.json'),
 Path('Database/FFXII TZA/_experiments/evidence/hp-write-execution/result.json')]:
 b=p.read_bytes();dest=ret/p.name;assert not any(x['retained']=='retained/'+p.name for x in refs)
 dest.write_bytes(b);refs.append({'path':p.as_posix(),'retained':'retained/'+p.name,'bytes':len(b),'sha256':sha(b)})
s={'method':'A exact original instructions and retained artifact controls; witnesses symbolic only',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'capstone_version':capstone.__version__,
 'python_version':sys.version,'python_sha256':sha(Path(sys.executable).read_bytes()),'bodies':bodies,'references':refs,
 'limits':'No new original-code or live execution. Admitted local clamp/write path with finite nonoverflow values and statuses0. Native getter success supplied for setter statement; no normal script/runtime occurrence or downstream status/death/recompute effect.'}
(HERE/'source.json').write_text(json.dumps(s,indent=2)+'\n');print('Retained original full HP/setter bytes and historical controls; no game execution.',flush=True)
