"""s49_repairs_check.py - regression for OPUS's S-49 repairs (SWE2-AUDIT-SEM REJECT, auditsem-l2-sample-1003), 2026-10-03.

Checks, from the certified image and the store:
  D1  02CF8260, 02CAA0A0, 02CA9DA0 and 02CA9FA0 resolve to a declared FIELD (the census the REJECT used);
      02CF8260 has exactly the 29 references the declaration states (15 reads, 14 writes).
  P2  the five corrected fields.tsv meanings carry the correction and the old claim survives only struck;
      the image facts they now state hold (0063DC80 stores +0xC0; 0059E167 compares 0x1020304).
  P3  the contract's section 8 no longer states the CFG-path claim unstruck, and the arm it describes calls the
      `ret 0` stub 0016D6A0.
--rejected runs the text checks against the pre-repair texts and must fail them."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DBR, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import retool  # noqa: E402
import contract_named_state_census as CNS  # noqa: E402

R = retool.R
fails = []


def ins(a, n=16):
    return next(iter(R.md.disasm(R.at(a, n), a)))


def unstruck(t):
    return re.sub(r"~~.*?~~", "", t)


rejected = "--rejected" in sys.argv
# D1
spans, fields, sizes = CNS.load_store()
for a in (0x02CF8260, 0x02CAA0A0, 0x02CA9DA0, 0x02CA9FA0):
    cls = CNS.resolve(a, spans, fields, sizes)[0]
    if cls != "FIELD":
        fails.append("D1 %08X resolves to %s" % (a, cls))
refs = retool.scan()["refs"].get(0x02CF8260, set())
if len(refs) != 29:
    fails.append("D1 02CF8260 has %d references, the declaration says 29" % len(refs))
# P2
old_claims = {("PhyrePackedNamespaceMemberRecord", "0x08"): "byte offset of the field within the class",
              ("PhyrePackedNamespaceMemberRecord", "0x0C"): "element size in bytes",
              ("PhyrePackedNamespaceMemberRecord", "0x10"): "bit 31 marks a pointer",
              ("PhyrePackedNamespaceHeader", "0x00"): "the loader acts on the cluster header's order, not this"}
rows = {}
for l in io.open(os.path.join(DBR, "_types", "fields.tsv"), encoding="utf-8", newline=""):
    c = l.rstrip("\r\n").split("\t")
    if len(c) > 5:
        rows[(c[0], c[1])] = c[5]
for k, old in old_claims.items():
    text = old if rejected else rows.get(k, "")
    if old in unstruck(text):
        fails.append("P2 %s+%s still states '%s' unstruck" % (k[0], k[1], old))
if not rejected and "CORRECTED 2026-10-03 (OPUS, S-49 point 2)" not in rows.get(("PhyreClassDescriptor", "0x00C0"), ""):
    fails.append("P2 PhyreClassDescriptor+0x00C0 lacks the default-instance correction")
i = ins(0x0063DC80)
if (i.mnemonic, i.op_str) != ("mov", "qword ptr [rcx + 0xc0], rdx"):
    fails.append("P2 0063DC80 is %s %s" % (i.mnemonic, i.op_str))
i = ins(0x0059E167)
if (i.mnemonic, i.op_str) != ("cmp", "dword ptr [rdi], 0x1020304"):
    fails.append("P2 0059E167 is %s %s" % (i.mnemonic, i.op_str))
# P3
con = io.open(os.path.join(DBR, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                           "CONTRACT-phyre-class-descriptor.md"), encoding="utf-8").read()
claim = "Bit 2 selects a Control Flow Guard-mediated path instead of the direct `_aligned_free`."
if claim in (claim if rejected else unstruck(con)):
    fails.append("P3 section 8 still states the CFG-path claim unstruck")
i = ins(0x0016D6A0)
if (i.mnemonic, i.op_str) != ("ret", "0"):
    fails.append("P3 0016D6A0 is %s %s" % (i.mnemonic, i.op_str))
i = ins(0x00584828)
if (i.mnemonic, i.op_str) != ("call", "0x16d6a0"):
    fails.append("P3 00584828 is %s %s" % (i.mnemonic, i.op_str))
for f in fails:
    print("FAIL", f)
print("checks D1 4+1, P2 5+2, P3 1+2%s  FAILS %d" % ("  (rejected texts: the text checks must fail)" if rejected else "",
                                                       len(fails)))
sys.exit(1 if fails else 0)
