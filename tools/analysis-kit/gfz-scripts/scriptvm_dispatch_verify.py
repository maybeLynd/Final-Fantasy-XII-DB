#!/usr/bin/env python3
"""scriptvm_dispatch_verify.py - re-derive the script verb -> handler column from the binary.

`01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv` maps 1,224 script call ids to the
native function that runs them. It is the script-to-engine bridge, and it arrived in the database
from a prior extraction that lived in a **gitignored scratch directory**.

This re-reads the dispatch table at stride 0x20 from VA 01EED720 for each call id in the file, and
compares.

CORRECTED 2026-09-16 (FABLE), on OPUS-CONTRA-DISPATCH-TABLE-HEADER-LINES-STILL-OLD-FRAME. The value
this reads is RIGHT and the LABEL was wrong. The table base is 01EED700 - count at +0, record 0 at
+8 - so 01EED720 is tbl+0x20 and `01EED720 + 0x20*id` is tbl+32+32*id, which is exactly what
VMNativeCommandDispatch_GetResultCallback (003DC2A0: inc rax / shl rax,5 / mov rax,[rax+rcx]) reads.
In the record's own frame that slot is +0x18, NOT +0x00. Every figure this tool has ever printed
stands; it was verifying the RESULT callback column and calling it the +0x00 one. BASE is left
numerically unchanged so nothing downstream shifts. It also checks every handler lands inside `.text` and on a known function
entry, so a spurious mapping cannot pass by looking numeric.

**Only the `handler` column is verifiable here.** `verb` and `args` come from an authored external
catalog and `owner` from the GFZ ledger; the file says so per column, and so does this tool by not
touching them.
"""
import io, struct, sys
sys.path.insert(0, r"C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos-XIIOnline\862388d6-126d-4d2f-ae78-c9bed3a0394d\scratchpad")
from xdis import load, rd
import kit_paths as KP  # noqa: E402
import os
EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
TSV = os.path.join(KP.ROOT, "Database", "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-dispatch.tsv")
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
# 0x01EED720 is tbl+0x20, the RESULT callback of record 0 - see the docstring. Left as it is
# because the arithmetic is correct and a downstream consumer reads these figures.
BASE, STRIDE = 0x01EED720, 0x20
# THE OTHER TWO COLUMNS ARE ALSO DERIVED NOW, and this script does not write them. `begin_handler`
# and `poll_handler` in scriptvm-dispatch.tsv were re-framed on 2026-09-19 (OPUS) to
#     begin(n) = [01EED700 + 8 + 0x20n + 0x00]     poll(n) = [01EED700 + 8 + 0x20n + 0x08]
# after FABLE measured them one call id early - they had been extracted in the old record frame.
# A regeneration that rewrites only the handler column is safe; one that rebuilds the whole file
# must read those two the same way, or the shift comes back.
d, b, secs = load(EXE)
entries = set()
f = io.open(FUNCS, encoding="utf-8", errors="replace"); f.readline()
for line in f:
    p = line.rstrip("\n").split("\t")
    if len(p) > 1 and not p[1].startswith(("Unwind@", "Catch_All@")):
        try: entries.add(int(p[0], 16))
        except ValueError: pass
text_lo, text_hi = None, None
for nm, sva, vs, ra, rs in secs:
    if nm == ".text":
        text_lo, text_hi = b + sva, b + sva + vs
rows = [l.split("\t") for l in io.open(TSV, encoding="utf-8").read().splitlines()
        if l.strip() and not l.startswith("#") and not l.startswith("call_id")]
agree = disagree = offtext = notentry = 0
bad = []
for r in rows:
    cid = int(r[0], 16); want = int(r[3], 16)
    raw = rd(d, b, secs, BASE + STRIDE * cid, 8, raw_only=True)
    got = struct.unpack("<Q", raw)[0] if raw else None
    if got == want: agree += 1
    else:
        disagree += 1
        if len(bad) < 6: bad.append((r[0], r[1], "%08X" % want, ("%016X" % got) if got else "None"))
    if not (text_lo <= want < text_hi): offtext += 1
    if want not in entries: notentry += 1
print("rows in the prior TSV                     : %d" % len(rows))
print("handler == RESULT callback at base+0x20*id: %d agree, %d disagree" % (agree, disagree))
print("handlers outside .text                    : %d" % offtext)
print("handlers that are not a known function entry : %d" % notentry)
for x in bad: print("   MISMATCH id=%s verb=%s tsv=%s image=%s" % x)
