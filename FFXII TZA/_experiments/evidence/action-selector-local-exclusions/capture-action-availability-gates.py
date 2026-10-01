"""OV42: are the downstream category/licence availability checks a candidate-row exclusion?
Source only; catalogue span lengths are validated for full contiguous decoding.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(0x2ffcf0,0x2ffecf),(0x3060e0,0x306333),(0x306480,0x3064e3),(0x323ec0,0x324012)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits='bounded source guards; no full caller CFG or natural command eligibility')
p.write_text(json.dumps(r,indent=2)+'\n')
