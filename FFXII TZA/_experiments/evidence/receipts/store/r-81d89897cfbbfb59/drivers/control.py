"""Three actual preparation-CLI refusals; no reviewer execution credit."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
DB='Database/FFXII TZA'
OLD=DB+'/_experiments/evidence/render-review-phase-qualification'
cases=[('missing-referent','missing local review referent'),
       ('conflicting-library','conflicting same-name review referent'),
       ('changed-old-member','old published member changed')]
out=Path(sys.argv[1]).resolve()
if out.exists():raise ValueError('existing control receipt: never replace')
out.mkdir()
receipts=[]
for name, expected in cases:
    root=out/name/'input'
    shutil.copytree(ROOT/OLD,root/OLD)
    for kind in ('clear-callee-footprints','removal-phase-contracts','slot-identity-publication'):
        rel=DB+'/_index/candidates/fable-review-astra-render-'+kind+'-1002'
        shutil.copytree(ROOT/rel,root/rel)
    if name=='missing-referent':
        (root/(DB+'/_index/candidates/fable-review-astra-render-clear-callee-footprints-1002/rv_clear.py')).unlink()
    elif name=='conflicting-library':
        path=root/(DB+'/_index/candidates/fable-review-astra-render-removal-phase-contracts-1002/rvlib.py')
        path.write_bytes(path.read_bytes()+b'\n# private contradictory referent\n')
    else:
        path=root/(OLD+'/fable-render-clear-callee-footprints-REVIEW.md')
        path.write_bytes(path.read_bytes()+b'\nchanged private input\n')
    output=out/name/'output'
    argv=[sys.executable,'-B',str(P/'prepare.py'),'--source',str(root),'--output',str(output)]
    r=subprocess.run(argv,capture_output=True,timeout=60)
    folder=out/name
    (folder/'stdout.txt').write_bytes(r.stdout);(folder/'stderr.txt').write_bytes(r.stderr)
    receipt=dict(id=name,case=name,argv=argv,exit=r.returncode,terminal=True,
                 expected_diagnostic=expected, diagnostic_observed=expected in r.stderr.decode('utf-8','replace'),
                 result_absent=not (output/'result.json').exists(), output_absent=not output.exists(),
                 driver_sha256=hashlib.sha256((P/'prepare.py').read_bytes()).hexdigest())
    (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if not (r.returncode and receipt['diagnostic_observed'] and receipt['output_absent']):
        raise ValueError('control failed: '+name)
    receipts.append(receipt)
(out/'result.json').write_text(json.dumps(dict(status='CONTROLS_PASS',cases=receipts,controller_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
print('PASS: 3 actual CLI refusals, no successful-looking output')
