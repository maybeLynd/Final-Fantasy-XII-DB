import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-CIRCLE-CELL-BOUNDARY');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not (W/'source.json').exists();R.mkdir(exist_ok=False)
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('rd',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=rd.img_rd(image,ss,0x4690B0,237);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x4690B0));assert sum(i.size for i in ins)==237 and ins[-1].mnemonic=='ret' and not any(i.mnemonic=='call' for i in ins)
for name,path in [('shipping-reader.py',rp),('reg_tracking.py',Path(roles.__file__)),('carrier.md',Path('Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md')),('navigation.md',Path('Database/FFXII TZA/06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md')),('flow.py',W.parent/'uc1-band-ruling/review.py')]: (R/name).write_bytes(path.read_bytes())
(R/'original237.bin').write_bytes(code);parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-mark-write-domain/retained/parent679.bin').read_bytes();assert parent==rd.img_rd(image,ss,0x392200,679);(R/'caller679.bin').write_bytes(parent)
source=dict(method='A original237B predicate/layout/caller preparation only; no code execution',driver_sha256=sha(Path(__file__).read_bytes()),reference=dict(exe_sha256=sha(image),body_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),policy_sha256=sha(Path(roles.__file__).read_bytes()),caller_sha256=sha(parent)),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ins])
(W/'source.json').write_text(json.dumps(source,indent=2)+'\n')
print('\n'.join(f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in ins));print('PREPARED_SOURCE55',len(ins),'instructions; choose sufficient execution boundaries before capture',flush=True)
