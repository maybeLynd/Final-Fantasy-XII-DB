"""Original lane-release discriminator; no registration census or live setup.

Read before retry: requested bit already set prevents the local enqueue path.
Prior queue membership is a premise to examine, not a pointer snapshot fact.
2EB890 is a lane-count helper, not a sweep-list writer.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=module('stale_lane_capture','capture-index-path.py');S=module('stale_lane_annotations','validate-title-source-annotations.py')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable source exists')
C.RANGES=[(0x2e4e50,0x2e4f34),(0x2eafa0,0x2eb027),(0x2eb890,0x2eb923),(0x2e6a80,0x2e6b0d),(0x2e2660,0x2e26e8)]
C.main();v=json.loads(out.read_text());v.update(wrapper_complete=True,invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),annotation_prerequisite=S.validate(v),limits='Five complete bounded bodies; branch/call/write evidence only, not full queue producers, initialization, natural scheduling or native/live execution')
out.write_text(json.dumps(v,indent=2)+'\n');print('Five original lane completion/request/count/sweep/allocator bodies; no game')
