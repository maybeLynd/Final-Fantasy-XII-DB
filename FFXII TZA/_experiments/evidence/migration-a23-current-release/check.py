"""Pure read-only check of the captured A23 release evidence and limits."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name):return json.loads((W/name).read_bytes())

capture=load('capture.json');terminal=load('capture-terminal.json')
assert terminal['terminal'] is True and terminal['returncode']==0 and not terminal['stderr']
assert terminal['driver_sha256']==sha(W/'capture.py')
assert capture['complete'] is True and capture['same_generation'] is True
assert [r['name'] for r in capture['observed']]==['status-before','root','progress','overview','status-after']
for r in capture['observed']:
    assert r['status']==200 and r['bytes']>0 and sha(W/r['body_file'])==r['sha256']
before=load('raw-http/status-before.body');after=load('raw-http/status-after.body')
gen='g20260929T184345Z-92fe9f'
assert before['generation']==after['generation']==capture['generation_after']==gen
assert before['problems']==after['problems']==[]
assert before['reader_stale'] is False and after['reader_stale'] is False
assert after['views']['progress']=='PARTIAL' and after['views']['overview']=='OK'

verified=load('verify-result.json');vr=load('verify-terminal.json')
assert vr['terminal'] is True and vr['returncode']==0 and not vr['stderr']
assert vr['driver_sha256']==sha(W/'verify-captured-generation.py')
assert json.loads(vr['stdout'])==verified
assert verified['status']=='CURRENT_CAPTURE_VERIFIED_NOT_A23_ACCEPTED'
assert verified['generation']==gen and verified['open_generation_problems']==[]
assert verified['matching_release_zips']==[]
manifest=load('retained/MANIFEST.json')
assert sha(W/'retained/MANIFEST.json')==verified['manifest_sha256']
assert manifest['generation']==gen and manifest['format']=='ff12-generation-2'
hist=[json.loads(line) for line in (W/'retained/history.jsonl').read_text().splitlines() if line.strip()]
matches=[r for r in hist if r['generation']==gen]
assert len(matches)==1 and matches[0]['manifest_sha256']==verified['manifest_sha256']
for name in ('progress','overview'):
    view=load('raw-http/'+name+'.body');output=load('retained/view-'+name+'.json')
    assert view['meta']['generation']==gen and view['view']==output
    assert sha(W/'retained'/('view-'+name+'.json'))==manifest['outputs']['view-'+name+'.json']['sha256']
    assert view['view']['status']==verified['captured_views'][name]['status']==after['views'][name]
assert verified['builder_current_matches_manifest'] is True
assert verified['verifier_current_matches_manifest'] is True

source=load('source-identity.json')
assert source['status']=='CURRENT_CHECKOUT_FILES_MATCH_HEAD' and len(source['files'])==4
for f in source['files']:assert f['git_blob']==f['head_blob'] and len(f['sha256'])==64
assert any(f['path'].endswith('/server.py') and f['sha256']==verified['server_current_sha256'] for f in source['files'])
assert 'UNMEASURED' in verified['loaded_pid_module_identity']

old=load('historical-export-terminal.json')
assert old['terminal'] is True and old['returncode']==0 and not old['stderr']
assert old['historical_only'] is True and old['zip_sha256']==old['sidecar_sha256']
assert 'VERIFIED' in old['stdout'] and 'g20260929T075521Z-fbf2f8' in old['stdout']
release=(W/'retained/RELEASE-DASHBOARD-2026-09-29.md').read_text()
matrix=(W/'retained/ACCEPTANCE-MATRIX.md').read_text()
assert 'DELIVERED, NOT ACCEPTED' in release and 'A23' in matrix
verdict=load('verdict.json')
assert verdict['item']=='A23' and verdict['status']=='INCOMPLETE_NOT_ACCEPTED'
assert verdict['full_l1_l2_goal']=='ACTIVE_NOT_MET'
assert len(verdict['missing'])==3
print(json.dumps({'status':'A23_EVIDENCE_SLICE_VALID_NOT_ACCEPTED','generation':gen,
                  'progress':'PARTIAL','overview':'OK','historical_zip_generation':'g20260929T075521Z-fbf2f8',
                  'a23':verdict['status']}))
