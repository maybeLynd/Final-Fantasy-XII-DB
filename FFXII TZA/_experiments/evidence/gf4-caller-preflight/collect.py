import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd();sha=lambda b:hashlib.sha256(b).hexdigest()
p=ROOT/'Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py'
spec=importlib.util.spec_from_file_location('retained_image_reader_gf4',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image();pe=struct.unpack_from('<I',raw,0x3c)[0]
pdata_rva,pdata_size=struct.unpack_from('<II',raw,pe+24+112+3*8)
pdata=m.img_rd(raw,secs,m.IMG_LO+pdata_rva,pdata_size)
entries={m.IMG_LO+a:(m.IMG_LO+b,m.IMG_LO+c) for a,b,c in struct.iter_unpack('<III',pdata)}
tables=[]
for i in range(37):
 a=0xD61E50+i*0x50;b=m.img_rd(raw,secs,a,0x50);q=struct.unpack('<10Q',b)
 if q[4]!=0x6571C0:break
 tables.append({'address':hex(a),'raw_hex':b.hex(),'slot4':hex(q[4]),'slot5':hex(q[5]),'slot6':hex(q[6])})
expected={0x65B8F0,0x65B270,0x65B340,0x65B400,0x65B4C0,0x65B590,0x65B650,0x65B750,0x65B820,0x65B920}
assert len(tables)==36 and {int(t['slot6'],16) for t in tables}==expected
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);bodies=[]
for a in sorted(expected):
 end,unwind=entries[a];b=m.img_rd(raw,secs,a,end-a);ins=list(md.disasm(b,a))
 assert ins and ins[0].address==a and ins[0].size>0
 bodies.append({'entry':hex(a),'PE_end':hex(end),'unwind':hex(unwind),'bytes':len(b),'sha256':sha(b),'raw_hex':b.hex(),
 'entry_instruction':{'size':ins[0].size,'bytes':ins[0].bytes.hex(),'op':ins[0].mnemonic,'args':ins[0].op_str}})
files=[
 'Database/FFXII TZA/22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md',
 'Database/FFXII TZA/_experiments/EXP-039-stack-native-control.md',
 'Database/FFXII TZA/_experiments/evidence/EXP-038-handler-stack/capture.py',
 'Database/FFXII TZA/_experiments/evidence/EXP-038-handler-stack/stack_receipt.py',
 'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control/capture_candidate.py',
 'Database/FFXII TZA/_experiments/evidence/exp127-instrument-control/ownership.py',
 'Database/FFXII TZA/_experiments/evidence/exp127-native-dispatch-control/README.md',
 'Database/FFXII TZA/_experiments/evidence/native-fp-context-control/README.md',
 'Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP127-INSTRUMENT-OWNERSHIP.md']
(HERE/'retained').mkdir(exist_ok=True)
refs=[]
for i,f in enumerate(files):
 b=Path(f).read_bytes();name=f'{i:02d}-'+Path(f).name;(HERE/'retained'/name).write_bytes(b)
 refs.append({'path':f,'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
for arm in ['positive','cold']:
 for n in ['control.json','target-ready.json','capture/result.json','capture/api.json']:
  f='Database/FFXII TZA/_experiments/evidence/EXP-039-stack-native-control/'+arm+'/'+n;b=Path(f).read_bytes()
  name=arm+'-'+n.replace('/','-');(HERE/'retained'/name).write_bytes(b)
  refs.append({'path':f,'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
source={'method':'A original-image identity + retained instrument evidence; no fresh native or FF12 execution',
 'exe_sha256':sha(raw),'preferred_image_base':hex(m.IMG_LO),'reader_path':p.relative_to(ROOT).as_posix(),'reader_sha256':sha(p.read_bytes()),
 'python_version':sys.version,'python_binary_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,
 'tables':tables,'bodies':bodies,'refs':refs,
 'limits':'Static address identity is not live object initialization/reachability. Existing evidence keeps historical limits; no rel32/pass-site sweep repeated.'}
(HERE/'source.json').write_text(json.dumps(source,indent=2)+'\n')
print('QUALIFIED36 original vtables /10 exact PE entry identities; retained raw stack controls and current ownership review. No native run.',flush=True)
