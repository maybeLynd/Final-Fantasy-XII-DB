"""Validate the live migration and seal owned evidence; no extraction writes to live TSV."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import contradiction_index as ci

command = [sys.executable, str(kit / 'test_contradiction_index.py'), '-v']
run = subprocess.run(command, capture_output=True, text=True)
assert run.returncode == 0, run.stderr
assert 'Ran 14 tests' in run.stderr
db = repo / 'Database/FFXII TZA'
ledger = db / '_index/CONTRADICTIONS.tsv'
old = ci.read_ledger(root / 'canonical-before.tsv')
current = ci.read_ledger(ledger)
before = ledger.read_bytes()
found = ci.extract(db)
again, _ = ci.merge(found, current)
assert again == current and ledger.read_bytes() == before
assert len(current) == 59
by_id = {r['id']: r for r in current}
preserved = 0
for row in old:
    assert row['id'] in by_id
    for column in ci.MANUAL:
        if row[column] and row[column] != 'UNSUMMARISED':
            assert by_id[row['id']][column] == row[column]
            preserved += 1
assert preserved == 120
for name in ['contradiction_index.py', 'test_contradiction_index.py']:
    (root / ('validated-' + name)).write_bytes((kit / name).read_bytes())
report = dict(command=command, exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr,
              historical_ids_preserved=len(old), curated_cells_preserved=preserved,
              current_rows=len(current), fresh_read_only_reextraction_equal=True,
              ledger_sha256=hashlib.sha256(before).hexdigest(),
              input_source_sha256={name: hashlib.sha256((kit / name).read_bytes()).hexdigest()
                                   for name in ['contradiction_index.py', 'test_contradiction_index.py']})
(root / 'publication-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
files = {p.relative_to(root).as_posix(): dict(bytes=p.stat().st_size,
         sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob('*'))
         if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(dict(files=files), indent=2) + '\n', encoding='utf-8')
print('PASS:14 tests;37 old IDs and120 curated cells;59 rows;fresh extraction unchanged;', len(files), 'sealed files')
