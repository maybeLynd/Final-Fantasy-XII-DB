import hashlib,json,sys
from pathlib import Path
import capstone
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent
assert team.board_status(team.BOARD)[0]
b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-SAVE-COUNT-BIT-SEMANTICS');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'result.json').exists(),'Do not repeat settled derivation'
sha=lambda b:hashlib.sha256(b).hexdigest()
P=Path('Database/FFXII TZA/_experiments/evidence/workbench-depth-target-alias')
m=json.loads((P/'manifest.json').read_text());x=next(x for x in m['members'] if x['path']=='source.json');raw=(P/'source.json').read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
s=json.loads(raw);body=next(x for x in s['bodies'] if x['name']=='save');code=bytes.fromhex(body['raw_hex']);assert len(code)==89 and sha(code)=='ebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def obligations(code):
 ii={i.address:i for i in cs.disasm(code,0x36D930)}
 assert sum(i.size for i in ii.values())==89 and ii[0x36D988].mnemonic=='ret'
 for pc,raw in [(0x36D948,'85c9'),(0x36D94A,'7436'),(0x36D950,'448bd1'),(0x36D97C,'4983ea01'),(0x36D980,'75df')]:assert ii[pc].bytes.hex()==raw,(hex(pc),ii[pc].mnemonic)
 assert ii[0x36D94A].operands[0].imm==0x36D982 and ii[0x36D980].operands[0].imm==0x36D961
 assert ii[0x36D950].reg_name(ii[0x36D950].operands[0].reg)=='r10d' and ii[0x36D950].reg_name(ii[0x36D950].operands[1].reg)=='ecx'
 assert ii[0x36D97C].reg_name(ii[0x36D97C].operands[0].reg)=='r10' and ii[0x36D97C].operands[1].imm==1
 return ii
ii=obligations(code)
mutant=bytearray(code);mutant[0x36D94A-0x36D930]=0x7E # JE -> JLE after TEST: negative-looking inputs skip
try:obligations(bytes(mutant))
except AssertionError:mutation_rejected=True
else:raise AssertionError('source obligation detector did not reject signed gate hypothesis')
cases=[]
for count in (0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF):
 signed=count if count<0x80000000 else count-(1<<32)
 cases.append(dict(ecx_hex=f'{count:08X}',signed_interpretation=signed,native_zero_gate_takes_tail=count==0,native_enters_first_iteration=count!=0,r10_after_mov_r10d_ecx=count if count else None,r10_after_first_sub=(count-1) if count else None,signed_for_skips=signed<=0,scope='source-level entry/countdown prefix, no execution or whole-loop completion claim'))
assert cases[-1]['native_enters_first_iteration'] and cases[-1]['signed_for_skips']
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.json').write_bytes(raw);(R/'parent-manifest.json').write_bytes((P/'manifest.json').read_bytes())
contract=Path('Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md');(R/'contract.md').write_bytes(contract.read_bytes())
result=dict(method='A original static code and conditional prefix; no native/live/emulator run',reference=s['reference'],source_sha256=sha(raw),body_sha256=sha(code),tools=dict(python=sys.version,capstone=capstone.__version__,capstone_module_sha256=sha(Path(capstone.__file__).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),contract_sha256=sha(contract.read_bytes()),anchors=[dict(pc=hex(pc),bytes=ii[pc].bytes.hex(),mnemonic=ii[pc].mnemonic,args=ii[pc].op_str) for pc in (0x36D948,0x36D94A,0x36D950,0x36D97C,0x36D980)],cases=cases,mutation=dict(kind='source obligation control, not original execution',change='74 JE -> 7E JLE at36D94A in disposable bytes only',rejected=mutation_rejected),established='Only raw ECX zero skips snapshots. Any sign-bit-set nonzero count enters unchecked loop and zero-extends ECX into64bit R10 before countdown, unlike signed-for pseudocode outside its valid domain.',limits='No original C declared signedness inferred; no completion/fault behavior for billions of items claimed. Existing structural<=32 safe-count constraint unchanged. Does not prove normal callers supply invalid counts or validate generic malformed inputs.',cleanup='Read-only shipping retained evidence; private data writes, no reference/save/config/process/input/instrument changes; PC OFF')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Source prefix derived: rawzero gate, R10D zero-extension,64bit countdown; sign-bit counts are not native no-op. Signed-gate mutation rejected, no execution.')
