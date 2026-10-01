import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');rb=reader.read_bytes()
sp=importlib.util.spec_from_file_location('original_reader',reader);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
raw,secs=m.load_image();cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
old=Path('Database/FFXII TZA/_experiments/evidence/vif-admission-progress/primary.json');oldbytes=old.read_bytes();s=json.loads(oldbytes)
decoder=next(b for b in s['bodies'] if int(b['entry'],16)==0x22C970)
assert decoder['size']==533 and m.img_rd(raw,secs,0x22C970,533).hex()==decoder['raw_hex']
window=m.img_rd(raw,secs,0x22C930,16);allins=list(cs.disasm(window,0x22C930));end=next(i.address+i.size for i in allins if i.mnemonic=='ret')
body=window[:end-0x22C930];ins=list(cs.disasm(body,0x22C930))
assert all(i.mnemonic in ('mov','xor','ret') for i in ins) and ins[-1].mnemonic=='ret'
reset={'entry':hex(0x22C930),'size':len(body),'sha256':sha(body),'raw_hex':body.hex(),'sample16_hex':window.hex(),
 'scope':'Complete straight-line reset leaf through sole RET; remaining bytes to known22C940 wrapper retained as alignment context, no invented PE extent',
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]}
fw=m.img_rd(raw,secs,0x22C8D0,96);fb=fw[:85];fi=list(cs.disasm(fb,0x22C8D0))
assert sum(i.size for i in fi)==85 and fi[-1].mnemonic=='ret' and fw[85:]==b'\xcc'*11
flush={'entry':hex(0x22C8D0),'size':85,'sha256':sha(fb),'raw_hex':fb.hex(),'sample96_hex':fw.hex(),
 'scope':'Complete two-exit flush leaf through22C924; both returns/branch and CC padding through next22C930 retained, not truncated at first RET',
 'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in fi]}
refs=[old,Path('Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md')]
(HERE/'retained').mkdir(exist_ok=True);pins=[]
for i,p in enumerate(refs):
 b=p.read_bytes();name=f'{i:02d}-'+p.name;(HERE/'retained'/name).write_bytes(b)
 pins.append({'path':p.as_posix(),'retained':'retained/'+name,'bytes':len(b),'sha256':sha(b)})
typepath=Path('Database/FFXII TZA/_types/types.tsv');tb=typepath.read_bytes()
rows=[x for x in tb.decode('utf-8-sig').splitlines() if x.startswith(('Vu1ProgramTable02068E30\t','Vif1Registers02088E30\t','Vif1InstalledAddressList02088E50\t'))];assert len(rows)==3
(HERE/'retained'/'type-rows.tsv').write_text('\n'.join(rows)+'\n');(HERE/'retained'/'image-reader.py').write_bytes(rb)
(HERE/'primary.json').write_text(json.dumps({'method':'A selected original decoder/reset dataflow; no execution',
 'exe_path':m.EXE,'exe_sha256':sha(raw),'image_base':hex(m.IMG_LO),'reader_sha256':sha(rb),'python_version':sys.version,
 'python_sha256':sha(Path(sys.executable).read_bytes()),'capstone_version':capstone.__version__,
 'decoder':decoder,'reset':reset,'flush':flush,'refs':pins,'type_source':{'path':typepath.as_posix(),'file_sha256':sha(tb),'selected_rows_sha256':sha((HERE/'retained'/'type-rows.tsv').read_bytes())},
 'limits':'Local original flow, not native helper/callback effects, normal reset scheduling, actual packet occurrence, all-time state/table extent or rendered consequences. Existing imm16/unmasked and room-only type qualification preserved, not rediscovered.'},indent=2)+'\n')
print('Reset bytes',reset['raw_hex'],'size',reset['size'])
for i in reset['instructions']:print(i['pc'],i['op'],i['args'])
