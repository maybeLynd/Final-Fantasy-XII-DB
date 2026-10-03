"""Copy immutable accepted input bytes; no new capture or scientific execution."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
SOURCE = ROOT / 'Database/FFXII TZA/_experiments/evidence/sd194-stale-name-slice'
destination = HERE / 'retained'; destination.mkdir()
files = ['source-01.json', 'capture.py', 'capture-01.status.json', 'capture-01.stdout', 'capture-01.stderr',
         'result-01.json', 'manifest.json', 'dependencies/validate-title-source-annotations.py', 'dependencies/prove_owner_reload_order.py']
receipt = []
for name in files:
    original, copied = SOURCE / name, destination / name
    copied.parent.mkdir(parents=True, exist_ok=True)
    raw = original.read_bytes(); shutil.copyfile(original, copied)
    if copied.read_bytes() != raw: raise ValueError('retained byte copy differs')
    receipt.append(dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
(HERE / 'retained-inputs-receipt.json').write_text(json.dumps(dict(source=str(SOURCE.relative_to(ROOT)),
    status='BYTE_IDENTICAL_RETAINED_INPUTS', files=receipt, limits='Existing ASTRA capture and external SPEC acceptance, not new captures or audit runs.'), indent=2))
print(json.dumps(dict(status='BYTE_IDENTICAL_RETAINED_INPUTS', members=len(receipt))))
