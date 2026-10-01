"""Small original-code deletion slice; no live or synthetic state execution.

Read before retry: flags are masks02/04/08, not bit-index numbers. The final
continuation is an explicit prefix/tail slice, not full scheduling reachability.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('namebinding_capture','capture-index-path.py');S=module('namebinding_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x2eaeb0,0x2eaf70),(0x2e4d20,0x2e4dfe),(0x2ea6e0,0x2ea77d),
    (0x2e6d60,0x2e6e25),(0x2e9360,0x2e946b),(0x2e60f0,0x2e6103),(0x2e629e,0x2e62db)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,
    invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    annotation_prerequisite=S.validate(v),
    limits='Five complete local catalog bodies, command-consumer prefix/tail only. No full consumer scheduling/native/live or malformed-state safety claim.')
out.write_text(json.dumps(v,indent=2)+'\n');print('Five original deletion/completion bodies and explicit continuation slices; no game')
