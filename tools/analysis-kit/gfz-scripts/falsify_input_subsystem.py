"""Falsification pass 1 on CONTRACT-input-subsystem (OPUS, 2026-09-29), from the shipping image, using the contract's own
"Falsified by" tests. Edge censuses are raw E8/E9 sweeps of .text; address censuses run bounded (to each function's chain union)
and as a linear rip-window sweep.

  N0  section 2: 002498B0 (002498BD..002498EE) and 002284F0 (00228605..00228636) each store 0 at the eight anchors 02F97360, 68, 70,
      78, 80, 88, 90 (qwords) and 98 (a dword, the 0x3C snapshot's tail)
  N1  I-1: 002498B0's inbound edges are calls in 0022A770, 0022B8C0 (0022B908) and 0022BC20 (0022BC50) and the tail-jump 00249C4D in
      00249C30; 0022BC20 calls 00314020 at 0022BCCF; 0022A580 dispatches through `jmp rcx` at 0022A6A3 after `cmp eax, 6`
  N2  I-2: 002E0D90 is a 5-byte jump to 00253C50, the only edge into 00253C50; 00253C50 is the only caller of 00253C70 (00253C56);
      in 00314020 the two 002E0D90 calls (00314137, 003141F2) follow the two 00234590 loops; 00234590 calls 00313A00 at 00234624
  N3  I-3 and section 4: the only by-name writer of 02F9736A is 00253C70, at 00253F70, 00253FE9, 002540C5, 0025415F, 002541BC (both
      instruments); edi is zeroed at 00253D12 and written only at 00254049, 00254189, 002541F9, each followed within one instruction
      by an unconditional jump to the epilogue; 002A329B stores a qword 0 at 02F97368; the number of functions reading 02F9736A by
      name is reported against the page's 51
  N4  I-4: no call to 002E0FA0 in 002498B0 or in its direct-call closure to depth 3
  N5  I-5: 002284F0 is 439 B with no direct caller; it tests [[0209AC30] + 0x308] (002285D1..002285E0) and compares against the word
      at 01E0C2A4 before the eight-store wipe
  N6  I-6: 002E0FA0 reads the 16 rows 0215F1C0..0215F1FF as four 16-byte loads and combines them with `por` only; the one
      `btr` clears bit 19 when 00360360() is non-zero
"""
import collections, io, os, struct
from array import array
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
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
pd = next(x for x in SECS if x[0] == ".pdata"); praw = blob[pd[3]:pd[3] + pd[4]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    if b_:
        pent[BASE + b_] = (BASE + e_, BASE + u_)


def root(bg):
    seen, r = set(), bg
    while r in pent and r not in seen:
        seen.add(r); u = pent[r][1]; h = blob[OFF(u):OFF(u) + 4]
        if not (h[0] >> 3) & 4:
            break
        c = OFF(u) + 4 + 2 * ((h[2] + 1) & ~1); r = BASE + struct.unpack("<I", blob[c:c + 4])[0]
    return r


uend = collections.defaultdict(int)
for b_ in pent:
    uend[root(b_)] = max(uend[root(b_)], pent[b_][0])
text = next(x for x in SECS if x[0] == ".text")
bodies = {}
for fa in sorted(sizes):
    if text[1] <= fa < text[1] + text[2]:
        try:
            bodies[fa] = list(md.disasm(blob[OFF(fa):OFF(fa) + max(sizes[fa], uend.get(fa, 0) - fa)], fa))
        except ValueError:
            pass
B = lambda fa: {x.address: x for x in bodies[fa]}
at = lambda I, a: S(I[a]) if a in I else "?"
raw = blob[text[3]:text[3] + text[4]]
edges = collections.defaultdict(list)
T = (0x002498B0, 0x00253C50, 0x00253C70, 0x002284F0, 0x002E0D90)
for k in range(len(raw) - 5):
    if raw[k] in (0xE8, 0xE9):
        t = text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0]
        if t in T:
            edges[t].append((text[1] + k, "call" if raw[k] == 0xE8 else "jmp"))
fn_of = lambda a: max(f for f in bodies if f <= a)


def wipe(fa, lo, hi):
    I = B(fa)
    return sorted(r for a, x in I.items() if lo <= a <= hi and x.mnemonic == "mov" and x.operands[0].type == X86_OP_MEM and x.operands[0].size in (4, 8)
                  for r in rip(x))


anch = [0x02F97360 + 8 * k for k in range(8)]
check("N0", wipe(0x002498B0, 0x002498BD, 0x002498EE) == anch and wipe(0x002284F0, 0x00228605, 0x00228636) == anch,
      "both wipes store 0 at the eight anchors %s (the last a dword)" % ["%08X" % a for a in anch])
e = sorted((a, fn_of(a), m) for a, m in edges[0x002498B0])
D = B(0x0022A580) if 0x0022A580 in bodies else {}
check("N1", sorted((f, m) for _a, f, m in e) == [(0x0022A770, "call"), (0x0022B8C0, "call"), (0x0022BC20, "call"), (0x00249C30, "jmp")]
      and {(a, f) for a, f, _m in e} >= {(0x0022B908, 0x0022B8C0), (0x0022BC50, 0x0022BC20), (0x00249C4D, 0x00249C30)}
      and any(S(x) == "call 0x314020" for a, x in B(0x0022BC20).items() if a == 0x0022BCCF) and at(D, 0x0022A6A3) == "jmp rcx",
      "edges into 002498B0 %s; 0022BC20 ticks at 0022BCCF; dispatcher %s" % (["%08X in %08X %s" % x for x in e], at(D, 0x0022A6A3)))
