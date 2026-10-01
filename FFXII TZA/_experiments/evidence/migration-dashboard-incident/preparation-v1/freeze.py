import copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-01'
P=Path('Database/FFXII TZA/_experiments/evidence/migration-dashboard-incident')
assert not P.exists(),'Published evidence must not be overwritten'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=sha(R/'raw.json');raw=json.loads((R/'raw.json').read_text());controls=W/'reducer-controls';controls.mkdir(exist_ok=True)
tests=[]
variants={
 'incomplete':lambda r:r.pop('finished'),
 'missing-case':lambda r:r['cases'].pop(),
 'tampered-bytes-served':lambda r:next(c for c in r['cases'] if c['name']=='stat-preserved-mismatch-detected')['observed']['http']['view'].update(sentinel='TAMPERED'),
 'not-same-stat':lambda r:next(c for c in r['cases'] if c['name']=='stat-preserved-mismatch-detected')['observed'].update(mtime_after=1)}
for name,change in variants.items():
 r=copy.deepcopy(raw);change(r);p=controls/(name+'.json');p.write_text(json.dumps(r));out=controls/(name+'-result.json');assert not out.exists()
 run=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(p),'--out',str(out)],capture_output=True,text=True)
 tests.append(dict(name=name,input_sha256=sha(p),returncode=run.returncode,stdout=run.stdout,stderr=run.stderr,result_exists=out.exists()))
 assert run.returncode!=0 and not out.exists(),tests[-1]
run=subprocess.run([sys.executable,'-B',str(W/'check.py')],capture_output=True,text=True);assert run.returncode==0,(run.stdout,run.stderr)
assert sha(R/'raw.json')==before
(W/'reducer-controls.json').write_text(json.dumps(dict(baseline=dict(returncode=run.returncode,stdout=run.stdout,stderr=run.stderr),negative_controls=tests,original_raw_unchanged=True),indent=2)+'\n')
P.mkdir(parents=True)
for n in ['PLAN.md','README.md','capture.py','check.py','freeze.py','cleanup_verify.py','cleanup-verification.json','cleanup-native-verification.json','post-source-identity.json','result.json','reducer-controls.json']:
 shutil.copyfile(W/n,P/n)
shutil.copyfile(R/'raw.json',P/'raw.json')
# Make the retained checker runnable without recapture. Preserve source/input fixtures,
# not the 81MB real-build snapshot or the certified game binary.
(P/'run-01').mkdir();shutil.copyfile(R/'raw.json',P/'run-01/raw.json')
shutil.copytree(R/'source',P/'run-01/source')
for name in ['external-baseline','warm-tamper','input-tamper','stat-preserved-tamper','failed-build','volatile-mid-build','unknown-format','stale-reader']:
 shutil.copytree(R/name,P/'run-01'/name)
real=R/'real-build';ptr=json.loads((real/'CURRENT').read_text());g=real/ptr['generation']
dest=P/'real-build-observation';dest.mkdir();shutil.copyfile(real/'CURRENT',dest/'CURRENT');shutil.copyfile(g/'MANIFEST.json',dest/'MANIFEST.json');shutil.copytree(g/'outputs',dest/'outputs')
deps=[]
for f in sorted(g.rglob('*')):
 if f.is_file():deps.append(dict(path=f.as_posix(),bytes=f.stat().st_size,sha256=sha(f),portable_retained=('/outputs/' in f.as_posix() or f.name=='MANIFEST.json')))
(dest/'external-retained-inputs.json').write_text(json.dumps(dict(scope='Real scratch build observation; complete original input snapshot remains at private work paths, not a claimed portable export acceptance. Certified EXE is external, never copied.',files=deps),indent=2)+'\n')
members=[]
for f in sorted(P.rglob('*')):
 if f.is_file():members.append(dict(path=f.relative_to(P).as_posix(),bytes=f.stat().st_size,sha256=sha(f)))
(P/'manifest.json').write_text(json.dumps(dict(package='migration-dashboard-incident',members=members),indent=2)+'\n')
print('FROZEN',len(members),sum(x['bytes'] for x in members),flush=True)
