"""Original producer/map spans through the shared reviewed capture path."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
out=P/'source-01.json'
if out.exists():raise RuntimeError('immutable source exists')
C=load('summon_selector_original_capture',W/'capture-index-path.py')
C.RANGES=[(0x50ffb0,0x50ffeb),(0x3139c0,0x3139ce),(0x3137e0,0x3137ef),(0x3266c0,0x326ba5)]
sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text())
v.update(wrapper_complete=True,wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 annotation_prerequisite=load('summon_selector_reviewed_roles',W/'validate-title-source-annotations.py').validate(v),
 limits='STATIC_ONLY original spans. Full source endpoints/CFG checked by producer; no native/VM/pop execution or natural argument/type proof.')
out.write_text(json.dumps(v,indent=2)+'\n');print('Captured producer, byte setter/getter and complete native map refresher source')
