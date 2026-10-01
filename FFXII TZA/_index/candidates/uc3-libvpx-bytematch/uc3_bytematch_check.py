"""uc3_bytematch_check.py OBJ_DIR - FABLE's independent spot check of the UC-3 byte match (FABLE, Claude Opus 5.5, 2026-09-27).
Own COFF reader (not coff.py); for 15 routines (7 chosen, 8 seeded-random) the instruction text of the yasm .obj routine is
compared with the image at the VA uc3-blocks.tsv claims, allowing only rip-relative displacement differences.
Null: the same routines compared 0x40 bytes later must score near 0. OBJ_DIR = the yasm -f win64 objects of libvpx v1.6.0
(asm_all.sh; obj-manifest.sha256 pins them). Exit 1 on any mismatch or a null above 0.2."""
import struct, glob, re, sys, random
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from pathlib import Path
HERE = Path(__file__).resolve().parent
EXE = HERE.parents[3] / "Tools/work/exe/FFXII_TZA.exe"
OBJ = sys.argv[1]
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(n):
    b = pe + 24 + opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
print("sections:", [(s[0], "%08X" % (0x120000 + s[2])) for s in SECS])
def off(v):
    for _, vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
def coff(p):
    b = open(p, "rb").read()
    nsec, _, symp, nsym = struct.unpack_from("<HHIII", b, 2)[0], None, struct.unpack_from("<I", b, 8)[0], struct.unpack_from("<I", b, 12)[0]
    nsec = struct.unpack_from("<H", b, 2)[0]; optsz = struct.unpack_from("<H", b, 16)[0]
    secs = []
    for i in range(nsec):
        h = 20 + optsz + i * 40
        name = b[h:h + 8].rstrip(b"\0").decode(errors="replace")
        size, ptr = struct.unpack_from("<II", b, h + 16)
        secs.append((name, b[ptr:ptr + size]))
    strt = symp + nsym * 18
    syms = []; i = 0
    while i < nsym:
        e = symp + i * 18
        nm = b[e:e + 8]
        if nm[:4] == b"\0\0\0\0":
            o = struct.unpack_from("<I", nm, 4)[0]; name = b[strt + o:b.index(b"\0", strt + o)].decode()
        else: name = nm.rstrip(b"\0").decode(errors="replace")
        val, sec = struct.unpack_from("<Ih", b, e + 8); cls = b[e + 16]; aux = b[e + 17]
        if sec > 0 and cls in (2, 3) and "." not in name and not name.startswith("$"): syms.append((name, sec - 1, val))
        i += 1 + aux
    return secs, syms
ROUT = {}
for p in glob.glob(OBJ + "/*.obj"):
    secs, syms = coff(p)
    for si, (sn, raw) in enumerate(secs):
        if not sn.startswith(".text"): continue
        st = sorted(s for s in syms if s[1] == si)
        st = sorted(st, key=lambda s: s[2])
        for k, (nm, _, a) in enumerate(st):
            e = st[k + 1][2] if k + 1 < len(st) else len(raw)
            ROUT.setdefault(nm, (raw, a))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def norm(code, base):
    out = []
    for x in cs.disasm(code, base):
        if x.mnemonic == "nop" or (x.mnemonic == "int3"): continue
        t = x.mnemonic + " " + re.sub(r"\[rip(?: [+-] 0x[0-9a-f]+)?\]", "[rip+R]", x.op_str)
        t = re.sub(r"0x[0-9a-f]{5,}", "ADDR", t) if x.mnemonic in ("call", "jmp") or x.mnemonic.startswith("j") else t
        out.append((x.address - base, t))
    return out
claims = {}
for l in open(HERE / "uc3-blocks.tsv", encoding="utf-8"):
    for m in re.finditer(r"(v\w+) @([0-9A-F]{8}) (\d+)B", l): claims[m.group(1)] = (int(m.group(2), 16), int(m.group(3)))
print("claimed routines:", len(claims), "routines in objs:", len(ROUT))
random.seed(27)
pick = ["vp8_short_idct4x4llm_mmx", "vpx_idct32x32_1024_add_ssse3", "vpx_quantize_b_avx", "vpx_sad64x64x4d_sse2",
        "vp8_variance_and_sad_16x16_sse2", "vpx_winx64_fldcw", "vpx_sub_pixel_variance16xh_sse2"] + random.sample(sorted(claims), 8)
bad = 0
for nm in pick:
    va, ln = claims[nm]; r = ROUT.get(nm)
    if r is None: print("NO OBJ", nm); bad += 1; continue
    code = r[0][r[1]:r[1] + ln]
    a = norm(code, 0); o = off(va); b = norm(d[o:o + len(code)], 0)
    same = sum(1 for x, y in zip(a, b) if x == y)
    ok = same == len(a) and len(a) > 0
    bad += not ok
    print("%-40s %08X obj %5dB  %4d/%4d instr identical %s" % (nm, va, len(code), same, len(a), "OK" if ok else "MISMATCH"))
# null: the same routines at a shifted address
null = 0
for nm in pick[:8]:
    va, ln = claims[nm]; r = ROUT[nm]; code = r[0][r[1]:r[1] + ln]; a = norm(code, 0); o = off(va + 0x40)
    b = norm(d[o:o + len(code)], 0); null = max(null, sum(1 for x, y in zip(a, b) if x == y) / max(1, len(a)))
print("null (shifted +0x40) best fraction identical: %.2f" % null)
print("BAD", bad)
sys.exit(1 if bad or null > 0.2 else 0)
