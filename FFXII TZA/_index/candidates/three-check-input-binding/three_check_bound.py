"""three_check_bound.py - three_check.py with its two inputs bound to each other (FABLE, Claude Opus 5.5, 2026-09-28,
on ASTRA-REQ-FABLE-CONSUMER-SOURCE-VIEW-BINDING). three_check.py is kept unchanged: ASTRA's receipts hash it.

The defect ASTRA showed: three_check.py read its instructions from the Y1P_CACHE text view and only constants from
FFXII_EXE, so an image with 00229E7E changed JB -> JBE still passed against the old view.

  B   binding, before any semantic check. Each of the four bodies is decoded from the EXE's own bytes over its full
      extent (00229E70 37 B, 0020E600 10 B, 0020E620 9 B, 00339630 1061 B: the extents of ASTRA's dependency-verified
      retained bodies). The decode must consume the extent exactly. The view's lines for that body must equal the
      decode, address for address and text for text. Any difference, gap, extra line or short decode -> REFUSE, exit 2.
      The EXE's SHA-256 and each body's SHA-256 are printed against the certified values; they are reported, not the
      binding (a hash says which file, not that the view describes it).
  R1  I1  A1  as in three_check.py, but every instruction is taken from the EXE decode, so a changed image fails
      its semantic check whatever the view says.
  C   three_check.py's controls, plus binding controls on in-memory copies (no file is written):
      both built from the input image and view with 00229E7E forced to 72 (JB) or 76 (JBE), so C does not depend on
      which byte the input holds:
      CB0 the JB image with the jb view binds, and R1/I1/A1 pass (the positive);
      CB1 the JBE image against the jb view is refused;
      CB2 the JB image against a jbe view is refused;
      CB3 the JBE image with the jbe view binds, and only R1 fails.

Domain of the R1 model (host Python, not the game's FPU): COMISS is modelled for ordered and unordered operands only.
DAZ is a parameter: with MXCSR.DAZ set, a positive subnormal compares as zero and resets to 1.0; with it clear it is
kept. The game's MXCSR state at 00229E70 is not established here, so neither reading is claimed. Nothing here is a
bit-exact FF12 result.
Exit: 0 all pass, 1 a semantic check failed, 2 the inputs do not describe the same program.
"""
import hashlib, math, os, re, struct, sys
import capstone
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
CERT_EXE = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BODIES = {0x00229E70: (37, "749953009c38a262b64c21f7bed7057d31ff25de5d32469b00ec0e55382bb5fa"),
          0x0020E600: (10, "8bde921e0db5b4c6b16e649c4df8172da2b8b8c3462664b675b377cf37450f65"),
          0x0020E620: (9, "9f88dce71d7cce301096aa6ab93885acc0103d2d044dbfad741262336cffd7d7"),
          0x00339630: (1061, "8a75e847cb7520bb1e19c64607ac094482fb0ad6ba8c825c7a8f8c363478d1f6")}
MUT_PC, JB, JBE = 0x00229E7E, 0x72, 0x76

def sections(d):
    pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]; o = pe + 24 + opt; s = []
    for i in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); s.append((va, rs, ra)); o += 40
    return s
def off(secs, v):
    r = v - 0x120000
    for va, rs, ra in secs:
        if va <= r < va + rs: return ra + r - va
    raise KeyError("%08X not in a raw section" % v)
def read_view(path):
    V = {}
    for l in open(path, encoding="utf-8", errors="replace"):
        p = l.rstrip("\n").split(None, 2)
        if len(p) == 3 and int(p[1], 16) in BODIES: V.setdefault(int(p[1], 16), []).append((int(p[0], 16), p[2].split(" ;")[0].rstrip()))
    return V
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def decode(d, secs):
    D = {}
    for e, (n, _) in BODIES.items():
        o = off(secs, e); ins = list(MD.disasm(d[o:o + n], e))
        end = ins[-1].address + ins[-1].size if ins else e
        D[e] = ([(i.address, (i.mnemonic + " " + i.op_str).rstrip()) for i in ins], end == e + n)
    return D
def bind(D, V):
    """Return the list of refusal reasons; empty means the view describes these bytes."""
    bad = []
    for e in BODIES:
        dec, full = D[e]
        if not full: bad.append("%08X decode does not consume its %d-byte extent" % (e, BODIES[e][0]))
        v = V.get(e, [])
        if v != dec:
            dv = dict(dec); vv = dict(v)
            diff = sorted(set(dv) ^ set(vv)) + sorted(a for a in set(dv) & set(vv) if dv[a] != vv[a])
            bad.append("%08X view differs from the image at %s" % (e, ", ".join("%08X" % a for a in diff[:4]) or "line order"))
    return bad

fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
fl = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
def rate(v, jbe=False, daz=False):
    if daz and v != 0.0 and abs(v) < fl(0x00800000): v_cmp = 0.0
    else: v_cmp = v
    unordered = math.isnan(v_cmp)
    cf = unordered or (0.0 < v_cmp); zf = unordered or (v_cmp == 0.0)
    take = (cf or zf) if jbe else cf
    return v if take else 1.0
