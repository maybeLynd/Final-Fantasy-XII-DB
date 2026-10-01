"""First small original-code rounding discriminator using existing70 guest runner."""
import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone,unicorn
from unicorn.x86_const import *
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/script-popv-conversion-order');sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (W/'feasibility-raw.json').exists(),'Do not replay settled/failed feasibility'
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SCRIPT-POPV-FLOAT-ROUNDING');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
source=(P/'capture.py').read_bytes();assert source==__import__('subprocess').check_output(['git','show','abdeacd85f705c135dab7929bc4e2205471a853d:'+P.as_posix()+'/capture.py'])
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='run');original=ast.unparse(fn);changed=original.replace('mutated=False):','mutated=False, mxcsr=0x1f80):').replace('u.reg_write(UC_X86_REG_MXCSR, 8064)','u.reg_write(UC_X86_REG_MXCSR, mxcsr)').replace("'mxcsr': '0x1f80'","'mxcsr': hex(mxcsr)")
assert changed!=original and 'UC_X86_REG_MXCSR, mxcsr' in changed and 'mxcsr=0x1f80' in changed
changed=changed.replace("struct.pack_into('<Q', rec, 16, DEST)","struct.pack_into('<H', rec, 4, 2)\n    struct.pack_into('<Q', rec, 16, DEST)")
changed=changed.replace("width << 28","(width << 28) | 0x08000000")
changed=changed.replace('u.reg_write(UC_X86_REG_RBX, STACK)','u.reg_write(UC_X86_REG_RBX, STACK)\n    u.reg_write(UC_X86_REG_R8D, 1)')
changed=changed.replace("'entry': hex(ENTRY)","'entry': hex(ENTRY), 'kind_selector_r8d': 1")
code=(P/'retained/original-popv256.bin').read_bytes();store=(P/'retained/original194.bin').read_bytes();table=(P/'retained/original-table24.bin').read_bytes();raw70=json.loads((P/'raw.json').read_text());assert sha(code)==raw70['reference']['popv_sha256'] and sha(store)==raw70['reference']['store_sha256'] and sha(table)==raw70['reference']['table_sha256']
assert sha(Path(sys.executable).read_bytes())==raw70['tools']['python_sha256'] and unicorn.__version__==raw70['tools']['unicorn'] and capstone.__version__==raw70['tools']['capstone']
for p in raw70['tools']['provider_files']:assert sha(Path(p['path']).read_bytes())==p['sha256']
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;LO,END,ENTRY,STOP=0x267e60,0x267f60,0x267e9c,0x267f1e;pi={i.address:i for i in cs.disasm(code,LO)};si={i.address:i for i in cs.disasm(store,0x26d530)};allowed={pc for pc in pi if ENTRY<=pc<STOP or 0x267f4c<=pc<END}
assert pi[0x267ed2].bytes.hex()=='0f5bc0' and pi[0x267ec9].bytes.hex()=='660f6e849384010000'
STACK,DEST,RSP,REC,SENT=0x40000100,0x40000900,0x60001800,0x60001830,0x60000200
exec(compile(changed,'explicitly adapted existing70 runner','exec'),globals())
(W/'runner-original70.py').write_text(original+'\n');(W/'runner-adapted.py').write_text(changed+'\n')
cases=[]
for mxcsr in [0x1f80,0x5f80]:
 c=run(1,16777217,5,mxcsr=mxcsr);cases.append(c);(W/'feasibility-in-progress.json').write_text(json.dumps(cases,indent=2)+'\n')
values=[c['conversion']['value_bits'] for c in cases];expected=['0000804b','0100804b'];valid=values==expected
for c in cases:
 assert c['conversion']['pc']==hex(STOP) and c['after']['pc']==hex(SENT) and any(v['pc']=='0x267ed2' for v in c['visits'])
 assert c['initial']['mxcsr'] in ['0x1f80','0x5f80'] and struct.unpack_from('<H',bytes.fromhex(c['initial']['record']),4)[0]==2 and struct.unpack_from('<I',bytes.fromhex(c['initial']['record']),24)[0]==0x58000000
 sw=[w for w in c['writes'] if w['phase']=='store'];assert len(sw)==1 and sw[0]['hex']==c['conversion']['value_bits'] and sw[0]['size']==4
result=dict(status='FEASIBLE_DIRECTED_ROUNDING_VALUE_DISCRIMINATOR' if valid else 'INVALID_ROUNDING_VALUE_CONTROL',method='B two bounded original float-kind stages thenexplicitverifiedstoreleafABI, existing70 runner adaptedonlyMXCSR/kind/descriptor/stateentry; no native/live/fullPOPV',original70_commit='abdeacd85f705c135dab7929bc4e2205471a853d',source_sha256=sha(source),original_runner_ast_sha256=sha(ast.dump(fn,include_attributes=True).encode()),adapted_runner_sha256=sha(changed.encode()),instructions=dict(MOVD=pi[0x267ec9].bytes.hex(),CVTDQ2PS=pi[0x267ed2].bytes.hex()),source_identity=raw70['reference'],provider_identity=raw70['tools'],input_signed=16777217,values=values,expected_control_values=expected,cases=cases,limits='Small feasibility/control only, not acceptedsemanticpackage; nativeMXCSRflag/unmasked parity/caller/bank/lifetime/live unproved. Ifcontrolfails do not repeatunchanged. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'feasibility-raw.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],values,flush=True)
assert valid,'Directed rounding observer control failed; preserve raw and revise method'
