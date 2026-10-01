"""navgrid_unitdef.py - the unit-definition page's grid-rebuild row, checked against the shipped bytes
(FABLE, Claude Opus 5.5, 2026-09-27).

  G1  003924B0 stores 0x24 to 02AEE0B8 BEFORE the getter call, and a zero return skips to the epilogue
  G2  budget = (0x2800 - [02AEE0B8]) / ([02AEE0B8] + 1): mov eax,0x2800 / sub eax,esi / lea edi,[rsi+1] / idiv edi
  G3  cell = floorf(max(w/trunc(w/c0), h/trunc(h/c0))) + [01CEBBA8] stored to 02AEE090; allocation = N*(n+1) + n
  G4  the caller's density scale is unread: 002342F0 loads xmm0 then calls 003924B0 (its only caller - no other
      call, jump or address-taken dword/qword reference outside unwind records), and 003924B0's first xmm0
      access is a WRITE, after a call that clobbers xmm0 anyway
  C   control for G4's detector: 00229EE0's first instruction stores xmm0 to a global (a float setter), a READ before any call - the detector must say so
  N   arithmetic: 50 x 50 gives cell 4, 13 x 13, allocation argument 6289 (ASTRA's authored case, recomputed in f32)

Reads the capstone listing (Y1P_CACHE env, default the session scratchpad) and the shipping image.
"""
import math, os, re, struct, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
body = {}
refs = []
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) < 3: continue
    if p[1] in ("003924B0", "002342F0", "00229EE0"): body.setdefault(p[1], []).append((p[0], p[2]))
    if "0x3924b0" in p[2]: refs.append((p[0], p[2]))
B = body["003924B0"]
def idx(pred, seq=B):
    return next(i for i, (a, s) in enumerate(seq) if pred(a, s))
i_store = idx(lambda a, s: s.startswith("mov dword ptr") and "0x24" in s and "02AEE0B8" in s)
i_get = idx(lambda a, s: s == "call 0x383740")
i_je = idx(lambda a, s: s.startswith("je "))
epi = [a for a, s in B if s.startswith("mov rcx, qword ptr [rsp + 0x40]")][0]
ok("G1", i_store < i_get < i_je and B[i_je][1] == "je 0x" + epi.lower().lstrip("0"),
   "0x24 -> 02AEE0B8 at %s, getter at %s, zero return -> %s" % (B[i_store][0], B[i_get][0], epi))
seq = [s for a, s in B]
g2 = ["mov eax, 0x2800", "sub eax, esi", "lea edi, [rsi + 1]", "idiv edi"]
pos = [next((i for i, s in enumerate(seq) if s == g), -1) for g in g2]
ok("G2", all(p >= 0 for p in pos) and pos == sorted(pos) and "02AEE0B8" in seq[pos[0] + 2], "budget = (0x2800 - n)/(n + 1), n = [02AEE0B8]")
i_sq = seq.index("call 0x861f14"); i_max = idx(lambda a, s: s.startswith("maxss")); i_fl = seq.index("call 0x861f86")
i_add = idx(lambda a, s: s.startswith("addss xmm0") and "01CEBBA8" in s); i_st = idx(lambda a, s: s.startswith("movss dword ptr") and "02AEE090" in s)
i_alloc = seq.index("call 0x384580")
alloc = seq[i_alloc - 5:i_alloc]  # imul ebx,eax / store cols / imul ebx,edi / add ebx,esi / mov ecx,ebx
ok("G3", i_sq < i_max < i_fl < i_add < i_st and alloc[0] == "imul ebx, eax" and alloc[2:] == ["imul ebx, edi", "add ebx, esi", "mov ecx, ebx"],
   "sqrtf -> maxss -> floorf -> +1.0 -> 02AEE090; size = cols*rows*(n+1) + n")
def first_xmm0(seq):
    for a, s in seq:
        if s.startswith("call"): return ("CALL", a, s)
        if "xmm0" in s:
            mn, ops = (s.split(None, 1) + [""])[:2]
            dst = ops.split(",")[0]
            w = "xmm0" in dst and mn in ("movss", "movsd", "movaps", "movups", "movd", "movq", "cvtdq2ps", "cvtsi2ss", "xorps")
            return ("W" if w else "R", a, s)
    return ("NONE", "", "")
fx = first_xmm0(B)
calls = [r for r in refs]
d = open(EXE, "rb").read(); rva = struct.pack("<I", 0x003924B0 - 0x120000)
raw = [m.start() for m in re.finditer(re.escape(rva), d)]
va_hits = len(re.findall(re.escape(struct.pack("<Q", 0x003924B0)), d)) + len(re.findall(re.escape(struct.pack("<I", 0x003924B0)), d))
unwind = all(d[o + 4:o + 8] == struct.pack("<I", 0x002724F1) for o in raw)
cal = body["002342F0"]; ci = idx(lambda a, s: s == "call 0x3924b0", cal)
ok("G4", fx[0] == "CALL" and first_xmm0(B[i_get + 1:])[0] == "W" and calls == [("0023441E", "call 0x3924b0")]
   and cal[ci - 1][1] == "movaps xmm0, xmm2" and va_hits == 0 and len(raw) == 3 and unwind,
   "only caller 0023441E passes xmm0; builder reaches a call first (%s), then writes xmm0 first (%s); RVA hits %d, all unwind records"
   % (fx[1], first_xmm0(B[i_get + 1:])[1], len(raw)))
cx = first_xmm0(body["00229EE0"])
ok("C", cx[0] == "R", "detector control: 00229EE0 first xmm0 access is a read (%s %s)" % (cx[1], cx[2]))
def f(x):  # round to IEEE single, as each SSE scalar op does
    return struct.unpack("<f", struct.pack("<f", x))[0]
def grid(w, h, floor=True):
    budget = (0x2800 - 0x24) // 0x25
    c0 = f(math.sqrt(f(f(w) * f(h)) / budget))
    refined = max(f(w / f(int(f(w / c0)))), f(h / f(int(f(h / c0)))))
    cell = f((math.floor(refined) if floor else refined) + 1.0)
    cols, rows = int(f(f(cell - 1.0 + w) / cell)), int(f(f(cell - 1.0 + h) / cell))
    return budget, cell, cols, rows, cols * rows * 0x25 + 0x24
g = grid(50, 50); g2 = grid(50, 50, floor=False)
ok("N", g == (275, 4.0, 13, 13, 6289) and g2[1:] == (4.125, 12, 12, 5364), "50x50: %r; without the floor: %r" % (g, g2))
print("FAILS", fails); sys.exit(1 if fails else 0)
