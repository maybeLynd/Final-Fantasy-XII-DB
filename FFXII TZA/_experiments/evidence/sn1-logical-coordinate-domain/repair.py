import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'check.py';old=p.read_bytes();assert not (W/'result.json').exists()
R=W/'retained';R.mkdir(exist_ok=False);(R/'check-before-global-phase-fix.py').write_bytes(old)
s=old.decode();lines=s.splitlines(keepends=True);start=next(i for i,x in enumerate(lines) if x.startswith(' new=['));end=next(i for i,x in enumerate(lines) if x.startswith('result=dict('));assert end-start==4
for i in range(start,end):assert lines[i].startswith(' ');lines[i]=lines[i][1:]
assert p.read_bytes()==old;p.write_bytes(''.join(lines).encode())
(W/'failure.json').write_text(json.dumps(dict(status='INVALID_GLOBAL_ASSERTION_PHASE_BEFORE_RESULT',cause='Final full-four-module counts/control assertions were incorrectly indented inside module loop; after ctrl incomplete missing[] cannot match expected six btl/map records. Barrier correctly failed before result.',repair='Move full-source/control/absence assertions after all modules; retain old checker, no parent input/record recapture or native/compiler execution.',old_checker_sha256=hashlib.sha256(old).hexdigest(),corrected_checker_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),indent=2)+'\n')
