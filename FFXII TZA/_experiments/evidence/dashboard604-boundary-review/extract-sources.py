"""Check all required original host sources before any experiment."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
REV = '604194276'
records = []
for leaf in ('build_views.py', 'server.py', 'vbf_index.py'):
    target = P / ('source-' + leaf)
    if target.exists(): raise RuntimeError('source exists; no overwrite')
    argv = ['git', 'show', REV + ':Database/Tools/dashboard/' + leaf]
    p = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
    (P / (leaf + '.git.stdout')).write_bytes(p.stdout)
    (P / (leaf + '.git.stderr')).write_bytes(p.stderr)
    r = {'argv': argv, 'exit': p.returncode, 'terminal': True, 'exception': None, 'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr), 'sha256': hashlib.sha256(p.stdout).hexdigest()}
    (P / (leaf + '.git.receipt.json')).write_text(json.dumps(r, indent=2) + '\n')
    if p.returncode or not p.stdout or p.stderr: raise RuntimeError('required source extraction failed: ' + leaf)
    target.write_bytes(p.stdout)
    records.append(r)
(P / 'source-identities.json').write_text(json.dumps({'commit': REV, 'sources': records}, indent=2) + '\n')
print(json.dumps({'sources': [{'path': r['argv'][-1], 'sha256': r['sha256']} for r in records]}))
