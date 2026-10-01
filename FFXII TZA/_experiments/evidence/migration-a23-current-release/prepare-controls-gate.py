"""Freeze one bounded A23 evidence slice after checking its actual controls."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/migration-a23-current-release')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def controls_preflight(root):
    root = Path(root)
    records = json.loads((root / 'checks-terminal.json').read_bytes())
    assert [r['case'] for r in records] == [
        'positive', 'failed-verifier', 'changed-served-view', 'fictional-a23-pass']
    assert all(r['terminal'] is True and r['checker_sha256'] == sha(root / 'check.py') for r in records)
    assert records[0]['returncode'] == 0 and not records[0]['stderr']
    assert json.loads(records[0]['stdout'])['status'] == 'A23_EVIDENCE_SLICE_VALID_NOT_ACCEPTED'
    assert all(r['returncode'] != 0 and r['stderr'] for r in records[1:])
    q = subprocess.run([sys.executable, '-B', str(root / 'check.py')], capture_output=True, text=True)
    assert q.returncode == 0 and not q.stderr and json.loads(q.stdout) == json.loads(records[0]['stdout'])
    assert json.loads((root / 'verdict.json').read_bytes())['status'] == 'INCOMPLETE_NOT_ACCEPTED'

root = Path(sys.argv[sys.argv.index('--controls-root') + 1]) if '--controls-root' in sys.argv else W
controls_preflight(root)
if '--controls-preflight' in sys.argv:
    print('REQUIRED_CONTROLS_VERIFIED_NO_WRITES')
    sys.exit(0)

assert not P.exists()
P.mkdir(parents=True)
root_names = [
    'README.md', 'PLAN.md', 'RESULT.md', 'handoff-header.txt',
    'capture.py', 'run-capture.py', 'capture.json', 'capture-terminal.json',
    'verify-captured-generation.py', 'run-verify.py', 'verify-result.json',
    'verify-terminal.json', 'verify-historical-export.py',
    'historical-export-terminal.json', 'source-identity.py',
    'source-identity.json', 'verdict.json', 'check.py', 'run-checks.py',
    'checks-terminal.json',
]
for name in root_names:
    shutil.copyfile(W / name, P / name)
for directory in ('raw-http', 'retained'):
    shutil.copytree(W / directory, P / directory)
shutil.copyfile(Path(__file__), P / 'prepare-controls-gate.py')
(P / '.gitattributes').write_bytes(b'* -text\n')
controls_preflight(P)
members = []
for f in sorted(P.rglob('*')):
    if f.is_file():
        members.append({'path': f.relative_to(P).as_posix(), 'bytes': f.stat().st_size,
                        'sha256': sha(f)})
(P / 'manifest.json').write_bytes((json.dumps({
    'schema': 1, 'members': members,
    'limits': 'Independent read-only served generation A23 slice. Historical ZIP is different. Loaded PID/module, matching selected release export, restart/adoption and full migration/L1+L2 acceptance unmeasured.'
}, indent=2) + '\n').encode())

pub = W / 'publication'
assert not pub.exists()
pub.mkdir()
source_pub = W.parent / 'heading-node-followup/publication'
for name in ('verify.py', 'manifest_closure.py'):
    shutil.copyfile(source_pub / name, pub / name)
text = (source_pub / 'publish.py').read_text()
text = text.replace('ASTRA-PUBLISH-HEADING-NODE-FOLLOWUP',
                    'ASTRA-PUBLISH-MIGRATION-A23-CURRENT-RELEASE')
text = text.replace('evidence/heading-node-followup',
                    'evidence/migration-a23-current-release')
(pub / 'publish.py').write_text(text)
paths = [f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()]
payload = '\n'.join(paths) + '\n'
outputs = []
for flags in ([], ['--no-filters']):
    q = subprocess.run(['git', 'hash-object', '--stdin-paths', *flags],
                       input=payload, capture_output=True, text=True)
    assert q.returncode == 0 and not q.stderr and len(q.stdout.splitlines()) == len(paths)
    outputs.append(q.stdout.splitlines())
assert outputs[0] == outputs[1] and len(paths) == len(members) + 1
(pub / 'reviewed.json').write_text(json.dumps(dict(zip(paths, outputs[0])), indent=2) + '\n')

a = [sys.executable, '-B', str(W.parent / 'migration-generation-independent/prepare-publication.py'),
     '--preflight-only', '--preflight-pins', str(pub / 'reviewed.json')]
q = subprocess.run(a, capture_output=True, text=True)
(pub / 'path-preflight.json').write_text(json.dumps({
    'argv': a, 'returncode': q.returncode, 'stdout': q.stdout,
    'stderr': q.stderr, 'terminal': True
}, indent=2) + '\n')
assert q.returncode == 0 and q.stdout.strip() == 'PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES' and not q.stderr

sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import team
sys.path.insert(0, str(pub))
from verify import normalized
ok, detail = team.board_status(team.BOARD)
assert ok, detail
board = json.loads(team.BOARD.read_bytes())
inbox = Path('Database/FFXII TZA/_index/_inbox/ASTRA.md')
current = inbox.read_text()
header = (W / 'handoff-header.txt').read_text()
(pub / 'reviewed-inbox-preimage.txt').write_text(normalized(current))
(pub / 'reviewed-inbox-next.txt').write_text(header + current)
(pub / 'reviewed-inbox-body.txt').write_text(normalized(header + current))
(pub / 'reviewed-epoch.json').write_text(json.dumps({'epoch': board['recovery_epoch']}) + '\n')
(pub / 'message.txt').write_text('ASTRA: independently verify bounded A23 served generation and preserve release gap\n')
task = 'ASTRA-PUBLISH-MIGRATION-A23-CURRENT-RELEASE'
assert not any(t['id'] == task for t in board['tasks'])
team.transaction(team.BOARD, 'ASTRA', {'action': 'add', 'task': {
    'id': task, 'kind': 'research', 'priority': 'P1',
    'target': 'Publish exact read-only A23 served-generation evidence and ASTRA handoff',
    'scope': 'Explicit frozen own evidence and ASTRA inbox; guarded shared publication',
    'completion': 'Actual committed blobs/body/epoch/manifest verified; publication released',
    'dependencies': [], 'resources': [{'key': '@publication'}],
}}, 'ASTRA-sol-20260929-a23-current-release')
print('PREPARED_A23_CURRENT_RELEASE', len(members))
