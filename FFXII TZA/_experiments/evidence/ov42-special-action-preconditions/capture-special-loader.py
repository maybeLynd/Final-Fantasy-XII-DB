"""OV42 follow-up: original action special-sequence loader argument gate.
Bounded prefix and complete contiguous selector helper; no original execution.
Uses the existing identity/role-controlled shipping-byte capture path.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.RANGES=[(0x306bd0,0x306c5b),(0x309230,0x3092f7)]
m.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         limits='original bounded caller prefix and selector helper; no action-table census, initialized runtime or all caller closure')
p.write_text(json.dumps(r,indent=2)+'\n')
