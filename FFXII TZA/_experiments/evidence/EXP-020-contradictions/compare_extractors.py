"""Run old/revised extractors against isolated copies of one loss-triggering fixture."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import contradiction_index as ci

old = subprocess.check_output(['git', 'show', '9f3c3f5:Database/Tools/analysis-kit/gfz-scripts/contradiction_index.py'], cwd=repo)
(root / 'baseline-old.py').write_bytes(old)
header = '## CORRECTED 2026-09-10 — fixture actor claim'
seed = dict(id='CON-021', date='2026-09-10', kind='CORRECTED', category='actor.md',
            document='actor.md', line='1', claim=ci.snippet(header),
            correction='curated correction must survive', instrument='curated writer trace',
            addresses='00265020')
report = dict(question='Line drift, earlier marker insertion, and self-documentation false positive',
              seed=seed, runs={})
with tempfile.TemporaryDirectory(prefix='astra-exp020-') as scratch:
    for label, tool in [('old', root / 'baseline-old.py'), ('revised', Path(ci.__file__))]:
        db = Path(scratch) / label
        (db / '_index').mkdir(parents=True)
        (db / 'actor.md').write_text('\n\n' + header + '\n', encoding='utf-8')
        (db / 'earlier.md').write_text('## CORRECTED 2020-01-01 — fixture earlier marker\n', encoding='utf-8')
        (db / '_index/CONTRADICTION-LEDGER.md').write_text('A dated header — `CORRECTED 2026-09-02`, etc.\n', encoding='utf-8')
        ledger = db / '_index/CONTRADICTIONS.tsv'
        ledger.write_text('\t'.join(ci.COLUMNS[:10]) + '\n' + '\t'.join(seed[c] for c in ci.COLUMNS[:10]) + '\n', encoding='utf-8')
        (root / (label + '-before.tsv')).write_bytes(ledger.read_bytes())
        command = [sys.executable, str(tool), 'extract', '--db', str(db), '--ledger', str(ledger)]
        run = subprocess.run(command, capture_output=True, text=True)
        rows = ci.read_ledger(ledger)
        (root / (label + '-after.tsv')).write_bytes(ledger.read_bytes())
        report['runs'][label] = dict(command=command, exit_code=run.returncode,
                                    stdout=run.stdout, stderr=run.stderr,
                                    source_sha256=hashlib.sha256(tool.read_bytes()).hexdigest(), rows=rows)
        assert run.returncode == 0, run.stderr
assert len(report['runs']['old']['rows']) == 3
old_actor = next(r for r in report['runs']['old']['rows'] if r['document'] == 'actor.md')
assert old_actor['id'] != seed['id'] and old_actor['instrument'] == 'UNSUMMARISED'
revised = report['runs']['revised']['rows']
assert len(revised) == 2
new_actor = next(r for r in revised if r['document'] == 'actor.md')
assert new_actor['id'] == seed['id'] and new_actor['line'] == '3'
assert all(new_actor[c] == seed[c] for c in ci.MANUAL)
report['verdict'] = 'OLD_LOSS_REPRODUCED; REVISED_PRESERVATION_PASSED'
(root / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(report['verdict'])
