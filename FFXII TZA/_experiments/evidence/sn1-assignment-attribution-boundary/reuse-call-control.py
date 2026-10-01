import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';P=Path('Database/FFXII TZA/_experiments/evidence/sn1-evctrl-jump-binding');sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (R/'result-before-reused-call-control.json').exists();current=(W/'check.py').read_bytes();assert b'retained_call_control=call_control' in current
(R/'checker-at-additive-control-preparation.py').write_bytes(current);(R/'result-before-reused-call-control.json').write_bytes((W/'result.json').read_bytes())
(W/'result.json').rename(W/'result-four-assignment-only.json')
for n in ['result.json','manifest.json']:(R/('parent63-'+n)).write_bytes((P/n).read_bytes())
print('Preserved valid four-assignment result; add retained63 positive to reject universal-minus-one interpretation, no old call execution repeated')
