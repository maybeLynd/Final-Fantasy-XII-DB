"""Bounded independent execution of pinned production host functions; no FF12 run."""
import ast
import hashlib
import json
import os
import platform
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
COMMIT = 'eae0ed3c7d1ed9f8f41a401b85e1fedb4ed39cc9'

def source(path):
    p = subprocess.run(['git', 'show', COMMIT + ':' + path], cwd=ROOT, capture_output=True)
    if p.returncode or not p.stdout:
        raise RuntimeError({'path': path, 'exit': p.returncode, 'stderr': p.stderr.decode(errors='replace')})
    out = HERE / ('source-' + Path(path).name)
    if out.exists() and out.read_bytes() != p.stdout:
        raise RuntimeError('immutable source mismatch: ' + str(out))
    if not out.exists():
        out.write_bytes(p.stdout)
    return p.stdout

builder = source('Database/Tools/dashboard/build_views.py')
server = source('Database/Tools/dashboard/server.py')
env = {'json': json, 'os': os}
picked = []
for raw, names, assignments in [(builder, {'M', 'annotate_deltas'}, set()),
                               (server, {'check_view', '_states'}, {'STATUSES', 'MEASURE_KEYS'})]:
    tree = ast.parse(raw)
    selected = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names)
                or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in assignments for t in n.targets))]
    found = {n.name for n in selected if isinstance(n, ast.FunctionDef)}
    if found != names:
        raise RuntimeError('missing production function: ' + repr(names - found))
    picked.extend(selected)
exec(compile(ast.Module(body=picked, type_ignores=[]), '<pinned production slices>', 'exec'), env)

def view(n, d, scope='same'):
    return {'view': 'types', 'status': 'OK', 'definition': 'same-v1',
            'measures': [env['M']('test', 'bounded control', n, d, scope, 'ASTRA fixture', '2026-09-30', 'host control only')]}

cases = [('count', (10, None), (15, None), 'same'),
         ('moved-ratio', (10, 100), (15, 200), 'same'),
         ('changed-scope', (10, None), (15, None), 'changed'),
         ('empty-ratio-to-count', (0, 0), (5, None), 'same'),
         ('ratio-to-empty-ratio', (1, 2), (0, 0), 'same'),
         ('unchanged-empty-ratio', (0, 0), (0, 0), 'same')]
observations = []
for name, old, new, scope in cases:
    prior, current = view(*old), view(*new, scope)
    validation = [env['check_view'](prior), env['check_view'](current)]
    if validation != [None, None]:
        raise RuntimeError({'case': name, 'invalid_fixture': validation})
    directory = HERE / ('fixture-' + name) / 'outputs'
    directory.mkdir(parents=True, exist_ok=True)
    input_path = directory / 'view-types.json'
    if input_path.exists():
        raise RuntimeError('refuse overwritten input: ' + str(input_path))
    input_path.write_text(json.dumps(prior, indent=2) + '\n', encoding='utf-8')
    env['annotate_deltas']({'types': current}, str(directory.parent), {'generation': 'bounded-prior', 'committed_at': 'fixture'})
    observations.append({'case': name, 'prior': prior, 'result': current, 'validation': validation})

delta = {r['case']: r['result']['measures'][0]['delta'] for r in observations}
checks = {'ordinary_count': delta['count'].get('count') == 5 and delta['count'].get('rel') == 50.0,
          'moved_ratio': delta['moved-ratio'].get('dnum') == 5 and delta['moved-ratio'].get('dden') == 100 and 'pp' not in delta['moved-ratio'],
          'changed_scope': 'na' in delta['changed-scope'] and 'count' not in delta['changed-scope'],
          'empty_ratio_not_count': 'count' not in delta['empty-ratio-to-count'] and delta['empty-ratio-to-count'].get('old', {}).get('denominator') == 0,
          'ratio_to_zero_keeps_new_basis': delta['ratio-to-empty-ratio'].get('new', {}).get('denominator') == 0,
          'unchanged_zero_keeps_basis': delta['unchanged-empty-ratio'].get('old', {}).get('denominator') == 0 and delta['unchanged-empty-ratio'].get('new', {}).get('denominator') == 0}
receipt = {'commit': COMMIT, 'python': platform.python_version(), 'method': 'pinned production host function slice; not full build/server/game',
           'builder_sha256': hashlib.sha256(builder).hexdigest(), 'server_sha256': hashlib.sha256(server).hexdigest(),
           'cases': observations, 'checks': checks, 'control_valid': all(checks[k] for k in ['ordinary_count', 'moved_ratio', 'changed_scope']),
           'verdict': 'REJECT_BASIS_BOUNDARY' if not all(checks.values()) else 'ACCEPT_SLICE'}
path = HERE / 'zero-basis-result.json'
if path.exists():
    raise RuntimeError('refuse overwritten result')
path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verdict': receipt['verdict'], 'checks': checks, 'receipt': str(path)}))
raise SystemExit(0 if all(checks.values()) else 1)
