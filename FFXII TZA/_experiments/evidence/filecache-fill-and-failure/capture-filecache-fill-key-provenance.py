"""Bounded resolver only; qualified direct/fill bodies are reused, not recaptured."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
out=W/'filecache-fill-key-resolver-source-01.json'
if out.exists():raise ValueError('immutable source exists')
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('fill_key_capture',W/'capture-index-path.py');C.RANGES=[(0x59ee90,0x59f1fc)]
sys.argv=[sys.argv[0],str(out)];C.main()
v=json.loads(out.read_text());v.update(wrapper_complete=True,
    invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    annotation_prerequisite=load('fill_key_annotations',W/'validate-title-source-annotations.py').validate(v),
    limits='Exact normal resolver throughRET59F1FB; no natural path state, all callers, opaque callee/MD5/CRT effects or lifetime proof')
out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
print('CLOSED DECLARED RESOLVER',v['ranges'][0]['sha256'],len(v['ranges'][0]['instructions']))
