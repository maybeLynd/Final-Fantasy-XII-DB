"""A13: execute the original CLI against one explicitly synthetic private fixture.

Read the previous shared-mutex failure before retrying. This source now keys the
fixture mutex to its path; never replace BOARD, monkeypatch locks, recover a board,
or replay the old transition operations. Stop after this discriminator is settled.
"""
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path.cwd().resolve()
W = Path(__file__).resolve().parent
RESUME = sys.argv[1:] == ['--resume-positive']
assert not sys.argv[1:] or RESUME
RUN = W / ('run-02' if RESUME else 'run-01')
SOURCE = ROOT / 'Database/Tools/analysis-kit/gfz-scripts/team.py'
sys.path.insert(0, str(SOURCE.parent))
import team


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_json(p, value):
    assert not p.exists(), str(p)
    p.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())


def git(*args):
    q = subprocess.run(['git', *args], capture_output=True)
    assert q.returncode == 0 and not q.stderr, (args, q.returncode, q.stderr)
    return q.stdout


assert not RUN.exists(), 'Published/attempted runs are never overwritten'
assert W.is_relative_to(ROOT / 'Database/Tools/work/ASTRA')
assert 'XIIOnlineTEAMBoardLock-{digest}' in SOURCE.read_text()
source_bytes = SOURCE.read_bytes()
rel = SOURCE.relative_to(ROOT).as_posix()
assert git('show', 'HEAD:' + rel) == source_bytes
RUN.mkdir()
(RUN / 'team.py').write_bytes(source_bytes)
(RUN / 'capture.py').write_bytes(Path(__file__).read_bytes())
identity = {
    'method': 'A: original repository Python/CLI, not FF12 native or live game',
    'head': git('rev-parse', 'HEAD').decode().strip(),
    'source_last_commit': git('log', '-1', '--format=%H', '--', rel).decode().strip(),
    'source_path': str(SOURCE), 'source_sha256': sha(source_bytes),
    'source_git_blob': git('hash-object', '--no-filters', str(SOURCE)).decode().strip(),
    'module_path': team.__file__, 'python': sys.version,
    'python_executable': sys.executable,
    'python_executable_sha256': sha(Path(sys.executable).read_bytes()),
    'python_base_executable': sys._base_executable,
    'python_base_sha256': sha(Path(sys._base_executable).read_bytes()),
    'driver_sha256': sha(Path(__file__).read_bytes()),
    'platform': sys.platform,
    'interventions': ['explicit synthetic schema-valid private board initialized once'],
    'limits': 'No production-board write, recovery, lock substitution, interrupted prefix, '
              'idempotent task transition, removed-lock, host controller or deployment proof.'
}
assert Path(team.__file__).resolve() == SOURCE
fixture = RUN / 'private' / 'TEAM.json'
fixture.parent.mkdir()
assert fixture.resolve().is_relative_to(RUN.resolve()) and fixture.resolve() != team.BOARD.resolve()
b = {'schema_version': 1, 'phase': 'DATABASE', 'revision': 0,
     'agents': {a: {'agent_id': a, 'primary_specialty': a, 'last_checkpoint': team.now()}
                for a in sorted(team.AGENTS)}, 'tasks': [], 'history': []}
team.refresh(b)
team.validate(b)
if RESUME:
    prior = W / 'run-01'
    old = json.loads((prior / 'raw.json').read_text())
    assert old['state'] == 'INVALID' and old['exception']['type'] == 'AssertionError'
    assert len(old['processes']) == 1 and len(old['stages']) == 1
    positive = old['processes'][0]
    assert positive['label'] == 'fresh-0' and positive['returncode'] == 0
    assert positive['terminal'] and not positive['timed_out'] and not positive['stderr']
    assert positive['stdout'] == 'Saved revision 1\r\n'
    assert old['identity']['source_sha256'] == identity['source_sha256']
    prior_board = prior / 'private/TEAM.json'
    prior_journal = team.journal_path(prior_board)
    oldb = json.loads(prior_board.read_bytes());team.validate(oldb)
    assert oldb['revision'] == 1 and oldb['history'][-1]['session'] == 'fresh-0'
    assert team.check_against_journal(prior_board.read_text(), oldb, team.journal_records(prior_board))['action'] == 'ok'
    assert not prior_board.with_suffix('.lock').exists()
    shutil.copyfile(prior_board, fixture)
    shutil.copyfile(prior_journal, team.journal_path(fixture))
    for n in ['initial-board.json', 'initial-journal.jsonl']:
        shutil.copyfile(prior / n, RUN / n)
    identity['interventions'].append('Copy exact prior successful private board+journal to a new private path; no fresh-positive replay')
    identity['retained_positive'] = {
        'raw_sha256': sha((prior / 'raw.json').read_bytes()),
        'driver_sha256': sha((prior / 'capture.py').read_bytes()),
        'board_sha256': sha(prior_board.read_bytes()),
        'journal_sha256': sha(prior_journal.read_bytes()),
        'status': 'Original overall run INVALID; successful fresh writer observation reused only at its stated scope'}
else:
    write_json(fixture, b)
write_json(RUN / 'identity.json', identity)
raw = {'identity': identity, 'stages': [], 'processes': [], 'state': 'INCOMPLETE'}
owned = []


