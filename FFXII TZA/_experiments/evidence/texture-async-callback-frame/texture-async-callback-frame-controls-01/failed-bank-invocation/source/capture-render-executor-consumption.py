"""Returned BG11 executor/context source confirmation; no new live observation.
Source only; catalogue span lengths are validated for full contiguous decoding.
"""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(0x6106a0,0x6107e2),(0x60a410,0x60aab7),(0x5fd050,0x5fd0d1),(0x624670,0x624675),(0x624660,0x624668),(0x1f4a10,0x1f4a3f)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    limits='source confirmation of already published callback executor/context; normal native ABI and initialized object premises, no actual live hit/thread sample')
p.write_text(json.dumps(r,indent=2)+'\n')
