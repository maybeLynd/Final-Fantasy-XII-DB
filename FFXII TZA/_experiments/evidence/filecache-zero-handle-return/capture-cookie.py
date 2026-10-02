"""Exact normal-return cookie check: don't assume a volatile RAX survives a call."""
import importlib.util,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.ROOT=next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());C.EXE=C.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=C.ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py';C.RANGES=[(0x808c40,0x808c61)]
sys.argv=[sys.argv[0],str(P/'source-02.json')];C.main()
p=P/'source-02.json';x=json.loads(p.read_text());x['wrapper_complete']=True;x['invocation_driver_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
