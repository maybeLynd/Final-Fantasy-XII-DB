"""composer_replay.py - OPUS (Claude Opus 5.5), 2026-09-28. A non-author corroboration of FABLE's correction of the
composer 003977B0 (e88336a16, on ASTRA's postmultiply-order-alias). MODEL-PROVEN: it replays 003977B0's own instruction
stream (003977CD to the 003978EE epilogue) over a memory model; it is not a native run. Any instruction the model does
not implement stops the run, so a changed body cannot be silently mis-modelled.
  O1  disjoint: A = diag(2,3,4,1) at rcx, B = I + e01 at rdx -> C[0][1] = 3, i.e. M[rcx] = M[rdx] x M[rcx] (row-major
      B*A); A*B would give 2
  O2  the same buffer (rcx == rdx) differs from two separately stored equal matrices: M = [[1,2],[3,4]] padded to 4x4
      gives (7,10,15,22) disjoint and (7,22,15,46) aliased, top-left 2x2
Refuses any image but the certified one (exit 2). Exit 1 on a failed check.
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
d = open(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
def f32(x): return struct.unpack("<f", struct.pack("<f", x))[0]
INS = {x.address: x for x in Cs(CS_ARCH_X86, CS_MODE_64).disasm(d[off(0x3977B0):off(0x3977B0) + 349], 0x3977B0)}
ORDER = sorted(INS)


def run(A, Bm, alias):
    mem = {}
    abase, bbase = 0x1000, (0x1000 if alias else 0x2000)
    for i, v in enumerate(A): mem[abase + 4 * i] = float(v)
    if not alias:
        for i, v in enumerate(Bm): mem[bbase + 4 * i] = float(v)
    g = {"rsp": 0x9000, "rcx": abase, "rdx": bbase, "rax": 0, "r8": 0, "r9": 0, "r10": 0, "r11": 0}
    x = {}
    def addr(s):
        m = re.match(r"(?:dword|xmmword|qword) ptr \[(\w+)(?: \+ (r\w+))?(?: ([+-]) (0x[0-9a-f]+|\d+))?\]", s)
        a = g[m.group(1)] + (g[m.group(2)] if m.group(2) else 0)
        if m.group(4): a += int(m.group(4), 0) * (-1 if m.group(3) == "-" else 1)
        return a
    pc = 0x3977CD
    while True:
        i = INS[pc]; mn = i.mnemonic; o = [p.strip() for p in i.op_str.split(",")]
        nxt = ORDER[ORDER.index(pc) + 1] if pc != ORDER[-1] else None
        if pc == 0x3978EE: break
        if mn == "movaps" and "ptr" in o[1]:
            a = addr(o[1]); x[o[0]] = [mem.get(a + 4 * k, 0.0) for k in range(4)]
        elif mn == "movaps" and "ptr" in o[0]:
            a = addr(o[0])
            for k in range(4): mem[a + 4 * k] = x[o[1]][k]
        elif mn == "movaps": x[o[0]] = list(x[o[1]])
        elif mn == "movss" and "ptr" in o[1]: x[o[0]] = [mem.get(addr(o[1]), 0.0), 0, 0, 0]
        elif mn == "movss": mem[addr(o[0])] = x[o[1]][0]
        elif mn == "mulss": x[o[0]][0] = f32(x[o[0]][0] * (mem.get(addr(o[1]), 0.0) if "ptr" in o[1] else x[o[1]][0]))
        elif mn == "addss": x[o[0]][0] = f32(x[o[0]][0] + x[o[1]][0])
        elif mn == "lea": g[o[0]] = addr("qword ptr " + o[1])
        elif mn == "sub" and o[1] in g: g[o[0]] -= g[o[1]]
        elif mn == "sub": g[o[0]] -= int(o[1], 0)
        elif mn == "add": g[o[0]] += int(o[1], 0)
        elif mn == "mov" and o[0] == "r11d": g["r11"] = int(o[1], 0)
        elif mn == "jne":
            if g["r11"] != 0: pc = int(o[0], 16); continue
        else: raise SystemExit("unmodelled %s %s" % (mn, i.op_str))
        pc = nxt
    return [mem[abase + 4 * i] for i in range(16)]


fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
I = [1 if r == c else 0 for r in range(4) for c in range(4)]
A = [2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1]
Bm = list(I); Bm[1] = 1
C = run(A, Bm, False)
check("O1", C[1] == 3.0, "disjoint C[0][1] = %s (B*A predicts 3, A*B predicts 2)" % C[1])
M = [1, 2, 0, 0, 3, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
Cd = run(M, M, False); Ca = run(M, None, True)
check("O2", [Cd[0], Cd[1], Cd[4], Cd[5]] == [7, 10, 15, 22] and [Ca[0], Ca[1], Ca[4], Ca[5]] == [7, 22, 15, 46],
      "disjoint %s, same buffer %s" % ([Cd[0], Cd[1], Cd[4], Cd[5]], [Ca[0], Ca[1], Ca[4], Ca[5]]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
