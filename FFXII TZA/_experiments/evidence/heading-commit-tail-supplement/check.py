"""Read-only check of already captured original entry stores; no new experiment."""
import hashlib, json, sys, types
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior = Path('Database/FFXII TZA/_experiments/evidence/heading-class-effects-slice')
manifest = {x['path']: x for x in json.loads((prior/'manifest.json').read_bytes())['members']}
parent = prior/'raw-commit-node-leaf.json'
assert sha(parent) == manifest['raw-commit-node-leaf.json']['sha256']
raw = json.loads((W/'raw-commit-tail-entries.json').read_bytes())
terminal = json.loads((W/'capture-commit-tail-entries-terminal.json').read_bytes())
if '--fault-upstream-failed' in sys.argv:
    terminal = json.loads((prior/'run-01-render-boundary-serialization-failure/capture-render-position-commit-boundaries-terminal.json').read_bytes())
assert terminal['terminal'] is True and terminal['returncode'] == 0 and not terminal['stderr'], 'Required original capture did not pass'
identity = json.loads((W/'identity-commit-tail-entries.json').read_bytes())
assert terminal['driver_sha256'] == identity['driver_sha256'] == sha(W/'retained/driver/capture-commit-tail-entries.py')
assert identity['position_source_sha256'] == sha(parent)
for x in identity['inputs'] + identity['providers']: assert sha(Path(x['path'])) == x['sha256']
assert identity['exe']['sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
exe = Path(identity['exe']['path']); assert sha(exe) == identity['exe']['sha256']
sys.path.insert(0, str(Path(identity['loaded_pefile']).parent)); import pefile, capstone
image = exe.read_bytes(); pe = pefile.PE(str(exe), fast_load=True); base = pe.OPTIONAL_HEADER.ImageBase
assert base == 0x120000
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); cs.detail = True
policy = W/'retained/commit-tail-entries/reg_tracking.py'
assert sha(policy) == '5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
roles = types.ModuleType('roles'); exec(compile(policy.read_bytes(), str(policy), 'exec'), roles.__dict__)
expected = {0x45fd00: 0x3d8, 0x529d40: 0x3d4, 0x52a8a0: 0x434, 0x52b5d0: 0x3f8}
if '--fault-missing-entry' in sys.argv: raw['callees'].pop()
assert len(raw['callees']) == 4 and {int(f['entry'],16) for f in raw['callees']} == set(expected), 'Incomplete entry set'
leaf = next(f for f in json.loads(parent.read_bytes())['callees'] if f['entry']=='0x43ee70')
assert {int(e['target'],16) for e in leaf['external_jumps']} == set(expected)
results = []
for f in raw['callees']:
    a = int(f['entry'],16); code = (W/f['code_file']).read_bytes(); off = pe.get_offset_from_rva(a-base)
    assert len(code) == 11 == f['bytes'] == f['decoded_bytes'] and sha(W/f['code_file']) == f['code_sha256'] and image[off:off+11] == code
    ins = list(cs.disasm(code,a)); assert len(ins)==2 and ins[0].size==10 and ins[1].size==1
    assert (ins[0].mnemonic,ins[0].op_str,ins[1].mnemonic)==('mov',f'dword ptr [rcx + {hex(expected[a])}], 1','ret')
    assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ins] == [(r['pc'],r['bytes'],r['mnemonic'],r['args']) for r in f['instructions']]
    assert roles.op_kind(ins[0],ins[0].operands[0],0)=='w' and ins[0].operands[0].size==4
    assert not f['call_sites'] and not f['external_jumps'] and f['extent_status']=='UNPROVED_CATALOGUE_ONLY'
    results.append({'entry':hex(a),'store':f'dword[node+{hex(expected[a])}]=1','owner_RDX_and_value_R8D':'unused in these entry instructions','scope':'MOV then RET under valid writable node/normal return; no type/reader/initialized lifetime or full caller claim'})
assert sha(exe)==identity['exe']['sha256']
family = (W/'retained/nativeleaf-fieldconststore.tsv').read_text()
assert all(f'{a:08X}\t' in family for a in expected), 'Existing family disposition must be consumed/preserved'
if '--fault-30-frame-delay' in sys.argv: assert any('r8' in i.op_str for i in ins), 'Forwarding30 is not a delay observation; these instructions do not read it'
if '--fault-class-closure' in sys.argv: assert False, 'Initialized node nonalias/lifetime/class stability is not established by entry stores'
print(json.dumps({'status':'STATIC_NORMAL_ENTRY_STORES_VALID','method':'A; retained certified original code, no native/game execution','class_stability':'OPEN','effects':results,'existing_family_disposition':'PRESERVED/CONSUMED, not newly classified','timing_or_flag_meaning':'UNRESOLVED; no30-frame delay or dirty/reset semantic inference'},indent=2))
