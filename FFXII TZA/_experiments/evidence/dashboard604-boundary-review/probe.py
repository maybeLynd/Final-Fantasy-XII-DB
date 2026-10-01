"""Original exact604 host paths; retained synthetic index fixture, no real archive."""
import ast
import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
W = P / 'run-01'
OLD = P.parent / 'dashboard-views-eae0ed3c7-review/vbf-chain'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
PINS = {'build_views.py': '924dbecfe617a749a6875c0d6a30055fd9ea7af5140b9771593f6fbfc675f330',
        'server.py': 'f3df8bf778ff6896cd8dc70eb9011435f245c7145cded9eb13d16f16343da8fd',
        'vbf_index.py': '7043d3d8f7ce127e4a337f6c060a3cb24f2ad6ecdb5c090fd233176094365198'}
for name, pin in PINS.items():
    r = json.loads((P / (name + '.git.receipt.json')).read_text())
    if sha(P / ('source-' + name)) != pin or r['exit'] != 0 or r['terminal'] is not True or r['sha256'] != pin or (P / (name + '.git.stderr')).read_bytes():
        raise RuntimeError('required source prerequisite failed: ' + name)
env = {'json': json, 'os': os, 'collections': collections}
picked = []
selection = []
for name, names, assignments in [('build_views.py', {'M', 'annotate_deltas', 'v_vbf'}, set()),
                                  ('server.py', {'check_view', '_states'}, {'STATUSES', 'MEASURE_KEYS'})]:
    raw = (P / ('source-' + name)).read_bytes()
    tree = ast.parse(raw)
    selected = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names) or
                (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in assignments for t in n.targets))]
    found = {n.name for n in selected if isinstance(n, ast.FunctionDef)}
    if found != names: raise RuntimeError('missing required exact original function')
    picked.extend(selected)
    selection.append({'file': 'source-' + name, 'sha256': PINS[name], 'functions': sorted(found), 'original_lines': [{'name': n.name, 'first': n.lineno, 'last': n.end_lineno} for n in selected if isinstance(n, ast.FunctionDef)]})
