"""Verify saved event ordering, controls, identities; seal exact evidence bytes."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
summary = {}
for mode in ('cold-direct','positive-direct'):
    result = json.loads((HERE/mode/'result.json').read_text())
    rows = json.loads((HERE/mode/'api.json').read_text())
    assert result['status'] == 'PASS' and result['detach']
    for name, digest in result['sources'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest
    stopped = False
    clears = 0
    for row in rows:
        if 'result' in row: assert row['result'], row
        if row['operation'] == 'WaitForDebugEvent': stopped = True
        if row['operation'] in ('GetThreadContext','SetThreadContext'): assert stopped
        if row['operation'] == 'stopped_cleanup':
            assert stopped and row['status'] == 'PASS'
            clears += 1
        if row['operation'] == 'ContinueDebugEvent': stopped = False
    assert clears == 1 and not stopped
    assert rows[-1]['operation'] == 'DebugActiveProcessStop'
    assert [x['operation'] for x in rows[:2]] == ['DebugActiveProcess','DebugSetProcessKillOnExit']
    assert all(x['debugger_present'] is False and x['exit'] is None for x in result['post'])
    assert all(b['beats']>a['beats'] for a,b in zip(result['post'],result['post'][1:]))
    assert result['child_final_exit'] is not None
    summary[mode] = dict(hits=result['hits'], cleared_threads=len(result['cleanup']['clears']),
                         post_beats=[x['beats'] for x in result['post']], api_rows=len(rows))
assert summary['cold-direct']['hits'] == 0 and summary['positive-direct']['hits'] > 0
test = subprocess.run([sys.executable,str(HERE/'test_cleanup.py')],capture_output=True,text=True)
assert test.returncode == 0, test.stderr
(HERE/'unit-tests.txt').write_text(test.stdout+test.stderr)
(HERE/'validation.json').write_text(json.dumps(dict(status='PASS', scope='disposable processes only',
    controls=summary, python=sys.version, platform=platform.platform(),
    base_executable=sys._base_executable,
    executable_sha256=hashlib.sha256(Path(sys._base_executable).read_bytes()).hexdigest()), indent=2)+'\n')
files = {p.relative_to(HERE).as_posix():dict(bytes=p.stat().st_size,
         sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in HERE.rglob('*')
         if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print(json.dumps(summary))
