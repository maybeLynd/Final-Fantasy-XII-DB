import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
REV = '0aa544606e35de0b2f6056b0af469fa048d7fe8a'
Z = ROOT / 'Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip'
EXPECTED = '23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7'
sha = lambda data: hashlib.sha256(data).hexdigest()
if sha(Z.read_bytes()) != EXPECTED:
    raise RuntimeError('ZIP identity failed')
p = subprocess.run(['git', 'show', REV + ':Database/Tools/analysis-kit/gfz-scripts/generation.py'], capture_output=True, cwd=ROOT)
if p.returncode or not p.stdout:
    raise RuntimeError('source extraction failed')
S = W / 'generation.py'
if S.exists():
    raise RuntimeError('refuse overwritten source')
S.write_bytes(p.stdout)
spec = importlib.util.spec_from_file_location('reviewed_generation_0aa', S)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
target = W / 'disposable-restored'
if target.exists():
    raise RuntimeError('fixture exists')
argv = [sys.executable, '-B', str(S), 'restore', str(Z), str(target)]
run = subprocess.run(argv, capture_output=True, text=True, timeout=45)
if run.returncode != 0:
    (W / 'invalid-terminal.json').write_text(json.dumps({'argv': argv, 'exit': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}, indent=2), encoding='utf-8')
    raise RuntimeError('positive restore failed; no acceptance')
man, directory, problems = G.Store(str(target)).open_current()
comparisons = []
with zipfile.ZipFile(Z) as z:
    for name, rec in man['inputs'].items():
        if rec['state'] in ('present', 'empty') and not rec.get('external'):
            path = Path(G.input_file(directory, name))
            comparisons.append({'logical': 'inputs/' + name, 'actual_filename': path.name,
                                'equal': path.read_bytes() == z.read('inputs/' + name)})
    for name in man['outputs']:
        path = Path(directory) / 'outputs' / name
        comparisons.append({'logical': 'outputs/' + name, 'actual_filename': path.name,
                            'equal': path.read_bytes() == z.read('outputs/' + name)})
    comparisons.append({'logical': 'MANIFEST.json', 'equal': (Path(directory) / 'MANIFEST.json').read_bytes() == z.read('MANIFEST.json')})
def tree():
    return {str(f.relative_to(target)): sha(f.read_bytes()) for f in target.rglob('*') if f.is_file()}
before = tree()
refuse = subprocess.run(argv, capture_output=True, text=True, timeout=45)
after = tree()
checks = {'restore_cli': run.returncode == 0 and run.stdout.startswith('RESTORED ') and not run.stderr,
          'ordinary_reader_clean': not problems and man['generation'] == 'g20260929T213407Z-9c7238',
          'all35_members_match': len(comparisons) == 35 and all(c['equal'] for c in comparisons),
          'five_pkg_portable_files': len([c for c in comparisons if c['logical'].startswith('inputs/pkg:') and c['actual_filename'].startswith('pkg%3A')]) == 5,
          'nonempty_target_refused': refuse.returncode == 1 and 'REFUSED' in refuse.stdout and 'non-empty' in refuse.stdout and not refuse.stderr,
          'refusal_no_changes': before == after}
receipt = {'source_commit': REV, 'source_sha256': sha(p.stdout), 'zip_sha256': EXPECTED,
           'python': sys.version, 'positive': {'argv': argv, 'exit': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr},
           'reader_problems': problems, 'comparisons': comparisons,
           'refusal': {'argv': argv, 'exit': refuse.returncode, 'stdout': refuse.stdout, 'stderr': refuse.stderr},
           'tree_before': before, 'tree_after': after, 'checks': checks,
           'verdict': 'ACCEPT_SCOPED_ORIGINAL_CANDIDATE_RESTORE' if all(checks.values()) else 'REJECT'}
(W / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verdict': receipt['verdict'], 'checks': checks}))
raise SystemExit(0 if all(checks.values()) else 1)
