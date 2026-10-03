"""Additive prerequisite qualification; original binding packet stays immutable."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=P/sys.argv[1];base=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'Database/FFXII TZA/_experiments/evidence/ov42-action-table-binding'
 if out.exists():raise ValueError('fresh qualification output required')
 s=importlib.util.spec_from_file_location('capture_checks',P/'capture_prerequisites.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
 checks=[C.check(base,'prepare-binding-extents.py','capture-binding.py','binding-extents-01','binding-capture-01','binding-extents-01.json','binding-source-01.json',['0x3845f0','0x236c30']),C.check(base,'prepare-binding-helper-extents.py','capture-binding-helpers.py','binding-helper-extents-01','binding-helper-capture-01','binding-helper-extents-01.json','binding-helper-source-01.json',['0x237fc0','0x3846f0'])]
 if sha(base/'manifest.json')!='e2ae054634b26a2ca12990781696b3ee041def5477fa4528863ab2f180029da3':raise ValueError('original binding manifest changed')
 manifest=json.loads((base/'manifest.json').read_text())
 for m in manifest['members']:
  p=base/m['path']
  if p.stat().st_size!=m['bytes'] or sha(p)!=m['sha256']:raise ValueError('original binding member changed')
 r=json.loads((base/'result-02.json').read_text())
 if r.get('producer_complete') is not True or r.get('driver_sha256')!=sha(base/'prove.py'):raise ValueError('original binding producer missing')
 with out.open('x')as f:json.dump(dict(complete=True,driver_sha256=sha(Path(__file__)),base_commit='ca2dd6483fdcd24535237d727d8ea2fa34e2c19b',base_manifest_sha256=sha(base/'manifest.json'),actual_capture_checks=checks,base_result_sha256=sha(base/'result-02.json'),limits='Additive producer-prerequisite qualification only; original bytes/facts unchanged, independent acceptance still pending. Does not prove live/callee/lifetime semantics.'),f,indent=2)
 print('QUALIFIED both original binding capture pipelines against complete metadata/wrappers and immutable members')
if __name__=='__main__':main()
