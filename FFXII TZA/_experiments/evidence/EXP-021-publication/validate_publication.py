"""Regenerate only claimed RULES, verify stable inputs and record source controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import gen_rules_index as rules

inputs = sorted(set(list(kit.glob('*.py')) + [repo / path for path, _, _ in rules.SOURCES]))
hashes = {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
target = repo / 'Database/FFXII TZA/_index/RULES.md'
before = root / 'rules-before.md.bin'
assert not before.exists()
before.write_bytes(target.read_bytes())
text = rules.build(repo)
target.write_text(text, encoding='utf-8', newline='\n')
assert rules.build(repo) == text
assert hashes == {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
runs = []
for name, arguments in [('test_publication_extractors.py', ['-v']),
                        ('census_bin_signatures.py', ['--self-test']),
                        ('gen_rules_index.py', ['--self-test']),
                        ('check_source_hygiene.py', ['--paths', str(kit)])]:
    command = [sys.executable, str(kit / name), *arguments]
    run = subprocess.run(command, capture_output=True, text=True)
    runs.append(dict(command=command, exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr))
    assert run.returncode == 0, runs[-1]
report = dict(input_hashes=hashes, stable_inputs=True, byte_idempotent=True, runs=runs,
              rules_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
(root / 'publication-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
for name in ['gen_address_index.py', 'knowledge_db.py', 'program_coverage.py',
             'census_bin_signatures.py', 'gen_rules_index.py', 'test_publication_extractors.py']:
    (root / ('validated-' + name + '.bin')).write_bytes((kit / name).read_bytes())
files = {p.relative_to(root).as_posix(): dict(bytes=p.stat().st_size,
         sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob('*'))
         if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(dict(files=files), indent=2) + '\n', encoding='utf-8')
print('PASS:5 regression controls, classifier/rules self-tests, whole current kit hygiene; stable RULES inputs;', len(files), 'sealed files')
