"""Certified local copy bodies; actual shared access-role adapter, no game."""
import importlib.util,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('capture',P/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x3325d0,0x33265b),(0x41e3a0,0x41e489),(0x409f10,0x409f42),(0x51f9f0,0x51fb6c),(0x51fb70,0x51fba7),(0x51fbb0,0x51fce3),(0x51f7a0,0x51f878),(0x41e580,0x41e58c)]
sys.argv=[sys.argv[0],str(P/'source-01.json')];C.main()
p=P/'source-01.json';x=json.loads(p.read_text());x['wrapper_complete']=True
x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
p.write_text(json.dumps(x,indent=2)+'\n')
