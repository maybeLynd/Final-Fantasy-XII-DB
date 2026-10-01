"""Check retained Method-A prerequisites and discriminators; never class closure."""
import ast, hashlib, json, sys
from pathlib import Path
import capstone
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
stems = ['', '-nested', '-closure-r3', '-object-state', '-position-effects',
         '-region-and-position-boundaries', '-render-position-commit-boundaries',
         '-commit-operation', '-commit-node-leaf']
historical = {'', '-nested', '-closure-r3', '-object-state'}
all_raw = {}
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); cs.detail = True
for stem in stems:
    terminal = json.loads((W / f'capture{stem}-terminal.json').read_bytes())
    if '--fault-upstream-failed' in sys.argv and stem == '-render-position-commit-boundaries':
        terminal = json.loads((W / 'run-01-render-boundary-serialization-failure/capture-render-position-commit-boundaries-terminal.json').read_bytes())
    assert terminal['terminal'] is True and terminal['returncode'] == 0 and not terminal['stderr'], 'Required capture failed/incomplete'
    driver = W / ('original-producers' if stem in historical else '') / f'capture{stem}.py'
    identity = json.loads((W / f'identity{stem}.json').read_bytes())
    assert terminal['driver_sha256'] == identity['driver_sha256'] == sha(driver), 'Actual executed driver identity'
    for x in identity['inputs'] + identity['providers']:
        assert sha(Path(x['path'])) == x['sha256'], 'Reference/provider changed'
    assert identity['exe']['sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    for key, name in [('previous_raw_sha256', 'raw.json'), ('nested_raw_sha256', 'raw-nested.json'), ('closure_source_sha256', 'raw-closure-r3.json')]:
        if key in identity: assert identity[key] == sha(W / name)
    if 'position_source_sha256' in identity:
        predecessor = {'-region-and-position-boundaries': '-position-effects', '-render-position-commit-boundaries': '-region-and-position-boundaries', '-commit-operation': '-render-position-commit-boundaries', '-commit-node-leaf': '-commit-operation'}[stem]
        assert identity['position_source_sha256'] == sha(W / f'raw{predecessor}.json')
    raw = json.loads((W / f'raw{stem}.json').read_bytes())
    if '--fault-empty-capture' in sys.argv and stem == '-commit-node-leaf': raw['callees'] = []
    assert raw['status'] == 'SOURCE_ONLY_NOT_CLASS_PRESERVATION'
    assert raw['callees'] and {int(f['entry'], 16) for f in raw['callees']} == set(raw['unique_targets']), 'Missing/zero-case capture'
    for f in raw['callees']:
        code = (W / f['code_file']).read_bytes()
        assert len(code) == f['bytes'] == f['decoded_bytes'] and hashlib.sha256(code).hexdigest() == f['code_sha256']
        ins = list(cs.disasm(code, int(f['entry'], 16)))
        assert [(hex(i.address), i.bytes.hex(), i.mnemonic, i.op_str) for i in ins] == [(x['pc'], x['bytes'], x['mnemonic'], x['args']) for x in f['instructions']]
        assert sum(i.size for i in ins) == len(code)
        if f['extent_status'] == 'UNWIND_UNION_MATCH':
            assert f['fragments'] and f['unwind_contiguous'] and f['unwind_union'] == len(code)
        else:
            assert f['extent_status'] == 'UNPROVED_CATALOGUE_ONLY' and not f['fragments'] and f['unwind_union'] is None
    # Actual capture path invokes the shared adapter, including LEA/address roles.
    tree = ast.parse(driver.read_bytes())
    calls = {ast.unparse(x.func) for x in ast.walk(tree) if isinstance(x, ast.Call)}
    assert 'roles.op_kind' in calls and 'roles.written' in calls
    all_raw[stem] = raw
assert sha(Path(identity['exe']['path'])) == identity['exe']['sha256']
if '--fault-missing-latest' in sys.argv: all_raw.pop('-commit-node-leaf')
assert set(all_raw) == set(stems), 'Required newest boundary missing'
edges = json.loads((W / 'edge-correction.json').read_bytes())
assert edges['status'] == 'ADDITIVE_EDGE_CORRECTION_VALID_SOURCE_ONLY' and edges['producer_sha256'] == sha(W / 'capture.py')
for x in edges['input_raw']: assert sha(W / x['path']) == x['sha256']
assert [(x['capture'], x['entry']) for x in edges['affected_edge_lists']] == [('raw-nested.json', '0x2e6300'), ('raw-closure-r3.json', '0x2ec3f0')]
actual = next(f for f in all_raw['-object-state']['callees'] if f['entry'] == '0x2e6300')['external_jumps']
if '--fault-drop-conditional' in sys.argv: actual = []
assert actual == [{'pc': '0x2e6303', 'target': '0x265510', 'mnemonic': 'js', 'conditional': True, 'resolved_immediate': True}], 'Real conditional-tail control missing'
selected = all_raw['-render-position-commit-boundaries']['selected_source_edges']
if '--fault-tail-as-call' in sys.argv: selected[1]['kind'] = 'direct_call'
assert selected == [{'pc': '0x3ec4dd', 'target': '0x4288b0', 'mnemonic': 'call', 'kind': 'direct_call'}, {'pc': '0x3ec4fb', 'target': '0x3b3ca0', 'mnemonic': 'jmp', 'kind': 'unconditional_tail'}]
def row(stem, entry, pc):
    return next(x for f in all_raw[stem]['callees'] if f['entry'] == entry for x in f['instructions'] if x['pc'] == pc)
def at(stem, entry, pc, mnemonic, args):
    x = row(stem, entry, pc); assert (x['mnemonic'], x['args']) == (mnemonic, args)
at('-position-effects', '0x2e6000', '0x2e6060', 'mov', 'dword ptr [rsp + 0x20], esi')
at('-region-and-position-boundaries', '0x3ec3d0', '0x3ec4af', 'mov', 'eax, dword ptr [rip + 0x27727db]')
at('-region-and-position-boundaries', '0x3ec3d0', '0x3ec4b5', 'or', 'eax, dword ptr [rsp + 0x50]')
at('-region-and-position-boundaries', '0x3ec3d0', '0x3ec4b9', 'je', '0x3ec500')
at('-commit-operation', '0x3a9490', '0x3a94e0', 'mov', 'r8d, esi')
at('-commit-operation', '0x3a9490', '0x3a94e9', 'call', '0x43ee70')
dispatch = next(f for f in all_raw['-commit-node-leaf']['callees'] if f['entry'] == '0x43ee70')['external_jumps']
assert [(e['pc'], e['target']) for e in dispatch] == [('0x43ee8c', '0x52b5d0'), ('0x43ee91', '0x52a8a0'), ('0x43ee96', '0x529d40'), ('0x43ee9b', '0x45fd00')]
if '--fault-fictional-closure' in sys.argv: assert not dispatch, 'Four original native tails remain; no class-closure acceptance'
failed = json.loads((W / 'run-01-render-boundary-serialization-failure/capture-render-position-commit-boundaries-terminal.json').read_bytes())
assert failed['terminal'] and failed['returncode'] != 0 and failed['stderr'] and failed['driver_sha256'] == sha(W / 'run-01-render-boundary-serialization-failure/capture-render-position-commit-boundaries.py')
print(json.dumps({'status': 'STATIC_EFFECT_BOUNDARIES_VALID_NOT_CLASS_CLOSURE', 'method': 'A; retained original code decoding, no machine-code/game execution', 'class_stability': 'OPEN', 'commit_dispatch_targets': [x['target'] for x in dispatch], 'limits': 'Conditional source facts only; initialized alias/lifetime/callback/normal reachability not established. No-root catalogue bodies remain qualified. Original failed capture and additive edge corrections preserved.'}, indent=2))
