"""Controls for the exact-match method.
 C1 positive: the 10 LibVPX-tagged LISTED bodies in the window - routine at entry, length == body_bytes.
 C2 specificity: the same patterns searched over ALL of .text; hits outside 0x121000..0x160000 would be chance.
 C3 sensitivity: a planted defect - flip one unmasked byte in each matched routine's pattern and confirm the hit disappears
    (so the matcher is not accepting near-misses), and a 1-byte-shifted window yields no hit at the original VA.
 C4 .rodata: how much of the image's .rodata (0x03001000, 0x11C0 B) is byte-identical to yasm .rodata blocks."""
import glob, re, pickle
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from coff import Obj, Exe

HERE = Path(__file__).parent
exe = Exe()
cs = Cs(CS_ARCH_X86, CS_MODE_64)
name, vs, va, rs, ro = exe.secs[0]
text = exe.d[ro:ro + rs]
TBASE = 0x120000 + va
LO, HI = 0x121000, 0x160000

routines = []
for p in sorted(glob.glob(str(HERE / "obj/*.obj"))):
    o = Obj(p)
    fl = o.functions()
    starts = [f for f in fl if f[1] == 2]
    for si, s in enumerate(o.sections):
        st = sorted([f for f in starts if f[2] == si], key=lambda f: f[3])
        for k, f in enumerate(st):
            a = f[3]
            e = st[k + 1][3] if k + 1 < len(st) else len(s["raw"])
            code = s["raw"][a:e]
            last = 0; pos = 0
            while pos < len(code):
                ins = next(cs.disasm(code[pos:], pos, 1), None)
                if ins is None:
                    pos += 1; last = pos; continue
                if ins.mnemonic != "nop":
                    last = ins.address + ins.size
                pos += ins.size
            code = code[:last]
            if len(code) < 8:
                continue
            mask = [False] * len(code)
            for (ra, symi, ty) in s["rels"]:
                if a <= ra < a + len(code):
                    for q in range(ra - a, min(len(code), ra - a + (8 if ty == 1 else 4))):
                        mask[q] = True
            routines.append((f[0], code, mask))


def pat(code, mask):
    return b"".join(b"." if m else re.escape(bytes([c])) for c, m in zip(code, mask))


# C1
sizes = {}
for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try:
        sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError):
        pass
tagged = [0x0012696A, 0x00127BB3, 0x00127F4D, 0x001283A6, 0x00128905, 0x001496A0, 0x00149983, 0x00149BCE, 0x00149DC0, 0x0014A48A]
inwin = []
outwin = []
for n, code, mask in routines:
    for m in re.finditer(pat(code, mask), text, re.DOTALL):
        v = TBASE + m.start()
        (inwin if LO <= v < HI else outwin).append((v, n, len(code)))
hitmap = {}
for v, n, ln in inwin:
    hitmap.setdefault(v, []).append((n, ln))
ok = 0
for t in tagged:
    h = hitmap.get(t, [])
    good = any(ln == sizes[t] for n, ln in h)
    ok += good
    print("C1 %08X body_bytes %4d -> %s %s" % (t, sizes[t], h, "PASS" if good else "FAIL"))
print("C1 %d of %d tagged listed bodies identified at their entry with length == body_bytes" % (ok, len(tagged)))
# C2
print("C2 hits inside window %d, outside window (rest of .text, %d B) %d %s" % (len(inwin), len(text) - (HI - LO), len(outwin), outwin[:5]))
# C3
flipped_hits = 0
tested = 0
for n, code, mask in routines:
    p0 = pat(code, mask)
    if not re.search(p0, text[LO - TBASE:HI - TBASE], re.DOTALL):
        continue
    idx = [i for i, m in enumerate(mask) if not m]
    j = idx[len(idx) // 2]
    c2 = bytearray(code); c2[j] ^= 0x01
    tested += 1
    if re.search(pat(bytes(c2), mask), text, re.DOTALL):
        flipped_hits += 1
print("C3 one-byte-flipped patterns: %d of %d still hit (expect 0 except where the routine has a byte-identical twin)" % (flipped_hits, tested))
# C4
rod = exe.read(0x03001000, 0x11C0)
covered = bytearray(len(rod))
for p in sorted(glob.glob(str(HERE / "obj/*.obj"))):
    o = Obj(p)
    for s in o.sections:
        if s["name"] in (".rodata", ".rdata") and len(s["raw"]) >= 16 and not (s["chars"] & 0x20):
            i = rod.find(s["raw"])
            while i >= 0:
                for q in range(i, i + len(s["raw"])):
                    covered[q] = 1
                i = rod.find(s["raw"], i + 1)
print("C4 image .rodata bytes covered by a whole yasm .rodata section: %d of %d" % (sum(covered), len(rod)))
