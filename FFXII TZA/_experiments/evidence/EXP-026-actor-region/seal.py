"""Validate captured observations and decoder failure controls; no lifetime inference."""
import ast
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import capture_actor

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(kit))
import team
board = json.loads(team.BOARD.read_text())
assert any(t['id'] == 'ASTRA-ACTORLIVE-PUB' and t['agent'] == 'ASTRA'
           and t['status'] == 'ACTIVE' for t in board['tasks'])
def read(name):
    return json.loads((root / name).read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

sources = {}
normalized = []
for name, seq, ordinal, actor in [('before-zone.json', 5, 9, 1734153104),
                                  ('after-zone.json', 7, 74, 1734369776)]:
    d = read(name)
    assert d['status'] == 'OBSERVED' and d['pid'] == 11300 and len(d['samples']) == 40
    sources.update(d['sources'])
    for s in d['samples']:
        decoded = capture_actor.decode(bytes.fromhex(s['actor_raw']), actor)
        assert decoded == s['decoded']
        assert decoded['sequence'] == seq and decoded['region_map_matches']
        assert decoded['observed_counts'] == decoded['expected_counts']
        assert decoded['cursor_in_array'] and decoded['ordinal_bytes'] == [0, 255, 0, 0]
        assert s['player']['actor'] == actor and s['player']['hp'] == 103
        assert s['memberships'] == [{'manager_slot': 0, 'ordinal': ordinal}]
        m = s['managers'][0]
        table = bytes.fromhex(m['table_raw'])
        assert len(table) == m['count']*8 and struct.unpack_from('<Q', table, ordinal*8)[0] == actor
    normalized.append(dict(file=name, actor=actor, manager_slot=0, ordinal=ordinal, sequence=seq,
        samples=40, pointer_deltas=d['samples'][0]['decoded']['pointer_deltas'],
        counts=d['samples'][0]['decoded']['observed_counts'],
        cursor_values=sorted({s['decoded']['cursor'] for s in d['samples']}),
        ordinal_bytes=[0, 255, 0, 0],
        cross_frame_reads=sum(s['frame_before'] != s['frame_after'] for s in d['samples']),
        frame_range=[d['samples'][0]['frame_before'], d['samples'][-1]['frame_after']]))

# Perturb retained bytes, never the live process. A static-map disagreement must
# remain an observation, while unsupported layouts and short reads must fail.
base = read('before-zone.json')['samples'][0]
raw = bytearray.fromhex(base['actor_raw'])
actor = base['player']['actor']
controls = []
changed = bytearray(raw)
struct.pack_into('<Q', changed, 0xA8, actor+0x578)
assert not capture_actor.decode(changed, actor)['region_map_matches']
controls.append('wrong sequence-specific pointer detected as observation')
changed = bytearray(raw)
changed[0x11] = 0xFF
assert not capture_actor.decode(changed, actor)['cursor_in_array']
assert capture_actor.decode(changed, actor)['cursor'] == -1
controls.append('signed cursor FF decoded as -1 and out of array')
for label, bad in [('short header', raw[:0x100]), ('truncated extent', raw[:-1]),
                   ('unsupported sequence', raw[:3]+bytes([0x60])+raw[4:])]:
    try:
        capture_actor.decode(bad, actor)
    except ValueError:
        controls.append(label+' rejected')
    else:
        raise AssertionError(label)
for name in ('qualified.json', 'identity-after.json'):
    q = read(name)
    assert q['pid'] == 11300 and q['status'] == 'OBSERVED' and q['module_verdict'] == 'clean'
    assert q['code_identity'][0]['sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    sources.update(q['source_sha256'])
for name in ('load-menu.json', 'load-stepping.json', 'dismiss-load.json', 'face-exit.json', 'exit-w01.json'):
    d = read(name)
    assert d['status'] == 'CONTROLLED_PULSE' and d['pid'] == 11300
    assert d['foreground']['ok'] and d['seen_indices'] == [d['expected_code']-28]
    assert not any(bytes.fromhex(d['after_release']))
    assert all(not any(bytes.fromhex(x)) for x in d['baseline'])
    sources.update(d['sources'])
assert read('save-restored.json')['after'] == read('save-before.json')['files']
assert read('save-restored.json')['verified_files'] == 26
assert not read('close-receipt.json')['remaining']
for file, digest in sources.items():
    p = Path(file)
    assert sha(p) == digest, file
    (root / ('validated-'+p.name+'.bin')).write_bytes(p.read_bytes())
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
report = dict(status='TWO_SEQUENCE_MAPS_VALIDATED_BYTE_TRANSITIONS_UNOBSERVED',
              publication_revision=board['revision'], normalized=normalized, controls=controls,
              sources=sources, checks=runs, restored_files=26)
(root/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(root.iterdir())
         if p.is_file() and p.name != 'manifest.json'}
(root/'manifest.json').write_text(json.dumps(dict(files=files), indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], normalized=normalized, controls=controls, files=len(files))))
