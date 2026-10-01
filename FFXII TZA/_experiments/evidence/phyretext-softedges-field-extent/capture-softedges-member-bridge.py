"""Focused Method A source supplement for array member offset resolution.
No game, census or native execution. Existing raw outputs stay immutable.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
out=W/'softedges-resource-source-01/member-bridge-code-01.json'
if out.exists(): raise ValueError('immutable output exists')
s=importlib.util.spec_from_file_location('reviewed_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x59bed0,0x59c17f)]
sys.argv=[sys.argv[0],str(out)];C.main()
r=json.loads(out.read_text());r.update(wrapper_complete=True,
 invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 limits='Original pdata fragment59BED0..59C17F only; packed/native member bridge, not game/resource initialization or lifetime.')
out.write_text(json.dumps(r,indent=2)+'\n')
