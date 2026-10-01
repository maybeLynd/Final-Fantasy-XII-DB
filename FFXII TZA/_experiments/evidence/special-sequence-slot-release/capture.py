"""Complete original slotrelease, ownerresolver and guarded globalrelease; no gameplay."""
import importlib.util,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.ROOT=next(q for q in W.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(0x30c970,0x30ca50),(0x306570,0x3065c7),(0x31b7e0,0x31b80a)]
sys.argv=[sys.argv[0],str(W/'source-01.json')];C.main()
p=W/'source-01.json';x=json.loads(p.read_text());x['wrapper_complete']=True;x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();p.write_text(json.dumps(x,indent=2)+'\n')
