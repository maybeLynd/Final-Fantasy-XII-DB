"""Record the existing input probe unchanged; this is an input intervention."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--keys', required=True)
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()
kit = Path(__file__).resolve().parents[4] / 'Tools/analysis-kit/gfz-scripts'
extension = Path(__file__).with_name('probe_extension.py')
cmd = [sys.executable, str(extension), '--keys', a.keys, '--hold', '0.35']
record = dict(command=cmd, start_unix=time.time(), status='INCOMPLETE',
              source_sha256={str(f): hashlib.sha256(f.read_bytes()).hexdigest()
                             for f in [Path(__file__), extension, kit / 'runtime_input_probe.py',
                                       kit / 'runtime_poke.py', kit / 'window_focus.py']})
try:
    r = subprocess.run(cmd, capture_output=True, text=True)
    record.update(exit_code=r.returncode, stdout=r.stdout, stderr=r.stderr, status='COMPLETED')
    print(r.stdout, r.stderr)
finally:
    record['end_unix'] = time.time()
    a.out.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
raise SystemExit(r.returncode)
