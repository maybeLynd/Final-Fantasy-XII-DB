"""Freeze explicit BJ1 preparation inputs/receipts and record their provenance."""
import hashlib
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database').is_dir())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    import check_bj1_preparation as checked
    checked.main(HERE)  # Required semantic/receipt prerequisite, exception propagates.
    status=json.loads((HERE/'bj1-prerequisite-controls-run-01.status.json').read_text())
    cases=json.loads((HERE/'bj1-prerequisite-controls-01/result.json').read_text())
    if (status['exit']!=0 or status['driver_sha256']!=sha(HERE/'control_bj1_prerequisites.py') or
            cases['status']!='PASS_ACTUAL_UPSTREAM_AND_ZERO_CASE_REFUSALS' or
            len(cases['cases'])!=2 or not all(c['exit'] and c['expected_refusal_seen'] and c['no_pass'] for c in cases['cases'])):
        raise ValueError('actual upstream refusal controls incomplete')
    inputs=HERE/'bj1-input-sources-01.json'
    if inputs.exists():raise ValueError('immutable input receipt already exists')
    names=['Database/FFXII TZA/_index/candidates/bj1-opus-replay-boot-statics/bj1-guards.tsv',
           'Database/FFXII TZA/_index/candidates/bj1-opus-replay-boot-statics/bj1_guard_list.py',
           'Database/FFXII TZA/_index/candidates/bj1-opus-replay-boot-statics/result.json',
           'Database/Tools/analysis-kit/gfz-scripts/runtime_probe.py',
           'Database/Tools/analysis-kit/gfz-scripts/ffxii_runtime.py']
    names += ['Database/FFXII TZA/_experiments/evidence/phyre-startup-globals/'+x
              for x in ['title-defaults.json','title-pilot-readable.json','title-full.json','observe.py']]
    inputs.write_text(json.dumps([dict(path=n,sha256=sha(ROOT/n)) for n in names],indent=2)+'\n')
    files=['bj1_guard_capture.py','control_bj1_guard_capture.py','control_bj1_prerequisites.py',
           'check_bj1_preparation.py','prepare_bj1_packet.py','bj1-input-sources-01.json',
           'BJ1-METHOD-1001.md']
    files += [p.name for p in HERE.glob('control_bj1_guard_capture-before-*.py')]
    files += [p.name for p in HERE.glob('bj1-*.json') if '-operation-' not in p.name]
    files += [p.name for p in HERE.glob('bj1-*-run-*.stdout')]
    files += [p.name for p in HERE.glob('bj1-*-run-*.stderr')]
    files += ['bj1-prerequisite-controls-01/result.json']
    files += ['bj1-prerequisite-controls-01/'+tag+'/'+name
              for tag in ['upstream-fail','zero-case'] for name in ['stdout','stderr']]
    files=sorted(set(files))
    out=HERE/'bj1-guard-preparation-frozen-ready'
    if out.exists():raise ValueError('immutable packet already exists')
    out.mkdir()
    for name in files:
        dest=out/name; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(HERE/name,dest)
    shutil.copy2(HERE/'BJ1-PREPARATION-README-1001.md',out/'README.md')
    (out/'.gitattributes').write_text('* -text\n')
    members=[dict(path=p.relative_to(out).as_posix(),sha256=sha(p),bytes=p.stat().st_size)
             for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(kind='BJ1 read preparation, no game semantic closure',members=members),indent=2)+'\n')
    print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))


if __name__=='__main__':main()
