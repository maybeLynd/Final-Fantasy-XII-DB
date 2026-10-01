"""atmospherics_ctor.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
PAtmosphericsBase's unregistered spans (+0x50, +0x62, +0xB0, +0xE4), from its constructor. The rows said only that no Phyre
reflection registration covers them; the constructor writes every one.

  C  00645520 = PAtmosphericsBase's constructor: 006461B0 (PPostEffectBase), then vtable 00D62800 (the class's, by the post-effect
     family table). Its stores: qwords +0x50 / +0x58 = 0; byte +0x62 = 0; dwords +0x64..+0x7C = 0x100, 0x40, 0x40, 0x10, 0x100,
     0x80, 0x20 and +0x80 = 2 (integer immediates); +0xB0..+0xBC = 32.0f, 128.0f, 32.0f, 8.0f; +0xE4 / +0xE8 / +0xEC = 128.0f,
     4.0f, 32.0f and qword +0xF0 = 4.0f with +0xF4 = 0; +0xF8 / +0x100 qwords, +0x108 dword, +0x110 qword, +0x118 dword and 45
     qwords +0x120..+0x280 = 0. +0x63, +0x10C and +0x11C are not written
  N  the family's 38 vtable bodies reach only +0x60 above the base (the post-effect family page, section 3d): these are
     constructor defaults with no reader in the class's own methods, so the float typing rests on the stored bit patterns
     (PROBABLE) and the integers on their immediates
  W  REGRESSION (FAILS before): the four spans are carved and the type's rows tile to 0x288
Not claimed: what the integers and floats parameterise.
Usage: python atmospherics_ctor.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
L = list(cs.disasm(d[off(0x645520):off(0x6457D2)], 0x645520))
A = {x.address: (x.mnemonic, x.op_str) for x in L}
st = {}
for x in L:
    if x.mnemonic == "mov" and "ptr [rbx + " in x.op_str.split(",")[0]:
        dst, src = x.op_str.split(", ")
        o = int(dst.split("+ ")[1].rstrip("]"), 16); w = {"qword": 8, "dword": 4, "word": 2, "byte": 1}[dst.split()[0]]
        v = 0 if src in ("rax", "eax", "ax", "al") else int(src, 16)
        for i in range(w): st[o + i] = (v >> (8 * i)) & 0xFF
def u32(o): return struct.unpack("<I", bytes(st[o + i] for i in range(4)))[0] if all(o + i in st for i in range(4)) else None
def f32(o): v = u32(o); return None if v is None else struct.unpack("<f", struct.pack("<I", v))[0]
zero = lambda a, b: all(st.get(o) == 0 for o in range(a, b))
check("C", A.get(0x645529) == ("call", "0x6461b0") and A.get(0x645538) == ("lea", "rax, [rip + 0x71d2c1]") and 0x64553F + 0x71D2C1 == 0xD62800
      and zero(0x50, 0x60) and st.get(0x62) == 0 and 0x63 not in st
      and [u32(o) for o in range(0x64, 0x84, 4)] == [0x100, 0x40, 0x40, 0x10, 0x100, 0x80, 0x20, 2]
      and [f32(o) for o in (0xB0, 0xB4, 0xB8, 0xBC)] == [32.0, 128.0, 32.0, 8.0]
      and [f32(o) for o in (0xE4, 0xE8, 0xEC, 0xF0)] == [128.0, 4.0, 32.0, 4.0] and u32(0xF4) == 0
      and zero(0xF8, 0x10C) and 0x10C not in st and zero(0x110, 0x11C) and 0x11C not in st and zero(0x120, 0x288) and 0x288 not in st,
      "00645520: the stores cover +0x50..+0x5F, +0x62, +0x64..+0x83, +0xB0..+0xBF, +0xE4..+0x10B, +0x110..+0x11B, +0x120..+0x287; +0x63 / +0x10C / +0x11C unwritten")
REC = "_index/candidates/phyre-motion-blur-opus/atmospherics_ctor.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
T = "PAtmosphericsBase"
U, M = ("DISCOVERED", "UNKNOWN"), ("TYPE RESOLVED", "PROBABLE")
CT = "stored by the constructor 00645520"
SPANS = {0x50: (16, [(0x50, 8, "qword50", "uint64", "zeroed; " + CT + "; no reader in the class's methods", U), (0x58, 8, "qword58", "uint64", "zeroed; " + CT, U)]),
         0x62: (34, [(0x62, 1, "byte62", "uint8", "zeroed; " + CT, U), (0x63, 1, "unobservedSpan0063", "u8[1]", "not written by the constructor", U)]
                   + [(o, 4, "dword%X" % o, "uint32", "%s; %s" % (v, CT), M) for o, v in zip(range(0x64, 0x84, 4), ("0x100", "0x40", "0x40", "0x10", "0x100", "0x80", "0x20", "2"))]),
         0xB0: (16, [(o, 4, "float%X" % o, "float", "%s; %s" % (v, CT), M) for o, v in zip(range(0xB0, 0xC0, 4), ("32.0", "128.0", "32.0", "8.0"))]),
         0xE4: (420, [(o, 4, "float%X" % o, "float", "%s; %s" % (v, CT), M) for o, v in zip(range(0xE4, 0xF4, 4), ("128.0", "4.0", "32.0", "4.0"))]
                   + [(0xF4, 4, "dwordF4", "uint32", "zeroed (the high half of the qword store that sets +0xF0); " + CT, U),
                      (0xF8, 8, "qwordF8", "uint64", "zeroed; " + CT, U), (0x100, 8, "qword100", "uint64", "zeroed; " + CT, U),
                      (0x108, 4, "dword108", "uint32", "zeroed; " + CT, U), (0x10C, 4, "unobservedSpan010C", "u8[4]", "not written by the constructor", U),
                      (0x110, 8, "qword110", "uint64", "zeroed; " + CT, U), (0x118, 4, "dword118", "uint32", "zeroed; " + CT, U),
                      (0x11C, 4, "unobservedSpan011C", "u8[4]", "not written by the constructor", U),
                      (0x120, 360, "qwords120", "uint64[45]", "45 qwords zeroed; " + CT, U)])}
tiles = all(sum(r[1] for r in rows) == n and all(a[0] + a[1] == b[0] for a, b in zip(rows, rows[1:])) and rows[0][0] == o for o, (n, rows) in SPANS.items())
FI = os.path.join(DB, "_types", "fields.tsv"); TYP = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    assert tiles
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []; hit = set()
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == T and int(c[1], 16) in SPANS and c[3].startswith("unobservedSpan") and int(c[2]) == SPANS[int(c[1], 16)][0]:
            was = "%s %s (%s)" % (c[3], c[4], c[5][:200])
            out += ["\t".join([T, "0x%03X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s C N). was %s. %s" % (REC, was, EXE)]) + e
                    for o, n, nm, ct, m, rd in SPANS[int(c[1], 16)][1]]; hit.add(int(c[1], 16)); continue
        out.append(l)
    assert hit == set(SPANS), hit
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TYP, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == T and not c[5]: c[5] = "00645520 (after 006461B0; installs 00D62800)"; tl[i] = "\t".join(c) + ee
    open(TYP, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
R = sorted((int(c[1], 16), int(c[2]), c[3]) for c in (cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()) if c[0] == T)
check("W", tiles and not any(nm in ("unobservedSpan0050", "unobservedSpan0062", "unobservedSpan00B0", "unobservedSpan00E4") for o, n, nm in R)
      and all(a[0] + a[1] == b[0] for a, b in zip(R, R[1:])) and R[-1][0] + R[-1][1] == 0x288, "the four spans are carved and the rows tile to 0x288")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
