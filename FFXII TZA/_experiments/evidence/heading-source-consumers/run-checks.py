"""Retain the actual read-only gate process and three concrete refusals."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
cases = W/'preflight-cases'
receipt = W/'checks-terminal.json'
assert not cases.exists() and not receipt.exists(), 'Preserve prior test evidence'
cases.mkdir()
names = ('check.py', 'arg5-source-boundary.py', 'arg5-source-result.json',
         'arg5-source-terminal.json', 'node-reader-feasibility.py',
         'node-reader-feasibility.json', 'node-reader-terminal.json')
records = []
def execute(label, root):
    argv = [sys.executable, '-B', str(root/'check.py')]
    p = subprocess.run(argv, capture_output=True, text=True)
    records.append({'case': label, 'argv': argv, 'returncode': p.returncode,
                    'stdout': p.stdout, 'stderr': p.stderr, 'terminal': True,
                    'checker_sha256': hashlib.sha256((root/'check.py').read_bytes()).hexdigest()})

execute('positive', W)
assert records[-1]['returncode'] == 0 and not records[-1]['stderr']
for label in ('failed-upstream', 'missing-result', 'fictional-class-closure'):
    root = cases/label
    root.mkdir()
    for name in names: shutil.copy2(W/name, root/name)
    if label == 'failed-upstream':
        p = root/'node-reader-terminal.json'
        x = json.loads(p.read_bytes()); x['returncode'] = 1
        p.write_text(json.dumps(x, indent=2)+'\n')
    elif label == 'missing-result':
        (root/'node-reader-feasibility.json').unlink()
    else:
        p = root/'arg5-source-result.json'
        x = json.loads(p.read_bytes()); x['class_stability'] = 'CLOSED'
        p.write_text(json.dumps(x, indent=2)+'\n')
    execute(label, root)
    assert records[-1]['returncode'] != 0 and records[-1]['stderr'], label
receipt.write_text(json.dumps(records, indent=2)+'\n')
print('SOURCE_CONSUMERS_GATE_POSITIVE_AND_THREE_REFUSALS', len(records))
