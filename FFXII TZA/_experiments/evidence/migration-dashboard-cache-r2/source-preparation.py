"""Bind returned cache repair to the current final source before a private HTTP run."""
import ast, hashlib, json, subprocess
from pathlib import Path
W = Path(__file__).resolve().parent
P = W / 'source-preparation'
assert not P.exists(), 'Retain preparation identity; use a new identity if source changes'
server = Path('Database/Tools/dashboard/server.py')
base = subprocess.check_output(['git', 'rev-parse', 'e8999f966'], text=True).strip()
final = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--', server.as_posix()], text=True).strip()
old = subprocess.check_output(['git', 'show', base + ':' + server.as_posix()])
working = server.read_bytes()
current = subprocess.check_output(['git', 'show', final + ':' + server.as_posix()])
# The actual identity guard caught unpublished peer edits. Execute only this
# immutable published object, never silently import the working source instead.
def selected(data):
    tree = ast.parse(data.decode('utf-8'))
    keys = {'State', 'VERIFY_INPUTS_EVERY', 'VERIFICATION', 'REQUIRED'}
    found = {}
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == 'State': found[n.name] = ast.dump(n, include_attributes=False)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id in keys: found[t.id] = ast.dump(n, include_attributes=False)
    assert set(found) == keys
    return found
before, after = selected(old), selected(current)
assert before == after, 'Cache implementation/timing changed beyond the returned repair; reassess controls'
P.mkdir()
(P / 'server-base-repair.py').write_bytes(old)
(P / 'server-final.py').write_bytes(current)
files = [Path('Database/Tools/analysis-kit/gfz-scripts/generation.py'),
         Path('Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md'),
         Path('Database/FFXII TZA/_index/completion-packages/README.md')]
receipts = []
for i, f in enumerate(files):
    data = subprocess.check_output(['git', 'show', final + ':' + f.as_posix()])
    target = P / ('dependency-' + str(i) + '-' + f.name)
    target.write_bytes(data)
    receipts.append({'path': f.as_posix(), 'sha256': hashlib.sha256(data).hexdigest(),
                     'retained': target.name,
                     'source_tree_commit': final,
                     'git_blob': subprocess.check_output(['git', 'rev-parse', final + ':' + f.as_posix()], text=True).strip()})
r = {'method': 'A static preparation, no HTTP or runtime capture', 'base_commit': base, 'final_server_commit': final,
     'base_sha256': hashlib.sha256(old).hexdigest(), 'final_sha256': hashlib.sha256(current).hexdigest(),
     'whole_source_identical': old == current, 'cache_AST_and_constants_identical': True,
     'working_source_matches_published': working == current,
     'unpublished_working_sha256': hashlib.sha256(working).hexdigest(),
     'pending_peer_code_not_executed': True,
     'selected_nodes': sorted(before), 'dependencies': receipts,
     'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'limit': 'Structural equivalence of selected cache implementation/constants in immutable published objects only. Unpublished peer code excluded, not accepted. Does not prove loaded process identity, actual detection, complete progress semantics or whole current deployment acceptance.',
     'next_action': 'Use these exact final copied sources in private HTTP controls; validate warmed baseline and observer, output next-request same-stat detection and separate input-snapshot timer. Bound/stoppable/cleanup as PLAN. Goal remains ACTIVE/NOT_MET.'}
(P / 'receipt.json').write_text(json.dumps(r, indent=2) + '\n')
print('CURRENT_CACHE_SOURCE_BOUND', final, 'different whole file; same selected cache AST/constants')
