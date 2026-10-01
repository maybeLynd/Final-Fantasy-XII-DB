"""Receipt refusal controls, private copies only; no original builder replay."""
import importlib.util, json, shutil, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('dependency_checker', W / 'check.py')
checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
checker.check(W)
results = []
for case in ('missing-manifest', 'nonzero-capture', 'changed-bound-table'):
    with tempfile.TemporaryDirectory(prefix='astra-uc1-receipt-') as d:
        target = Path(d)
        shutil.copytree(W / 'run-02', target / 'run-02')
        for name in ('capture.py', 'capture-terminal.json'): shutil.copyfile(W / name, target / name)
        if case == 'missing-manifest': (target / 'run-02/MANIFEST.json').unlink()
        elif case == 'nonzero-capture':
            p = target / 'capture-terminal.json'; q = json.loads(p.read_bytes()); q['returncode'] = 1
            p.write_text(json.dumps(q))
        else:
            p = target / 'run-02/bound-positive-inputs/uc1_1_64'; p.write_bytes(p.read_bytes() + b'\n# modified control\n')
        try: checker.check(target)
        except (AssertionError, FileNotFoundError) as e:
            results.append({'case': case, 'refused': True, 'exception': type(e).__name__, 'detail': str(e)})
        else: raise AssertionError('Required negative control accepted: ' + case)
assert len(results) == 3
out = W / 'reducer-controls.json'; assert not out.exists(), 'Write-once control receipt'
out.write_bytes((json.dumps(results, indent=2) + '\n').encode())
print(json.dumps(results, indent=2))
