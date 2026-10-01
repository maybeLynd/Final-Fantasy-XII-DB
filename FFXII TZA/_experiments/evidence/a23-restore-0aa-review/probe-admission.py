"""Four bounded real restore-CLI cases, exact pinned source, synthetic names."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
W = P / 'admission-01'
W.mkdir(exist_ok=False)
ROOT = Path.cwd().resolve()
Z = ROOT / 'Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip'
S = P / 'generation.py'
sha = lambda b: hashlib.sha256(b).hexdigest()
if sha(Z.read_bytes()) != '23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7' or sha(S.read_bytes()) != 'c165172d618ccfb276f1ec117107b76e27ca7e96e294a841ef8fd913b5206658':
    raise RuntimeError('required original ZIP/module identity failed')
spec = importlib.util.spec_from_file_location('admission_generation_0aa', S)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
with zipfile.ZipFile(Z) as z:
    base = {n: z.read(n) for n in z.namelist()}
original_manifest = json.loads(base['MANIFEST.json'])
keys = [n for n, r in original_manifest['inputs'].items() if n.startswith('pkg:') and not r.get('external')][:2]
if len(keys) != 2 or sys.platform != 'win32':
    raise RuntimeError('native Windows or two snapshot inputs missing')

def variant(label, names=None, corrupt=False):
    payload = dict(base)
    man = copy.deepcopy(original_manifest)
    if names:
        value = copy.deepcopy(man['inputs'][keys[0]])
        body = payload['inputs/' + keys[0]]
        for old in keys:
            del man['inputs'][old]
            del payload['inputs/' + old]
        for new in names:
            man['inputs'][new] = copy.deepcopy(value)
            payload['inputs/' + new] = body
        payload['MANIFEST.json'] = (json.dumps(man, indent=2) + '\n').encode()
    if corrupt:
        target = 'inputs/' + keys[0]
        body = bytearray(payload[target])
        body[0] ^= 1
        payload[target] = bytes(body)
    path = W / (label + '.zip')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, value in payload.items():
            z.writestr(name, value)
    verified, info = G.verify_zip(path)
    target = W / ('disposable-' + label)
    argv = [sys.executable, '-B', str(S), 'restore', str(path), str(target)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=15)
    current = (target / 'CURRENT').exists()
    out = {'case': label, 'zip_sha256': sha(path.read_bytes()), 'verify': verified, 'verify_info': info,
           'argv': argv, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'current': current,
           'logical_names': names, 'snapshot_names': [G.snapshot_name(n) for n in names] if names else None}
    if current:
        _, directory, problems = G.Store(str(target)).open_current()
        out['reader_problems'] = problems
        out['physical_input_names'] = sorted(os.listdir(Path(directory) / 'inputs'))
        paths = [G.input_file(directory, n) for n in names] if names else []
        if paths:
            out['same_physical_file'] = os.path.samefile(*paths)
            out['bytes_equal'] = [Path(f).read_bytes() == base['inputs/' + keys[0]] for f in paths]
    return out

records = [variant('percent-distinct', ['ASTRA:a', 'ASTRA%3Aa']),
           variant('case-pair', ['ASTRA-case', 'astra-case']),
           variant('unverified', corrupt=True),
           variant('trailing-period', ['ASTRA-alias', 'ASTRA-alias.'])]
by = {r['case']: r for r in records}
checks = {'percent_distinct_positive': by['percent-distinct']['verify'] == 'VERIFIED' and by['percent-distinct']['exit'] == 0 and by['percent-distinct']['reader_problems'] == [] and by['percent-distinct']['same_physical_file'] is False,
          'case_pair_refused': by['case-pair']['verify'] == 'VERIFIED' and by['case-pair']['exit'] == 1 and 'REFUSED' in by['case-pair']['stdout'] and not by['case-pair']['current'],
          'unverified_refused': by['unverified']['verify'] == 'UNVERIFIED' and by['unverified']['exit'] == 1 and 'REFUSED' in by['unverified']['stdout'] and not by['unverified']['current'],
          'trailing_period_no_alias_acceptance': not (by['trailing-period']['current'] and by['trailing-period'].get('same_physical_file') is True)}
out = {'source_sha256': sha(S.read_bytes()), 'base_zip_sha256': sha(Z.read_bytes()), 'python': sys.version,
       'method': 'native Windows exact production restore CLI; labelled derived name/content fixtures, not game/runtime evidence',
       'records': records, 'checks': checks, 'controls_valid': all(v for k, v in checks.items() if k != 'trailing_period_no_alias_acceptance'),
       'verdict': 'ACCEPT_BOUNDED_ADMISSION' if all(checks.values()) else 'REJECT_TRAILING_PERIOD_PHYSICAL_ALIAS'}
(W / 'result.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verdict': out['verdict'], 'checks': checks}))
raise SystemExit(0 if all(checks.values()) else 1)
