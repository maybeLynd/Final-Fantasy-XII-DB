"""Read-only replay of the scoped preparation controls; no launch/attach/API."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

E=Path(__file__).resolve().parent
if (E/'manifest.json').exists():
    manifest=json.loads((E/'manifest.json').read_text())
    assert manifest,'empty manifest'
    for path,digest in manifest.items():
        assert hashlib.sha256((E/path).read_bytes()).hexdigest()==digest,path
for script in ('qualify_boundaries.py','staging_check.py','layout_check.py','project_control.py','bind_contexts.py','control.py','observe_control.py','native_read_check.py','scoped_dispatch_check.py','native_stop_check.py','native_instruction_stop_check.py','eo3_callback_check.py','timeout_completion_check.py','owned_game_abort_check.py','run_eo3_check.py'):
    r=subprocess.run([sys.executable,str(E/script)],capture_output=True,text=True)
    assert r.returncode==0,(script,r.stdout,r.stderr)
    print(r.stdout.strip())
print('Preparation checks PASS. No fresh original-code or live execution; no live-readiness verdict.')
