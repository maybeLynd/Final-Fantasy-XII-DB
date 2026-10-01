"""Seal advisory controls, replay the preserved affected sources and regenerate claimed RULES."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
db = repo / 'Database/FFXII TZA'
sys.path.insert(0, str(kit))
import gen_rules_index as rules
import check_answered_not_established as checker
import tempfile
import team

board = json.loads(team.BOARD.read_text(encoding='utf-8'))
assert any(t['id'] == 'ASTRA-ANSWERED-ADVISORIES-PUB' and t['status'] == 'ACTIVE'
           and t['agent'] == 'ASTRA' for t in board['tasks']), 'active publication reservation required'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

comparison = json.loads((root / 'comparison.json').read_text())
with tempfile.TemporaryDirectory(prefix='astra-exp022-replay-') as scratch:
    ledger = Path(scratch) / '_index/OPEN-QUESTIONS.md'
    ledger.parent.mkdir()
    ledger.write_bytes((root / 'question-ledger.md.bin').read_bytes())
    ids = checker.answered_ids(scratch)
hits = []
for name, receipt in comparison['source_receipts'].items():
    path = root / receipt['file']
    assert sha(path) == receipt['sha256']
    checker.scan(ids, path.read_text(encoding='utf-8-sig'), name, hits)
assert sorted(map(list, hits)) == comparison['new_hits']

inputs = sorted(set(list(kit.glob('*.py')) + [repo / path for path, _, _ in rules.SOURCES]))
hashes = {p.relative_to(repo).as_posix(): sha(p) for p in inputs}
target = db / '_index/RULES.md'
before = root / 'rules-before.md.bin'
if not before.exists():
    before.write_bytes(target.read_bytes())
text = rules.build(repo)
target.write_text(text, encoding='utf-8', newline='\n')
assert rules.build(repo) == text
runs = []
commands = [('test_answered_advisories.py', ['-v'], 0),
            ('check_answered_not_established.py', ['--self-test'], 0),
            ('check_answered_not_established.py', ['--db', str(db)], 1),
            ('check_source_hygiene.py', ['--paths', str(kit)], 0),
            ('check_links.py', ['--db', str(db)], 0),
            ('team.py', ['validate'], 0)]
for name, args, expected in commands:
    command = [sys.executable, str(kit / name), *args]
    run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    runs.append(dict(command=command, exit_code=run.returncode, expected_exit=expected,
                     stdout=run.stdout, stderr=run.stderr))
    assert run.returncode == expected, runs[-1]
assert hashes == {p.relative_to(repo).as_posix(): sha(p) for p in inputs}
report = dict(input_hashes=hashes, stable_inputs=True, byte_idempotent=True,
              publication_board_revision=board['revision'],
              frozen_candidate_replay_equal=True, runs=runs, rules_sha256=sha(target),
              comparison_note='Initial instrument hash predates explanatory docstring edit; sealed checker replays all preserved affected sources with identical candidates.')
(root / 'publication-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
for name in ['check_answered_not_established.py', 'check_questions.py', 'test_answered_advisories.py']:
    (root / ('validated-' + name + '.bin')).write_bytes((kit / name).read_bytes())
files = {p.relative_to(root).as_posix(): dict(bytes=p.stat().st_size, sha256=sha(p))
         for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(dict(files=files), indent=2) + '\n', encoding='utf-8')
print('PASS: eight controls, original self-test, frozen candidate replay, links, hygiene, board; advisory exit 1 retained;', len(files), 'sealed files')
