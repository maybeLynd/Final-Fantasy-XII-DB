"""Independent exact historical CLI cases; never open reserved device paths."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
W = P / 'run-01'
S = P / 'generation.py'
BASE = ROOT / 'Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip'
OLD = P.parent / 'restore-repair-0aa/admission-01'
sha = lambda b: hashlib.sha256(b).hexdigest()
EXPECTED_SOURCE = '033c37bd65cf4e9b5f33c94af14ad867877ac32cf992ad1515d4c230a6597dec'
INPUTS = {
    'original': (BASE, '23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7', None),
    'percent-distinct': (OLD / 'percent-distinct.zip', 'df0d9efa25ac741a62bb52722ebe05e1a398eaa21cf9b30b916366bcea009735', ['ASTRA:a', 'ASTRA%3Aa']),
    'case-pair': (OLD / 'case-pair.zip', 'd3ecb1b6cde9c7832b5d84b3a30135a89dc53ea81761f3d678a889c5b72cd0ba', None),
    'unverified': (OLD / 'unverified.zip', 'af46e93f3eaecc35d5900fcc3ae71cb51fb91d0a721ee5ae1d8382381de17a8a', None),
    'trailing-period': (OLD / 'trailing-period.zip', 'af7c3d88f51f7f7ebd2cd40b4c01428171d4dfc86d21a95f89e7a4c512a7ae09', ['ASTRA-alias', 'ASTRA-alias.']),
}
if sys.platform != 'win32' or sha(S.read_bytes()) != EXPECTED_SOURCE:
    raise RuntimeError('native Windows/source prerequisite failed')
for label, (path, expected, _) in INPUTS.items():
    if sha(path.read_bytes()) != expected:
        raise RuntimeError('retained ZIP prerequisite failed: ' + label)
spec = importlib.util.spec_from_file_location('astra_review_generation_87c', S)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
W.mkdir(exist_ok=False)

def write(name, value):
    (W / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

write('preconditions.json', {'source': str(S), 'source_sha256': EXPECTED_SOURCE,
      'driver_sha256': sha(Path(__file__).read_bytes()), 'python': sys.version,
      'interpreter': str(Path(sys.executable).resolve()), 'interpreter_sha256': sha(Path(sys.executable).read_bytes()),
      'platform': platform.platform(), 'retained_inputs': {k: {'path': str(v[0]), 'sha256': v[1]} for k, v in INPUTS.items()},
      'method': 'exact historical production Python CLI on native Windows; synthetic ZIP contents; pure reserved-name calls; no FF12 process'})

def invoke(label, archive, target):
    argv = [sys.executable, '-B', str(S), 'restore', str(archive), str(target)]
    out = {'argv': argv, 'target': str(target), 'deadline_seconds': 30}
    try:
        p = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
        (W / (label + '.stdout')).write_bytes(p.stdout)
        (W / (label + '.stderr')).write_bytes(p.stderr)
        out.update(exit=p.returncode, terminal=True, exception=None, stdout=p.stdout.decode('utf-8', 'replace'), stderr=p.stderr.decode('utf-8', 'replace'))
    except subprocess.TimeoutExpired as e:
        out.update(exit=None, terminal=False, exception='TimeoutExpired', stdout=(e.stdout or b'').decode('utf-8', 'replace'), stderr=(e.stderr or b'').decode('utf-8', 'replace'))
        write(label + '.receipt.json', out)
        raise
    write(label + '.receipt.json', out)
    return out

def tree(path):
    return {str(f.relative_to(path)): sha(f.read_bytes()) for f in path.rglob('*') if f.is_file()}

records = []
for label, (archive, expected, pair) in INPUTS.items():
    target = W / ('disposable-' + label)
    verified, info = G.verify_zip(archive)
    run = invoke(label, archive, target)
    r = {'case': label, 'zip_sha256': expected, 'verify': verified, 'verify_info': info, 'run': run,
         'target_exists': target.exists(), 'current': (target / 'CURRENT').exists()}
    if r['current']:
        man, directory, problems = G.Store(str(target)).open_current()
        r.update(reader_problems=problems, generation=man['generation'])
        rows = []
        with zipfile.ZipFile(archive) as z:
            for name, c in man['inputs'].items():
                if c['state'] in ('present', 'empty') and not c.get('external'):
                    f = Path(G.input_file(directory, name))
                    body = f.read_bytes()
                    rows.append({'logical': 'inputs/' + name, 'physical': f.name, 'bytes': len(body), 'sha256': sha(body), 'equal': body == z.read('inputs/' + name)})
            for name in man['outputs']:
                f = Path(directory) / 'outputs' / name
                body = f.read_bytes()
                rows.append({'logical': 'outputs/' + name, 'physical': f.name, 'bytes': len(body), 'sha256': sha(body), 'equal': body == z.read('outputs/' + name)})
            body = (Path(directory) / 'MANIFEST.json').read_bytes()
            rows.append({'logical': 'MANIFEST.json', 'sha256': sha(body), 'equal': body == z.read('MANIFEST.json')})
            r['zip_member_count'] = len(z.namelist())
        r.update(comparisons=rows, tree=tree(target), physical_inputs=sorted(os.listdir(Path(directory) / 'inputs')))
        if pair:
            paths = [G.input_file(directory, n) for n in pair]
            r.update(logical_pair=pair, mapped_pair=[G.snapshot_name(n) for n in pair], samefile=os.path.samefile(*paths))
    records.append(r)
    write('partial-records.json', records)

original_target = W / 'disposable-original'
before = tree(original_target)
nonempty = invoke('nonempty', BASE, original_target)
after = tree(original_target)
write('nonempty-trees.json', {'before': before, 'after': after, 'unchanged': before == after})

# A safe output alias fixture; never attempt reserved-name file creation.
with zipfile.ZipFile(BASE) as z:
    payload = {n: z.read(n) for n in z.namelist()}
man = json.loads(payload['MANIFEST.json'])
outkey = next(iter(man['outputs']))
record = copy.deepcopy(man['outputs'][outkey])
body = payload.pop('outputs/' + outkey)
del man['outputs'][outkey]
for name in ('ASTRA-view.json', 'ASTRA-view.json.'):
    man['outputs'][name] = copy.deepcopy(record)
    payload['outputs/' + name] = body
payload['MANIFEST.json'] = (json.dumps(man, indent=2) + '\n').encode()
derived = W / 'derived-trailing-output.zip'
with zipfile.ZipFile(derived, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, body in payload.items():
        z.writestr(name, body)
verified, info = G.verify_zip(derived)
target = W / 'disposable-trailing-output'
trailing_output = {'verify': verified, 'verify_info': info, 'zip_sha256': sha(derived.read_bytes()),
                   'run': invoke('trailing-output', derived, target), 'target_exists': target.exists(), 'current': (target / 'CURRENT').exists()}
write('trailing-output.json', trailing_output)

# Actual exact-source functions, without file-system/device access.
ordinary = [{'name': n, 'mapped': G.snapshot_name(n), 'reason': G.portable_component(n)} for n in ('ASTRA-plain.md', 'COM10.txt', 'LPT10.txt')]
ascii_devices = [{'name': n, 'mapped': G.snapshot_name(n), 'mapped_reason': G.portable_component(G.snapshot_name(n)), 'reason': G.portable_component(n)} for n in ('CON', 'nul.json', 'COM1.txt', 'LPT9')]
superscripts = [{'name': n, 'mapped': G.snapshot_name(n), 'reason': G.portable_component(n)} for stem in ('COM', 'LPT') for digit in ('\u00b9', '\u00b2', '\u00b3') for n in (stem + digit, stem.lower() + digit + '.json')]
devices = {'ordinary_controls': ordinary, 'ascii_controls': ascii_devices, 'documented_superscript_cases': superscripts,
           'no_device_path_opened': True, 'primary_contract_url': 'https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file'}
write('device-functions.json', devices)

by = {r['case']: r for r in records}
def positive(label):
    r = by[label]
    return r['verify'] == 'VERIFIED' and r['run']['terminal'] and r['run']['exit'] == 0 and not r['run']['stderr'] and r['current'] and r['reader_problems'] == [] and len(r['comparisons']) == r['zip_member_count'] and all(c['equal'] for c in r['comparisons'])
def refusal(r):
    return r['run']['terminal'] and r['run']['exit'] == 1 and 'REFUSED' in r['run']['stdout'] and not r['run']['stderr'] and not r['current'] and not r['target_exists']
checks = {'original_all35_preserved': positive('original') and by['original']['zip_member_count'] == 35,
          'percent_pair_distinct': positive('percent-distinct') and by['percent-distinct']['samefile'] is False,
          'retained_trailing_pair_distinct': positive('trailing-period') and by['trailing-period']['samefile'] is False and by['trailing-period']['mapped_pair'] == ['ASTRA-alias', 'ASTRA-alias%2E'],
          'case_pair_refused_before_writes': by['case-pair']['verify'] == 'VERIFIED' and refusal(by['case-pair']),
          'unverified_refused_before_writes': by['unverified']['verify'] == 'UNVERIFIED' and refusal(by['unverified']),
          'nonempty_refused_unchanged': nonempty['terminal'] and nonempty['exit'] == 1 and 'non-empty' in nonempty['stdout'] and not nonempty['stderr'] and before == after,
          'trailing_output_refused_before_writes': trailing_output['verify'] == 'VERIFIED' and refusal(trailing_output),
          'ordinary_device_control': all(r['mapped'] == r['name'] and r['reason'] is None for r in ordinary),
          'ascii_device_control': all(r['mapped'] != r['name'] and r['reason'] is not None and r['mapped_reason'] is None for r in ascii_devices),
          'superscript_devices_encoded_and_refused': all(r['mapped'] != r['name'] and r['reason'] is not None for r in superscripts)}
controls_valid = all(v for k, v in checks.items() if k != 'superscript_devices_encoded_and_refused')
result = {'source_sha256': EXPECTED_SOURCE, 'records': records, 'trailing_output': trailing_output, 'device_functions': devices,
          'checks': checks, 'controls_valid': controls_valid,
          'verdict': 'ACCEPT_BOUNDED_REPAIR' if all(checks.values()) else 'REJECT_DOCUMENTED_DEVICE_CLASS' if controls_valid else 'INVALID_CONTROLS',
          'limits': ['No device I/O; static admission counterexample only.', 'Native restore samples do not establish all Windows aliases, Unicode folding, legacy generations or deployment.', 'Synthetic ZIP fixtures are database workflow evidence, not game runtime evidence.']}
write('result.json', result)
print(json.dumps({'verdict': result['verdict'], 'checks': checks, 'native_runs': len(records) + 2}))
raise SystemExit(0 if all(checks.values()) else 1)
