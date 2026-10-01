"""Resolve the concrete prefix ABI prerequisite from original stack-probe bytes."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'stack-probe-source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('summon_stack_original_capture',W/'capture-index-path.py');C.RANGES=[(0x808f10,0x808f61)]
sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('summon_stack_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY stack-probe register/prefix prerequisite; no OS page-commit/fault/MPX-state or live stack proof.')
out.write_text(json.dumps(v,indent=2)+'\n');print('Captured original stack probe for receiver/register preservation; no OS execution')
