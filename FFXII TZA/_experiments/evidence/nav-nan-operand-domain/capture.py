"""B bounded operand-domain counterexample with existing original237B runner."""
import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-NAN-OPERAND-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists();R.mkdir(exist_ok=False)
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-circle-cell-boundary');source=json.loads((parent/'source.json').read_text());code=(parent/'retained/original237.bin').read_bytes();ref=source['reference'];assert len(code)==237 and sha(code)==ref['body_sha256']
reader=parent/'retained/shipping-reader.py';sp=importlib.util.spec_from_file_location('rd',reader);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and code==rd.img_rd(image,ss,0x4690B0,237)
old=(parent/'capture.py').read_bytes();oldtext=old.decode();runner=oldtext[oldtext.index('ENTRY,END,SENTINEL='):oldtext.index('cases=[]')]
changes=[('def run(name,x,z,r_bits,mutated=False):','def run(name,x,z,r_bits,mutated=False,rect_bits=(0,0,0x41200000,0x41200000)):'),
 ('for off,val in [(0,0.),(8,0.),(0x10,10.),(0x18,10.)]:struct.pack_into(\'<f\',rectangle,off,val)','for off,val in zip([0,8,0x10,0x18],rect_bits):struct.pack_into(\'<I\',rectangle,off,val)'),
 ('visits=[];reads=[];writes=[];comparisons=[]','visits=[];reads=[];writes=[];comparisons=[];branch_flags=[]'),
 ('visits.append(hex(pc));i=by_pc[pc]','visits.append(hex(pc));i=by_pc[pc]\n  if i.mnemonic in [\'jb\',\'ja\',\'jae\',\'seta\']:branch_flags.append(dict(pc=hex(pc),eflags=hex(uc.reg_read(UC_X86_REG_EFLAGS))))'),
 ('after=after,failure=failure)','after=after,failure=failure,branch_flags=branch_flags)')]
for a,b in changes:assert runner.count(a)==1;runner=runner.replace(a,b)
for n,data in [('parent-capture.py',old),('parent-source.json',(parent/'source.json').read_bytes()),('original237.bin',code),('shipping-reader.py',reader.read_bytes()),('runner.py',runner.encode()),('driver-before-run.py',Path(__file__).read_bytes()),('opus-consumer.py',Path('Database/FFXII TZA/_index/candidates/nav-population-opus/nav_circle_cell.py').read_bytes())]:(R/n).write_bytes(data)
fields=Path('Database/FFXII TZA/_types/fields.tsv');fieldbytes=fields.read_bytes();rows=[x for x in fieldbytes.decode().splitlines() if x.startswith('NavGridParams\t0x040\t8\tcellBitsetArray\t')];assert len(rows)==1 and 'a NaN fails every test' in rows[0];(R/'affected-field-row.txt').write_text(rows[0]+'\n')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;seq=list(cs.disasm(code,0x4690B0));by_pc={i.address:i for i in seq};assert len(seq)==67 and not any(i.mnemonic=='call' for i in seq)
tools=dict(before_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,unicorn.__file__,backend.__file__,backend.uclib._name]])
exec(compile(runner,'retained derived55 runner','exec'),globals())
qnan=0x7FC00000;finite=(0,0,0x41200000,0x41200000);badbound=(qnan,0,0x41200000,0x41200000)
specs=[('finite-opposite-corner-positive',13.,14.,bits(6.),finite,1),('finite-opposite-corner-tangent-negative',13.,14.,bits(5.),finite,0),('minA-qnan-opposite-corner',13.,14.,bits(6.),badbound,1),('centerA-qnan',to_float(qnan),14.,bits(6.),finite,0),('radius-qnan',13.,14.,qnan,finite,0)]
cases=[]
for name,x,z,r,rect,want in specs:
 c=run(name,x,z,r,rect_bits=rect);c['rectangle_bits']=[f'{b:08x}' for b in rect];cases.append(c);(W/'in-progress-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 assert c['failure'] is None and c['running_sha256']==ref['body_sha256'] and not c['mutated'] and c['after']['stop_pc']==hex(SENTINEL) and c['after']['rsp']==hex(RSP+8) and c['after']['eax']==want and 0<len(c['visits'])<128 and c['reads'] and c['comparisons'] and c['branch_flags']
 assert not c['writes'] and all(c['after'][k]==c['initial'][k] for k in ['rectangle','circle','stack'])
for p in tools['providers']:assert sha(Path(p['path']).read_bytes())==p['sha256'] and Path(p['path']).stat().st_size==p['bytes']
raw=dict(method='A original operand-specific branches plus B full verified237B call-free leaf in5 fresh isolated guests, injected ABI/argument/MXCSR1F80, reused55 runner with explicit rectangle-bit parameter/branch-flags observer only',reference=ref,parent_commit='9998e98b8ae823f8fc703bccfe23118f1de8b5e9',parent_runner_sha256=sha(old),runner_sha256=sha(runner.encode()),driver_sha256=sha(Path(__file__).read_bytes()),consumer=dict(opus_commit='d87bb8501',fields_path=fields.as_posix(),fields_preimage_sha256=sha(fieldbytes),affected_row_sha256=sha((rows[0]+'\n').encode()),scope='Only cellBitsetArray blanket NaN clause; no prior finite source/output finding revoked'),tools=tools,cases=cases,limits='NaNminA specific counterexample under completed guest comparisons; no general malformed-safety/NaN payload/all-bounds/native exception/status/unmasked continuation/actual game MXCSR/normal reachability/game scene proof.57 nativeprecisionstatus omission forbids promoting guest unchanged status to nativeabsence.',cleanup='Fresh disposable guest each, original code unchanged, no writes/calls/stubs, completeRET/stack+8/argumentbytes unchanged, reference matched; standalone host normal exit, PC OFF/noFF12/save/config/reference/peer writes/S19parked/fullL1+L2NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURED59 quiet-NaN minA still returns1 at finite opposite corner; center/radius controls0, raw retained for source/path reduction',flush=True)
