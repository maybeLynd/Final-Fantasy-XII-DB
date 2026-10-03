"""Actual prerequisite invocation controls, not additional FF12 experiments."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
SOURCE = ROOT / 'Database/FFXII TZA/_experiments/evidence/sd194-stale-name-slice'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    positive = HERE / 'result-02.json'
    receipt = HERE / 'proof-02.status.json'
    status = json.loads(receipt.read_text())
    if (status.get('terminal') is not True or status.get('exit') != 0 or status.get('exception') is not None
        or status.get('driver_sha256') != sha(HERE / 'prove.py')
        or not positive.is_file() or json.loads(positive.read_text()).get('producer_complete') is not True):
        raise ValueError('positive producer prerequisite absent/failed')
    destination = HERE / sys.argv[1]; destination.mkdir()
    rows = []
    for case, expected in [('upstream-failed', 'upstream capture failed/incomplete'),
                           ('incomplete-source', 'retained source identity changed'),
                           ('changed-limit-branch', 'retained source identity changed')]:
        folder = destination / case; folder.mkdir()
        src = folder / 'source'; src.mkdir()
        for name in ['source-01.json', 'capture.py', 'capture-01.status.json', 'capture-01.stdout', 'capture-01.stderr']:
            shutil.copyfile(SOURCE / name, src / name)
        (src / 'dependencies').mkdir()
        for name in ['validate-title-source-annotations.py', 'prove_owner_reload_order.py']:
            shutil.copyfile(SOURCE / 'dependencies' / name, src / 'dependencies' / name)
        if case == 'upstream-failed':
            path = src / 'capture-01.status.json'; value = json.loads(path.read_text()); value['exit'] = 1
        else:
            path = src / 'source-01.json'; value = json.loads(path.read_text())
            body = next(r for r in value['ranges'] if r['start'] == '0x2df880')
            if case == 'incomplete-source':
                body['instructions'].pop(); body['end_exclusive'] = '0x2df8d8'
            else:
                ins = next(i for i in body['instructions'] if i['pc'] == '0x2df8c7')
                ins.update(bytes='7f05', mnemonic='jg')
            body['sha256'] = hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in body['instructions']))).hexdigest()
        path.write_text(json.dumps(value, indent=2))
        output = folder / 'result.json'
        command = [sys.executable, '-B', str(HERE / 'prove.py'), str(output), '--source', str(src)]
        row = dict(case=case, expected=expected, argv=command, driver_sha256=sha(HERE / 'prove.py'))
        try:
            child = subprocess.run(command, capture_output=True, text=True, timeout=60)
            (folder / 'stdout').write_text(child.stdout); (folder / 'stderr').write_text(child.stderr)
            row.update(exit=child.returncode, terminal=True, exception=None, output_exists=output.exists(),
                       stdout_sha256=sha(folder / 'stdout'), stderr_sha256=sha(folder / 'stderr'))
            valid = child.returncode != 0 and expected in child.stderr and not output.exists()
        except Exception as error:
            row.update(terminal=False, exception=repr(error)); valid = False
        row['expected_refusal'] = valid
        (folder / 'receipt.json').write_text(json.dumps(row, indent=2))
        rows.append(row)
        if not valid: raise ValueError('actual prerequisite refusal control failed: ' + case)
    result = dict(producer_complete=True, status='THREE_ACTUAL_PREREQUISITE_REFUSALS',
                  driver_sha256=sha(Path(__file__)), positive_result_sha256=sha(positive), positive_receipt_sha256=sha(receipt), controls=rows)
    (destination / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(dict(status=result['status'], native_or_live_runs=0)))

if __name__ == '__main__': main()
