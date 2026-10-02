"""Original source-carrier boundaries, not new live observations."""
import importlib.util,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x59ee90,0x59f1fc),(0x59a9b0,0x59aad5),(0x20c1b0,0x20c2f2)]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';x=json.loads(p.read_text());x['wrapper_complete']=True
x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
