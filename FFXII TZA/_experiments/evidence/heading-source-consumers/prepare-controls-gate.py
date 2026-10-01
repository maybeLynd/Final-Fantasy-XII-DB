"""Freeze reviewed own evidence with required controls before board claim."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/heading-source-consumers')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def controls_preflight(root):
    root = Path(root)
    rs = json.loads((root/'checks-terminal.json').read_bytes())
    assert [r['case'] for r in rs] == ['positive', 'failed-upstream', 'missing-result', 'fictional-class-closure']
    assert all(r['terminal'] is True and r['checker_sha256'] == sha(root/'check.py') for r in rs)
    assert rs[0]['returncode'] == 0 and not rs[0]['stderr'] and rs[0]['stdout'].strip()
    assert all(r['returncode'] != 0 and r['stderr'] for r in rs[1:])
    expected = json.loads(rs[0]['stdout'])
    assert expected['status'] == 'STATIC_ONLY_BOUNDARIES_VALID' and expected['class_stability'] == 'OPEN'
    q = subprocess.run([sys.executable, '-B', str(root/'check.py')], capture_output=True, text=True)
    assert q.returncode == 0 and not q.stderr and json.loads(q.stdout) == expected, (q.returncode, q.stderr)

gate_root = Path(sys.argv[sys.argv.index('--controls-root')+1]) if '--controls-root' in sys.argv else W
controls_preflight(gate_root)
if '--controls-preflight' in sys.argv:
    print('REQUIRED_CONTROLS_VERIFIED_NO_WRITES')
    sys.exit(0)

assert not P.exists()
shutil.copytree(W, P, ignore=shutil.ignore_patterns('prepare-publication.py', 'publication', 'deliver.py', 'preflight-cases', '__pycache__'))
shutil.copyfile(Path(__file__), P/'prepare-controls-gate.py')
(P/'.gitattributes').write_bytes(b'* -text\n')
members = []
for f in sorted(P.rglob('*')):
    if f.is_file():
        members.append({'path': f.relative_to(P).as_posix(), 'bytes': f.stat().st_size, 'sha256': sha(f)})
(P/'manifest.json').write_bytes((json.dumps({'schema': 1, 'members': members,
    'limits': 'Method A source only. First selected arg5 zero, later call conditional; three candidate direct type readers, fourth unresolved. No initialized/live/class/lifetime/scheduling conclusion or full L1+L2 award.'}, indent=2)+'\n').encode())

pub = W/'publication'
assert not pub.exists()
pub.mkdir()
old = W.parent/'transition-actual-write/publication'
for name in ('verify.py', 'manifest_closure.py'):
    shutil.copyfile(old/name, pub/name)
sid = 'ASTRA-sol-20260929-heading-class-effects'
task = 'ASTRA-PUBLISH-HEADING-SOURCE-CONSUMERS'
source = (W.parent/'heading-commit-tail-supplement/publication/publish.py').read_text()
source = source.replace('ASTRA-PUBLISH-HEADING-COMMIT-TAIL-SUPPLEMENT', task)
source = source.replace('evidence/heading-commit-tail-supplement', 'evidence/heading-source-consumers')
(pub/'publish.py').write_text(source)
paths = [f.as_posix() for f in sorted(P.rglob('*')) if f.is_file()]
payload = '\n'.join(paths)+'\n'
objects = []
for flags in ([], ['--no-filters']):
    q = subprocess.run(['git','hash-object','--stdin-paths',*flags], input=payload, capture_output=True, text=True)
    assert q.returncode == 0 and not q.stderr and len(q.stdout.splitlines()) == len(paths)
    objects.append(q.stdout.splitlines())
assert objects[0] == objects[1] and len(paths) == len(members)+1
(pub/'reviewed.json').write_text(json.dumps(dict(zip(paths, objects[0])), indent=2)+'\n')

a = [sys.executable,'-B',str(W.parent/'migration-generation-independent/prepare-publication.py'),
     '--preflight-only','--preflight-pins',str(pub/'reviewed.json')]
q = subprocess.run(a, capture_output=True, text=True)
(pub/'path-preflight.json').write_text(json.dumps({'argv':a,'returncode':q.returncode,'stdout':q.stdout,
                                                  'stderr':q.stderr,'terminal':True},indent=2)+'\n')
assert q.returncode == 0 and q.stdout.strip() == 'PUBLICATION_PATH_ADMISSIBILITY_ONLY_NO_WRITES' and not q.stderr
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts')
import team
sys.path.insert(0,str(pub))
from verify import normalized
ok, detail = team.board_status(team.BOARD)
assert ok, detail
b = json.loads(team.BOARD.read_bytes())
inbox = Path('Database/FFXII TZA/_index/_inbox/ASTRA.md')
current = inbox.read_text()
header = (W/'handoff-header.txt').read_text()
(pub/'reviewed-inbox-preimage.txt').write_text(normalized(current))
(pub/'reviewed-inbox-next.txt').write_text(header+current)
(pub/'reviewed-inbox-body.txt').write_text(normalized(header+current))
(pub/'reviewed-epoch.json').write_text(json.dumps({'epoch':b['recovery_epoch']})+'\n')
(pub/'message.txt').write_text('ASTRA: identify bounded heading argument and effect-field consumers without live promotion\n')
assert not any(t['id'] == task for t in b['tasks'])
team.transaction(team.BOARD,'ASTRA',{'action':'add','task':{
    'id':task,'kind':'research','priority':'P1',
    'target':'Publish bounded original-source heading argument and type-reader evidence',
    'scope':'Explicit frozen own evidence and ASTRA handoff; supported writes only',
    'completion':'Actual committed blobs/body/epoch/manifest verified; reservation released',
    'dependencies':[],'resources':[{'key':'@publication'}]}},sid)
print('PREPARED_HEADING_SOURCE_CONSUMERS', len(members))
