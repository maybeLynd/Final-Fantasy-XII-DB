"""Read-only gate for the two bounded original-source consumer findings."""
import hashlib, json, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name): return json.loads((W/name).read_bytes())

arg_driver = W/'arg5-source-boundary.py'
arg_saved = load('arg5-source-result.json')
arg_receipts = load('arg5-source-terminal.json')
assert [r['case'] for r in arg_receipts] == ['positive', 'intervening-call', 'mid-entry-edge']
assert all(r['terminal'] is True and r['driver_sha256'] == sha(arg_driver) for r in arg_receipts)
assert arg_receipts[0]['returncode'] == 0 and not arg_receipts[0]['stderr']
assert all(r['returncode'] != 0 and r['stderr'] for r in arg_receipts[1:])
assert json.loads(arg_receipts[0]['stdout']) == arg_saved

node_driver = W/'node-reader-feasibility.py'
node_saved = load('node-reader-feasibility.json')
node_receipt = load('node-reader-terminal.json')
assert node_receipt['terminal'] is True and node_receipt['returncode'] == 0 and not node_receipt['stderr']
assert node_receipt['driver_sha256'] == sha(node_driver)
assert json.loads(node_receipt['stdout']) == node_saved

# Check the actual invocation paths, not only stored transcripts or helper text.
for driver, expected in ((arg_driver, arg_saved), (node_driver, node_saved)):
    p = subprocess.run([sys.executable, '-B', str(driver)], capture_output=True, text=True)
    assert p.returncode == 0 and not p.stderr and p.stdout.strip(), (driver, p.returncode, p.stderr)
    assert json.loads(p.stdout) == expected, driver

assert arg_saved['status'] == 'FIRST_SELECTED_POSITION_CALL_ARG5_ZERO_STATIC'
assert arg_saved['first_call']['pc'] == '0x2e4751' and arg_saved['first_call']['arg5'] == 0
assert arg_saved['second_call']['pc'] == '0x2e4928'
assert 'Conditional' in arg_saved['second_call']['status']
assert arg_saved['class_stability'] == 'OPEN'
assert node_saved['status'] == 'OFFSET_FEASIBILITY_ONLY'
assert node_saved['exe_sha256'] == arg_saved['reference_sha256']
rows = node_saved['rows']
assert [(r['step'], r['offset']) for r in rows] == [
    ('0x45fd10', '0x3d8'), ('0x529d50', '0x3d4'),
    ('0x52a8b0', '0x434'), ('0x52b5e0', '0x3f8')]
assert [len(r['step_direct_offset_hits']) for r in rows] == [0, 2, 2, 1]
assert [[h['kind'] for h in r['step_direct_offset_hits']] for r in rows] == [[], ['r', 'w'], ['r', 'w'], ['r']]
assert all(h['base'] == 'rbx' for r in rows for h in r['step_direct_offset_hits'])
assert all(r['receiver_source_before_first_hit'][0]['instruction'] == 'mov rbx, rcx' for r in rows[1:])
assert all(len(r['calls_before_first_hit']) > 0 for r in rows[1:])
assert all(r['store_control'][1] == 'mov' for r in rows)
print(json.dumps({'status': 'STATIC_ONLY_BOUNDARIES_VALID',
                  'first_selected_arg5': 0,
                  'step_direct_hit_counts': [len(r['step_direct_offset_hits']) for r in rows],
                  'class_stability': 'OPEN',
                  'limits': 'No normal gameplay, initialized ownership, universal second-arg zero, full nested effects or presentation claim.'}))