exec(compile(ast.Module(body=picked, type_ignores=[]), '<exact604 original host slices>', 'exec'), env)
W.mkdir(exist_ok=False)
def write(name, value):
    (W / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

inputs = W / 'inputs'
inputs.mkdir()
oldpins = {}
for name in ('positive.vbf', 'corrupt.vbf', 'listing.txt', 'drift.txt'):
    source = OLD / name
    oldpins[name] = {'retained_path': str(source), 'sha256': sha(source), 'bytes': source.stat().st_size}
    shutil.copyfile(source, inputs / name)
(inputs / 'rowless.txt').write_text('ASTRA deliberately rowless comparison fixture\n', encoding='utf-8')
(inputs / 'facts.json').write_text(json.dumps({'facts': [], 'gaps': {}, 'failed': {}}), encoding='utf-8')
initial_input_pins = {p.name: sha(p) for p in inputs.iterdir() if p.is_file()}
write('preconditions.json', {'commit': '604194276', 'source_pins': PINS, 'driver_sha256': sha(Path(__file__)), 'python': sys.version,
      'interpreter': sys.executable, 'interpreter_sha256': sha(Path(sys.executable)), 'ast_slices': selection,
      'retained_fixture_identity': oldpins, 'input_pins': initial_input_pins,
      'limits': 'Original historical host function slices and real capture CLI; synthetic header only, not full server/build/real archive/game.'})

def view(n, d, scope='same'):
    return {'view': 'types', 'status': 'OK', 'definition': 'same-v1', 'measures': [env['M']('test', 'ASTRA bounded measure', n, d, scope, 'independent fixture', '2026-10-01', 'host control only')]}

delta_cases = [('count', (10, None), (15, None), 'same'), ('moved-ratio', (10, 100), (15, 200), 'same'),
               ('changed-scope', (10, None), (15, None), 'changed'), ('empty-ratio-to-count', (0, 0), (5, None), 'same'),
               ('ratio-to-empty-ratio', (1, 2), (0, 0), 'same'), ('unchanged-empty-ratio', (0, 0), (0, 0), 'same'),
               ('count-to-ratio', (5, None), (3, 10), 'same'), ('empty-to-ten', (0, 0), (0, 10), 'same')]
deltas = []
for label, old, new, scope in delta_cases:
    prior, current = view(*old), view(*new, scope)
    valid_before = [env['check_view'](prior), env['check_view'](current)]
    if valid_before != [None, None]: raise RuntimeError('invalid delta fixture: ' + label)
    original_current = copy.deepcopy(current)
    directory = W / ('fixture-' + label) / 'outputs'
    directory.mkdir(parents=True)
    path = directory / 'view-types.json'
    path.write_text(json.dumps(prior, indent=2) + '\n', encoding='utf-8')
    pin = sha(path)
    env['annotate_deltas']({'types': current}, str(directory.parent), {'generation': 'ASTRA-retained-prior', 'committed_at': 'synthetic fixture'})
    d = current['measures'][0]['delta']
    deltas.append({'case': label, 'prior': prior, 'original_current': original_current, 'result': current, 'delta': d,
                   'prior_file_sha256': pin, 'prior_file_unchanged': sha(path) == pin, 'before_validation': valid_before, 'after_validation': env['check_view'](current)})
write('delta-observations.json', deltas)

archive = inputs / 'positive.vbf'
cases = [('positive', archive, inputs / 'listing.txt'), ('drift', archive, inputs / 'drift.txt'),
         ('missing-archive', inputs / 'missing.vbf', inputs / 'listing.txt'), ('corrupt-archive', inputs / 'corrupt.vbf', inputs / 'listing.txt'),
         ('missing-listing', archive, inputs / 'missing-listing.txt'), ('no-listing', archive, None), ('rowless-listing', archive, inputs / 'rowless.txt')]
records = []
for label, arc, listing in cases:
    out = W / (label + '.json')
    out.write_text(json.dumps({'entries': [['stale/file.dat', 999]], 'archive_index': {'stale': True}}), encoding='utf-8')
    argv = [sys.executable, '-B', str(P / 'source-vbf_index.py'), '--archive', str(arc), '--out', str(out)]
    if listing is not None: argv += ['--listing', str(listing)]
    p = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
    (W / (label + '.stdout')).write_bytes(p.stdout)
    (W / (label + '.stderr')).write_bytes(p.stderr)
    capture = json.loads(out.read_text(encoding='utf-8'))
    v = env['v_vbf']({'vbf_index': str(out), 'requirement_facts': str(inputs / 'facts.json')}, 'ASTRA synthetic header fixture')
    record = {'case': label, 'argv': argv, 'exit': p.returncode, 'terminal': True, 'exception': None, 'stdout': p.stdout.decode('utf-8', 'replace'), 'stderr': p.stderr.decode('utf-8', 'replace'),
              'capture': capture, 'capture_sha256': sha(out), 'view': v, 'validation': env['check_view'](v), 'temporary_output_left': Path(str(out) + '.tmp').exists()}
    (W / (label + '.receipt.json')).write_text(json.dumps(record, indent=2) + '\n')
    records.append(record)
    write('capture-partial.json', records)

# This malformed-comparison intervention does not claim the capture CLI produced it.
malformed = copy.deepcopy(records[0]['capture'])
malformed['vs_listing'] = {'missing_from_archive': 0, 'missing_from_listing': 0, 'size_mismatch': '0'}
mpath = W / 'malformed-comparison.json'
mpath.write_text(json.dumps(malformed, indent=2) + '\n')
mv = env['v_vbf']({'vbf_index': str(mpath), 'requirement_facts': str(inputs / 'facts.json')}, 'ASTRA labeled malformed comparison intervention')
write('malformed-observation.json', {'method': 'Synthetic view input intervention, not capture output', 'capture': malformed, 'view': mv, 'validation': env['check_view'](mv)})

D = {r['case']: r['delta'] for r in deltas}
by = {r['case']: r for r in records}
measure = lambda v, name: next((m for m in v.get('measures', []) if m['id'] == name), None)
def unavailable(v):
    return v['status'] == 'PARTIAL' and measure(v, 'listing-drift') is None and 'Listing comparison UNMEASURED:' in v['source']['limits'] and any('UNMEASURED' in row for row in v['rows']['data']) and measure(v, 'files')['numerator'] == 2 and measure(v, 'bytes')['numerator'] == 300
def changed_basis(label, old, new):
    return D[label].get('na') == 'N/A - basis changed' and not any(k in D[label] for k in ('count', 'rel', 'pp', 'dnum', 'dden')) and D[label]['old'] == {'numerator': old[0], 'denominator': old[1]} and D[label]['new'] == {'numerator': new[0], 'denominator': new[1]}
checks = {'ordinary_count': D['count'].get('count') == 5 and D['count'].get('rel') == 50.0,
          'moved_ratio_current_rule': D['moved-ratio'].get('dnum') == 5 and D['moved-ratio'].get('dden') == 100 and D['moved-ratio'].get('pp') == -2.5,
          'changed_scope': 'na' in D['changed-scope'] and 'count' not in D['changed-scope'],
          'empty_ratio_to_count': changed_basis('empty-ratio-to-count', (0, 0), (5, None)), 'count_to_ratio': changed_basis('count-to-ratio', (5, None), (3, 10)),
          'ratio_to_empty': D['ratio-to-empty-ratio']['old'] == {'numerator': 1, 'denominator': 2} and D['ratio-to-empty-ratio']['new'] == {'numerator': 0, 'denominator': 0} and D['ratio-to-empty-ratio'].get('pp') == 50.0,
          'same_empty': D['unchanged-empty-ratio']['old']['denominator'] == 0 and D['unchanged-empty-ratio']['new']['denominator'] == 0 and D['unchanged-empty-ratio'].get('pp') == 0.0,
          'empty_to_ten': D['empty-to-ten']['old']['denominator'] == 0 and D['empty-to-ten']['new']['denominator'] == 10 and D['empty-to-ten'].get('pp') == -100.0,
          'delta_schema_and_inputs': all(r['before_validation'] == [None, None] and r['after_validation'] is None and r['prior_file_unchanged'] and (r['result']['measures'][0]['numerator'], r['result']['measures'][0]['denominator']) == (r['original_current']['measures'][0]['numerator'], r['original_current']['measures'][0]['denominator']) for r in deltas),
          'positive_capture': by['positive']['exit'] == 0 and measure(by['positive']['view'], 'files')['numerator'] == 2 and measure(by['positive']['view'], 'bytes')['numerator'] == 300 and measure(by['positive']['view'], 'listing-drift')['numerator'] == 0 and by['positive']['view']['status'] == 'OK',
          'drift_capture': by['drift']['exit'] == 0 and measure(by['drift']['view'], 'listing-drift')['numerator'] == 2 and by['drift']['view']['status'] == 'PARTIAL',
          'archive_failures': all(by[k]['exit'] == 1 and by[k]['view']['status'] == 'FAILED' and by[k]['view']['measures'] == [] and 'entries' not in by[k]['capture'] for k in ('missing-archive', 'corrupt-archive')),
          'listing_unavailable': all(by[k]['exit'] == 0 and by[k]['capture'].get('vs_listing_failed') and unavailable(by[k]['view']) for k in ('missing-listing', 'no-listing', 'rowless-listing')),
          'malformed_intervention': unavailable(mv) and env['check_view'](mv) is None,
          'capture_schema_and_atomicity': all(r['terminal'] is True and r['exception'] is None and r['validation'] is None and not r['stderr'] and not r['temporary_output_left'] for r in records),
          'source_and_fixture_unchanged': all(sha(P / ('source-' + name)) == pin for name, pin in PINS.items()) and {p.name: sha(p) for p in inputs.iterdir() if p.is_file()} == initial_input_pins}
result = {'verdict': 'ACCEPT_BOUNDED_BOUNDARY_REPAIR' if all(checks.values()) else 'REJECT_OR_INVALID', 'checks': checks, 'delta_cases': len(deltas), 'actual_capture_clis': len(records),
          'malformed_comparison_interventions': 1, 'preconditions_sha256': sha(W / 'preconditions.json'), 'driver_sha256': sha(Path(__file__)),
          'limits': 'Exact604 isolated host functions and capture CLI with retained two-entry synthetic header. No old/producer campaign repetition, full deployed build/server acceptance, actual archive/game binding or FF12 native/live execution.'}
write('result.json', result)
print(json.dumps(result))
raise SystemExit(0 if all(checks.values()) else 1)
