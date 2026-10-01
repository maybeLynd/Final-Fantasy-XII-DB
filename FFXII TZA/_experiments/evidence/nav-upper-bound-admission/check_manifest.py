import hashlib,json
from pathlib import Path
w=Path(__file__).resolve().parent
# This checker can run in the frozen evidence tree; root manifest required.
manifest=json.loads((w/'manifest.json').read_text())
actual={x.relative_to(w).as_posix() for x in w.rglob('*') if x.is_file() and x!=w/'manifest.json' and '__pycache__' not in x.parts}
members=manifest['members'];listed={x['path'] for x in members}
assert actual and len(listed)==len(members) and actual==listed,(actual-listed,listed-actual)
for x in members:
 b=(w/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
h=w/'historical-manifest-omission'
f=json.loads((h/'failure.json').read_text());old=json.loads((h/'manifest.json').read_text())
missing=set(f['actual_preimage_paths'])-{x['path'] for x in old['members']}
assert missing==set(f['missing_manifest_members'])=={'historical-incomplete-precondition/manifest.json'}
assert missing<=listed
print('PASS complete exact manifest/file coverage; actual omitted historical manifest regression detected and corrected.',flush=True)
