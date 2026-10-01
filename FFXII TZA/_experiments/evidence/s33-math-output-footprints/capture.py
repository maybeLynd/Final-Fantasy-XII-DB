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
C=load('s33math_reviewed_capture',W/'capture-index-path.py')
C.RANGES=[(0x202b10,0x202b61),(0x202de0,0x202e01),(0x203080,0x2030d1),(0x270720,0x270874),(0x203170,0x20319c),(0x270a10,0x270b37),(0x270cf0,0x270f45),(0x270b40,0x270ce4),(0x216660,0x21671a),(0x202e90,0x202ef4),(0x202f00,0x202f64),(0x217790,0x21787c),(0x217880,0x21796a)]
sys.argv=[sys.argv[0],str(out)];C.main()
v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('s33math_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY complete local bodies; new math helper bytes only; native tails need explicitclosure. Retained parent caller/vectorwrapper/leaf reused. No floattrajectory/interference/scheduler/ownership/presentation/native/live claim')
out.write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'ranges':[{'start':r['start'],'end':r['end_exclusive'],'sha256':r['sha256']} for r in v['ranges']]}))
