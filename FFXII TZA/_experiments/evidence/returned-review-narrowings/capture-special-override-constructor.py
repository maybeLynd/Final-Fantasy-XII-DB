"""OV42: constructor source for the override control's initial-domain premise.
Full first constructor fragment is a normal native body, not EH/lifetime proof.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
C.RANGES=[(0x1ccb20,0x1ccfda)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 limits='original normal constructor source; actual helper effects/alias and initialized lifetime remain distinct',wrapper_complete=True)
p.write_text(json.dumps(r,indent=2)+'\n')
