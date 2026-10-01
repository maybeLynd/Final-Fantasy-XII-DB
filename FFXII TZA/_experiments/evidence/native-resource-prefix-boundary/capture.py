"""A exact selector postcondition; supplied logical spans, no original-code execution."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess,types
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NATIVE-RESOURCE-PREFIX-BOUNDARY');assert t['agent']=='ASTRA' and t['status']=='ACTIVE';assert not R.exists();R.mkdir()
P=Path('Database/FFXII TZA/_experiments/evidence/native-filter-message-resource');m=json.loads((P/'manifest.json').read_text());assert len(m['members'])==43
for x in m['members']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
c=subprocess.check_output(['git','log','-1','--format=%H','--',(P/'raw.json').as_posix()],text=True).strip() or None
files=[]
for n in ['raw.json','manifest.json','retained/selector.bin','retained/shipping-reader.py','retained/reg_tracking.py']:
 p=P/n;b=p.read_bytes()
 if c:assert b==subprocess.check_output(['git','show',c+':'+p.as_posix()])
 copy='parent82-'+Path(n).name;(R/copy).write_bytes(b);files.append(dict(path=n,copy=copy,sha256=sha(b)))
rd=types.ModuleType('reader');rd.__file__=str((R/'parent82-shipping-reader.py').resolve());exec(compile((R/'parent82-shipping-reader.py').read_bytes(),rd.__file__,'exec'),rd.__dict__);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and rd.img_rd(image,ss,0x19a5b0,159)==(R/'parent82-selector.bin').read_bytes()
prefixes=b'\0\0'*7
cases=[dict(name='complete-one-unit',resource_hex=(prefixes+b'\x01\x00A\x00').hex(),declared_size=18),dict(name='prefix-only-one-unit',resource_hex=(prefixes+b'\x01\x00').hex(),declared_size=16),dict(name='one-byte-selected-prefix',resource_hex=(prefixes+b'\x01').hex(),declared_size=15),dict(name='complete-empty-selected',resource_hex=(prefixes+b'\0\0').hex(),declared_size=16)]
parent=json.loads((R/'parent82-raw.json').read_text())
raw=dict(method='A verified retained original159B selector/source accesses and four supplied logical-span counterexamples; no execution',reference=dict(exe_sha256=sha(image),parent82_commit=c,parent82_view='Committed input bytes checked' if c else 'Own frozen43 manifest allmembers verified, publicationpending; original159B independently matched shipping image, not acceptance',files=files),tools=parent['tools'],id='0x7837',cases=cases,driver_sha256=sha(Path(__file__).read_bytes()),limits='Conditional source result assuming preceding native LoadResource/LockResource/SizeofResource succeed with supplied state. Does not prove Windows accepts malformed blocks or actual native/game reachability/callback effects/physical read fault/language/module initialization/lifetime/visiblemessage. Incomplete selected word outcome unknown, only source read attempt established. Four cases are calculations, not guest/live tests. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE83 source prefix versus fulltextspan boundary',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