def semantic(D, u32, tag=""):
    """R1, I1, A1 on the EXE decode; returns {tag: passed}."""
    T = {e: [s for a, s in D[e][0]] for e in BODIES}; res = {}
    r = T[0x00229E70]
    res["R1"] = (r[:4] == ["movss xmm1, dword ptr [rip + 0x1bd89a8]", "xorps xmm0, xmm0", "comiss xmm0, xmm1", "jb 0x229e91"]
                 and u32(0x01CEBBA8) == 0x3F800000
                 and rate(0.5) == 0.5 and rate(0.0) == 1.0 and rate(-0.0) == 1.0 and rate(-1.0) == 1.0 and math.isnan(rate(float("nan")))
                 and rate(fl(1), daz=False) == fl(1) and rate(fl(1), daz=True) == 1.0)
    B = 0x0000000140000000
    Dd = lambda u: (B + (u & 0xFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    E = lambda p: ((p & 0xFFFFFFFF) - (B & 0xFFFFFFFF)) & 0xFFFFFFFF
    samples = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x12345678]
    res["I1"] = (T[0x0020E600] == ["mov eax, ecx", "add rax, qword ptr [rip + 0x1d74f27]", "ret"]
                 and T[0x0020E620] == ["sub ecx, dword ptr [rip + 0x1d74f0a]", "mov eax, ecx", "ret"]
                 and all(E(Dd(u)) == u for u in samples) and all(Dd(E(p)) == p for p in [B, B + 0xFFFFFFFF])
                 and not any(Dd(E(p)) == p for p in [B - 1, B + 0x100000000, 0]) and Dd(0) == B)
    x9 = [(a, s) for a, s in D[0x00339630][0] if re.match(r"\w+ xmm9,", s)]
    res["A1"] = (x9 == [(0x00339723, "movss xmm9, dword ptr [rip + 0x5b9a0c]"), (0x00339A02, "movaps xmm9, xmmword ptr [rsp + 0x120]")]
                 and u32(0x008F3138) == 0x43340000 and dict(D[0x00339630][0]).get(0x00339880, "").startswith("divss xmm0, xmm9"))
    return res

if __name__ == "__main__":
    d = open(EXE, "rb").read(); secs = sections(d)
    u32 = lambda v: struct.unpack_from("<I", d, off(secs, v))[0]
    print("inputs  FFXII_EXE %s  Y1P_CACHE %s" % (EXE, CACHE))
    h = hashlib.sha256(d).hexdigest()
    print("report  exe sha256 %s (%s)" % (h, "certified" if h == CERT_EXE else "NOT the certified image"))
    for e, (n, bh) in BODIES.items():
        o = off(secs, e); print("report  body %08X %d B sha256 %s" % (e, n, "certified" if hashlib.sha256(d[o:o + n]).hexdigest() == bh else "DIFFERS"))
    D = decode(d, secs); V = read_view(CACHE)
    bad = bind(D, V)
    for b in bad: print("REFUSE B  " + b)
    if bad: print("REFUSED: the view and the image do not describe the same program; no semantic check was run"); sys.exit(2)
    print("PASS B  view equals the image decode for %s" % ", ".join("%08X (%d lines)" % (e, len(D[e][0])) for e in BODIES))
    res = semantic(D, u32)
    ok("R1", res["R1"], "jb at 00229E7E from the image; kept: 0.5, NaN; reset: 0, -0, -1; subnormal kept without DAZ, reset with DAZ")
    ok("I1", res["I1"], "leaves from the image; E(D(u)) = u; D(E(p)) = p only inside [B, B + 2^32); D(0) = B")
    ok("A1", res["A1"], "xmm9 written only at 00339723 (008F3138 = 180.0) and the epilogue 00339A02")
    # controls: three_check.py's, then binding controls on in-memory copies
    # Both variants are built from the input image and view, so C tests the instrument whatever byte the input holds.
    B0 = 0x0000000140000000
    Eadd = lambda p: ((p & 0xFFFFFFFF) + (B0 & 0xFFFFFFFF)) & 0xFFFFFFFF
    c_old = rate(0.0, jbe=True) == 0.0 and not all(Eadd((B0 + u) & 0xFFFFFFFFFFFFFFFF) == u for u in [1, 0x12345678])
    mo = off(secs, MUT_PC)
    def variant(byte, text):
        b = bytearray(d); b[mo] = byte; b = bytes(b)
        v = {e: [(a, text if a == MUT_PC else s) for a, s in lines] for e, lines in V.items()}
        return decode(b, secs), v, (lambda x: struct.unpack_from("<I", b, off(secs, x))[0])
    D0, V0, u0 = variant(JB, "jb 0x229e91"); Dm, Vm, um = variant(JBE, "jbe 0x229e91")
    cb0 = not bind(D0, V0) and all(semantic(D0, u0).values())
    cb1 = bool(bind(Dm, V0)); cb2 = bool(bind(D0, Vm))
    sm = semantic(Dm, um); cb3 = not bind(Dm, Vm) and not sm["R1"] and sm["I1"] and sm["A1"]
    ok("C", c_old and cb0 and cb1 and cb2 and cb3,
       "input byte at 00229E7E = %02X; old controls %s; CB0 JB pair binds and passes %s; CB1 stale view refused %s; "
       "CB2 stale image refused %s; CB3 JBE pair binds and fails R1 only %s" % (d[mo], c_old, cb0, cb1, cb2, cb3))
    print("FAILS", fails); sys.exit(1 if fails else 0)
