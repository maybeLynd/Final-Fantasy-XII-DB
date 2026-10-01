"""Actual retained-only producer invocation: failure propagation, never guest replay."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
SOURCE = W.parent / 'script-integer-divide-overflow'
OUT = W / 'invocation-status-controls'
assert not OUT.exists(), 'Immutable controls already exist; inspect receipt, never replay'
OUT.mkdir()
sha = lambda b: hashlib.sha256(b).hexdigest()
source = {n: sha((SOURCE/n).read_bytes()) for n in ['capture.py','check.py','freeze.py','raw.json','result.json']}
arms = []
for name in ['baseline','upstream-exit','upstream-exception','missing-checker','missing-member','empty-cases','missing-raw']:
    p = OUT/name
    p.mkdir()
    for n in ['capture.py','check.py','raw.json']:
        shutil.copyfile(SOURCE/n,p/n)
    shutil.copytree(SOURCE/'retained',p/'retained',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    if name == 'upstream-exit':
        (p/'check.py').write_text("import sys\nprint('PASS downstream-looking marker is not acceptance')\nsys.exit(7)\n")
    elif name == 'upstream-exception':
        (p/'check.py').write_text("raise RuntimeError('required upstream control failed')\n")
    elif name == 'missing-checker':
        (p/'check.py').rename(p/'withheld-checker.py')
    elif name == 'missing-member':
        (p/'retained/original5.bin').rename(p/'retained/withheld-original5.bin')
    elif name == 'empty-cases':
        raw=json.loads((p/'raw.json').read_text()); raw['cases']=[]
        (p/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
    elif name == 'missing-raw':
        # Retained directory remains: actual capture refuses fresh setup before a guest.
        (p/'raw.json').rename(p/'withheld-raw.json')
    before = sha((p/'raw.json').read_bytes()) if (p/'raw.json').exists() else None
    r=subprocess.run([sys.executable,str(p/'capture.py')],capture_output=True,text=True,timeout=30)
    (p/'stdout.txt').write_text(r.stdout); (p/'stderr.txt').write_text(r.stderr)
    if name == 'baseline':
        assert r.returncode == 0 and 'PASS80' in r.stdout and (p/'result.json').exists()
        assert json.loads((p/'result.json').read_text()) == json.loads((SOURCE/'result.json').read_text())
    else:
        assert r.returncode != 0 and not (p/'result.json').exists(), (name,r.returncode,r.stdout)
        expected={'upstream-exit':'CalledProcessError','upstream-exception':'RuntimeError',
                  'missing-checker':'AssertionError','missing-member':'FileNotFoundError',
                  'empty-cases':'AssertionError','missing-raw':'assert not R.exists()'}[name]
        assert expected in r.stderr, (name,r.stderr)
    assert 'CAPTURE80' not in r.stdout and not (p/'in-progress-cases.json').exists()
    assert not (p/'raw.json').exists() if before is None else sha((p/'raw.json').read_bytes()) == before
    arms.append(dict(name=name,returncode=r.returncode,stdout_sha256=sha(r.stdout.encode()),
                     stderr_sha256=sha(r.stderr.encode()),result_present=(p/'result.json').exists(),
                     raw_before_sha256=before,intervention='Private checker/input withholding; actual producer bytes unchanged'))
assert source == {n:sha((SOURCE/n).read_bytes()) for n in source}
receipt=dict(status='PASS_ACTUAL_RETAINED_PRODUCER_FAIL_CLOSED',source=source,
             driver_sha256=sha(Path(__file__).read_bytes()),arms=arms,
             limits='Only actual80 default retained path; not universal runner proof, no guest/native/live replay. Missing raw blocked by retained precondition, never treated as empty valid evidence. Freeze/publication separately inspect checked subprocess status; OPUS partition repair remains peer owned.')
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2),flush=True)
