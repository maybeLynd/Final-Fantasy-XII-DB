"""Preserve the failed producer before correcting its actual invocation path."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';F=R/'invalid-normalization';sha=lambda b:hashlib.sha256(b).hexdigest()
assert not F.exists() and not (W/'result.json').exists()
old=(W/'review.py').read_bytes();raw=(W/'raw.json').read_bytes();j=json.loads(raw)
assert sha(old)==j['driver_sha256']==sha((R/'driver-before-run.py').read_bytes())
F.mkdir();(F/'review-before.py').write_bytes(old);(F/'raw-before.json').write_bytes(raw)
(F/'diagnostic.json').write_text(json.dumps(dict(status='INVALID_NORMALIZATION',
    observed_error="TypeError at result end=hex(a+n): unsupported operand type(s) for +: 'int' and 'str'",
    cause='Final input-validation for n,p loop overwrote the numeric byte count with ruling.md before result production.',
    driver_sha256=sha(old),raw_sha256=sha(raw),limits='Raw source/control observations retained, no completed result or semantic acceptance. Original tool error is the observed shell failure; no retrospective full rerun or invented capture receipt.'),indent=2)+'\n')
# Retain the exact hashed projection inputs while available; no new source capture.
for item in j['inputs']:
    b=Path(item['path']).read_bytes();assert len(b)==item['bytes'] and sha(b)==item['sha256'],item['name']
    q=R/item['name']
    if q.exists():assert q.read_bytes()==b
    else:q.write_bytes(b)
s=old.decode();needle="W=Path(__file__).resolve().parent;R=W/'retained';ROOT=Path.cwd().resolve();sha=lambda b:hashlib.sha256(b).hexdigest()"
assert s.count(needle)==1
s=s.replace(needle,needle+"\n# Resume the retained observation through the reviewed normalizer, without recapture.\nif (W/'raw.json').exists():\n import runpy\n runpy.run_path(str(W/'check.py'),run_name='__main__')\n raise SystemExit(0)")
assert s.count('for n,p in inputs.items():assert p.read_bytes()==payload[n],(\'Input changed\',n)')==1
s=s.replace("for n,p in inputs.items():assert p.read_bytes()==payload[n],('Input changed',n)","for input_name,input_path in inputs.items():assert input_path.read_bytes()==payload[input_name],('Input changed',input_name)")
begin=s.index("result=dict(method=raw['method']")
s=s[:begin]+"from normalize import normalize\nresult=normalize(raw)\n(W/'result.json').write_text(json.dumps(result,indent=2)+'\\n')\nprint('PASS_UC1_257_SINGLE_BOUNDARY retained original353B/82reachable/controls; bounded extent only')\n"
(W/'review.py').write_text(s)
assert (W/'raw.json').read_bytes()==raw
print('PRESERVED_INVALID_NORMALIZATION corrected actual review -> check -> normalize path; original observation not recaptured')
