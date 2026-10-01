"""Exact positive setter and submitter; candidates alone are not type proof."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('accounting_capture','capture-index-path.py');S=module('accounting_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x36d170,0x36d1f5)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Actual callback tree-access release133B; header stamp and tree eligibility, opaque insertion/native lifetime limits')
out.write_text(json.dumps(v,indent=2)+'\n');print('Actual36D170 tree-access release133B; no game')
