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
C=load('s33clock_reviewed_capture',W/'capture-index-path.py')
C.RANGES=[(0x3fa820,0x3fa900),(0x3fc510,0x3fc8fd),(0x3fa790,0x3fa81f),(0x3fa4e0,0x3fa567),(0x1ede80,0x1edebd)]
sys.argv=[sys.argv[0],str(out)];C.main()
v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('s33clock_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY complete bytes; no native execution, actual cadence, initialized motion/flags, render effects or gameplay exhaustion')
out.write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'ranges':[{'start':r['start'],'end':r['end_exclusive'],'sha256':r['sha256']} for r in v['ranges']]}))
