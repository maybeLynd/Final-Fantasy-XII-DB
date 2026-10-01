"""builder_store_extents.py - the publishable census: every hub call (object, builder), the three helpers it calls,
immediate/register store counts, store extent, gap to the next object, memset size; header words the helper-free
builders write at +8/+0xC/+0x18/+0x1C/+0x20. Writes builder-store-extents.tsv beside this script.
Band = 00480000-004FFFFF (the page's 66). Needs builder_store_census.py in the same directory (FABLE, 2026-09-17).

memset_size is the r8d immediate of the LAST memset call in the body only; three builders call memset on interior
sub-buffers (see section 11's correction), so read it with the store extent, never instead of it."""
import sys, os, io, collections
sys.argv = [sys.argv[0]]
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
import contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import builder_store_census as B
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
OUT = os.path.join(S, "builder-store-extents.tsv")
rows = B.rows
objs = sorted(o for _, o, *_ in rows if o)
gap = {o: (objs[i + 1] - o if i + 1 < len(objs) else None) for i, o in enumerate(objs)}
def details(b):
    imm = reg = 0; hdr = {}; memset = None
    xs = B.ins(b)
    for i, x in enumerate(xs):
        if x.mnemonic.startswith("mov") and x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base and B.md.reg_name(x.operands[0].mem.base) != "rip":
            src = x.operands[1]
            if src.type == X86_OP_IMM: imm += 1
            else: reg += 1
            o = x.operands[0].mem.disp
            if o in (8, 0xC, 0x18, 0x1C, 0x20) and src.type == X86_OP_IMM and o not in hdr:
                hdr[o] = src.imm
        if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x861EC0:
            for y in reversed(xs[max(0, i - 8):i]):
                if y.mnemonic == "mov" and y.operands[0].type == X86_OP_REG and B.md.reg_name(y.operands[0].reg) == "r8d" and y.operands[1].type == X86_OP_IMM:
                    memset = y.operands[1].imm; break
    return imm, reg, hdr, memset
out = ["hub\tobject\tbuilder\tbuilder_bytes\thelpers\timm_stores\treg_stores\tstore_extent\tgap_to_next\tmemset_size_last_call\tband\tw8\twC\tw18\tw1C\tw20"]
hdrs = collections.Counter(); band48 = []; helperfree = []
for hub, obj, b, sz, h, others, nrel, ext, nabs, st in sorted(rows, key=lambda r: (r[0], r[1] or 0)):
    imm, reg, hdr, ms = details(b)
    band = 0x480000 <= b < 0x500000
    g = gap.get(obj)
    out.append("%08X\t%08X\t%08X\t%d\t%s\t%d\t%d\t0x%X\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s" % (
        hub, obj or 0, b, sz, "+".join(h) or "-", imm, reg, ext, ("0x%X" % g) if g else "-", ("0x%X" % ms) if ms else "-", 1 if band else 0,
        *[("0x%x" % hdr[k]) if k in hdr else "-" for k in (8, 0xC, 0x18, 0x1C, 0x20)]))
    if not h:
        helperfree.append((b, obj, hdr, ext, g, sz, imm, reg))
        hdrs[tuple((k, hdr.get(k)) for k in (8, 0xC, 0x18))] += 1
    if band and "memset" not in h and g is not None:
        band48.append((obj, b, ext, g))
io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("wrote", OUT, len(out) - 1, "rows")
print("helper-free builders:", len(helperfree), " of which in band:", sum(1 for b, *_ in helperfree if 0x480000 <= b < 0x500000))
print("their (+8, +0xC, +0x18) immediates:", dict(hdrs))
print("their +0x1C words:", sorted({"0x%x" % h.get(0x1C, 0) for _, _, h, *_ in helperfree}))
print("their +0x20 words:", sorted({"0x%x" % h.get(0x20, 0) for _, _, h, *_ in helperfree}))
print("band objects with no memset and a gap:", len(band48), " exact (extent == gap):", sum(1 for o, b, e, g in band48 if e == g), " below:", [("%08X" % o, "0x%X" % e, "0x%X" % g) for o, b, e, g in band48 if e < g])
tot = [r for r in rows if r[1] and gap.get(r[1]) is not None]
print("all objects with a gap:", len(tot), " exact:", sum(1 for r in tot if r[7] == gap[r[1]]), " above:", sum(1 for r in tot if r[7] > gap[r[1]]))
