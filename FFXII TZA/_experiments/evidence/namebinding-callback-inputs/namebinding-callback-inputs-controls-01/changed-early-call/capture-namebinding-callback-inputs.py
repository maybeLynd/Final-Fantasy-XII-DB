"""Original early-call argument-dependency graph; retained callback not recaptured."""
import hashlib, importlib.util, json, pathlib, sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('callback_inputs_capture','capture-index-path.py')
S=module('callback_inputs_roles','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x32f3d0,0x32f427),(0x408b30,0x408b38),(0x408b10,0x408b18),
          (0x36b130,0x36b159),(0x409090,0x4090c5),(0x5c5230,0x5c5233)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,
    invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    annotation_prerequisite=S.validate(v),limits='Static original early-call graph only, no live content/error reachability or execution. 5C5230 shipping zero stub is not evidence of native storage effects.')
out.write_text(json.dumps(v,indent=2)+'\n')
print('Six source-directed early bodies200B; callback retained unchanged')