W = B(0x00314020)
tk = sorted(a for a, x in W.items() if x.mnemonic == "call" and imm(x) == 0x002E0D90)
lp = sorted(a for a, x in W.items() if x.mnemonic == "call" and imm(x) == 0x00234590)
th = [S(x) for x in md.disasm(blob[OFF(0x002E0D90):OFF(0x002E0D90) + 5], 0x002E0D90)]
check("N2", th == ["jmp 0x253c50"] and edges[0x00253C50] == [(0x002E0D90, "jmp")] and edges[0x00253C70] == [(0x00253C56, "call")]
      and tk == [0x00314137, 0x003141F2] and len(lp) == 2 and lp[0] < tk[0] < lp[1] < tk[1]
      and any(a == 0x00234624 and S(x) == "call 0x313a00" for a, x in B(0x00234590).items()),
      "thunk %s; 00253C50 edges %s; arbiter edges %s; tick: loop calls %s, arbiter calls %s"
      % (th, edges[0x00253C50], ["%08X %s" % x for x in edges[0x00253C70]], ["%08X" % a for a in lp], ["%08X" % a for a in tk]))
EDGE = 0x02F9736A
wr, rd = [], set()
for fa, ins in bodies.items():
    for x in ins:
        for n_, o in enumerate(x.operands):
            if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP and x.address + x.size + o.mem.disp == EDGE:
                if n_ == 0 and x.mnemonic.startswith(("mov", "and", "or", "xor", "add", "sub")) and not x.mnemonic.startswith(("movzx", "movsx")):
                    wr.append((x.address, fa))
                else:
                    rd.add(fa)
want = {EDGE - t for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        if base + 4 * kk + d in want:
            cands.add(text[1] + s + 4 * kk)
lw = set()
for pos in cands:
    for L in range(11, 0, -1):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and EDGE in rip(x):
            if x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov") and not x.mnemonic.startswith(("movzx", "movsx")):
                lw.add(x.address)
            break
A = B(0x00253C70)
edi_all = sorted(a for a, x in A.items() if x.operands and x.operands[0].type == 1 and x.reg_name(x.operands[0].reg) in ("edi", "dil", "di", "rdi"))
# the epilogue's register restore (mov rdi, [rsp + ...]) after the last clear store is not a write "in the body"
restore = [a for a in edi_all if a > 0x002541BC and "rsp" in A[a].op_str]
edi_w = [a for a in edi_all if a not in restore]
nxt = lambda a: sorted(A)[sorted(A).index(a) + 1]
follow = {a: [S(A[nxt(a)]), S(A[nxt(nxt(a))])] for a in edi_w if a != 0x00253D12}
w2a = [r for x in B(0x002A3250).values() if x.address == 0x002A329B for r in rip(x)]
check("N3", sorted(wr) == [(a, 0x00253C70) for a in (0x00253F70, 0x00253FE9, 0x002540C5, 0x0025415F, 0x002541BC)] and sorted(lw) == [a for a, _ in sorted(wr)]
      and edi_w[0] == 0x00253D12 and edi_w[1:] == [0x00254049, 0x00254189, 0x002541F9]
      and all(any(s.startswith("jmp") for s in f) for f in follow.values()) and w2a == [0x02F97368],
      "by-name writers %s (linear %s); edi written at %s (epilogue restore %s), each followed by %s; 002A329B stores %s; functions reading it by name: %d (page: 51)"
      % (["%08X" % a for a, _ in sorted(wr)], sorted("%08X" % a for a in lw), ["%08X" % a for a in edi_w], ["%08X" % a for a in restore], {"%08X" % k: v for k, v in follow.items()}, ["%08X" % r for r in w2a], len(rd)))
seen, frontier = set(), {0x002498B0}
for depth in range(4):
    nf = set()
    for f in frontier:
        if f in seen or f not in bodies:
            continue
        seen.add(f)
        for x in bodies[f]:
            if x.mnemonic in ("call", "jmp") and imm(x) in bodies and not (f <= imm(x) < f + sizes[f]):
                nf.add(imm(x))
    frontier = nf
check("N4", 0x002E0FA0 not in seen, "closure of 002498B0 to depth 3: %d functions, 002E0FA0 absent" % len(seen))
H = B(0x002284F0)
check("N5", sizes[0x002284F0] == 439 and not [e_ for e_ in edges[0x002284F0] if e_[1] == "call"]
      and any("0x308]" in S(H[a]) for a in H if 0x002285D1 <= a <= 0x002285E0) and any(0x01E0C2A4 in rip(H[a]) for a in H if a < 0x00228605),
      "439 B; direct callers %s; +0x308 precondition and the 01E0C2A4 compare precede the wipe" % edges[0x002284F0])
P = B(0x002E0FA0)
loads = sorted(x.address for x in P.values() if x.mnemonic == "movdqu" and x.operands[1].type == X86_OP_MEM)
comb = sorted({x.mnemonic for x in P.values() if x.mnemonic in ("por", "pand", "pandn", "and", "or", "btr", "bts", "pxor")})
covered = rip(P[0x002E0FA9]) == [0x0215F1D0] and rip(P[0x002E0FB4]) == [0x0215F210] and at(P, 0x002E0FD1) == "add rax, 0x20"     and at(P, 0x002E0FC0) == "movdqu xmm0, xmmword ptr [rax - 0x10]" and at(P, 0x002E0FCD) == "movdqu xmm0, xmmword ptr [rax]"
check("N6", covered and comb == ["btr", "por"] and at(P, 0x002E1012) == "btr ebx, 0x13" and at(P, 0x002E1010) == "je 0x2e1016",
      "two 16-byte loads per pass from 0215F1D0 - 0x10 step 0x20 to 0215F210 (rows 0215F1C0..0215F1FF); combining ops %s; %s when 00360360() != 0"
      % (comb, at(P, 0x002E1012)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
