"""Single original body for a specific erroneous consumer description."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('drain_capture','capture-index-path.py');S=module('drain_roles','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x2e6900,0x2e6a7a)];C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Single complete normal body, not full caller/IO or opaque callee behavior')
out.write_text(json.dumps(v,indent=2)+'\n');print('Original378B drain body; no game')
