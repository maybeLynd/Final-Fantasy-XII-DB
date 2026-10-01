"""Minimum shipping spans for the new tail-effect question; no process observer."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('summon_tail_original_capture',W/'capture-index-path.py');C.RANGES=[(0x313550,0x31358a),(0x35c620,0x35c62c),(0x273e30,0x273ebc)]
sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('summon_tail_reviewed_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY full setter/thunk plus140B initializer prefix only, not full callee/function effects/natural type/caller proof.')
out.write_text(json.dumps(v,indent=2)+'\n');print('Captured exact mode setter/tail and only required initializer prefix')
