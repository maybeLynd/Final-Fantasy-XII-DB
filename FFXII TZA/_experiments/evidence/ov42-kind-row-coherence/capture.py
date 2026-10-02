"""New145B classifier suffix; committed139B prefix is retained separately."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
s=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
e=json.loads((P/'extent-01.json').read_text());z=json.loads((P/'extent-01.status.json').read_text())
if z.get('terminal') is not True or z.get('exit')!=0 or z.get('exception') is not None or z['driver_sha256']!=hashlib.sha256((P/'extent.py').read_bytes()).hexdigest() or e.get('complete') is not True:raise ValueError('required successful current extent')
C.RANGES=[(0x306c5b,0x306cec)];sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';x=json.loads(p.read_text());x.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),code_limit='Classifier code ends306CEB RET; embedded tables follow. Prefix306BD0..306C5B retained, not recaptured.');p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
