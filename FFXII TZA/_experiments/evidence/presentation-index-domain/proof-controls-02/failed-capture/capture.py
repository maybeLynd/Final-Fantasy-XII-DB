"""Capture only the newly required original body/caller prefix with shared roles."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('presentation_reviewed_capture',W/'capture-index-path.py')
C.RANGES=[(0x309230,0x3092f7),(0x306bd0,0x306c5b)]
sys.argv=[sys.argv[0],str(out)];C.main()
v=json.loads(out.read_text());v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=load('presentation_roles_validator',W/'validate-title-source-annotations.py').validate(v),limits='STATIC_ONLY complete309230 body and306BD0 prefix through32FC30; prefix is not complete caller CFG or natural admission.')
out.write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'complete_original_body':'0x309230','caller_prefix_end':'0x306c5b'}))