def snapshot(label):
    assert SOURCE.read_bytes() == source_bytes, 'Source changed during experiment'
    board_bytes = fixture.read_bytes()
    jp = team.journal_path(fixture)
    journal_bytes = jp.read_bytes() if jp.exists() else b''
    (RUN / (label + '-board.json')).write_bytes(board_bytes)
    (RUN / (label + '-journal.jsonl')).write_bytes(journal_bytes)
    current = json.loads(board_bytes)
    team.validate(current)
    recs = [json.loads(x) for x in journal_bytes.decode().splitlines() if x.strip()]
    return {'label': label, 'revision': current['revision'],
            'board_sha256': sha(board_bytes), 'journal_sha256': sha(journal_bytes),
            'normalized_board_sha256': sha(fixture.read_text(encoding='utf-8').encode()),
            'history_sessions': [x.get('session') for x in current['history']],
            'checkpoint_notes': [x['note'] for x in current.get('checkpoints', [])],
            'journal': recs, 'lock_absent': not fixture.with_suffix('.lock').exists()}


def start(label, expected, note):
    opfile = RUN / (label + '-op.json')
    write_json(opfile, {'action': 'note', 'note': note})
    args = [sys.executable, '-B', str(SOURCE), 'apply', '--board', str(fixture),
            '--agent', 'ASTRA', '--session', label, '--expect-revision', str(expected),
            '--file', str(opfile)]
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    began = time.monotonic()
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    owned.append(p)
    r = {'label': label, 'argv': args, 'pid': p.pid, 'expected_revision': expected,
         'note': note, 'start_monotonic': began, 'op_sha256': sha(opfile.read_bytes())}
    raw['processes'].append(r)
    return p, r


def finish(p, r):
    try:
        out, err = p.communicate(timeout=5)
        r['timed_out'] = False
    except subprocess.TimeoutExpired:
        r['timed_out'] = True
        p.terminate()  # only this owned direct CLI, never another process or its lock
        out, err = p.communicate(timeout=5)
    r.update(stdout=out.decode(), stderr=err.decode(), returncode=p.returncode,
             elapsed_seconds=time.monotonic() - r['start_monotonic'], terminal=p.poll() is not None)
    assert r['terminal'] and not r['timed_out'], r
    return r


def boardcheck(label):
    args = [sys.executable, '-B', str(SOURCE), 'boardcheck', '--board', str(fixture)]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    owned.append(p)
    r = {'label': label, 'argv': args, 'pid': p.pid, 'start_monotonic': time.monotonic()}
    raw['processes'].append(r)
    finish(p, r)
    assert r['returncode'] == 0 and r['stdout'].splitlines() == ['board ok: ok'] and not r['stderr'], r
    return r


try:
    if RESUME:
        raw['stages'].append(old['stages'][0])
        raw['processes'].append(positive)
    else:
        raw['stages'].append(snapshot('initial'))
        p, r = start('fresh-0', 0, 'fresh-positive')
        finish(p, r)
        assert r['returncode'] == 0 and r['stdout'].splitlines() == ['Saved revision 1'] and not r['stderr']
    raw['stages'].append(snapshot('after-fresh'))
    boardcheck('fresh-health')  # feasibility/control before concurrent work
    p, r = start('stale-0', 0, 'must-not-land-stale')
    finish(p, r)
    assert r['returncode'] == 1 and not r['stdout'] and 'expected revision 0, board is at 1' in r['stderr']
    raw['stages'].append(snapshot('after-stale'))
    p1, r1 = start('race-a', 1, 'race-a-note')
    first_live_before_second = p1.poll() is None
    p2, r2 = start('race-b', 1, 'race-b-note')
    raw['race'] = {'first_live_before_second_launch': first_live_before_second,
                   'both_launched_before_communicate': True,
                   'limit': 'Process lifetime overlap, not proof of simultaneous lock entry.'}
    finish(p1, r1)
    finish(p2, r2)
    assert first_live_before_second and sorted([r1['returncode'], r2['returncode']]) == [0, 1]
    raw['stages'].append(snapshot('after-race'))
    boardcheck('race-health')
    p, r = start('fresh-2', 2, 'fresh-follow-on')
    finish(p, r)
    assert r['returncode'] == 0 and r['stdout'].splitlines() == ['Saved revision 3'] and not r['stderr']
    raw['stages'].append(snapshot('after-follow-on'))
    boardcheck('final-health')
    assert all(p.poll() is not None for p in owned)
    assert not fixture.with_suffix('.lock').exists() and SOURCE.read_bytes() == source_bytes
    raw['cleanup'] = {'all_owned_direct_processes_terminal': True, 'private_lock_absent': True,
                      'source_unchanged': True, 'fixture_retained_for_review': True,
                      'production_board_not_used_as_fixture': True,
                      'normal_game_or_production_host_health': 'NOT_OBSERVED'}
    raw['state'] = 'OBSERVED'
except BaseException as e:
    raw['exception'] = {'type': type(e).__name__, 'message': str(e)}
    raw['state'] = 'INVALID'
    raise
finally:
    for p in owned:
        if p.poll() is None:
            p.terminate()
            p.communicate(timeout=5)
    write_json(RUN / 'raw.json', raw)
print('ORIGINAL_WRITER_OBSERVED; checker acceptance required')
