"""Complete local original bodies through the actual reviewed role adapter."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('s33history_reviewed_capture',W/'capture-index-path.py')
C.RANGES=[(0x3fc170,0x3fc3e2),(0x3fbe90,0x3fc16a),(0x3fa160,0x3fa4d6),(0x275550,0x27556c),(0x202c90,0x202c97)]
sys.argv=[sys.argv[0],str(out)];C.main()
v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('s33history_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY complete local bodies; conditional history count/address bounds, no mathematicalcallee closure/actualownership/interference/presentation/native/live gameplay')
out.write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'ranges':[{'start':r['start'],'end':r['end_exclusive'],'sha256':r['sha256']} for r in v['ranges']]}))
