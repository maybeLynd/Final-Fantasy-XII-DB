"""Only three new original width3 boundaries; don't replay retained22 cases."""
import ast,hashlib,json,struct,sys
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());assert not (W/'extra-s16-boundary.json').exists();src=(W/'capture.py').read_bytes();assert sha(src)==raw['driver_sha256'];tree=ast.parse(src);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run');code=(R/'original194.bin').read_bytes();tab=(R/'original-table24.bin').read_bytes();assert sha(code)==raw['reference']['body_sha256'] and sha(tab)==raw['reference']['table_sha256'];cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ns=dict(globals());ns.update(ENTRY=0x26d530,code=code,tab=tab,TABLE=0x26d5f4,cs=cs,seen={int(x,16) for x in raw['reference']['reachable_pcs']},rets=[int(x,16) for x in raw['reference']['returns']],DEST=0x40000100,REC=0x40000200,RSP=0x60001808,SENT=0x60000200)
exec(compile(ast.Module(body=[fn],type_ignores=[]),'unchanged original bounded runner selection','exec'),ns)
cases=[ns['run'](3,value) for value in [-32767,-32766,32769]];assert all(c['error'] is None and c['after']['pc']=='0x60000200' for c in cases)
(R/'runner-source-used-for-extra.py').write_bytes(src);(W/'extra-s16-boundary.json').write_text(json.dumps(dict(method='B three new original width3 edge/control cases through unchanged AST-selected captured runner; original22 not replayed',parent_raw_sha256=sha((W/'raw.json').read_bytes()),runner_source_sha256=sha(src),function_ast_sha256=sha(ast.dump(fn,include_attributes=True).encode()),cases=cases),indent=2)+'\n');print('ADDITIVE67 original width3 true low/above-low/high+1 boundaries retained',flush=True)
