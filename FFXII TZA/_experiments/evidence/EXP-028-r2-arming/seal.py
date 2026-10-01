"""Validate short-press arming observations at sampled precision, not atomic writer order."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import team
board = json.loads(team.BOARD.read_text())
assert any(t['id'] == 'ASTRA-R2-ARMING-PUB' and t['agent'] == 'ASTRA'
           and t['status'] == 'ACTIVE' for t in board['tasks'])
def read(name):
    return json.loads((root/name).read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
sources = {}
players = []
normalized = []
for name in ('activation.json', 'deactivation.json'):
    d = read(name)
    assert d['pid'] == 35836 and d['status'] == 'CONTROLLED_PRESS_RELEASE'
    assert d['down_accepted'] == d['up_accepted'] == 1
    ss = d['samples']
    assert Counter(s['phase'] for s in ss) == {'baseline': 96, 'held': 15, 'released': 191}
    sources.update(d['sources'])
    for phase in ('baseline', 'held', 'released'):
        seen = set()
        for s in (s for s in ss if s['phase'] == phase):
            raw = bytes.fromhex(s['held_raw'])
            assert len(raw) == 256
            held = {i for i, b in enumerate(raw) if b}
            assert held <= ({89} if phase == 'held' else set())
            seen.update(held)
            assert s['foreground'] == d['foreground']['expected']
            assert all(s['values'][k] == v for k, v in {'arming_threshold': 60, 'time_base': 2,
                'enable_a': 1, 'enable_b': 1, 'ui_register': 0, 'override': 0,
                'audio_word': 0, 'audio_byte': 0}.items())
        assert seen == ({89} if phase == 'held' else set())
    for field in ('field_before', 'field_after'):
        players.append(next(r for r in d[field]['rows'] if r['slot'] == 0))
    normalized.append(dict(file=name, samples=len(ss),
        frame_range=[ss[0]['frame_before'], ss[-1]['frame_after']],
        cross_frame_reads=sum(s['frame_before'] != s['frame_after'] for s in ss),
        first=ss[0], last=ss[-1]))
assert all(p['hp'] == 103 and p['position_raw'] == players[0]['position_raw'] for p in players)
a = read('activation.json')['samples']
cross = next(i for i, s in enumerate(a) if s['values']['flag'] == 0)
before, after = a[cross-1], a[cross]
assert before['values']['arming_counter'] == 59 and before['values']['arming_word'] == 0x11
assert after['values']['arming_counter'] == 60 and after['values']['arming_word'] == 0x15
assert before['frame_before'] == before['frame_after'] == 1499
assert after['frame_before'] == after['frame_after'] == 1500
assert before['phase'] == after['phase'] == 'released'
released = [s for s in a if s['phase'] == 'released']
assert released[0]['values']['arming_counter'] == 13
assert all(s['values']['latch'] == 0 and s['values']['toggle'] == 1 for s in released)
assert all(s['values']['arming_counter'] == 60 and s['values']['arming_word'] == 0x15
           and s['values']['flag'] == 0 for s in a[cross:])
d = read('deactivation.json')['samples']
assert all(s['values']['arming_counter'] == 60 and s['values']['sound_handle'] == 9 for s in d)
assert all(s['values']['arming_word'] == 2 and s['values']['flag'] == 1
           and s['values']['toggle'] == 0 for s in d if s['phase'] == 'released')
for name in ('qualified.json', 'identity-after.json'):
    q = read(name)
    assert q['pid'] == 35836 and q['status'] == 'OBSERVED' and q['module_verdict'] == 'clean'
    assert q['code_identity'][0]['sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    sources.update(q['source_sha256'])
for name in ('load-menu.json', 'load-stepping.json', 'dismiss-load.json'):
    q = read(name)
    assert q['status'] == 'CONTROLLED_PULSE' and q['pid'] == 35836
    assert q['seen_indices'] == [52] and not any(bytes.fromhex(q['after_release']))
    sources.update(q['sources'])
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
report = dict(status='ARMING_AFTER_SHORT_RELEASE_VALIDATED_AT_SAMPLE_PRECISION',
    publication_revision=board['revision'], normalized=normalized,
    threshold_bracket=[before, after], bracket_seconds=after['seconds']-before['seconds'],
    sources=sources, checks=runs, restored_files=26)
(root/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(root.iterdir())
         if p.is_file() and p.name != 'manifest.json'}
(root/'manifest.json').write_text(json.dumps(dict(files=files), indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], samples=604, bracket_seconds=report['bracket_seconds'], files=len(files))))
