"""sec_rederive.py - own-tool checks for the section-addressing page (C1, F1) and the queue gap's second writer (G1).

  C1  002ED570: raw E8/E9/jcc call sites and distinct .pdata-root owners; relocated pointers
  F1  004096C0 body: the guards and the unguarded 32-bit add + cdqe
  G1  0032EAE0's caller and that caller's .pdata root (the page says the boot hub 0022A0B0)
  S10 one SECTION-10 sample: every rip reference to the query scratch 02B62E20 (the page: "shared scratch")
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402

cs = I.calls_to(0x002ED570)
own = {I.func_of(s) for s, _ in cs}
print("C1 002ED570: %d sites %s, %d distinct owners, None-owner %d, relocated pointers %d" % (
    len(cs), sorted({k for _, k in cs}), len(own), sum(1 for s, _ in cs if I.func_of(s) is None),
    len(I.abs64_refs(0x002ED570, 0x002ED571))))
print("F1 004096C0:")
for i in I.dis(0x004096C0, 0x004096F0):
    print("   %08X %s" % (i.address, I.txt(i)))
    if i.mnemonic == "ret":
        break
for s, k in I.calls_to(0x0032EAE0):
    print("G1 0032EAE0 caller %08X %s, owner %08X" % (s, k, I.func_of(s) or 0))
rr = I.rip_refs(0x02B62E20, 0x02B62E40)
print("S10 rip refs into 02B62E20..02B62E3F: %d; owners %s" % (len(rr), sorted({"%08X" % (I.func_of(i.address) or 0) for i in rr})))
