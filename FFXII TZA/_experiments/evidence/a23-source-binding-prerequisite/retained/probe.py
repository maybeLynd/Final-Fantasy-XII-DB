"""Execute just the captured headsha function with real Git, no release setup."""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source-release.py'
REPO = Path.cwd().resolve()
REL = 'Database/Tools/dashboard/server.py'
source = SOURCE.read_bytes()
if hashlib.sha256(source).hexdigest() != '838d4882e545c353061888ba5d06eae76514f1a219a73fff400df51dc9948469':
    raise ValueError('captured helper source changed; not this evidence identity')
tree = ast.parse(source)
functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'headsha']
if len(functions) != 1:
    raise ValueError('expected one exact source helper')
module = ast.Module(body=[functions[0]], type_ignores=[])
ast.fix_missing_locations(module)
namespace = {'subprocess': subprocess, 'hashlib': hashlib, 'REPO': REPO}
exec(compile(module, str(SOURCE), 'exec'), namespace)


def checked_context(repo):
    receipts = []
    for argv in (['git', '-C', str(repo), 'show', 'HEAD:' + REL],
                 ['git', '-C', str(repo), 'log', '-1', '--format=%H', '--', REL]):
        p = subprocess.run(argv, capture_output=True)
        receipts.append({'argv': argv, 'exit': p.returncode,
                         'stdout_bytes': len(p.stdout),
                         'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                         'stderr': p.stderr.decode('utf-8', errors='replace')})
    return receipts


positive = namespace['headsha'](REL)
positive_receipts = checked_context(REPO)
if not all(r['exit'] == 0 for r in positive_receipts):
    raise ValueError('positive Git context failed')
if positive[0] != positive_receipts[0]['stdout_sha256'] or len(positive[1]) != 40:
    raise ValueError('positive source binding mismatch')
missing = HERE / 'NONEXISTENT-GIT-CONTEXT'
if missing.exists():
    raise ValueError('negative Git context must actually be missing')
namespace['REPO'] = missing
negative = namespace['headsha'](REL)
negative_receipts = checked_context(missing)
if not all(r['exit'] != 0 and r['stdout_bytes'] == 0 for r in negative_receipts):
    raise ValueError('real negative Git control failed')
empty = hashlib.sha256(b'').hexdigest()
if negative != (empty, ''):
    raise ValueError('helper behavior changed; re-evaluate captured-source finding')
if SOURCE.read_bytes() != source:
    raise ValueError('peer source changed during probe; receipt invalid')
out = {'status': 'SOURCE_HELPER_GIT_FAILURE_NOT_PROPAGATED',
       'source_path': str(SOURCE), 'source_sha256': hashlib.sha256(source).hexdigest(),
       'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'python': sys.version, 'invocation': 'Exact AST-extracted headsha, real subprocess/Git; release top-level not executed',
       'positive': {'helper_return': positive, 'checked_git': positive_receipts},
       'negative': {'helper_return': negative, 'checked_git': negative_receipts},
       'implication': 'Failed Git queries return SHA256(empty stdout) and an empty commit rather than preserving their nonzero exits.',
       'limits': ['No complete release/deployment executed or accepted.',
                  'No claim that actual valid release binding differs or its aggregate verdict passes on this negative.',
                  'FRONTIER owns repair of its helper and source binding; ASTRA existing Git checker checks exits.'],
       'cleanup': 'No release top-level, export, server, board, reference, game or file write; output is stdout only'}
print(json.dumps(out, indent=2))
