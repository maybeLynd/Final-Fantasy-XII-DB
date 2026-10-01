"""Isolated actual team.apply finish-path control for M2/A16.

Runs the current production apply/transition functions on a deep-copied,
validated live board. No board, journal, lock or canonical file is written.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TOOLS = ROOT / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(TOOLS))
import team
import transitions


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


source = {
    'team.py': sha(TOOLS / 'team.py'),
    'transitions.py': sha(TOOLS / 'transitions.py'),
}
original_bytes = team.BOARD.read_bytes()
base = json.loads(original_bytes)
team.validate(base)
task_id = 'ASTRA-A16-REVIEW-ADMISSION-CONTROL'
assert all(t['id'] != task_id for t in base['tasks'])
task = {
    'id': task_id, 'kind': 'research', 'priority': 'P1',
    'target': 'isolated A16 review admission control',
    'scope': 'disposable deep-copy only',
    'completion': 'one structured independent review verdict',
    'dependencies': [], 'resources': [{'key': 'probe:astra-a16-admission'}],
    'reviews': {
        'author': 'ASTRA', 'commit': 'abcdef1',
        'record': 'Database/FFXII TZA/_experiments/evidence/control-only',
        'incorporation_owner': 'OPUS',
    },
}


def one(label, refs):
    board = copy.deepcopy(base)
    team.apply(board, 'ASTRA', {'action': 'add', 'task': task}, 'astra-a16-isolated')
    team.apply(board, 'SWE2-AUDIT-SPEC',
               {'action': 'claim', 'task': task_id, 'note': 'isolated control'},
               'astra-a16-isolated')
    error = None
    try:
        team.apply(board, 'SWE2-AUDIT-SPEC',
                   {'action': 'finish', 'task': task_id, 'note': label,
                    'result_refs': refs}, 'astra-a16-isolated')
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    row = next(t for t in board['tasks'] if t['id'] == task_id)
    planned = [x for x in transitions.plan(board) if x[1] == task_id]
    return {'case': label, 'finish_error': error, 'status': row['status'],
            'result_refs': row.get('result_refs'),
            'transition': [{'kind': x[0], 'id': x[1], 'detail': x[2],
                            'has_operation': x[3] is not None} for x in planned]}


cases = [
    one('missing-verdict', ['receipt:isolated']),
    one('exact-accept', ['receipt:isolated', 'verdict:ACCEPT']),
    one('malformed-verdict-lf', ['receipt:isolated', 'verdict:ACCEPT\n']),
]
assert cases[0]['status'] == 'DONE' and cases[0]['finish_error'] is None
assert [x['kind'] for x in cases[0]['transition']] == ['VERDICT-MISSING']
assert cases[1]['status'] == 'DONE' and cases[1]['finish_error'] is None
assert [x['kind'] for x in cases[1]['transition']] == ['INCORPORATE']
assert cases[1]['transition'][0]['has_operation']
assert cases[2]['status'] == 'DONE' and cases[2]['finish_error'] is None
assert [x['kind'] for x in cases[2]['transition']] == ['VERDICT-MISSING']
assert team.BOARD.read_bytes() == original_bytes, 'live board changed during isolated probe'
result = {
    'scope': 'Method A: actual imported apply/plan functions, isolated deep-copy; no CLI transaction/journal/lock',
    'source_sha256': source,
    'live_board_preimage_sha256': hashlib.sha256(original_bytes).hexdigest(),
    'live_board_revision': base['revision'],
    'live_board_unchanged': True,
    'cases': cases,
    'finding': 'team.apply finish admits DONE independent review without a structured verdict; transitions refuses incorporation',
    'limit': 'Does not test CLI/transaction, races, durable review receipt, OPUS repair or deployed A16 transition.',
}
if '--write' in sys.argv:
    (Path(__file__).parent / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'revision': base['revision'],
                  'outcomes': [(c['case'], c['status'], c['transition'][0]['kind']) for c in cases]}, indent=2))
