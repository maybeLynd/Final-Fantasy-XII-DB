"""Freeze the additive independent review after checked, nonempty prerequisites."""
import hashlib
import json
from pathlib import Path
import shutil

P = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
W = ROOT/'Database/Tools/work/ASTRA/runtime-residue-method-retriage'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = W/'a23-restore-0aa-review-frozen-ready'
    if out.exists():
        raise ValueError('immutable packet exists; reconcile instead of retry')
    positive = json.loads((P/'terminal-01/result.json').read_text())
    receipt = json.loads((P/'terminal-01/driver-terminal.json').read_text())
    controls = json.loads((P/'terminal-01/prerequisite-controls.json').read_text())
    if (positive.get('status') != 'PASS_SCOPED_MP16' or not positive.get('complete')
            or positive.get('case_count') != 99 or len(positive['records']) != 99
            or not all(r['pass'] for r in positive['records'])
            or receipt.get('returncode') != 0 or receipt.get('terminal') is not True
            or receipt.get('stderr') or not receipt.get('stdout')
            or positive.get('driver_sha256') != sha(P/'probe-terminal.py')
            or receipt.get('driver_sha256') != sha(P/'probe-terminal.py')):
        raise ValueError('required terminal evidence failed/incomplete/stale')
    if (controls.get('pass') is not True or controls.get('complete') is not True
            or len(controls['records']) != 2 or not all(r['pass'] for r in controls['records'])
            or controls.get('driver_sha256') != sha(P/'probe-terminal.py')):
        raise ValueError('required source prerequisite controls failed/incomplete')
    admission = json.loads((P/'admission-01/result.json').read_text())
    old = json.loads((P/'result.json').read_text())
    if (admission.get('verdict') != 'REJECT_TRAILING_PERIOD_PHYSICAL_ALIAS'
            or admission.get('controls_valid') is not True
            or old['positive']['exit'] != 0 or old['reader_problems']
            or old['refusal']['exit'] != 1):
        raise ValueError('retained review inputs do not support the bounded verdict')
    if sha(P/'generation.py') != 'c165172d618ccfb276f1ec117107b76e27ca7e96e294a841ef8fd913b5206658':
        raise ValueError('retained module changed')
    archives = json.loads((P/'archive-inputs-qualified-1001.json').read_text())
    if not archives.get('complete') or len(archives['archives']) != 4:
        raise ValueError('retained raw archive prerequisites incomplete')
    for a in archives['archives']:
        if sha(ROOT/a['retained_path']) != a['sha256']:
            raise ValueError('retained archive changed')
    files = ['PLAN.md', 'RESULT.md', 'result.json', 'probe.py', 'generation.py',
             'cleanup.json', 'ADMISSION-PLAN.md', 'ADMISSION-RESULT.md',
             'probe-admission.py', 'admission-01/result.json', 'admission-01/cleanup.json',
             'archive-inputs-qualified-1001.json', 'TERMINAL-PLAN-1001.md',
             'TERMINAL-RESULT-1001.md', 'probe-terminal.py', 'freeze-review-1001.py']
    files += [p.relative_to(P).as_posix() for p in sorted((P/'terminal-01').iterdir())
              if p.is_file() and p.suffix in ('.py', '.json', '.tsv')]
    out.mkdir()
    for n in sorted(set(files)):
        dst = out/n
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(P/n, dst)
    shutil.copy2(P/'REVIEW-1001.md', out/'README.md')
    (out/'.gitattributes').write_text('* -text\n', encoding='utf-8')
    members = [{'path':p.relative_to(out).as_posix(), 'sha256':sha(p), 'bytes':p.stat().st_size}
               for p in sorted(out.rglob('*')) if p.is_file()]
    manifest = {'kind':'independent exact 0aa restore/terminal review', 'verdict':'REJECT',
                'external_inputs':'four pinned raw ZIP bodies retained at qualified paths; absent is INCOMPLETE',
                'members':members}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'members':len(members), 'manifest_sha256':sha(out/'manifest.json')}))


if __name__ == '__main__':
    main()
