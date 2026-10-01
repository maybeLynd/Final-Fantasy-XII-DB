"""Offline source refresh: immutable prior candidate, one changed dependency."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'EXP-042-command-source-refresh'
KEY = '../../../../Tools/analysis-kit/gfz-scripts/runtime_probe.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    before = json.loads((OLD / 'dependencies.json').read_text())
    after = json.loads((HERE / 'dependencies.json').read_text())
    assert set(before) == set(after)
    assert [key for key in before if before[key] != after[key]] == [KEY]
    assert after[KEY] == digest(HERE / KEY)
    identical = {}
    for name in ('observe.py', 'test_observe.py'):
        assert (OLD / name).read_bytes() == (HERE / name).read_bytes()
        identical[name] = digest(HERE / name)
    old = load(OLD / 'observe.py', 'prior_observer')
    try:
        old.receipts()
    except ValueError as error:
        rejection = str(error)
        assert rejection == 'dependency changed: ' + KEY
    else:
        raise AssertionError('prior dependency pin did not reject changed source')
    current = load(HERE / 'observe.py', 'current_observer')
    receipts = current.receipts()
    run = subprocess.run([sys.executable, str(HERE / 'test_observe.py')],
                         capture_output=True, text=True)
    (HERE / 'unit-tests.txt').write_text(run.stdout + run.stderr, encoding='utf-8')
    assert run.returncode == 0, run.stderr
    assert 'Ran 11 tests' in run.stderr and '\nOK\n' in run.stderr
    assert receipts == current.receipts(), 'dependency changed during qualification'
    result = dict(status='OFFLINE QUALIFIED', prior_rejection=rejection,
                  prior_pin=before[KEY], current_pin=after[KEY], identical_files=identical,
                  sources=receipts, tests=11, native_process_calls=False,
                  limitation='Fake memory and time; no live original-game qualification or observations')
    (HERE / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: prior pin rejects; one dependency changed; identical observer; 11 offline tests')


if __name__ == '__main__':
    main()
