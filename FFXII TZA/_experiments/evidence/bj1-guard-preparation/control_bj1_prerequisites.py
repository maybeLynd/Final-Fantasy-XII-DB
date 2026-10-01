"""Actual checker CLI: upstream FAIL and zero-case output cannot become PASS."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main(out):
    if out.exists():
        raise ValueError('immutable control directory already exists')
    out.mkdir()
    sources = ['bj1_guard_capture.py', 'control_bj1_guard_capture.py',
               'bj1-retained-coverage-01.json','bj1-transport-controls-04.json']
    sources += [p.name for p in HERE.glob('bj1-*-run-*.status.json') if '-03.' not in p.name]
    sources += [p.name for p in HERE.glob('bj1-*-run-01.stdout')]
    sources += [p.name for p in HERE.glob('bj1-*-run-01.stderr')]
    sources += ['bj1-transport-controls-run-04.stdout','bj1-transport-controls-run-04.stderr',
                'bj1-transport-controls-01.json','bj1-transport-controls-02.json']
    sources = sorted(set(sources))
    result = dict(status='INVALID', driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), cases=[])
    for tag, file, field, replacement, message in [
        ('upstream-fail','bj1-transport-controls-run-04.status.json','exit',1,'required upstream execution failed/stale'),
        ('zero-case','bj1-transport-controls-04.json','controls',[],'control/cleanup incomplete')]:
        case=out/tag
        case.mkdir()
        for source in sources:
            shutil.copy2(HERE/source,case/source)
        path=case/file
        before=hashlib.sha256(path.read_bytes()).hexdigest()
        raw=json.loads(path.read_text()); raw[field]=replacement
        path.write_text(json.dumps(raw,indent=2)+'\n')
        command=[sys.executable,str(HERE/'check_bj1_preparation.py'),str(case)]
        p=subprocess.run(command,capture_output=True,text=True,timeout=25)
        (case/'stdout').write_text(p.stdout); (case/'stderr').write_text(p.stderr)
        receipt=dict(tag=tag, command=command, exit=p.returncode, mutation_file=file,
                     field=field,replacement=replacement, before_sha256=before,
                     mutated_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                     expected_refusal_seen=message in p.stderr,
                     no_pass='BJ1_PREPARATION_VALID' not in p.stdout)
        result['cases'].append(receipt)
        if not(p.returncode and receipt['expected_refusal_seen'] and receipt['no_pass']):
            raise AssertionError('required prerequisite refusal failed')
    result['status']='PASS_ACTUAL_UPSTREAM_AND_ZERO_CASE_REFUSALS'
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':
    main(Path(sys.argv[1]))
