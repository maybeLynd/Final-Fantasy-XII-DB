"""Validate retained observations; rejecting incident acceptance is the scientific result."""
import argparse,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01'
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=R/'raw.json');ap.add_argument('--out',type=Path,default=W/'result.json');args=ap.parse_args()
r=json.loads(args.raw.read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r.get('finished') is True and not r.get('fatal')
assert r['driver_sha256']==sha(W/'capture.py')
assert all(r['sources_restored'].values())
for rel,s in r['sources'].items():assert sha(R/s['retained'])==s['sha256']
cases={c['name']:c for c in r['cases']};assert len(cases)==len(r['cases'])==14
names={'deployed-seven-view-coherence','external-input-baseline','actual-http-read-only','warm-output-tamper-rejected',
       'snapshot-tamper-no-fallback','stat-preserved-mismatch-detected','stat-preserved-tampered-bytes-not-served',
       'missing-output-failed-build-preserves-current','strict-input-mid-build-rejected','volatile-change-coherent-commit',
       'unknown-format-unsupported','stale-reader-reports-change','actual-build-cli-while-board-advances','real-scratch-build-seven-views'}
assert set(cases)==names
bad=cases['stat-preserved-mismatch-detected']['observed']
assert bad['size_before']==bad['size_after'] and bad['mtime_before']==bad['mtime_after']
assert bad['cli']['returncode']==1 and 'does not match the manifest' in bad['cli']['stdout']
assert bad['http']['view']['sentinel']=='ORIGINAL' and bad['http']['meta']['historical'] is False
assert bad['status']['current']['problems']==[] and bad['status']['problems']==[]
assert bad['status']['views']['overview']=='OK' and not bad['status']['no_verified_generation']
assert 'TAMPERED' not in json.dumps(bad['http'])
assert cases['stat-preserved-mismatch-detected']['passed'] is False
assert all(c['passed'] is True for n,c in cases.items() if n!='stat-preserved-mismatch-detected')
# Recompute important positive/negative controls from actual observations.
obs=cases['deployed-seven-view-coherence']['observed'];assert len(set(obs['generations']))==1 and None not in obs['generations']
obs=cases['external-input-baseline']['observed'];assert obs['cli']==0 and obs['http']['view']['sentinel']=='VALID_EXTERNAL'
obs=cases['warm-output-tamper-rejected']['observed'];assert obs['cli']==1 and obs['status']['historical'] and obs['view']['view']['sentinel']=='PRIOR_VALID'
obs=cases['snapshot-tamper-no-fallback']['observed'];assert obs['cli']==1 and obs['http']['status']=='INVALID' and 'view' not in obs['http']
obs=cases['missing-output-failed-build-preserves-current']['observed'];assert 'required outputs missing' in obs['error'] and obs['cli']==0
obs=cases['strict-input-mid-build-rejected']['observed'];assert 'inputs moved during the build' in obs['error']
obs=cases['volatile-change-coherent-commit']['observed'];assert obs['problems']==[] and obs['drift']=={'controlled':'changed'}
obs=cases['unknown-format-unsupported']['observed'];assert obs['cli']['returncode']==1 and obs['view']['status']=='UNSUPPORTED'
obs=cases['stale-reader-reports-change']['observed'];assert obs==dict(before=False,after=True)
obs=cases['actual-build-cli-while-board-advances']['observed'];assert obs['command']['returncode']==0 and obs['problems']==[] and obs['revision_after']>obs['revision_before'] and obs['epoch_before']==obs['epoch_after']==3
cl=json.loads((W/'cleanup-native-verification.json').read_text());assert cl['verified'] and len(cl['servers'])==7 and all(x['process_state']=='ABSENT' and not x['listener_present'] for x in cl['servers'])
result=dict(verdict='REJECT',status='REJECT_INCIDENT_ACCEPTANCE_CACHE_MISMATCH',method=r['method'],
    raw_sha256=sha(args.raw),driver_sha256=r['driver_sha256'],observations=14,
    established='Deployed seven views coherent/stale reported; external input accepted; ordinary output/snapshot tamper rejected; failed/strict build preserves current; volatile coherent commit and actual scratch build with board38747->38749; unknown format unsupported; stale reader reports private code change.',
    defect='Warm server cache ignores same-size same-mtime output alteration: CLI verifies mismatch/exit1 while HTTP declares no problems and all views OK. Cached ORIGINAL returned, not corrupted TAMPERED bytes. Do not inflate into tampered-data exposure.',
    cause='server.State._key uses path/size/mtime_ns and CURRENT/history metadata, not content fingerprint. Preserving stat key avoids open_current re-verification.',
    acceptance_discriminator='Actual warm HTTP path must detect this retained same-stat mismatch or enforce a demonstrated immutable generation boundary with a correct limited claim. Matching verifier rejects it; no silent CURRENT/OK for unchecked changed disk evidence.',
    limits='Synthetic fault stores/private actual server CLI, read-only deployed HTTP sample and real scratch producer build. Not deployment cutover/controller/host adapters/whole M0-M5 acceptance, game evidence or raw tampered bytes being served. Full L1+L2 NOT_MET.',
    cleanup='Seven owned parent PIDs absent (OpenProcess error87), seven loopback ports not LISTENING; private source restored. Initial URL timeouts were not terminal proof; additive correction retained.')
args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
