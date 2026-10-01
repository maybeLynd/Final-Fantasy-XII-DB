import json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;T=W/'initial-parser-failure'
assert "assert 'FAIL S '" in (W/'capture.py').read_text(), 'Archive failed source BEFORE editing it; do not label a corrected copy as original'
assert not T.exists();T.mkdir()
for n in ('capture.py','invoke_private.py','invocation.json','retained','disposable'):
    p=(W/n).resolve();assert p.is_relative_to(W.resolve()) and p.exists()
    q=(T/n).resolve();assert q.is_relative_to(W.resolve())
    if p.is_file() and n=='capture.py':shutil.copyfile(p,q)
    else:shutil.move(str(p),str(q))
record=dict(status='INVALID_NORMALIZATION',error='AssertionError at capture.py line53 requiring literal FAIL S, while actual producer emits FAIL  S (two spaces).',source_returncode_assertion='[0,0,1] assertion line50 passed before parser failure; rawoutputs/privatefixtures retained, but result.json/finalidentity-readback not reached. No complete valid package inferred.',impact='Normalization/receipts incomplete, no freshproducer claim accepted; original41 source semantics/canonical evidence unaffected.',repair='Whitespace-token parser over nonempty required R1/R2/M/S tags; use initialrawcontrols to regress before correctedthreeboundedhostinvocations. No FF12/native/game rerun.',cleanup='Only ownclaimedW files moved to verifiedchild path; no peer/control/save/config/reference/board changes or lock operations.')
(T/'failure.json').write_text(json.dumps(record,indent=2)+'\n')
print('Preserved initialparser source/raw/privatefixtures, no semanticcompletion',flush=True)
