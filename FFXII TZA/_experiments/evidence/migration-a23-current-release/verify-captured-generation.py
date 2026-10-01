"""Verify the exact HTTP-observed generation against its on-disk manifest."""
import hashlib, json, sys
from pathlib import Path

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ROOT=Path('Database/Tools/work/dashboard')
EXPORTS=Path('Database/Tools/work/dashboard-exports')
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts')
import generation as G
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

capture=json.loads((W/'capture.json').read_bytes())
terminal=json.loads((W/'capture-terminal.json').read_bytes())
assert terminal['terminal'] and terminal['returncode']==0 and not terminal['stderr']
assert terminal['driver_sha256']==sha(W/'capture.py')
assert capture['complete'] and capture['same_generation']
gen=capture['generation_after']
before=json.loads((W/'raw-http/status-before.body').read_bytes())
after=json.loads((W/'raw-http/status-after.body').read_bytes())
assert before['generation']==after['generation']==gen
assert before['problems']==after['problems']==[]
assert before['reader_stale'] is False and after['reader_stale'] is False
for rec in capture['observed']:
    assert rec['status']==200 and sha(W/rec['body_file'])==rec['sha256']

history=[json.loads(line) for line in (ROOT/'history.jsonl').read_text().splitlines() if line.strip()]
matches=[r for r in history if r['generation']==gen]
assert len(matches)==1,matches
expected=matches[0]['manifest_sha256']
manifest_path=ROOT/gen/'MANIFEST.json'
assert sha(manifest_path)==expected
store=G.Store(str(ROOT))  # existing root, reading only
manifest,d,problems=store.open_generation(gen,expected)
assert problems==[] and manifest['generation']==gen and Path(d)==ROOT/gen,(gen,problems)
views={}
for name in ('progress','overview'):
    http=json.loads((W/f'raw-http/{name}.body').read_bytes())
    output=ROOT/gen/'outputs'/f'view-{name}.json'
    assert sha(output)==manifest['outputs'][output.name]['sha256']
    assert http['meta']['generation']==gen and http['view']==json.loads(output.read_bytes())
    assert http['view']['status']==after['views'][name]
    views[name]={'status':http['view']['status'],'output_sha256':sha(output),
                 'http_sha256':sha(W/f'raw-http/{name}.body')}

builder=Path('Database/Tools/dashboard/build_views.py')
generator=Path('Database/Tools/analysis-kit/gfz-scripts/generation.py')
server=Path('Database/Tools/dashboard/server.py')
matches_export=sorted(p.name for p in EXPORTS.glob(gen+'*.zip'))
result={'status':'CURRENT_CAPTURE_VERIFIED_NOT_A23_ACCEPTED',
        'generation':gen,'manifest_sha256':expected,'manifest_format':manifest['format'],
        'open_generation_problems':problems,'captured_views':views,
        'builder_manifest_sha256':manifest['generator']['sha256'],
        'builder_current_sha256':sha(builder),
        'builder_current_matches_manifest':manifest['generator']['sha256']==sha(builder),
        'verifier_manifest_sha256':manifest['verifier'],'verifier_current_sha256':sha(generator),
        'verifier_current_matches_manifest':manifest['verifier']==sha(generator),
        'server_current_sha256':sha(server),'http_reader_stale':False,
        'matching_release_zips':matches_export,
        'loaded_pid_module_identity':'UNMEASURED; targeted Get-NetTCPConnection failed CimException Access denied',
        'limits':'One captured stable HTTP generation; CURRENT can advance later. No launcher/restart, loaded module or official release-export acceptance. A23 remains unaccepted.'}
if '--write-result' in sys.argv:
    (W/'verify-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
