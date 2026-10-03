"""Original terminal helper; retained decoder/caller are not recaptured."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 s=json.loads((P/'extents-01.status.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s.get('driver_sha256')!=sha(P/'prepare-extents.py') or not(P/'extents-01.stdout').read_bytes() or(P/'extents-01.stderr').read_bytes():raise ValueError('required successful current binding extent')
 e=json.loads((P/'extents-01.json').read_text())
 if e.get('complete') is not True or e.get('driver_sha256')!=sha(P/'prepare-extents.py') or [b['entry'] for b in e['bodies']]!=['0x305640']:raise ValueError('missing/stale/wrong binding extents')
 if sha(P/'capture-index-path.py')!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':raise ValueError('reviewed capture changed')
 spec=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
 C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(int(b['entry'],16),int(b['end_exclusive'],16)) for b in e['bodies']]
 out=P/sys.argv[1];sys.argv=[sys.argv[0],str(out)];C.main()
 x=json.loads(out.read_text());x.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),limits='Original complete binding bodies only; no execution, natural scheduling or initialized-resource invariance. Decoder/current caller retained separately.')
 out.write_text(json.dumps(x,indent=2)+'\n')
if __name__=='__main__':main()
