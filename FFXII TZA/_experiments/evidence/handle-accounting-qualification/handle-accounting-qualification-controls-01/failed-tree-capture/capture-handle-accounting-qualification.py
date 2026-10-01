"""Exact positive setter and submitter; candidates alone are not type proof."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('accounting_capture','capture-index-path.py');S=module('accounting_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x36c5d0,0x36c61f),(0x369800,0x369855)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Complete accounting leaf/free entry with explicit external tail; no protective pin, arbitrary-handle safety or full physical reclamation claim')
out.write_text(json.dumps(v,indent=2)+'\n');print('Original accounting leaf/free entry164B; no game')
