"""OV42 admission residue: the original class20 validity and slot readiness guards.
Source only; catalogue span lengths are validated for full contiguous decoding.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(0x322c50,0x323051),(0x30c890,0x30c964)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits='bounded source guards; no full caller CFG or natural command eligibility')
p.write_text(json.dumps(r,indent=2)+'\n')
