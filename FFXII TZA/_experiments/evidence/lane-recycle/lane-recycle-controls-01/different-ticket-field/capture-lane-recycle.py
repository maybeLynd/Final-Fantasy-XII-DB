"""Capture only three missing bodies; retained lane code is not recaptured.

Read before retry: a pending mask is not a proven outstanding accepted read.
Local recycle without a pending test is not proof of natural late callbacks.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('recycle_capture','capture-index-path.py');S=module('recycle_roles','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x2e6eb0,0x2e7072),(0x2e9470,0x2e9552),(0x2e4000,0x2e4145)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Three bounded complete original bodies; no natural callback/service scheduling, IO acceptance or native/live execution proof')
out.write_text(json.dumps(v,indent=2)+'\n');print('Three missing original ticket/recycler/group-release bodies; retained source reused')
