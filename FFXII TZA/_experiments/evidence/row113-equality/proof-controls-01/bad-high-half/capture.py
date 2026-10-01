"""Capture the required original normalization body, not old caller/table samples."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('row113_original_capture',W/'capture-index-path.py');C.RANGES=[(0x30ce10,0x30cf3f)]
sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text())
v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('row113_reviewed_roles',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY full original30CE10; no game/native execution or natural initialized state.')
out.write_text(json.dumps(v,indent=2)+'\n');print('Complete normalization body captured with actual reviewed role adapter')
