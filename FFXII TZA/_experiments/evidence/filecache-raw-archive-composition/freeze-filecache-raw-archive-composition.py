"""Freeze the bounded stage lemma after real producer/refusal checks."""
import hashlib,json
from pathlib import Path
import shutil
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=W/'filecache-raw-archive-composition-frozen-ready'
 if out.exists():raise ValueError('immutable packet exists')
 stages=[('filecache-format-boundary-capture-01','capture-filecache-format-boundary.py'),('filecache-raw-archive-composition-positive-02','prove-filecache-raw-archive-composition.py'),('filecache-raw-archive-composition-controls-run-01','control-filecache-raw-archive-composition.py')]
 for tag,driver in stages:
  s=json.loads((W/(tag+'.status.json')).read_text())
  if s.get('exit')!=0 or s.get('terminal') is not True or s.get('driver_sha256')!=sha(W/driver):raise ValueError('upstream failed/incomplete/stale')
  if not(W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes():raise ValueError('upstream missing/error output')
 r=json.loads((W/'filecache-raw-archive-composition-result-02.json').read_text())
 if r.get('producer_complete') is not True or r['driver_sha256']!=sha(W/'prove-filecache-raw-archive-composition.py') or len(r['graphs'])!=4 or len(r['ascii_stage_controls'])!=128 or len(r['external_dependencies'])!=3:raise ValueError('nonempty proof result incomplete')
 for x in r['source_pins']:
  if sha(W/x['path'])!=x['sha256']:raise ValueError('required source changed')
 c=json.loads((W/'filecache-raw-archive-composition-controls-01/result.json').read_text())
 if c.get('complete') is not True or len(c['cases'])!=4 or c['status']!='PASS_FOUR_ACTUAL_REFUSALS' or not all(x['passed'] and x['terminal'] and x['exit']!=0 and x['result_absent'] for x in c['cases']):raise ValueError('required actual controls incomplete')
 if c['driver_sha256']!=sha(W/'control-filecache-raw-archive-composition.py') or c['producer_sha256']!=r['driver_sha256']:raise ValueError('control/producer changed')
 files=['capture-index-path.py','validate-title-source-annotations.py','prove_owner_reload_order.py','run-filecache-equal-key.py',
 'filecache-format-boundary-source-01.json','prove-filecache-raw-archive-composition.py','prove-filecache-raw-archive-composition-before-classifier-prerequisite-01.py',
 'filecache-raw-archive-composition-result-01.json','filecache-raw-archive-composition-result-02.json','control-filecache-raw-archive-composition.py','freeze-filecache-raw-archive-composition.py',
 'FILECACHE-RAW-ARCHIVE-COMPOSITION-METHOD-1001.md','filecache-raw-archive-composition-controls-01/result.json']
 for tag,driver in stages:
  files.append(driver);files.extend(tag+s for s in ['.status.json','.stdout','.stderr'])
 files.extend('filecache-raw-archive-composition-positive-01'+s for s in ['.status.json','.stdout','.stderr'])
 for case in c['cases']:
  base=Path('filecache-raw-archive-composition-controls-01')/case['tag']
  for name,pin in case['inherited_from_baseline'].items():
   if sha(W/base/name)!=pin or sha(W/name)!=pin:raise ValueError('delta not lossless')
  if sha(W/base/case['changed_file'])!=case['changed_sha256']:raise ValueError('delta changed')
  files.extend((base/name).as_posix() for name in [case['changed_file'],'stdout','stderr','receipt.json'])
 out.mkdir()
 for name in sorted(set(files)):
  p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,p)
 shutil.copy2(W/'FILECACHE-RAW-ARCHIVE-COMPOSITION-README-1001.md',out/'README.md')
 (out/'external-dependencies.json').write_text(json.dumps(dict(required=r['external_dependencies'],missing='INCOMPLETE/refusal; pinned repository parents required'),indent=2)+'\n')
 (out/'toupper-contract.json').write_text(json.dumps(dict(method='Named API premise, not loaded CRT',url='https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/toupper-toupper-towupper-toupper-l-towupper-l?view=msvc-170',read_date='2026-10-01',paraphrase='The documented conversion uses the currently set locale. This proof explicitly assumes C-ASCII conversion; it does not establish the game locale. The initial URL omitted the separate _toupper slug and failed; corrected official source found by domain-filtered search.'),indent=2)+'\n')
 (out/'.gitattributes').write_text('* -text\n')
 members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
 (out/'manifest.json').write_text(json.dumps(dict(kind='bounded original raw/archive cache-name composition',members=members),indent=2)+'\n')
 print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
if __name__=='__main__':main()
