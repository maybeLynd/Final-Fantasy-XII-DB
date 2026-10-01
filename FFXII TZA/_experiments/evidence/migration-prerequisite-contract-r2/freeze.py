import copy, hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/migration-prerequisite-contract-r2')
assert not P.exists(), 'Published inputs immutable'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw = json.loads((W / 'run-01/raw.json').read_text())
D = W / 'reducer-controls'
D.mkdir()
receipts = []
for name in ('incomplete', 'missing-required-case', 'failed-composer-masquerades-as-pass'):
    r = copy.deepcopy(raw)
    if name == 'incomplete': r['finished'] = False
    elif name == 'missing-required-case': r['cases'].pop(0)
    else:
        c = next(c for c in r['cases'] if c['name'] == 'generic--custom-tab-fail')
        c.update(returncode=0, stdout='COMPOSER_PASS {"complete":true,"rows":[7,9]}\n')
    f = D / (name + '.json'); out = D / (name + '-result.json')
    f.write_text(json.dumps(r, indent=2) + '\n')
    q = subprocess.run([sys.executable, '-B', str(W / 'check.py'), '--raw', str(f), '--out', str(out)], capture_output=True, text=True)
    receipts.append({'name': name, 'input_sha256': sha(f), 'returncode': q.returncode,
                     'stdout': q.stdout, 'stderr': q.stderr, 'result_exists': out.exists()})
    assert q.returncode != 0 and not out.exists(), name
before = sha(W / 'run-01/raw.json')
q = subprocess.run([sys.executable, '-B', str(W / 'check.py')], capture_output=True, text=True)
assert q.returncode == 0, q.stderr
assert sha(W / 'run-01/raw.json') == before
(W / 'reducer-controls.json').write_text(json.dumps({'baseline': {'returncode': q.returncode, 'stdout': q.stdout},
    'negative_controls': receipts, 'original_raw_unchanged': True}, indent=2) + '\n')
P.mkdir(parents=True)
(P / '.gitattributes').write_bytes(b'* -text\n')
for name in ('PLAN.md', 'README.md', 'capture.py', 'check.py', 'legacy-control.py', 'freeze.py', 'result.json', 'reducer-controls.json'):
    shutil.copyfile(W / name, P / name)
for name in ('run-01', 'legacy-corrected', 'preparation-v1', 'reducer-controls'):
    shutil.copytree(W / name, P / name)
members = [{'path': f.relative_to(P).as_posix(), 'bytes': f.stat().st_size, 'sha256': sha(f)}
           for f in sorted(P.rglob('*')) if f.is_file()]
(P / 'manifest.json').write_text(json.dumps({'package': P.name, 'members': members}, indent=2) + '\n')
for f in P.rglob('*'):
    if f.is_file():
        filtered = subprocess.check_output(['git', 'hash-object', '--', f.as_posix()], text=True).strip()
        unfiltered = subprocess.check_output(['git', 'hash-object', '--no-filters', '--', f.as_posix()], text=True).strip()
        assert filtered == unfiltered, 'RAW-BYTE-FILTER-MISMATCH ' + str(f)
q = subprocess.run([sys.executable, '-B', str(P / 'check.py'), '--out', str(P / 'result.json')], capture_output=True, text=True)
assert q.returncode == 0, q.stderr
print('FROZEN_R2', len(members), 'portable read-only reducer verified', flush=True)
