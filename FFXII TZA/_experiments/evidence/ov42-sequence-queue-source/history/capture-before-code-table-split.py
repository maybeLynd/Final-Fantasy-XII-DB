"""Original chained special-sequence code, including previously unread queue writer, with reviewed access-role path."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
s=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';x=json.loads((P/'extent-01.json').read_text());s0=json.loads((P/'extent-01.status.json').read_text())
if s0.get('terminal') is not True or s0.get('exit')!=0 or s0.get('exception') is not None or s0['driver_sha256']!=hashlib.sha256((P/'extent.py').read_bytes()).hexdigest() or not x.get('complete'):raise ValueError('required current extent failed')
C.RANGES=[(int(x['entry'],16),int(x['end_exclusive'],16))]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';x=json.loads(p.read_text());x.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest());p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
