"""Seal failed windows and controls without manufacturing an enemy-death or handler verdict."""
import ast
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import team
board = json.loads(team.BOARD.read_text())
assert any(t['id'] == 'ASTRA-ORDINARY-KILL-PUB' and t['agent'] == 'ASTRA'
           and t['status'] == 'ACTIVE' for t in board['tasks'])
def read(name):
    return json.loads((root/name).read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
sources = {}
normalized = []
for name in ('fight.json', 'fight-second.json'):
    d = read(name)
    assert d['pid'] == 38872 and d['target'] == 754798080
    assert d['status'] == 'WINDOW_EXPIRED' and len(d['samples']) == 590
    sources.update(d['sources'])
    gaps = []
    health = {}
    for sample in d['samples']:
        rows = sample['field']['rows']
        player = next(r for r in rows if r['slot'] == 0)
        target = next(r for r in rows if r['actor'] == d['target'])
        assert player['hp'] == 103 and target['hp'] == 84
        gaps.append(math.dist(player['position'], target['position']))
        for row in rows:
            health.setdefault(row['actor'], set()).add(row['hp'])
            if row['hp_raw_recheck'] is not None:
                assert struct.unpack('<i', bytes.fromhex(row['hp_raw_recheck']))[0] == row['hp']
    assert all(len(values-{None}) <= 1 for values in health.values())
    normalized.append(dict(file=name, status=d['status'], samples=len(d['samples']),
        sample_time_range=[d['samples'][0]['seconds'], d['samples'][-1]['seconds']],
        candidate_distance_range=[min(gaps), max(gaps)],
        actor_health_values={str(k): sorted(v, key=str) for k, v in health.items()},
        interpretation='No sampled numeric HP decline; no observed death; UI-to-actor binding not direct'))
inputs = []
for p in root.glob('*.json'):
    d = json.loads(p.read_text())
    if not isinstance(d, dict) or d.get('status') != 'CONTROLLED_PULSE':
        continue
    assert d['pid'] == 38872 and d['foreground']['ok']
    assert d['seen_indices'] == [d['expected_code']-28]
    assert not any(bytes.fromhex(d['after_release']))
    assert all(not any(bytes.fromhex(x)) for x in d['baseline'])
    assert 0 < d['hold'] <= 1
    sources.update(d['sources'])
    inputs.append(dict(file=p.name, key=d['key'], hold=d['hold']))
assert sum(x['key'] == 'W' for x in inputs) == 7
assert len(inputs) == 21, len(inputs)
for name in ('qualified.json', 'identity-after.json'):
    q = read(name)
    assert q['pid'] == 38872 and q['status'] == 'OBSERVED' and q['module_verdict'] == 'clean'
    assert q['code_identity'][0]['sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    sources.update(q['source_sha256'])
assert read('save-restored.json')['after'] == read('save-before.json')['files']
assert read('save-restored.json')['verified_files'] == 26
assert not read('close-receipt.json')['remaining']
for file, digest in sources.items():
    p = Path(file)
    assert sha(p) == digest, file
    (root/('validated-'+p.name+'.bin')).write_bytes(p.read_bytes())
for p in root.glob('*.py'):
    ast.parse(p.read_bytes())
runs = []
for name, args in [('check_source_hygiene.py', ['--paths', str(root)]),
                   ('check_links.py', ['--db', str(repo/'Database/FFXII TZA')]),
                   ('team.py', ['validate'])]:
    cmd = [sys.executable, str(kit/name), *args]
    run = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    runs.append(dict(command=cmd, exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr))
    assert run.returncode == 0, runs[-1]
report = dict(status='FAILED_KILL_RECIPE_EVIDENCE_SEALED_NO_HANDLER_COVERAGE',
              publication_revision=board['revision'], normalized=normalized, input_receipts=inputs,
              source_sha256=sources, checks=runs, restored_files=26,
              unexercised_live_branches=['player health stop', 'target zero HP', 'target absent stop'])
(root/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(root.iterdir())
         if p.is_file() and p.name != 'manifest.json'}
(root/'manifest.json').write_text(json.dumps(dict(files=files), indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], normalized=normalized, input_count=len(inputs), files=len(files))))
