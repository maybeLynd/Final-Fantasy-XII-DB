"""Re-execute only changed prerequisite code against retained original controls."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
R = W / 'run-01'
assert not R.exists(), 'Retained run exists; never overwrite/replay'
P = Path('Database/FFXII TZA/_experiments/evidence/migration-prerequisite-contract')
OLD = 'c5c0111ebf885668e06804da3642fc0117c644eb'
FIX = subprocess.check_output(['git', 'rev-parse', '1f11830e9'], text=True).strip()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def blob(commit, path): return subprocess.check_output(['git', 'show', commit + ':' + Path(path).as_posix()])
manifest = json.loads((P / 'manifest.json').read_text())
assert len(manifest['members']) == 64
assert blob(OLD, P / 'manifest.json') == (P / 'manifest.json').read_bytes()
for m in manifest['members']:
    f = P / m['path']
    assert f.stat().st_size == m['bytes'] and sha(f) == m['sha256'], f
    assert blob(OLD, f) == f.read_bytes(), f
old = json.loads((P / 'run-01/raw.json').read_text())
assert old['finished'] and len(old['cases']) == 16
sources = {'generic': Path('Database/Tools/analysis-kit/gfz-scripts/prereq.py'),
           'legacy': Path('Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_prereq.py')}
for f in sources.values(): assert f.read_bytes() == blob(FIX, f), 'Current code differs from reviewed final commit: ' + str(f)
R.mkdir()
shutil.copyfile(P / 'manifest.json', R / 'original-manifest.json')
shutil.copyfile(P / 'run-01/composer.py', R / 'composer.py')
base = Path(sys._base_executable)
assert base.is_file()
raw = {'method': 'A: exact repaired software; retained synthetic inputs through actual composer subprocess',
       'source_commit': FIX, 'original_commit': OLD, 'original_manifest_sha256': sha(P / 'manifest.json'),
       'original_members_verified': 64, 'driver_sha256': sha(__file__),
       'composer_sha256': sha(R / 'composer.py'), 'python': sys.version,
       'child_executable': str(base), 'run_directory': str(R), 'sources': {}, 'cases': [], 'finished': False}
for name, f in sources.items():
    copy = R / (name + '-prereq.py')
    shutil.copyfile(f, copy)
    raw['sources'][name] = {'path': f.as_posix(), 'sha256': sha(f), 'retained': copy.name,
                            'git_blob': subprocess.check_output(['git', 'rev-parse', FIX + ':' + f.as_posix()], text=True).strip()}
for source in ('generic', 'legacy'):
    for c in old['cases']:
        if source == 'legacy' and c['name'] not in ('custom-tab-fail', 'custom-tab-pass'): continue
        name = source + '--' + c['name']
        d = R / name
        d.mkdir()
        fixture = P / 'run-01' / c['name']
        for n in ('upstream.py', 'declaration.json'):
            if (fixture / n).exists(): shutil.copyfile(fixture / n, d / n)
        args = [str(base), '-B', str(R / 'composer.py'), str(R / raw['sources'][source]['retained']),
                str(d / 'upstream.py'), str(d / 'declaration.json')]
        deadline = 1 if c['name'] == 'bounded-timeout' else 5
        try:
            p = subprocess.run(args, capture_output=True, text=True, timeout=deadline)
            obs = {'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
                   'timed_out': False, 'child_reaped': True}
        except subprocess.TimeoutExpired as e:
            def txt(x): return x.decode() if isinstance(x, bytes) else x or ''
            obs = {'returncode': None, 'stdout': txt(e.stdout), 'stderr': txt(e.stderr),
                   'timed_out': True, 'child_reaped': True}
        item = {'name': name, 'source': source, 'original_case': c['name'],
                'original_fixture_commit': OLD, 'expected_accepted': c['expected_accepted'],
                'invocation': args, 'deadline_seconds': deadline,
                'declaration_sha256': sha(d / 'declaration.json'),
                'upstream_sha256': sha(d / 'upstream.py') if (d / 'upstream.py').exists() else None,
                **obs}
        (d / 'receipt.json').write_text(json.dumps(item, indent=2) + '\n')
        raw['cases'].append(item)
raw['source_unchanged'] = all(sha(f) == raw['sources'][n]['sha256'] for n, f in sources.items())
raw['finished'] = True
(R / 'raw.json').write_text(json.dumps(raw, indent=2) + '\n')
print('R2_CAPTURE_FINISHED', len(raw['cases']), flush=True)
