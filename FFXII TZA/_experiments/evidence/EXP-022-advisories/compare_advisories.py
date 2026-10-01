"""Compare candidate sets using identical document text and the same question ledger."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import types

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
db = repo / 'Database/FFXII TZA'
sys.path.insert(0, str(kit))
import check_answered_not_established as revised
import check_questions as questions

old = types.ModuleType('baseline_checker')
old.__file__ = str(root / 'baseline-checker.py.bin')
exec(compile(Path(old.__file__).read_bytes(), old.__file__, 'exec'), old.__dict__)
ledger = (db / '_index/OPEN-QUESTIONS.md').read_bytes()
texts = {p.relative_to(db).as_posix(): p.read_bytes() for p in db.rglob('*.md')
         if '_index' not in p.relative_to(db).parts}
with tempfile.TemporaryDirectory(prefix='astra-exp022-') as scratch:
    folder = Path(scratch) / '_index'
    folder.mkdir()
    (folder / 'OPEN-QUESTIONS.md').write_bytes(ledger)
    old_ids = old.answered_ids(ledger.decode('utf-8'))
    new_ids = revised.answered_ids(scratch)
    statuses, duplicates = questions.read_table(scratch)
    assert not duplicates
old_hits, new_hits = [], []
for name, raw in texts.items():
    text = raw.decode('utf-8-sig')
    old.scan(old_ids, text, name, old_hits)
    revised.scan(new_ids, text, name, new_hits)
assert len(old_hits) == 9, old_hits
assert len(new_hits) == 4, new_hits
assert sorted(r[2] for r in new_hits) == ['DD-1', 'I-6', 'I-6', 'Z-11']
contexts = []
for document, line, qid, text in sorted(set(map(tuple, old_hits + new_hits))):
    lines = texts[document].decode('utf-8-sig').splitlines()
    contexts.append(dict(document=document, line=line, qid=qid, matched_text=text,
                         canonical_status=statuses.get(qid),
                         context_start=max(1, line - 6), context=lines[max(0, line - 7):line + 6],
                         ledger_rows=[s for s in ledger.decode('utf-8').splitlines() if s.startswith('| ' + qid + ' |')]))
affected = sorted(set(row[0] for row in old_hits + new_hits))
for i, name in enumerate(affected, 1):
    (root / ('source-%02d.md.bin' % i)).write_bytes(texts[name])
(root / 'question-ledger.md.bin').write_bytes(ledger)
report = dict(old_answered_count=len(old_ids), new_answered_count=len(new_ids),
              old_hits=sorted(old_hits), new_hits=sorted(new_hits), contexts=contexts,
              source_receipts={name: dict(file='source-%02d.md.bin' % i,
                              sha256=hashlib.sha256(texts[name]).hexdigest()) for i, name in enumerate(affected, 1)},
              corpus_hashes={name: hashlib.sha256(raw).hexdigest() for name, raw in texts.items()},
              ledger_sha256=hashlib.sha256(ledger).hexdigest(),
              instrument_hashes={name: hashlib.sha256((kit / name).read_bytes()).hexdigest()
                                 for name in ['check_answered_not_established.py', 'check_questions.py']})
(root / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('Compared same text: old9 candidates, revised4 (I-6 twice, DD-1, Z-11); semantic dispositions required')
