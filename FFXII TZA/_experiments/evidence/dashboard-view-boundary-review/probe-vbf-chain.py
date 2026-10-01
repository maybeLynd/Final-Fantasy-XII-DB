"""Actual pinned capture CLI -> pinned view adapter, disposable archive fixture."""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent / 'vbf-chain'
W.mkdir(exist_ok=False)
ROOT = Path.cwd().resolve()
REV = 'eae0ed3c7d1ed9f8f41a401b85e1fedb4ed39cc9'
p = subprocess.run(['git', 'show', REV + ':Database/Tools/dashboard/vbf_index.py'], cwd=ROOT, capture_output=True)
if p.returncode or not p.stdout:
    raise RuntimeError('source extraction failed')
source = W / 'vbf_index.py'
source.write_bytes(p.stdout)
builder = Path(__file__).resolve().parent / 'source-build_views-eae0ed3c7.py'
raw = builder.read_bytes()
if hashlib.sha256(raw).hexdigest() != '812d7f0ce2c7681044f657ce0af51c09f3fad5a22bc641116691675b190016ab':
    raise RuntimeError('builder identity mismatch')
tree = ast.parse(raw)
selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'M', 'v_vbf'}]
if len(selected) != 2:
    raise RuntimeError('missing exact adapter')
env = {'json': json, 'collections': collections}
exec(compile(ast.Module(body=selected, type_ignores=[]), '<pinned VBF view>', 'exec'), env)
# Two header entries; payload not involved. Offsets and sizes are synthetic,
# deliberately disclosed; this does not certify original VBF format semantics.
names = b'folder/a.dat\0folder/b.src\0'
header_size = 16 + 32 + 64 + 4 + len(names)
header = struct.pack('<4sIQ', b'SRYK', header_size, 2) + bytes(32)
header += struct.pack('<IIQQQ', 0, 0, 100, 0, 0) + struct.pack('<IIQQQ', 0, 0, 200, 0, 13)
header += struct.pack('<I', 4 + len(names)) + names
archive = W / 'positive.vbf'
archive.write_bytes(header)
corrupt = W / 'corrupt.vbf'
corrupt.write_bytes(b'WRNG' + header[4:])
listing = W / 'listing.txt'
listing.write_text('100 folder/a.dat\n200 folder/b.src\n', encoding='utf-8')
drift = W / 'drift.txt'
drift.write_text('100 folder/a.dat\n201 folder/b.src\n2 folder/c.dat\n', encoding='utf-8')
facts = W / 'facts.json'
facts.write_text(json.dumps({'facts': [], 'gaps': {}, 'failed': {}}), encoding='utf-8')
cases = [('positive', archive, listing), ('drift', archive, drift),
         ('missing-archive', W / 'missing.vbf', listing), ('corrupt-archive', corrupt, listing),
         ('missing-listing', archive, W / 'missing-listing.txt')]
records = []
for name, arc, lst in cases:
    out = W / (name + '.json')
    out.write_text(json.dumps({'entries': [['stale/file.dat', 999]], 'archive_index': {'stale': True}}), encoding='utf-8')
    argv = [sys.executable, '-B', str(source), '--archive', str(arc), '--listing', str(lst), '--out', str(out)]
    result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
    capture = json.loads(out.read_text(encoding='utf-8'))
    view = env['v_vbf']({'vbf_index': str(out), 'requirement_facts': str(facts)}, 'bounded fixture')
    records.append({'case': name, 'argv': argv, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
                    'capture': capture, 'view': view, 'temporary_output_left': Path(str(out) + '.tmp').exists()})
by = {r['case']: r for r in records}
measure = lambda r, name: next((m for m in r['view'].get('measures', []) if m['id'] == name), None)
checks = {'positive': by['positive']['exit'] == 0 and measure(by['positive'], 'files')['numerator'] == 2 and measure(by['positive'], 'bytes')['numerator'] == 300 and measure(by['positive'], 'listing-drift')['numerator'] == 0,
          'drift': by['drift']['exit'] == 0 and measure(by['drift'], 'listing-drift')['numerator'] == 2 and by['drift']['view']['status'] == 'PARTIAL',
          'missing_archive': by['missing-archive']['exit'] == 1 and by['missing-archive']['view']['status'] == 'FAILED' and by['missing-archive']['view']['measures'] == [] and 'entries' not in by['missing-archive']['capture'],
          'corrupt_archive': by['corrupt-archive']['exit'] == 1 and by['corrupt-archive']['view']['status'] == 'FAILED' and by['corrupt-archive']['view']['measures'] == [] and 'entries' not in by['corrupt-archive']['capture'],
          'missing_listing_not_measured_zero': measure(by['missing-listing'], 'listing-drift') is None or measure(by['missing-listing'], 'listing-drift')['numerator'] is None,
          'atomic_outputs_completed': not any(r['temporary_output_left'] for r in records)}
receipt = {'commit': REV, 'capture_source_sha256': hashlib.sha256(p.stdout).hexdigest(),
           'builder_sha256': hashlib.sha256(raw).hexdigest(), 'method': 'actual capture CLI and original host view function, disclosed synthetic VBF fixture',
           'checks': checks, 'records': records, 'verdict': 'ACCEPT_BOUNDED_CHAIN' if all(checks.values()) else 'REJECT_MISSING_LISTING_BOUNDARY'}
(W / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verdict': receipt['verdict'], 'checks': checks}))
raise SystemExit(0 if all(checks.values()) else 1)
