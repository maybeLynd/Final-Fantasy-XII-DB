"""Read-only receipt reduction. Does not execute writers or import producer tests."""
import copy
import hashlib
import json
from pathlib import Path
import sys


def sha(b):
    return hashlib.sha256(b).hexdigest()


def reduce(raw, run):
    assert raw['state'] == 'OBSERVED' and 'exception' not in raw
    assert sha((run / 'team.py').read_bytes()) == raw['identity']['source_sha256']
    assert sha((run / 'capture.py').read_bytes()) == raw['identity']['driver_sha256']
    assert raw['identity']['method'].startswith('A: original repository Python')
    labels = ['fresh-0', 'fresh-health', 'stale-0', 'race-a', 'race-b', 'race-health', 'fresh-2', 'final-health']
    cases = {r['label']: r for r in raw['processes']}
    assert len(cases) == len(raw['processes']) and set(cases) == set(labels)
    for r in cases.values():
        assert r['terminal'] is True and r['timed_out'] is False
        assert r['returncode'] in (0, 1) and r['elapsed_seconds'] < 6
        assert r['argv'][0] == raw['identity']['python_executable']
        assert r['argv'][1:3] == ['-B', raw['identity']['source_path']]
        if 'op_sha256' in r:
            folder = run.parent / 'run-01' if r['label'] == 'fresh-0' and 'retained_positive' in raw['identity'] else run
            opbytes = (folder / (r['label'] + '-op.json')).read_bytes()
            assert sha(opbytes) == r['op_sha256']
            assert json.loads(opbytes) == {'action': 'note', 'note': r['note']}
            assert r['argv'][r['argv'].index('--expect-revision') + 1] == str(r['expected_revision'])
            assert r['argv'][r['argv'].index('--session') + 1] == r['label']
    for n in ['fresh-health', 'race-health', 'final-health']:
        assert cases[n]['returncode'] == 0 and cases[n]['stdout'].splitlines() == ['board ok: ok'] and not cases[n]['stderr']
    states = raw['stages']
    assert [s['label'] for s in states] == ['initial', 'after-fresh', 'after-stale', 'after-race', 'after-follow-on']
    assert [s['revision'] for s in states] == [0, 1, 1, 2, 3]
    for s in states:
        board_bytes = (run / (s['label'] + '-board.json')).read_bytes()
        jb = (run / (s['label'] + '-journal.jsonl')).read_bytes()
        assert sha(board_bytes) == s['board_sha256'] and sha(jb) == s['journal_sha256']
        assert sha(board_bytes.decode().replace('\r\n', '\n').replace('\r', '\n').encode()) == s['normalized_board_sha256']
        board = json.loads(board_bytes)
        assert board['revision'] == s['revision'] and s['lock_absent'] is True
        assert [x.get('session') for x in board['history']] == s['history_sessions']
        assert [x['note'] for x in board.get('checkpoints', [])] == s['checkpoint_notes']
        recs = [json.loads(x) for x in jb.decode().splitlines() if x.strip()]
        assert recs == s['journal']
        if s['revision']:
            assert recs[-1]['kind'] == 'commit' and recs[-1]['rev'] == s['revision']
            assert recs[-1]['board_sha'] == s['normalized_board_sha256']
    assert states[1]['board_sha256'] == states[2]['board_sha256']
    assert states[1]['journal_sha256'] == states[2]['journal_sha256']
    assert cases['stale-0']['returncode'] == 1 and not cases['stale-0']['stdout']
    assert cases['stale-0']['stderr'].splitlines() == ['expected revision 0, board is at 1']
    race = [cases['race-a'], cases['race-b']]
    assert sorted(r['returncode'] for r in race) == [0, 1]
    winner = next(r for r in race if r['returncode'] == 0)
    loser = next(r for r in race if r['returncode'] == 1)
    assert winner['stdout'].splitlines() == ['Saved revision 2'] and not winner['stderr']
    assert loser['stderr'].splitlines() == ['expected revision 1, board is at 2'] and not loser['stdout']
    assert raw['race']['first_live_before_second_launch'] is True
    assert raw['race']['both_launched_before_communicate'] is True
    assert states[-1]['history_sessions'] == ['fresh-0', winner['label'], 'fresh-2']
    assert states[-1]['checkpoint_notes'] == ['fresh-positive', winner['note'], 'fresh-follow-on']
    assert [x['kind'] for x in states[-1]['journal']] == ['genesis', 'intent', 'commit', 'intent', 'commit', 'intent', 'commit']
    for label, revision in [('fresh-0', 1), ('fresh-2', 3)]:
        r = cases[label]
        assert r['returncode'] == 0 and r['stdout'].splitlines() == [f'Saved revision {revision}'] and not r['stderr']
    if 'retained_positive' in raw['identity']:
        prior = run.parent / 'run-01'
        old = json.loads((prior / 'raw.json').read_text())
        pin = raw['identity']['retained_positive']
        assert sha((prior / 'raw.json').read_bytes()) == pin['raw_sha256']
        assert sha((prior / 'capture.py').read_bytes()) == pin['driver_sha256']
        assert sha((prior / 'private/TEAM.json').read_bytes()) == pin['board_sha256']
        assert sha((prior / 'private/TEAM.json.journal.jsonl').read_bytes()) == pin['journal_sha256']
        assert old['state'] == 'INVALID' and old['processes'][0] == cases['fresh-0']
        assert states[1]['board_sha256'] == pin['board_sha256']
        assert states[1]['journal_sha256'] == pin['journal_sha256']
    assert all(raw['cleanup'][k] is True for k in ('all_owned_direct_processes_terminal', 'private_lock_absent', 'source_unchanged', 'fixture_retained_for_review', 'production_board_not_used_as_fixture'))
    assert raw['cleanup']['normal_game_or_production_host_health'] == 'NOT_OBSERVED'
    return {'scope': 'Fresh/stale expected-revision arbitration in original private-fixture CLI',
            'winner': winner['label'], 'stale_write_landed': False, 'race_commits': 1,
            'fresh_follow_on': True, 'full_A13': 'NOT_ACCEPTED',
            'limits': 'Two processes launched before collection; first nonterminal before second launch. Simultaneous child execution/contention, fairness, fault/recovery, removed-lock, controller/deployment and FF12 behavior are not proved.'}


if __name__ == '__main__':
    run = Path(__file__).resolve().parent / 'run-02'
    raw = json.loads((run / 'raw.json').read_text())
    result = reduce(raw, run)
    controls = []
    for name in ['missing-race', 'hidden-exit', 'extra-output']:
        bad = copy.deepcopy(raw)
        if name == 'missing-race':
            bad['processes'] = [x for x in bad['processes'] if x['label'] != 'race-b']
        elif name == 'hidden-exit':
            bad['processes'][2]['returncode'] = 0
        else:
            bad['processes'][0]['stdout'] += 'unexpected additional line\r\n'
        try:
            reduce(bad, run)
        except AssertionError:
            controls.append({'name': name, 'refused': True})
        else:
            raise AssertionError('Malformed receipt admitted: ' + name)
    print(json.dumps({'result': result, 'receipt_controls': controls}, indent=2))
