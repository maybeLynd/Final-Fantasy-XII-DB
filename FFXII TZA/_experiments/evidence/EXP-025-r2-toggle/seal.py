"""Seal the two captured input cycles without asserting writer timing or combat effects."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import team

board = json.loads(team.BOARD.read_text())
assert any(t['id'] == 'ASTRA-R2-VISUAL-PUB' and t['agent'] == 'ASTRA'
           and t['status'] == 'ACTIVE' for t in board['tasks'])
def read(name):
    return json.loads((root / name).read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = {}
normalized = []
players = []
keys = ['toggle', 'latch', 'sticky', 'flag']
expected = [
    {'baseline': {(0, 0, 1, 1): 96},
     'held': {(0, 0, 1, 1): 1, (1, 1, 0, 1): 94, (1, 1, 0, 0): 1},
     'released': {(1, 0, 0, 0): 96}},
    {'baseline': {(1, 0, 0, 0): 96},
     'held': {(1, 0, 0, 0): 1, (0, 1, 0, 1): 95},
     'released': {(0, 0, 0, 1): 96}}]
for i in (1, 2):
    d = read(f'press-{i}.json')
    assert d['pid'] == 38024 and d['status'] == 'CONTROLLED_PRESS_RELEASE'
    assert d['down_accepted'] == d['up_accepted'] == 1
    assert len(d['samples']) == 288
    sources.update(d['sources'])
    phases = {}
    for phase in ('baseline', 'held', 'released'):
        samples = [s for s in d['samples'] if s['phase'] == phase]
        counts = Counter(tuple(s['values'][k] for k in keys) for s in samples)
        assert counts == expected[i-1][phase]
        seen = set()
        for s in samples:
            raw = bytes.fromhex(s['held_raw'])
            assert len(raw) == 256
            held = {j for j, b in enumerate(raw) if b}
            assert held <= ({89} if phase == 'held' else set())
            seen.update(held)
            assert s['foreground'] == d['foreground']['expected']
            assert all(s['values'][k] == v for k, v in
                       {'enable_a': 1, 'enable_b': 1, 'override': 0,
                        'audio_word': 0, 'audio_byte': 0, 'ui_register': 0}.items())
        assert seen == ({89} if phase == 'held' else set())
        phases[phase] = [{'tuple': list(k), 'count': v} for k, v in counts.items()]
    for field in ('field_before', 'field_after'):
        players.append(next(r for r in d[field]['rows'] if r['slot'] == 0))
    anomaly = [s for s in d['samples'] if s['phase'] == 'held'
               and tuple(s['values'][k] for k in keys) == (1, 1, 0, 1)]
    normalized.append(dict(file=f'press-{i}.json', phases=phases,
        frame_range=[d['samples'][0]['frame_before'], d['samples'][-1]['frame_after']],
        cross_frame_reads=sum(s['frame_before'] != s['frame_after'] for s in d['samples']),
        equal_one_held_span=([anomaly[0]['seconds'], anomaly[-1]['seconds']] if anomaly else None)))
assert all(p['hp'] == 103 and p['position_raw'] == players[0]['position_raw'] for p in players)
for name in ('qualified.json', 'identity-after.json'):
    q = read(name)
    assert q['pid'] == 38024 and q['status'] == 'OBSERVED' and q['module_verdict'] == 'clean'
    assert q['code_identity'][0]['sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    sources.update(q['source_sha256'])
assert read('save-restored.json')['after'] == read('save-before.json')['files']
assert read('save-restored.json')['verified_files'] == 26
assert not read('close-receipt.json')['remaining']
for file, digest in sources.items():
    p = Path(file)
    assert sha(p) == digest, file
    (root / ('validated-' + p.name + '.bin')).write_bytes(p.read_bytes())
for p in root.glob('*.py'):
    ast.parse(p.read_bytes())
runs = []
for name, args in [('check_source_hygiene.py', ['--paths', str(root)]),
                   ('check_links.py', ['--db', str(repo / 'Database/FFXII TZA')]),
                   ('team.py', ['validate'])]:
    command = [sys.executable, str(kit / name), *args]
    run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    runs.append(dict(command=command, exit_code=run.returncode, stdout=run.stdout, stderr=run.stderr))
    assert run.returncode == 0, runs[-1]
report = dict(status='SETTLED_VISUAL_RESULT_VALIDATED_HELD_TIMING_UNRESOLVED',
              publication_revision=board['revision'], cycles=2, loaded_states=1, samples=576,
              tuple_fields=keys, normalized=normalized, player=players[0], source_sha256=sources,
              checks=runs, restored_files=26)
(root / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(root.iterdir())
         if p.is_file() and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(dict(files=files), indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], normalized=normalized, evidence_files=len(files))))
