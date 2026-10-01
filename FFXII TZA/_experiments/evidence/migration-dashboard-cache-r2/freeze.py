import copy, hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/migration-dashboard-cache-r2')
assert not P.exists(), 'Immutable package already exists'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r = json.loads((W / 'run-01/raw.json').read_text()); original = sha(W / 'run-01/raw.json')
D = W / 'reducer-controls'; D.mkdir()
receipts = []
for name in ('incomplete', 'missing-required-case', 'mtime-not-preserved', 'hide-late-current'):
    x = copy.deepcopy(r)
    if name == 'incomplete': x['finished'] = False
    elif name == 'missing-required-case': x['cases'].pop()
    elif name == 'mtime-not-preserved':
        c = next(c for c in x['cases'] if c['name'] == 'same-stat-output-next-request')
        c['observed']['edit']['mtime_after'] += 1
    else:
        c = next(c for c in x['cases'] if c['name'] == 'same-stat-input-periodic-detection')
        q = c['observed']['polls'][-1]; q['body']['current']['problems'] = []
    f = D / (name + '.json'); out = D / (name + '-result.json'); f.write_text(json.dumps(x, indent=2) + '\n')
    q = subprocess.run([sys.executable, '-B', str(W / 'check.py'), '--raw', str(f), '--out', str(out)], capture_output=True, text=True)
    receipts.append({'name': name, 'input_sha256': sha(f), 'returncode': q.returncode,
                     'stdout': q.stdout, 'stderr': q.stderr, 'result_exists': out.exists()})
    assert q.returncode != 0 and not out.exists(), name
q = subprocess.run([sys.executable, '-B', str(W / 'check.py')], capture_output=True, text=True)
assert q.returncode == 0 and sha(W / 'run-01/raw.json') == original, q.stderr
(W / 'reducer-controls.json').write_text(json.dumps({'baseline': {'returncode': q.returncode, 'stdout': q.stdout},
    'negative_controls': receipts, 'raw_unchanged': True}, indent=2) + '\n')
P.mkdir(parents=True); (P / '.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md', 'README.md', 'capture.py', 'check.py', 'freeze.py', 'source-preparation.py',
          'source-preparation-failure.json', 'result.json', 'reducer-controls.json'):
    shutil.copyfile(W / n, P / n)
for n in ('run-01', 'source-preparation', 'preparation-v1', 'reducer-controls'): shutil.copytree(W / n, P / n)
members = [{'path': f.relative_to(P).as_posix(), 'bytes': f.stat().st_size, 'sha256': sha(f)} for f in sorted(P.rglob('*')) if f.is_file()]
(P / 'manifest.json').write_text(json.dumps({'package': P.name, 'members': members}, indent=2) + '\n')
for f in P.rglob('*'):
    if f.is_file():
        a = subprocess.check_output(['git', 'hash-object', '--', f.as_posix()], text=True).strip()
        b = subprocess.check_output(['git', 'hash-object', '--no-filters', '--', f.as_posix()], text=True).strip()
        assert a == b, 'RAW-BYTE-FILTER-MISMATCH ' + str(f)
q = subprocess.run([sys.executable, '-B', str(P / 'check.py'), '--out', str(P / 'result.json')], capture_output=True, text=True)
assert q.returncode == 0, q.stderr
print('FROZEN_CACHE_R2', len(members), 'read-only portable reducer verified', flush=True)
