"""Exact byte match (relocations masked) of every libvpx 1.6.0 x86 asm routine (yasm win64) against the image
window 0x121000..0x160000. Writes asm_hits_ext.tsv: image_va, routine, obj, len, masked_bytes, reloc checks."""
import glob, re, sys, pickle
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from coff import Obj, Exe, BASE

HERE = Path(__file__).parent
exe = Exe()
LO, HI = 0x121000, 0x160000
win = exe.read(LO, HI - LO)
cs = Cs(CS_ARCH_X86, CS_MODE_64)

routines = []
for p in sorted(glob.glob(str(HERE / "obj/*.obj"))):
    o = Obj(p)
    fl = o.functions()
    # routine starts: external, or static without a dot
    starts = [f for f in fl if f[1] == 2]
    for si, s in enumerate(o.sections):
        st = sorted([f for f in starts if f[2] == si], key=lambda f: f[3])
        for k, f in enumerate(st):
            a = f[3]
            e = st[k + 1][3] if k + 1 < len(st) else len(s["raw"])
            code = s["raw"][a:e]
            # trim trailing nop padding
            last = 0
            pos = 0
            while pos < len(code):
                ins = next(cs.disasm(code[pos:], pos, 1), None)
                if ins is None:
                    pos += 1; last = pos; continue
                if ins.mnemonic not in ("nop",):
                    last = ins.address + ins.size
                pos += ins.size
            code = code[:last]
            if len(code) < 8:
                continue
            mask = [False] * len(code)
            rel = []
            for (ra, symi, ty) in s["rels"]:
                if a <= ra < a + len(code):
                    w = 8 if ty == 1 else 4
                    for q in range(ra - a, min(len(code), ra - a + w)):
                        mask[q] = True
                    sym = o.syms.get(symi, {})
                    rel.append((ra - a, ty, sym.get("name"), sym.get("sec"), sym.get("value")))
            routines.append(dict(name=f[0], obj=Path(p).stem, code=code, mask=mask, rel=rel, o=o))

print("routines", len(routines), file=sys.stderr)
hits = []
for r in routines:
    pat = b"".join(b"." if m else re.escape(bytes([c])) for c, m in zip(r["code"], r["mask"]))
    for m in re.finditer(pat, win, re.DOTALL):
        va = LO + m.start()
        # check relocations: for REL32 to a data section symbol, compare constant bytes
        chk = []
        for (ro, ty, sname, ssec, sval) in r["rel"]:
            if ty == 4:  # IMAGE_REL_AMD64_REL32
                disp = int.from_bytes(win[m.start() + ro:m.start() + ro + 4], "little", signed=True)
                tgt = va + ro + 4 + disp
                # addend in obj
                add = int.from_bytes(r["code"][ro:ro + 4], "little", signed=True)
                o = r["o"]
                if ssec and ssec > 0:
                    sec = o.sections[ssec - 1]
                    so = (sval or 0) + add
                    ref = sec["raw"][so:so + 16]
                    img = exe.read(tgt, len(ref)) or b""
                    chk.append((tgt, sec["name"], ref == img))
                else:
                    chk.append((tgt, "ext:" + str(sname), None))
        hits.append((va, r["name"], r["obj"], len(r["code"]), sum(r["mask"]), chk))

hits.sort()
with open(HERE / "asm_hits_ext.tsv", "w") as f:
    f.write("va\troutine\tobj\tlen\tmasked\tconst_checks\n")
    for va, n, ob, ln, mk, chk in hits:
        cc = ";".join("%08X:%s:%s" % (t, s, {True: "eq", False: "NE", None: "-"}[e]) for t, s, e in chk)
        f.write("%08X\t%s\t%s\t%d\t%d\t%s\n" % (va, n, ob, ln, mk, cc))
print("hits", len(hits), file=sys.stderr)
pickle.dump([(h[0], h[1], h[2], h[3], h[4], h[5]) for h in hits], open(HERE / "asm_hits_ext.pkl", "wb"))
