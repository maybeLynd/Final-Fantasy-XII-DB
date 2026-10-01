"""Reviewed legacy anchor migration; default writes a proposal, never the live TSV."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import contradiction_index as ci

parser = argparse.ArgumentParser()
parser.add_argument('--publish', action='store_true', help='requires current @publication and TSV ownership')
args = parser.parse_args()
db = repo / 'Database/FFXII TZA'
ledger = db / '_index/CONTRADICTIONS.tsv'
original = ledger.read_bytes()
old = ci.read_ledger(ledger)
assert len(old) == 37, 'this is the one-time reviewed legacy migration, not a general merger'
assert all(not r.get('source_header') for r in old)
source_paths = sorted(p for p in db.rglob('*.md') if '_index/AUDIT-LOG' not in p.relative_to(db).as_posix())
source_hashes = {p.relative_to(db).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
found = ci.extract(db)
anchored = [dict(r) for r in old]
selectors = {
    'CON-034': 'the two pops fail differently on an empty stack',
    'CON-035': 'Only the *float* pop reports an empty stack',
    'CON-036': 'if (depth <= 0) return 0;',
    'CON-037': 'The reset clears `memberMask`',
}
overrides = []
for row in anchored:
    if row['id'] not in selectors:
        continue
    candidates = [r for r in found if r['document'].casefold() == row['document'].casefold()
                  and r['date'] == row['date'] and r['kind'] == row['kind']
                  and selectors[row['id']] in r['source_header']]
    assert len(candidates) == 1, (row['id'], candidates)
    match = candidates[0]
    row['source_header'] = match['source_header']
    overrides.append(dict(id=row['id'], document=match['document'], old_line=row['line'],
                          current_line=match['line'], source_header=match['source_header']))
merged, kept = ci.merge(found, anchored)
again, _ = ci.merge(found, merged)
assert again == merged, 'second extraction must be idempotent'
by_id = {r['id']: r for r in merged}
for row in old:
    assert row['id'] in by_id
    for column in ci.MANUAL:
        if row[column] and row[column] != 'UNSUMMARISED':
            assert by_id[row['id']][column] == row[column], (row['id'], column)
assert by_id['CON-021']['line'] != next(r['line'] for r in old if r['id'] == 'CON-021')
assert by_id['CON-033']['source_status'] == 'legacy-unmatched'
assert all(hashlib.sha256((db / p).read_bytes()).hexdigest() == digest for p, digest in source_hashes.items())
assert source_paths == sorted(p for p in db.rglob('*.md') if '_index/AUDIT-LOG' not in p.relative_to(db).as_posix())
assert ledger.read_bytes() == original
before_path = root / 'canonical-before.tsv'
if before_path.exists():
    assert before_path.read_bytes() == original
else:
    before_path.write_bytes(original)
proposal = root / 'proposal.tsv'
ci.write_ledger(proposal, merged, proposal.read_bytes() if proposal.exists() else None)
receipt = dict(before_sha256=hashlib.sha256(original).hexdigest(), old_records=len(old),
               found_markers=len(found), resulting_records=len(merged), preserved_cells=kept,
               curated_cells_retained_total=sum(bool(r[c] and r[c] != 'UNSUMMARISED') for r in old for c in ci.MANUAL),
               reviewed_anchor_overrides=overrides, idempotent=True,
               unmatched=[r['id'] for r in merged if r['source_status'] != 'present'],
               source_hashes=source_hashes,
               source_sha256=hashlib.sha256(Path(ci.__file__).read_bytes()).hexdigest(),
               published=args.publish)
if args.publish:
    ci.write_ledger(ledger, merged, original)
    assert ledger.read_bytes() == proposal.read_bytes()
receipt['proposal_sha256'] = hashlib.sha256(proposal.read_bytes()).hexdigest()
(root / ('published-migration.json' if args.publish else 'proposal-validation.json')).write_text(
    json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in receipt.items() if k != 'source_hashes'}, indent=2))
