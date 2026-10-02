"""Original rig owner producers and separate link/full-reset rebinding bodies; actual shared access-role adapter, no game."""
import importlib.util,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x372350,0x3723a4),(0x3e3ca0,0x3e3d64),(0x3e3d70,0x3e4131),(0x4215a0,0x421892)]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';x=json.loads(p.read_text());x['wrapper_complete']=True
x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
p.write_text(json.dumps(x,indent=2)+'\n')
