"""cu3_fixup_tables.py - CU-3: the three packed fixup tables of a .phyre cluster, decoded (FABLE, Claude Opus 5.5,
2026-09-26; the decoder is a line-for-line transcription of the loader's 00595EF0 / 00596890 made by a delegated read-only
pass, adopted here with its controls and re-run).

  K1 the loader: the orchestrator 0059E300 runs its stages from 0059E46B (0059E780) to 0059E526 (0059C250). The three
     fixup stages read the header's size and count pairs: pointer-array +0x24/+0x28 (0059CEDF, 0059CED3), pointer
     +0x1C/+0x20 (0059C7CE, 0059C7C7) and array +0x14/+0x18 (0059C2D1, 0059C2C7). Each reads S packed bytes through
     stream slot +0x28 (0059C346). Both decoders take the group mode from the header byte's low 3 bits (00595F6B,
     00596926), and the group key is a varint rotated right by one (00595FB3).
  K2 the corpus: every .phyre under the extract's gamedata. The stream position is the one the stage order implies:
     header, namespace, list headers, instance data, user fixups, header-class tables, then the pointer-array,
     pointer and array tables. Each table must decode every list to exactly its per-list count, and consume exactly
     the header's size. For meshes and "neither" clusters, what remains after the array table is exactly
     index + vertex buffer size.
  K3 sensitivity: on a fixed sample, starting one byte early or late, or reading the tables in the wrong order, must
     fail every file.
So `size` is a packed byte length and `count` is the decoded entry count. The encoding is groups of {mode byte,
varint key, per-mode indices, varint payload}, with modes 0 dense, 1 sub-groups, 2 explicit list, 3 all-except,
4 bitmask, 5 explicit entries and 6 arithmetic progression. What each entry's fields mean is not decoded here.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, os, random, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
EXTRACT = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract") / "gamedata"

class Cur:
    def __init__(s, b, p): s.b = b; s.p = p
    def u8(s):
        v = s.b[s.p]; s.p += 1; return v
    def vi(s):
        v = 0; sh = 0
        while True:
            c = s.b[s.p]; s.p += 1
            v |= (c & 0x7F) << sh; sh += 7
            if not (c & 0x80): return v & 0xFFFFFFFFFFFFFFFF

class Bad(Exception): pass

LIMIT = [1 << 20]
def guard(k):
    if k > LIMIT[0]: raise Bad('count %d' % k)


def ror1(v):
    v &= 0xFFFFFFFF
    return ((v >> 1) | ((v & 1) << 31)) & 0xFFFFFFFF

def idx(c, m):  # u8 when the list has fewer than 256 objects, else varint (00596063-0059610E)
    return c.u8() if m < 0x100 else c.vi()

def excl(c, m):  # 005972C0 / 00597400: all indices except a varint-counted exclusion list
    n = c.vi(); guard(n); out = []; i = 0
    for _ in range(n):
        e = idx(c, m)
        while i < e: out.append(i); i += 1
        i = e + 1
    while i < m: out.append(i); i += 1
    return out

def bitmask(c, m):
    nb = (m >> 3) + (1 if m & 7 else 0)
    mask = c.b[c.p:c.p + nb]; c.p += nb
    return [i for i in range(m) if mask[i >> 3] & (1 << (i & 7))]

def dec_arr(c, n, m):
    """00595EF0: decode n 16-byte entries for a list of m objects; returns list of (d0,idx,d2,d3)."""
    out = []
    while len(out) < n:
        h = c.u8(); mode = h & 7
        fl = (h & ~6) | 1
        if m == 1: fl |= 2
        d0 = ror1(c.vi())
        def tail(inl=True):
            d2 = 0 if fl & 8 else c.vi()
            d3 = c.vi(); return d2, d3
        if mode == 0:
            for i in range(m):
                out.append((d0, i) + tail())
        elif mode == 2:
            k = c.vi(); guard(k); ids = [idx(c, m) for _ in range(k)]
            for i in ids: out.append((d0, i) + tail())
        elif mode == 3:
            for i in excl(c, m): out.append((d0, i) + tail())
        elif mode == 4:
            nb = (m >> 3) + (1 if m & 7 else 0)
            mask = c.b[c.p:c.p + nb]; c.p += nb
            for i in range(m):
                if mask[i >> 3] & (1 << (i & 7)): out.append((d0, i) + tail())
        elif mode == 5:
            k = c.vi(); guard(k)
            for _ in range(k):
                i = 0 if fl & 2 else c.vi()
                out.append((d0, i) + tail())
        elif mode == 6:
            st = c.vi(); sd = c.vi(); k = c.vi(); guard(k)
            for j in range(k): out.append((d0, st + j * sd) + tail())
        elif mode == 1:
            target = len(out) + m
            while len(out) < target:
                sm = c.u8(); d2, d3 = tail()
                if sm == 2:
                    k = c.vi(); guard(k); ids = [idx(c, m) for _ in range(k)]
                elif sm == 3: ids = excl(c, m)
                elif sm == 4: ids = bitmask(c, m)
                elif sm == 6:
                    st = c.vi(); sd = c.vi(); k = c.vi(); guard(k); ids = [st + j * sd for j in range(k)]
                else: raise Bad("arr submode %d" % sm)
                for i in ids: out.append((d0, i, d2, d3))
                if len(out) > target: raise Bad("arr mode1 overrun")
        else: raise Bad("arr mode %d" % mode)
    if len(out) != n: raise Bad("arr overrun %d/%d" % (len(out), n))
    return out

def ptail(c, fl, e):  # 0059FFC0
    if not fl & 0x10:
        v = c.vi(); e[6] = (v - 1) if v else -1
        if v:
            if not fl & 8: e[5] = c.vi()
            return
    e[2] = c.vi()
    if not fl & 0x20: e[3] = c.vi()
    if not fl & 0x40: e[4] = c.vi()
    if not fl & 8: e[5] = c.vi()

def dec_ptr(c, n, m):
    out = []
    while len(out) < n:
        h = c.u8(); mode = h & 7
        fl = (h & ~6) | 1
        if m == 1: fl |= 2
        t = [ror1(c.vi()), 0, 0, 0, 0, 0, -1]
        if fl & 0x20: t[3] = c.vi()
        def emit(i, tl=True, tpl=None):
            e = list(tpl or t); e[1] = i
            if tl: ptail(c, fl, e)
            out.append(e)
        if mode == 0:
            for i in range(m): emit(i)
        elif mode == 2:
            k = c.vi(); guard(k); ids = [idx(c, m) for _ in range(k)]
            for i in ids: emit(i)
        elif mode == 3:
            for i in excl(c, m): emit(i)
        elif mode == 4:
            nb = (m >> 3) + (1 if m & 7 else 0)
            mask = c.b[c.p:c.p + nb]; c.p += nb
            for i in range(m):
                if mask[i >> 3] & (1 << (i & 7)): emit(i)
        elif mode == 5:
            k = c.vi(); guard(k)
            for _ in range(k):
                i = 0 if fl & 2 else c.vi(); emit(i)
        elif mode == 6:
            st = c.vi(); sd = c.vi(); k = c.vi(); guard(k)
            for j in range(k): emit(st + j * sd)
        elif mode == 1:
            target = len(out) + m
            while len(out) < target:
                sm = c.u8(); tpl = list(t); ptail(c, fl, tpl)
                if sm == 2:
                    k = c.vi(); guard(k); ids = [idx(c, m) for _ in range(k)]
                elif sm == 3: ids = excl(c, m)
                elif sm == 4: ids = bitmask(c, m)
                elif sm == 6:
                    st = c.vi(); sd = c.vi(); k = c.vi(); guard(k); ids = [st + j * sd for j in range(k)]
                else: raise Bad("ptr submode %d" % sm)
                for i in ids: emit(i, False, tpl)
                if len(out) > target: raise Bad("ptr mode1 overrun")
        else: raise Bad("ptr mode %d" % mode)
    if len(out) != n: raise Bad("ptr overrun %d/%d" % (len(out), n))
    return out

def check(path):
    b = open(path, "rb").read()
    w = struct.unpack_from("<21I", b, 0)
    ns, L = w[2], w[4]
    lists = [struct.unpack_from("<9I", b, 84 + ns + 36 * i) for i in range(L)]
    p = 84 + ns + 36 * L + sum(l[2] for l in lists)
    p += w[13] + 12 * w[12]
    p += 4 * w[15] + 16 * w[16]
    res = {}
    for name, S, col, fn in (("parr", w[9], 8, dec_arr), ("ptr", w[7], 7, dec_ptr), ("arr", w[5], 6, dec_arr)):
        c = Cur(b, p)
        try:
            ents = []
            for l in lists:
                ents += fn(c, l[col], l[1])
            ok = (c.p - p == S)
            res[name] = ("OK" if ok else "LEN %d/%d" % (c.p - p, S), ents)
        except (Bad, IndexError) as e:
            res[name] = ("ERR " + str(e), [])
        p += S
    res["tail"] = len(b) - p
    return w, lists, res


d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
fails = 0
def verdict(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
A = {0x59E46B: "call 0x59e780", 0x59E526: "call 0x59c250", 0x59CEDF: "mov ebp, dword ptr [rcx + 0x24]",
     0x59CED3: "mov r8d, dword ptr [rcx + 0x28]", 0x59C7CE: "mov esi, dword ptr [rcx + 0x1c]", 0x59C7C7: "mov eax, dword ptr [rcx + 0x20]",
     0x59C2D1: "mov esi, dword ptr [rcx + 0x14]", 0x59C2C7: "mov eax, dword ptr [rcx + 0x18]", 0x59C346: "call qword ptr [rax + 0x28]",
     0x595F6B: "and r10d, 7", 0x596926: "and r10d, 7", 0x595FB3: "ror r9d, 1"}
verdict("K1 the loader's stage order, size/count fields, packed read, mode bits and rotated key",
        all(at(a) == s for a, s in A.items()), str({"%08X" % a: at(a) for a in A if at(a) != A[a]}))
files = sorted(str(p) for p in EXTRACT.rglob("*.phyre"))
tally = collections.Counter(); tails = collections.Counter()
for f in files:
    w, lists, r = check(f)
    tally["all3"] += all(r[k][0] == "OK" for k in ("parr", "ptr", "arr"))
    kind = "mesh" if (w[18] or w[19]) else ("tex" if w[20] else "neither")
    if kind != "tex": tails[kind, r["tail"] == w[18] + w[19] + w[20]] += 1
nonTex = sum(tails.values()); nonTexEq = sum(v for (k, eq), v in tails.items() if eq)
verdict("K2 every cluster decodes all three tables to their counts and consumes exactly their sizes; mesh and other tails "
        "equal the buffer sizes", len(files) == 35984 and tally["all3"] == len(files) and nonTexEq == nonTex,
        "files %d, all three OK %d, non-texture tails equal %d of %d" % (len(files), tally["all3"], nonTexEq, nonTex))
def run(path, shift=0, order=("parr", "ptr", "arr")):
    b = open(path, "rb").read(); w = struct.unpack_from("<21I", b, 0); ns, L = w[2], w[4]
    lists = [struct.unpack_from("<9I", b, 84 + ns + 36 * i) for i in range(L)]
    p = 84 + ns + 36 * L + sum(l[2] for l in lists) + w[13] + 12 * w[12] + 4 * w[15] + 16 * w[16] + shift
    spec = {"parr": (w[9], 8, dec_arr), "ptr": (w[7], 7, dec_ptr), "arr": (w[5], 6, dec_arr)}
    ok = True
    for name in order:
        S, col, fn = spec[name]; c = Cur(b, p)
        try:
            for l in lists:
                LIMIT[0] = max(l[col], l[1]) + 1
                fn(c, l[col], l[1])
            if c.p - p != S: ok = False
        except (Bad, IndexError): ok = False
        p += S
    LIMIT[0] = 1 << 20
    return ok
random.seed(12); sample = random.sample(files, 300)
base = sum(run(f) for f in sample); plus = sum(run(f, 1) for f in sample); minus = sum(run(f, -1) for f in sample)
wrong = sum(run(f, 0, ("arr", "ptr", "parr")) for f in sample)
verdict("K3 sensitivity on 300 files: baseline passes all; +1, -1 and the wrong table order pass none",
        base == 300 and plus == 0 and minus == 0 and wrong == 0, "baseline %d, +1 %d, -1 %d, wrong order %d" % (base, plus, minus, wrong))
print("FAILS", fails)
sys.exit(1 if fails else 0)
