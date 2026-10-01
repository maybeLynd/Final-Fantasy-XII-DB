"""SWE2-AUDIT-SPEC: who references the glyph packet ring and the kick cell (SD-102 modding sentence).
C1 the ring descriptors 02EBEFC0..02EBEFF4 (two 24-byte rows + index 02EBEFF0), rip-relative and image-base-relative
C2 the kick cell 02EBA3F8..02EBA404, rip-relative and image-base-relative
Control: C1 must list 002DAF30 (the emitter opens its chunk from the ring) and 003A1DB0 (the kick flips the index).
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
for tag, lo, hi in (("C1 ring", 0x02EBEFC0, 0x02EBEFF4), ("C2 kick cell", 0x02EBA3F8, 0x02EBA404)):
    refs, raw = tk.rip_refs(lo, hi)
    owners = {}
    for x, k, tgt in refs:
        w = "W" if tk.is_store(x, k) else "R"
        owners.setdefault(tk.fname(x.address), []).append("%08X%s->%08X" % (x.address, w, tgt))
    print("%s rip refs %d, raw-only %d, owners %d" % (tag, len(refs), len(raw), len(owners)))
    for o in sorted(owners):
        print("   %s: %s" % (o, " ".join(owners[o][:6]) + (" ..." if len(owners[o]) > 6 else "")))
    # image-base-relative form: [reg + (VA - 0x120000)] with reg = image base; also absolute-VA disp32
    for form, a, b in (("RVA-disp", lo - tk.BASE, hi - tk.BASE), ("VA-disp", lo, hi)):
        dr, draw = tk.disp_refs(a, b)
        print("%s %s refs %d (raw-only %d): %s" % (tag, form, len(dr), len(draw),
              " ".join("%08X %s" % (x.address, tk.fname(x.address)) for x, k, v in dr[:6])))
