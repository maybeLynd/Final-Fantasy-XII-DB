"""Seal exact CLI captures, validity controls and source identities."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
summary = {}
for mode in ('cold','positive'):
    root = HERE/mode
    control = json.loads((root/'control.json').read_text())
    result = json.loads((root/'capture/result.json').read_text())
    rows = json.loads((root/'capture/api.json').read_text())
    assert control['status']==result['status']=='PASS'
    assert control['capture_exit']==0 and result['detach'] and not result['errors']
    for name,digest in result['sources'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
    assert control['target_source_sha256']==hashlib.sha256((HERE.parent/'EXP-029-timeout-cleanup/run.py').read_bytes()).hexdigest()
    assert control['harness_sha256']==hashlib.sha256((HERE/'run_control.py').read_bytes()).hexdigest()
    stopped = False
    initial = None
    cleanup_event = None
    for row in rows:
        if 'result' in row: assert row['result'],row
        if row['operation']=='WaitForDebugEvent':
            stopped = True
            if row.get('exception')==0x80000003:
                if initial is None: initial=row['address']
                else: cleanup_event=row
        if row['operation'] in ('GetThreadContext','SetThreadContext'): assert stopped
        if row['operation']=='stopped_cleanup': assert stopped and row['status']=='PASS'
        if row['operation']=='ContinueDebugEvent': stopped=False
    assert cleanup_event and initial==cleanup_event['address'] and not stopped
    assert rows[-1]['operation']=='capture_end' and rows[-1]['status']=='PASS'
    assert len(result['hits'])==control['hits']
    assert all(x['exit'] is None and not x['debugger'] for x in control['post'])
    assert all(b['beats']>a['beats'] for a,b in zip(control['post'],control['post'][1:]))
    assert all(x is not None for x in control['final_exits'])
    summary[mode]=dict(hits=control['hits'],cleared=len(result['cleanup']['clears']),
                       post_beats=[x['beats'] for x in control['post']],api_rows=len(rows),
                       breakpoint_address=initial)
assert summary['cold']['hits']==0 and summary['positive']['hits']>0
test=subprocess.run([sys.executable,str(HERE/'test_capture.py')],capture_output=True,text=True)
assert test.returncode==0,test.stderr
(HERE/'unit-tests.txt').write_text(test.stdout+test.stderr)
(HERE/'validation.json').write_text(json.dumps(dict(status='PASS',scope='exact CLI, disposable targets only',
    controls=summary,python=sys.version,platform=platform.platform(),
    base_executable=sys._base_executable,
    executable_sha256=hashlib.sha256(Path(sys._base_executable).read_bytes()).hexdigest()),indent=2)+'\n')
files={p.relative_to(HERE).as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print(json.dumps(summary))
