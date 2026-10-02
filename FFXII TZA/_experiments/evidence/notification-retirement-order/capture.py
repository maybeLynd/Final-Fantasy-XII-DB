"""Static source capture, using the reviewed adapter on the actual invocation."""
import hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
x=json.loads((P/'retained-body-identities.json').read_text())
C.RANGES=[(int(b['entry'],16),int(b['entry'],16)+b['length']) for b in x['bodies']]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';v=json.loads(p.read_text())
v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
p.write_bytes((json.dumps(v,indent=2)+'\n').encode())
