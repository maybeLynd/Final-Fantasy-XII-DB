"""Falsification pass 1 on CONTRACT-spatial-source-objects (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  P0  section 2: each vtable's slot 34 and slot 39 are the cited bodies and stubs; the slot-34 sizes are 33 / 35 / 497 / 742 /
      2,115 B, and each equals the body's .pdata chain union (or the body has no .pdata entry)
  P1  SA-1: every slot-34 body stores to [rcx|rdi|rbx + 0xD0 .. 0xDC] and to +0xE0
  P2  SA-2: 007F1D12 stores +0xDC = 0x3F800000; 007F1F80 loads +0x100 and 007F1F89 `movdqa` stores all 16 bytes at +0xD0,
      then 007F1F91 overwrites +0xDC with 0x3F800000
  P3  SA-3: +0xE0 = 1 unconditionally at 007F1D29 and 007F1F9B; Point, Dynamic and Polygon write it from a compare against +0xE4
  P4  SA-4: among the five bodies +0xE4 is written only by DynamicSound, at 007F13EC
  P5  SA-5: SoundObject's vtable 01CBAB68 holds 0 at slot 34
  P6  SA-6: 007E5800 is `mov al, 1; ret`, 007E57B0 `xor al, al; ret`; slot 39 is the true stub for Point / Dynamic / Polygon and
      the false stub for Ambient / Direction; slot 36 of Ambient and Direction is one of the same two stubs
  P7  SA-7: the functions containing sqrtps / rsqrtps number 12, all inside 007EF1E0..007F74E0
  P8  section 10: PolygonSound writes +0xE0 = 0 at 007F2DF9 and returns -1; the computed path returns 0 (007F2DF5)
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
pd = next(x for x in SECS if x[0] == ".pdata"); praw = blob[pd[3]:pd[3] + pd[4]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    if b_:
        pent[BASE + b_] = (BASE + e_, BASE + u_)


def root(bg):
    seen = set()
    while bg in pent and bg not in seen:
        seen.add(bg); u = pent[bg][1]; h = blob[OFF(u):OFF(u) + 4]
        if not (h[0] >> 3) & 4:
            return bg
        c = OFF(u) + 4 + 2 * ((h[2] + 1) & ~1); bg = BASE + struct.unpack("<I", blob[c:c + 4])[0]
    return bg


def union(fa):
    fr = [(b_, pent[b_][0]) for b_ in pent if fa <= b_ < fa + 0x2000 and root(b_) == fa]
    return (max(e for _, e in fr) - fa) if fr else None


CL = {"Ambient": (0x01CB9C88, 0x007F1D10, 33, 0x007E57B0), "Direction": (0x01CB9DD0, 0x007F1F80, 35, 0x007E57B0),
      "Point": (0x01CB9B40, 0x007F1A50, 497, 0x007E5800), "Dynamic": (0x01CB99F0, 0x007F1340, 742, 0x007E5800),
      "Polygon": (0x01CB9F18, 0x007F25E0, 2115, 0x007E5800)}
got = {k: (q(v[0] + 34 * 8), q(v[0] + 39 * 8)) for k, v in CL.items()}
un = {k: union(v[1]) for k, v in CL.items()}
check("P0", all(got[k] == (v[1], v[3]) and sizes[v[1]] == v[2] and un[k] in (None, v[2]) for k, v in CL.items()),
      "slot 34 / 39 %s; sizes %s; chain unions %s" % ({k: ("%08X" % a, "%08X" % b_) for k, (a, b_) in got.items()}, {k: sizes[v[1]] for k, v in CL.items()}, un))
bodies = {k: {x.address: x for x in md.disasm(blob[OFF(v[1]):OFF(v[1]) + sizes[v[1]]], v[1])} for k, v in CL.items()}


def stores(I, lo, hi):
    return sorted(a for a, x in I.items() if x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith(("mov", "set"))
                  and x.reg_name(x.operands[0].mem.base) not in ("rsp", "rip") and lo <= x.operands[0].mem.disp < hi)


pos = {k: stores(I, 0xD0, 0xE0) for k, I in bodies.items()}
e0 = {k: stores(I, 0xE0, 0xE1) for k, I in bodies.items()}
check("P1", all(pos[k] and e0[k] for k in CL), "position stores %s; +0xE0 stores %s" % ({k: len(v) for k, v in pos.items()}, {k: ["%08X" % a for a in v] for k, v in e0.items()}))
A, D = bodies["Ambient"], bodies["Direction"]
at = lambda I, a: S(I[a]) if a in I else "?"
check("P2", at(A, 0x007F1D12).endswith("0x3f800000") and "+ 0xdc]" in at(A, 0x007F1D12) and at(D, 0x007F1F80) == "movaps xmm0, xmmword ptr [rcx + 0x100]" and at(D, 0x007F1F89) == "movdqa xmmword ptr [rcx + 0xd0], xmm0"
      and at(D, 0x007F1F91).endswith("0x3f800000") and "+ 0xdc]" in at(D, 0x007F1F91), "%s | %s | %s" % (at(A, 0x007F1D12), at(D, 0x007F1F89), at(D, 0x007F1F91)))
geo = {k: any(x.mnemonic in ("comiss", "ucomiss", "cmpltps", "cmpps", "minss") and "0xe4]" in x.op_str for x in bodies[k].values())
          or any("0xe4]" in x.op_str for x in bodies[k].values()) for k in ("Point", "Dynamic", "Polygon")}
check("P3", at(A, 0x007F1D29) == "mov byte ptr [rcx + 0xe0], 1" and at(D, 0x007F1F9B) == "mov byte ptr [rcx + 0xe0], 1" and all(geo.values()),
      "unconditional %s / %s; geometric classes read +0xE4 %s" % (at(A, 0x007F1D29), at(D, 0x007F1F9B), geo))
e4w = {k: stores(I, 0xE4, 0xE8) for k, I in bodies.items()}
check("P4", {k: v for k, v in e4w.items() if v} == {"Dynamic": [0x007F13EC]} and at(bodies["Dynamic"], 0x007F13EC) == "movss dword ptr [rdi + 0xe4], xmm0",
      "+0xE4 stores %s" % {k: ["%08X" % a for a in v] for k, v in e4w.items() if v})
check("P5", q(0x01CBAB68 + 34 * 8) == 0, "SoundObject slot 34 = %X" % q(0x01CBAB68 + 34 * 8))
st = lambda a: [S(x) for x in md.disasm(blob[OFF(a):OFF(a) + 3], a)]
s36 = {k: q(CL[k][0] + 36 * 8) for k in ("Ambient", "Direction")}
check("P6", st(0x007E5800) == ["mov al, 1", "ret"] and st(0x007E57B0) == ["xor al, al", "ret"] and all(v in (0x007E5800, 0x007E57B0) for v in s36.values()),
      "true stub %s, false stub %s; slot 36 %s" % (st(0x007E5800), st(0x007E57B0), {k: "%08X" % v for k, v in s36.items()}))
text = next(x for x in SECS if x[0] == ".text")
sq = set()
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        if any(x.mnemonic in ("sqrtps", "rsqrtps", "vsqrtps", "vrsqrtps") for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)):
            sq.add(fa)
    except ValueError:
        continue
check("P7", len(sq) == 12 and all(0x007EF1E0 <= f <= 0x007F74E0 for f in sq), "%d functions with sqrtps/rsqrtps, range %08X..%08X" % (len(sq), min(sq), max(sq)))
Pg = bodies["Polygon"]
check("P8", "+ 0xe0], 0" in at(Pg, 0x007F2DF9) and ("0xffffffff" in at(Pg, 0x007F2E00) or "-1" in at(Pg, 0x007F2E00) or at(Pg, 0x007F2E00).startswith("or eax"))
      and ("xor eax, eax" == at(Pg, 0x007F2DF5)), "%s | %s | %s" % (at(Pg, 0x007F2DF9), at(Pg, 0x007F2E00), at(Pg, 0x007F2DF5)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
