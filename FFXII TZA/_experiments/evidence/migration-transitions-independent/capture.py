"""Actual transition CLI and supported writer on explicit, isolated fixtures."""
import copy, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent; R = W / 'run-01'
assert not R.exists(), 'Retain original run; never overwrite/replay'
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
R.mkdir(); root = R / 'source'; here = root / 'Database/Tools/analysis-kit/gfz-scripts'; here.mkdir(parents=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw = {'method': 'A actual CLI/private validated fixtures; one explicit failed-writer intervention',
       'source_tree_commit': commit, 'driver_sha256': sha(__file__), 'python': sys.version,
       'sources': {}, 'cases': [], 'finished': False}
for n in ('transitions.py', 'team.py'):
    rel = 'Database/Tools/analysis-kit/gfz-scripts/' + n
    data = subprocess.check_output(['git', 'show', commit + ':' + rel]); (here / n).write_bytes(data)
    raw['sources'][n] = {'sha256': sha(here / n), 'path': rel,
        'blob': subprocess.check_output(['git', 'rev-parse', commit + ':' + rel], text=True).strip(),
        'last_commit': subprocess.check_output(['git', 'log', '-1', '--format=%H', commit, '--', rel], text=True).strip()}
spec = importlib.util.spec_from_file_location('isolated_transition_team', here / 'team.py')
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
assert T.ROOT == root and T.JOURNAL_DIR.is_relative_to(root) and T.BOARD.is_relative_to(root)
base = str(Path(sys._base_executable)); env = os.environ.copy()
env['TEAM_SESSION'] = 'ASTRA-labelled-private-transition-controls'; env.pop('TEAM_AGENT', None)
stamp = '2026-09-29T06:30:00+00:00'
reference = raw['sources']['transitions.py']['last_commit']
rv = {'author': 'OPUS', 'commit': reference, 'record': 'Database/Tools/analysis-kit/gfz-scripts/transitions.py'}
def fixture(name, reviews=None, refs=None, reviewer='ASTRA', note='labelled fixture; no production review'):
    d = R / name; d.mkdir(); bp = d / 'TEAM.json'
    t = {'id': 'REVIEW-' + name.upper(), 'kind': 'research', 'priority': 'P2', 'agent': reviewer,
         'assigned_to': reviewer, 'status': 'DONE', 'target': 'labelled fixture only', 'scope': 'synthetic review routing',
         'completion': 'synthetic input only', 'checkpoint': note, 'started_at': stamp, 'updated_at': stamp,
         'dependencies': [], 'resources': [{'key': 'request:fixture/' + name}],
         'reviews': copy.deepcopy(rv if reviews is None else reviews),
         'result_refs': ['verdict:REJECT', 'receipt:labelled-fixture'] if refs is None else refs}
    agents = {n: {'agent_id': n, 'primary_specialty': 'labelled fixture only', 'current_task': [],
              'claimed_scope': [], 'dependencies': [], 'blockers': [], 'last_checkpoint': stamp, 'status': 'READY'} for n in T.AGENTS}
    b = {'schema_version': 1, 'phase': 'DATABASE', 'revision': 0, 'recovery_epoch': 0,
         'agents': agents, 'tasks': [t], 'history': [], 'checkpoints': []}
    T.refresh(b); T.validate(b)
    text = json.dumps(b, indent=2) + '\n'; bp.write_text(text); (d / 'before.json').write_text(text)
    return d, bp
def command(bp): return [base, '-B', str(here / 'transitions.py'), '--board', str(bp), '--agent', 'SWE2-FRONTIER', '--apply', '--json']
def run(bp):
    args = command(bp); q = subprocess.run(args, env=env, capture_output=True, text=True, timeout=20)
    try: report = json.loads(q.stdout)
    except json.JSONDecodeError: report = None
    return {'args': args, 'returncode': q.returncode, 'stdout': q.stdout, 'stderr': q.stderr,
            'parsed_report': report, 'timed_out': False, 'child_reaped': True}
def retain(name, bp, receipt, expected):
    after = json.loads(bp.read_text()); T.validate(after)
    (bp.parent / 'after.json').write_text(json.dumps(after, indent=2) + '\n')
    added = [t for t in after['tasks'] if not t['id'].startswith('REVIEW-')]
    item = {'name': name, 'expected': expected, 'cli': receipt, 'added': added,
            'revision': after['revision'], 'history': after['history'], 'board_sha256': sha(bp)}
    raw['cases'].append(item); (bp.parent / 'receipt.json').write_text(json.dumps(item, indent=2) + '\n')
try:
    declarations = [
      ('valid-reject', rv, None, 'ASTRA', 'repair'),
      ('valid-accept', dict(rv, incorporation_owner='FABLE'), ['verdict:ACCEPT', 'receipt:labelled-fixture'], 'ASTRA', 'incorporate'),
      ('accepted-no-owner', rv, ['verdict:ACCEPT', 'receipt:labelled-fixture'], 'ASTRA', 'accepted-no-op'),
      ('accepted-author-owner', dict(rv, incorporation_owner='OPUS'), ['verdict:ACCEPT', 'receipt:labelled-fixture'], 'ASTRA', 'accepted-no-op'),
      ('missing-verdict', rv, ['receipt:labelled-fixture'], 'ASTRA', 'VERDICT-MISSING'),
      ('prose-verdict', rv, ['receipt:labelled-fixture'], 'ASTRA', 'VERDICT-MISSING'),
      ('conflicting-verdict', rv, ['verdict:ACCEPT', 'verdict:REJECT'], 'ASTRA', 'VERDICT-CONFLICT'),
      ('malformed-review-string', 'wrong type', None, 'ASTRA', 'MALFORMED'),
      ('missing-commit', dict(rv, commit=None), None, 'ASTRA', 'MALFORMED'),
      ('typed-commit', dict(rv, commit={'not': 'a SHA'}), None, 'ASTRA', 'MALFORMED'),
      ('non-sha-commit', dict(rv, commit='not a SHA'), None, 'ASTRA', 'MALFORMED'),
      ('typed-record', dict(rv, record={'not': 'a repository path'}), None, 'ASTRA', 'MALFORMED'),
      ('invalid-author', dict(rv, author='UNKNOWN'), None, 'ASTRA', 'MALFORMED'),
      ('typed-author', dict(rv, author=['OPUS']), None, 'ASTRA', 'MALFORMED'),
      ('self-review', dict(rv, incorporation_owner='FABLE'), ['verdict:ACCEPT', 'receipt:labelled-fixture'], 'OPUS', 'independent-review-refusal'),
    ]
    for name, reviews, refs, reviewer, expected in declarations:
        d, bp = fixture(name, reviews, refs, reviewer, 'verdict:ACCEPT in prose is not structured' if name == 'prose-verdict' else 'labelled fixture')
        retain(name, bp, run(bp), expected)
    # Real supported writer idempotence: one add then an actual CLI rerun.
    d, bp = fixture('sequential-idempotence')
    first, second = run(bp), run(bp)
    retain('sequential-idempotence', bp, {'first': first, 'second': second}, 'one-repair')
    # Two actual processes, same disposable board and original lock/journal.
    d, bp = fixture('concurrent-idempotence'); args = command(bp)
    children = [subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
    receipts = []
    try:
        for p in children:
            out, err = p.communicate(timeout=20)
            try: report = json.loads(out)
            except json.JSONDecodeError: report = None
            receipts.append({'args': args, 'pid': p.pid, 'returncode': p.returncode, 'stdout': out, 'stderr': err,
                             'parsed_report': report, 'timed_out': False, 'child_reaped': True})
    finally:
        for p in children:
            if p.poll() is None: p.kill(); p.communicate(timeout=5)
    retain('concurrent-idempotence', bp, {'processes': receipts}, 'one-repair')
    # Explicit caller-failure intervention, not a natural team.py failure claim.
    d, bp = fixture('failed-writer-saved-prefix'); original = (here / 'team.py').read_bytes()
    needle = b'if __name__ == "__main__":\n    main()'
    assert original.count(needle) == 1
    fault = original.replace(needle, b'if __name__ == "__main__":\n    print("Saved revision 1")\n    sys.exit(1)')
    (R / 'fault-writer.py').write_bytes(fault); (here / 'team.py').write_bytes(fault)
    try:
        witness = subprocess.run([base, '-B', str(here / 'team.py'), 'apply'], env=env, capture_output=True, text=True, timeout=10)
        assert witness.returncode == 1 and witness.stdout.strip() == 'Saved revision 1'
        receipt = run(bp)
        receipt['fault_control'] = {'returncode': witness.returncode, 'stdout': witness.stdout, 'stderr': witness.stderr,
                                    'source_sha256': sha(R / 'fault-writer.py'), 'intervention': 'copied writer prints misleading success then exits1 without applying'}
        retain('failed-writer-saved-prefix', bp, receipt, 'upstream-failure-refusal')
    finally: (here / 'team.py').write_bytes(original)
    # Check fixture journals through the unmodified supported observer.
    raw['fixture_health'] = []
    for item in raw['cases']:
        bp = R / item['name'] / 'TEAM.json'; ok, detail = T.board_status(bp)
        raw['fixture_health'].append({'name': item['name'], 'ok': ok, 'detail': detail}); assert ok, detail
    raw['sources_restored'] = all(sha(here / n) == info['sha256'] for n, info in raw['sources'].items())
    assert raw['sources_restored']
    raw['finished'] = True
except BaseException as e:
    raw['fatal'] = {'type': type(e).__name__, 'reason': str(e)}
    raise
finally: (R / 'raw.json').write_text(json.dumps(raw, indent=2) + '\n')
print('TRANSITIONS_CAPTURE_FINISHED', len(raw['cases']), flush=True)
