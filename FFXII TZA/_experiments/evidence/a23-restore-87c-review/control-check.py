"""Actual checker CLI must reject failed upstream and missing raw output."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
files = [p for p in P.rglob('*') if p.is_file() and p.suffix != '.zip' and not any(s.startswith('disposable-') for s in p.parts)]
W = P / 'controls-01'
W.mkdir(exist_ok=False)
records = []
for label in ('failed-upstream', 'missing-output'):
    temp = W / ('disposable-' + label)
    temp.mkdir()
    for path in files:
        dst = temp / path.relative_to(P)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dst)
    changed = temp / ('run-01/case-pair.receipt.json' if label == 'failed-upstream' else 'run-01/original.stdout')
    original = changed.read_bytes()
    if label == 'failed-upstream':
        data = json.loads(original)
        data['exit'] = 0
        changed.write_text(json.dumps(data, indent=2) + '\n')
        required = 'upstream CLI result: case-pair'
    else:
        changed.unlink()
        required = 'FileNotFoundError'
    after = changed.read_bytes() if changed.exists() else None
    delta = {'path': changed.relative_to(temp).as_posix(), 'original_utf8': original.decode('utf-8'), 'changed_utf8': after.decode('utf-8') if after is not None else None}
    (W / (label + '.input-delta.json')).write_text(json.dumps(delta, indent=2) + '\n')
    argv = [sys.executable, '-B', str(P / 'check.py'), str(temp)]
    p = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
    (W / (label + '.stdout')).write_bytes(p.stdout)
    (W / (label + '.stderr')).write_bytes(p.stderr)
    record = {'case': label, 'argv': argv, 'checker_sha256': sha(P / 'check.py'), 'terminal': True,
              'exit': p.returncode, 'exception': None, 'expected_error_seen': required in p.stderr.decode('utf-8', 'replace'), 'no_success_output': not p.stdout,
              'delta_sha256': sha(W / (label + '.input-delta.json'))}
    if temp.resolve().parent != W.resolve() or temp.is_symlink():
        raise RuntimeError('control cleanup containment failed')
    shutil.rmtree(temp)
    record['disposable_absent'] = not temp.exists()
    records.append(record)
    (W / (label + '.receipt.json')).write_text(json.dumps(record, indent=2) + '\n')
valid = len(records) == 2 and all(r['exit'] != 0 and r['terminal'] and r['expected_error_seen'] and r['no_success_output'] and r['disposable_absent'] for r in records)
(W / 'result.json').write_text(json.dumps({'status': 'ACTUAL_PREREQUISITE_REFUSALS' if valid else 'INVALID', 'cases': records, 'limits': 'Checker detection controls only; no new semantic restore or device experiment.'}, indent=2) + '\n')
print(json.dumps({'status': 'ACTUAL_PREREQUISITE_REFUSALS' if valid else 'INVALID', 'cases': len(records)}))
raise SystemExit(0 if valid else 1)
