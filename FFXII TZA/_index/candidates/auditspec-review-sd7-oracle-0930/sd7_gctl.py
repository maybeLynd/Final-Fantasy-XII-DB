"""sd7_gctl.py - positive controls for sd7_indep.py section G (the address-taken test), run on the instrument itself
(runpy of sd7_indep.py, its stdout discarded). Defect named: a `taken()` or caller-chain that can never fire would make
G's "0 rows at risk" a property of the filter.
  G1 0017D1A0 (GameApplication slot 15, one vtable qword) must show q >= 1
  G2 00227EE0 (widget procedure, registered by `lea rdx,[rip+0x21]` at 00227EB8) must show lea >= 1
  G3 the caller chain from 002475D0 must reach the root of its caller 00228070 in one level (rawcalls keys unpadded)
"""
import contextlib, io, os, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    g = runpy.run_path(os.path.join(HERE, "sd7_indep.py"), run_name="__ctl__")
q, l = g["qref"], g["learef"]
print("G1 0017D1A0 q%d lea%d taken %d  -> %s" % (q.get(0x0017D1A0, 0), l.get(0x0017D1A0, 0), g["taken"](0x0017D1A0),
      "PASS" if q.get(0x0017D1A0, 0) >= 1 else "FAIL"))
print("G2 00227EE0 q%d lea%d taken %d  -> %s" % (q.get(0x00227EE0, 0), l.get(0x00227EE0, 0), g["taken"](0x00227EE0),
      "PASS" if l.get(0x00227EE0, 0) >= 1 else "FAIL"))
RAW, fs = g["RAW"], g["fstart"]
lvl1 = {fs(int(c, 16)) for c in RAW.get("%X" % 0x002475D0, ())}
want = fs(0x00228070)
print("G3 callers of 002475D0: %d sites, %d roots; root of 00228070 = %s in chain: %s" % (
    len(RAW.get("%X" % 0x002475D0, ())), len(lvl1), ("%08X" % want) if want else None, "PASS" if want in lvl1 else "FAIL"))
