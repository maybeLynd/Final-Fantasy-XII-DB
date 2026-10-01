"""In-memory controls for the publication line-ending correction; no game access."""
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('metadata_reader', HERE / 'check.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
records = json.loads((HERE / 'recovery.json').read_text(encoding='utf-8'))['records']
git_bodies = {r['record']: r for r in json.loads((HERE / 'publication-normalization.json').read_text(encoding='utf-8'))['records']}
results = []
for row in records:
    raw = (reader.EXPERIMENTS / row['record']).read_bytes()
    lf = raw.replace(b'\r\n', b'\n')
    for label, data in [('LF', lf), ('CRLF', lf.replace(b'\n', b'\r\n'))]:
        body, original_raw_match = reader.verified_body(data, row, git_bodies[row['record']])
        results.append(dict(record=row['record'], representation=label, accepted=True,
                            observed_body_sha256=reader.digest(body), original_raw_match=original_raw_match))
    # Keep a valid prefix but alter actual historical text; line-ending tolerance must not hide it.
    changed = lf.replace(b'# EXP-', b'# EPX-', 1)
    assert changed != lf
    try:
        reader.verified_body(changed, row, git_bodies[row['record']])
    except AssertionError:
        results.append(dict(record=row['record'], representation='body text mutation', rejected=True))
    else:
        raise AssertionError(('changed body accepted', row['record']))
assert len(results) == 114
print(json.dumps(dict(scope='Private in-memory line-ending and changed-text controls only.', results=results), indent=2))
