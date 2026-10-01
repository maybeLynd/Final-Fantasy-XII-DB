"""RC-29: who walks the .rdata block 008FCE00..008FD2D0 (SWE2-DATA 2026-09-30), static on the certified image.

The owning pages read the block as a "menu resource manifest" of fourteen u32-2-tagged kind-7 id lists and record
"no rip-relative or pointer-table reference reaches the block". This script sweeps for every way code can address it:
  R1 raw rip-relative sweep of all .text (function-list independent, pe.raw_rip_refs)
  R2 raw image-base-relative sweep: every .text int32 in [0x7DCE00, 0x7DD2D0) (the block's RVA), decoded in place
  R3 qword VA pointers into the block anywhere in the file-backed image (pointer tables)
and then decodes the readers it finds: the block is 14 rows x 0x16 u32 (stride 0x58), row = [obj+0xA88], column 0..0x15,
each entry an item id handed to the item formatter 001CD0E0 (jump table on id-1, 0x126 arms) through the gate 001D0190.
Controls: R1 must re-find a known rip reader of a neighbouring constant (the '<Information Page>' string 008FF960 at
001D52BE); R2 must re-find a known image-base-relative jump-table base use (001CD1CB, disp 0xAFCEC) when swept over its
own RVA; the row decode must reproduce the 14-page count the reader hard-codes (mov [rbx+0xA88], 0xE / '<Page %d/%d>').
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, BASE, secs, owner, names, dis, ins_at, raw_rip_refs, text_range, containing_ins, cstr  # noqa

LO, HI = 0x008FCE00, 0x008FD2D0
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def raw_rva_refs(lo_rva, hi_rva):
    t0, t1, ro = text_range()
    blob = d[ro:ro + (t1 - t0)]
    out = set()
    for p in range(len(blob) - 4):
        v = struct.unpack_from("<I", blob, p)[0]
        if lo_rva <= v < hi_rva:
            x, how = containing_ins(t0 + p)
            if x is not None and ("0x%x" % v) in x.op_str:
                out.add((x.address, x.mnemonic, x.op_str, how))
    return sorted(out)


def qword_ptrs(lo, hi):
    hits = []
    for name, va, vs, ro, rs in secs:
        blob = d[ro:ro + rs]
        for p in range(0, len(blob) - 8, 8):
            q = struct.unpack_from("<Q", blob, p)[0]
            if lo <= q < hi:
                hits.append((BASE + va + p, name, q))
    return hits


# --- R1
r1 = raw_rip_refs(LO, HI)
print("R1 raw rip-relative references into %08X..%08X: %d" % (LO, HI, len(r1)))
for a, m, o, t in r1:
    print("   %08X %-6s %-40s -> %08X  in %s" % (a, m, o, t, "%08X" % owner(a) if owner(a) else "unlisted"))
ctl = raw_rip_refs(0x008FF960, 0x008FF961)
check("R1 control: raw rip sweep re-finds 001D52BE -> 008FF960 '<Information Page>'",
      any(a == 0x001D52BE for a, *_ in ctl), "%d hits" % len(ctl))

# --- R2
r2 = raw_rva_refs(LO - BASE, HI - BASE)
print("R2 image-base-relative int32 in [%X, %X): %d" % (LO - BASE, HI - BASE, len(r2)))
for a, m, o, how in r2:
    print("   %08X %-6s %-44s in %s (%s)" % (a, m, o, "%08X" % owner(a) if owner(a) else "-", how))
ctl2 = raw_rva_refs(0xAFCEC, 0xAFCED)
check("R2 control: the RVA sweep re-finds the 001CD0E0 jump-table base use at 001CD1CB (disp 0xAFCEC)",
      any(a == 0x001CD1CB for a, *_ in ctl2), "%d hits" % len(ctl2))

# --- R3
r3 = qword_ptrs(LO, HI)
print("R3 qword pointers into the block: %d" % len(r3))
for a, s, q in r3[:20]:
    print("   %08X (%s) -> %08X" % (a, s, q))

readers = sorted({owner(a) for a, *_ in r1} | {owner(a) for a, *_ in r2})
print("reader functions:", " ".join("%08X" % f for f in readers if f))
check("R: the block has readers (the page's 'no reference reaches the block' is refuted)", len(readers) >= 1)

# --- the reader's geometry: 001D5260 indexes [r14 + (row*0x16 + col)*4], col < 0x16
body = {x.address: x for x in dis(0x001D5260)}
geo = [body[a] for a in (0x001D53A9, 0x001D53B0, 0x001D540C, 0x001D536D) if a in body]
for x in geo:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
check("G1 row stride 0x16 u32 (imul ..,0x16) and column bound 0x16 in 001D5260",
      "0x16" in body[0x001D53A9].op_str and "0x16" in body[0x001D540C].op_str)
check("G2 the page count the reader hard-codes is 0xE (mov dword ptr [rbx + 0xa88], 0xe)",
      body[0x001D536D].op_str.endswith("0xe"))
rows = (HI - LO) // (0x16 * 4)
check("G3 block length = 14 rows x 0x58 bytes exactly", (HI - LO) == 14 * 0x58, "%d rows" % rows)
check("G4 the '<Page %%d/%%d>' header string sits beside the block's reader", cstr(0x008FF978).startswith("<Page %d/%d>"),
      repr(cstr(0x008FF978)))

# --- decode the rows
tab = [[struct.unpack_from("<I", d, off(LO) + (r * 0x16 + c) * 4)[0] for c in range(0x16)] for r in range(14)]
ids = set()
for r, row in enumerate(tab):
    nz = [v for v in row if v]
    ids.update(nz)
    print("   page %2d: %s" % (r + 1, " ".join(str(v) for v in row)))
check("D1 every non-zero entry is an item id inside the formatter's jump-table range 1..0x126",
      all(1 <= v <= 0x126 for v in ids), "max %d" % max(ids))
# the formatter: id-1 bounded by 0x125, table at image base + 0xAFCEC
fb = {x.address: x for x in dis(0x001CD0E0)}
check("D2 001CD0E0 switches on id-1 <= 0x125 (cmp eax, 0x125) and reads the row entry [rsi + rcx*4 + 0x7dce00]",
      fb[0x001CD1BE].op_str.endswith("0x125") and "0x7dce00" in fb[0x001CD186].op_str)

print("FAILS %d" % FAILS)
