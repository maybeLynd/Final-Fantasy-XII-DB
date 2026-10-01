"""A: decode retained original instructions; conditional calculations, no execution."""
import hashlib,json,shutil,subprocess,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-ARRAY-CLAMP-PRECONDITION');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding');C=P/'publication-correction';assert not R.exists();R.mkdir()
commit='ec5e54a990122f7a071cc1d2c811dfd2271e96b3';files=[]
for name in ['resolver591.bin','reg_tracking.py']:
 p=P/'retained'/name;b=p.read_bytes();committed=subprocess.check_output(['git','show',commit+':'+p.as_posix()]);assert b==committed
 m=next(x for x in json.loads((P/'manifest.json').read_text())['members'] if x['path']=='retained/'+name);assert len(b)==m['bytes'] and sha(b)==m['sha256'];(R/name).write_bytes(b);files.append(dict(path=p.as_posix(),bytes=len(b),sha256=sha(b),verified_at=commit))
for name in ['README.md','material-publication.json']:
 p=C/name;assert p.exists();(R/('65-correction-'+name)).write_bytes(p.read_bytes())
prior=json.loads((P/'raw.json').read_text());(R/'65-reference.json').write_text(json.dumps(dict(reference=prior['reference'],resolver=prior['resolver']),indent=2)+'\n')
code=(R/'resolver591.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes();roles=types.ModuleType('roles');exec(compile(policy,'retained shared reviewed access adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x262440));assert len(code)==591 and sum(i.size for i in ii)==591
rows=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i)),memory=[dict(kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp,size=o.size) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ii]
consumer='Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md';b=Path(consumer).read_bytes();(R/'consumer-before.md').write_bytes(b)
raw=dict(method='A retained original machine-code disassembly and signed-predicate reasoning; conditional arithmetic tables are calculations, not isolated/native/live execution',reference=dict(exe_sha256='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8',imagebase='0x120000',entry='0x262440',bytes=591,body_sha256=sha(code),access_adapter_sha256=sha(policy),files=files,parent_original_commit=commit,parent_publication='Original65 strict47 publication INVALID; additive b94b449ac08ffecde9c9045f984ab6f64c0b8db7 material46+1relocation correction applies; selected scientific inputs present and exactly verified at original commit'),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]]),driver_sha256=sha(Path(__file__).read_bytes()),instructions=rows,consumer=dict(path=consumer,sha256=sha(b)),limits='Selected original clamp/dataflow only, no shipping asset dimension census/upstream validation/full resolver banks/array access/actual native faults/init/lifetime/reachability/game. PC OFF/S19 persists/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE69 static original dataflow; reducer required',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
