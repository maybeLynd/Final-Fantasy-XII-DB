"""Unmodified plan/apply/schema controls; explicit in-memory effects, no journal or disk write."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent; R = W / 'run-01'; here = R / 'source/Database/Tools/analysis-kit/gfz-scripts'
out = W / 'inmemory-controls.json'; assert not out.exists()
spec = importlib.util.spec_from_file_location('bounded_original_transition', here / 'transitions.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
assert Path(C.team.__file__).resolve() == here / 'team.py'
items = []
for name in ('valid-reject', 'typed-commit', 'non-sha-commit', 'typed-record', 'self-review'):
    p = W / 'read-only-01' / name / 'TEAM.json'; before = p.read_bytes(); b = json.loads(before)
    plan = C.plan(b); assert len(plan) == 1 and plan[0][3] is not None
    op = copy.deepcopy(plan[0][3]); op['task']['requester'] = 'SWE2-FRONTIER'
    C.team.apply(b, 'SWE2-FRONTIER', op, 'ASTRA-labelled-memory-control')
    C.team.validate(b)
    assert p.read_bytes() == before
    items.append({'name': name, 'plan_kind': plan[0][0], 'actual_inmemory_added': b['tasks'][-1],
                  'schema_valid': True, 'original_fixture_unchanged': True})
result = {'method': 'A original Python plan/apply/schema with synthetic in-memory state',
    'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'cases': items,
    'limits': 'Actual original function effects in Python memory only. No transaction/journal/lock/disk write, no current production rows and no concurrency/host cancellation proof. Original full CLI write campaign remains INCOMPLETE.'}
out.write_text(json.dumps(result, indent=2) + '\n')
print('INMEMORY_ADMISSION_EFFECTS', [c['name'] for c in items], flush=True)
