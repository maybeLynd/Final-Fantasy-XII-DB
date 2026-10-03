"""Verify exact earlier driver bytes from known edits before retaining them.

These are hash-verified recovered preimages, not invented launch receipts.
"""
import hashlib
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
destination = HERE / 'driver-preimages'; destination.mkdir()
current = (HERE / 'prove.py').read_text()
previous = current.replace("DEFAULT = HERE / 'retained' if (HERE / 'retained/source-01.json').is_file() else ROOT / 'Database/FFXII TZA/_experiments/evidence/sd194-stale-name-slice'",
                           "DEFAULT = ROOT / 'Database/FFXII TZA/_experiments/evidence/sd194-stale-name-slice'")
previous = previous.replace("        source_pins=[dict(path='retained/source-01.json', sha256=PINS['source-01.json'])],\n", '')
initial = previous.replace('unconditional first byte copied, at most max(1,signed32(R9D)) copied bytes',
                           'unconditional first byte copied, max(1,signed32(R9D)) copied bytes')
controller = (HERE / 'control.py').read_text().replace("positive = HERE / sys.argv[2]", "positive = HERE / 'result-02.json'").replace("receipt = HERE / sys.argv[3]", "receipt = HERE / 'proof-02.status.json'")
members = []
for name, source, pin in [('prove-01.py', initial, '62d34593906b99d651d4908b2e3f6be909294db49d0caa44c64f45c97c9f5169'),
                          ('prove-02.py', previous, 'afd6b2e25b540b32066658d5866758adc55ee0d38f2c25996d3ec8aed41ed2fc'),
                          ('control-01.py', controller, '4ddc66dc2bb54ed85d85bdb84bdf4c91655a24929ec15bd375d0b5b767643cb9')]:
    raw = source.encode(); digest = hashlib.sha256(raw).hexdigest()
    if digest != pin: raise ValueError('recovered preimage does not match actual invocation: ' + name)
    (destination / name).write_bytes(raw); members.append(dict(path=name, sha256=digest))
(destination / 'receipt.json').write_text(json.dumps(dict(status='EXACT_HASH_VERIFIED_RECOVERED_DRIVER_PREIMAGES', members=members,
    limits='Recovery from known local edits checked against original actual launch hashes. No evidence of an additional launch.'), indent=2))
print(json.dumps(dict(status='EXACT_HASH_VERIFIED_RECOVERED_DRIVER_PREIMAGES', members=len(members))))
