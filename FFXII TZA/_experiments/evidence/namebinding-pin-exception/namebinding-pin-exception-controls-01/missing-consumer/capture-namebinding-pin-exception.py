"""Exact positive setter and submitter; candidates alone are not type proof."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('pin_capture','capture-index-path.py');S=module('pin_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x2e6700,0x2e687d),(0x2ead50,0x2eae1e),(0x2e25e0,0x2e2651)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Positive setter/submitter/constructor local boundaries; no complete writer census, real allocation/read acceptance or natural pending-state exclusion')
out.write_text(json.dumps(v,indent=2)+'\n');print('Original mask04 setter/clear-before-submit and record constructor; no game')
