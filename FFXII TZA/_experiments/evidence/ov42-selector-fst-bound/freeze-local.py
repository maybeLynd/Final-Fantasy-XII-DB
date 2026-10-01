"""Existing manifest-style local evidence freeze; not an acceptance/sealing system.
Fresh owned destination only; canonical copy requires a separate publication claim.
"""
import hashlib, json, pathlib, shutil, sys
W=pathlib.Path(__file__).resolve().parent; ROOT=W.parents[4]
F=W/'frozen-ready'
if F.exists(): raise ValueError('immutable freeze already exists')
def sha(b): return hashlib.sha256(b).hexdigest()
raw=json.loads((W/'index-path-raw-02.json').read_text())
res=json.loads((W/'index-domain-result-01.json').read_text())
assert raw['driver_sha256']==sha((W/'capture-index-path.py').read_bytes())
assert res['driver_sha256']==sha((W/'prove-index-domain.py').read_bytes())
assert res['raw_sha256']==sha((W/'index-path-raw-02.json').read_bytes())
assert len(res['results'])==12 and len(res['valid_controls'])==4
assert all(c['rejected'] for c in res['valid_controls'])
F.mkdir(); (F/'.gitattributes').write_bytes(b'* -text\n')
for n in ['README.md','METHODS.md','capture-index-path.py','prove-index-domain.py',
          'index-path-raw-02.json','index-domain-result-01.json','freeze-local.py']:
    shutil.copyfile(W/n,F/n)
shutil.copytree(W/'fst-inputs-01',F/'fst-inputs-01')
source=pathlib.Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables')
pins=[]
for p in sorted((F/'fst-inputs-01').glob('*.fst')):
    data=(source/p.name).read_bytes(); assert data==p.read_bytes()
    pins.append(dict(source=str(source/p.name),frozen=str(p.relative_to(F)),bytes=len(data),sha256=sha(data),
                     source_equals_copy_after_analysis=True))
(F/'input-restoration-receipt.json').write_text(json.dumps(dict(game_started=False,
    game_inputs=False,memory_interventions=False,instruments_attached=False,
    saves_config_touched=False,install_tables=pins,
    exe_sha256_after=sha((ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes())),indent=2)+'\n')
assert json.loads((F/'input-restoration-receipt.json').read_text())['exe_sha256_after']==raw['exe_sha256']
paths=[
 'Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/README.md',
 'Database/FFXII TZA/_index/candidates/ov-rt-probes-0929/notes.md',
 'Database/FFXII TZA/_index/candidates/ov-rt-probes-0929/successor-request.md',
 'Database/FFXII TZA/_index/OPEN-QUESTIONS.md',
 'Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md',
 'Database/FFXII TZA/18-Audio/the-voice-pack-slots-and-the-voice-verbs.md',
 'Database/FFXII TZA/02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md',
 'Database/FFXII TZA/_index/candidates/ov10-request-bounds-fable/README.md',
 'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py']
source_dir=F/'source-preimages'; source_dir.mkdir()
records=[]
for i,rel in enumerate(paths):
    p=ROOT/rel; blob=p.read_bytes(); name='%02d-%s'%(i,p.name)
    assert p.read_bytes()==blob, 'source changed during read; retry fresh freeze'
    (source_dir/name).write_bytes(blob)
    records.append(dict(source=rel,frozen='source-preimages/'+name,sha256=sha(blob)))
(F/'source-preimages.json').write_text(json.dumps(records,indent=2)+'\n')
members=[dict(path=p.relative_to(F).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
         for p in sorted(F.rglob('*')) if p.is_file()]
(F/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALIDATED_PENDING_INDEPENDENT_REVIEW',
    limits='STATIC_ONLY; bounded selector domain; natural shipped rejection OPEN; no live execution',
    members=members),indent=2)+'\n')
for m in members: assert sha((F/m['path']).read_bytes())==m['sha256']
print('Frozen locally',len(members),'members; exact input/source receipts; not independent acceptance')
