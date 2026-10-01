"""OV29 cheapest-method preparation: original watcher/teardown boundaries.

Reuses the reviewed capture and its *actual* access-role controls.  Existing
SECTION-04 title-handler/ticket/release observations stay separate; do not rerun
their native fixtures. Selected .pdata records and explicit small leaves are
source spans, not a claim of complete transitive lifetimes or natural scheduling.
Usage: python capture-title-watcher-lifetime.py FRESH_OUTPUT_JSON
"""
import hashlib, importlib.util, json, pathlib, sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('verified_capture', W / 'capture-index-path.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [
    (0x181610, 0x18162e), (0x244f00, 0x244f44),
    (0x245020, 0x2450a4), (0x248700, 0x24879f),
    (0x249210, 0x249319), (0x2494f0, 0x24957a),
    (0x2495c0, 0x249653), (0x394130, 0x394342),
    (0x394400, 0x394411), (0x511ea0, 0x511eb2),
    (0x511ec0, 0x511ed7), (0x582860, 0x582fc0),
]
C.main()
p = pathlib.Path(sys.argv[1])
r = json.loads(p.read_text())
r.update(
    invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    wrapper_complete=True,
    limits='original selected contiguous source; no live state, no full callback/caller census, no natural reachability or transitive lifetime proof',
)
p.write_text(json.dumps(r, indent=2) + '\n')
