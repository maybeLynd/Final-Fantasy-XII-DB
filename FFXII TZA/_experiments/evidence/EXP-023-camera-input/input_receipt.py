"""Capture bounded private/original probe commands; accepted events are not scientific success."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
kit = root.parents[3] / 'Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import runtime_probe as rp
p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['original', 'candidate'], required=True)
p.add_argument('--keys', required=True)
p.add_argument('--hold', type=float, default=0.35)
p.add_argument('--out', required=True)
a = p.parse_args()
assert 0 < a.hold <= 2
assert [pid for pid, path in rp.find_process('FFXII_TZA.exe')] == [15600]
script = root / 'key_packet.py' if a.mode == 'candidate' else root.parent / 'EXP-019-ledger/probe_extension.py'
command = [sys.executable, str(script), '--keys', a.keys, '--hold', str(a.hold)]
record = dict(command=command, pid=15600, start_unix=time.time(), status='INCOMPLETE',
              source_hashes={str(f): hashlib.sha256(f.read_bytes()).hexdigest()
                             for f in [Path(__file__),script,kit/'runtime_input_probe.py',kit/'runtime_poke.py',kit/'window_focus.py']})
try:
    run = subprocess.run(command, capture_output=True, text=True)
    record.update(exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr,status='COMPLETED')
finally:
    record['end_unix']=time.time()
    (root / a.out).write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print(run.stdout,run.stderr)
raise SystemExit(run.returncode)
