"""Check for the flow-aware CharacterRenderRecord census and the re-cuts it supports (OPUS, 2026-09-27, BT-2).
Runs crr_flow_census (about a minute) and checks:
  P1 positive control: 002EDF90's four literal +0x6C8 stores (002EDFF9, 002EE00C, 002EE025, 002EE038) are found
  P2 every recorded field lies inside the 0x740-byte record
  N1 +0x5F5 / +0x5F6: 0046CDC3 word write at +0x5F5, 0046CDC9 byte read +0x5F6, 0046CDD1 byte read +0x5F5; and the
     receiver chain in bytes - 0046CBB0 forms the record from the pool (0046CBD3 imul rcx, rax, 0x740; 0046CBDC add rcx,
     [022C6F28]), adds 0x5F0 (0046CBF2) and calls 0046CC70 (0046CC01)
  N2 entries 1 and 4 of the channel array are written whole: 003E5D30 stores qword 0x1000 at +0x4C0 / +0x4C8 / +0x4E0
  S  the store declares +0x5F5, +0x5F6, +0x4CE, +0x4D6, +0x4DE, +0x4E6 with widths 1 / 1 / 2 / 2 / 2 / 2 and none is
     DISCOVERED (FAILS on the store before the re-cut)
Writes the census rows to a temporary file by default; only with --receipt to crr-flow-accesses.tsv beside this file
(the tracked receipt). A review re-run must NOT pass --receipt (2026-09-28, OPUS: the same rule the type-flow checks
follow, after review re-runs overwrote published receipts there).
Usage: python crr_flow_check.py [exe] [functions.tsv] [fields.tsv] [--receipt]
"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
RECEIPT = "--receipt" in sys.argv
if RECEIPT: sys.argv.remove("--receipt")
EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
FIELDS = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("FIELDS_PATH") or "FFXII TZA/_types/fields.tsv"
OUTP = (os.path.join(HERE, "crr-flow-accesses.tsv") if RECEIPT
        else os.path.join(tempfile.mkdtemp(prefix="crr_"), "crr-flow-accesses.tsv"))
sys.argv = [sys.argv[0], EXE, FUN, OUTP]
sys.path.insert(0, HERE)
import crr_flow_census as C
rows = C.main()
by = {}
for f, a, fld, w, k, ins in rows: by.setdefault(a, []).append((fld, w, k))
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


check("P1 002EDF90's literal +0x6C8 stores", all((0x6C8, 4, "w") in by.get(a, []) for a in (0x2EDFF9, 0x2EE00C, 0x2EE025, 0x2EE038)))
check("P2 every field inside the record", all(0 <= r[2] < 0x740 for r in rows), "(%d rows)" % len(rows))
n1 = (0x5F5, 2, "w") in by.get(0x46CDC3, []) and (0x5F6, 1, "r") in by.get(0x46CDC9, []) and (0x5F5, 1, "r") in by.get(0x46CDD1, [])
ins = {x.address: (x.mnemonic, x.op_str) for x in C.body(0x46CBB0)}
n1 &= ins.get(0x46CBD3) == ("imul", "rcx, rax, 0x740") and ins.get(0x46CBDC, ("", ""))[1].startswith("rcx, qword ptr [rip + ") \
      and ins.get(0x46CBF2) == ("add", "rcx, 0x5f0") and ins.get(0x46CC01) == ("call", "0x46cc70")
check("N1 +0x5F5 / +0x5F6 through record + 0x5F0", n1)
i2 = {x.address: (x.mnemonic, x.op_str) for x in C.body(0x3E5D30)}
check("N2 003E5D30 writes channel entries 0, 1 and 4 whole", [i2.get(a) for a in (0x3E5D30, 0x3E5D3B, 0x3E5D46)] ==
      [("mov", "qword ptr [rcx + 0x4c0], 0x1000"), ("mov", "qword ptr [rcx + 0x4c8], 0x1000"), ("mov", "qword ptr [rcx + 0x4e0], 0x1000")])
st = {}
for l in open(FIELDS, encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "CharacterRenderRecord": st[int(c[1], 16)] = c
want = {0x5F5: "1", 0x5F6: "1", 0x4CE: "2", 0x4D6: "2", 0x4DE: "2", 0x4E6: "2"}
check("S the store's re-cut rows", all(o in st and st[o][2] == w and st[o][6] != "DISCOVERED" for o, w in want.items()))
print("FAILS", fails); sys.exit(1 if fails else 0)
