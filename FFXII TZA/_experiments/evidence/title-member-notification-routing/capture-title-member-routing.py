"""OV29 title request factories, member callbacks and watcher attachment source.
No repeat of SECTION-04 synthetic/native fixtures, and no live session.
"""
import hashlib, importlib.util, json, pathlib, sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.RANGES=[(0x2491b0,0x24920c),(0x249320,0x24934b),
          (0x249660,0x249669),(0x249670,0x24967d),
          (0x24a1d0,0x24a440),(0x24a4e0,0x24a591)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         wrapper_complete=True,
         limits='selected original normal source, not complete service/IO effects or natural-lifetime/caller closure')
p.write_text(json.dumps(r,indent=2)+'\n')
