"""Original special-action admission gate and selector path; source analysis only.
Separate final driver preserves prior special-loader capture/source identities.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.RANGES=[(0x30ce10,0x30cf3f),(0x306bd0,0x306c5b),(0x309230,0x3092f7)]
m.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         limits='contiguous source gates under initialized row/codec and normal ABI premises; no command eligibility or natural execution proof')
p.write_text(json.dumps(r,indent=2)+'\n')
