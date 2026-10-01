"""Falsification pass 1 on CONTRACT-ui-request-router (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. Censuses decode every function to
the larger of its catalogue size and its .pdata chain union.

  U0  section 2 sizes: 263 / 85 / 1,002 / 193 / 29 / 71 / 123 / 104 B
  U1  section 3: `and` with 0x7FFF at 00254B69; ids 1..24 index the byte table 00254C70, whose value indexes the dword RVA table
      00254C58 (+ image base); the decoded arms map 1,4 -> 00254BFB; 3 -> 00254C04; 5 -> 00254C0D; 12 -> 00254C16; 24 -> 00254C24;
      the rest -> 00254C2D; 00254C37 passes ebp (the raw request) to the generic scheduler
  U2  section 4: R-a `cmp [02092734], 1` at 00254B71 precedes the policy call 002E0FA0; R-b `bt` at 00254BC1; R-c tests root
      +0xB8 / +0xC0 at 00280A1A / 00280A28; the inhibit table 01E0C2C0 has 22 dwords, 9 non-zero, union 0x20402E (ids 1, 2, 3, 5, 14, 21)
  U3  section 5: 0215F1A4 and 0215F1A8 each have the same five writing functions (002E1B10, 002E1A60, 002E1AE0, 002E09A0,
      002E15D0) and one reading function (002E09A0); 0215F1A0 the same five writers and readers {002E09A0, 002E12D0}; 0215F1A1
      writers {002E09A0, 002E15D0, 002E1690}, readers {002E1B10, 002E1A60, 002E1AE0, 002E25B0}; the post's producer sites are
      00253D78, 00253EE6, 00253F44, 00253F53, 0035C81E, 0035D750 and the tail-jump 0050DAC4
  U4  R-1 / R-2: 002E1B3C `mov eax, 1`; the post calls 002E0FA0 only on the id-2 path and tests bit 0 of its result
  U5  R-3: 00252B40 masks the id and writes 02092734, 020927D8 and 02092730, then tail-jumps 00254740; the router body 00254B50
      stores to none of them
  U6  R-4: 02092734 is read by exactly three functions (00254B50 at 00254B71, 00253C70 at 00253FE3, 003F4E70); cleared only at
      00252DCB and 00252E05, set only by 00252B40
  U7  R-5: 002E09A0 has one call site, 0031427D, in World_UpdateSimulationTick, after the arbiter call sites 00314137 / 003141F2
  U8  R-6: 00280A00 tests both root slots before the 00252B40 call at 00280A60, and mounts the procs 0027FB70 and 00280140
"""
import collections, io, os, struct
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
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
is_w = lambda x, k: k == 0 and x.mnemonic.startswith(("mov", "and", "or", "add", "sub", "inc", "dec", "set", "xchg")) and not x.mnemonic.startswith(("movzx", "movsx"))

acc = collections.defaultdict(lambda: {"w": set(), "r": set(), "wa": set(), "ra": set()})
calls = collections.defaultdict(list)
CELLS = (0x0215F1A0, 0x0215F1A1, 0x0215F1A4, 0x0215F1A8, 0x02092734, 0x02092730, 0x020927D8)
for fa, ins in bodies.items():
    for x in ins:
        for k, o in enumerate(x.operands):
            if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                t = x.address + x.size + o.mem.disp
                if t in CELLS:
                    kind = "w" if is_w(x, k) else "r"
                    acc[t][kind].add(fa); acc[t][kind + "a"].add(x.address)
        if x.mnemonic in ("call", "jmp") and imm(x) in (0x002E1B10, 0x002E09A0, 0x00280A00, 0x002E0FA0):
            if not (fa <= imm(x) < fa + sizes[fa]):
                calls[imm(x)].append((x.address, fa, x.mnemonic))

F = [0x00254B50, 0x002E1B10, 0x002E09A0, 0x00280A00, 0x00252B40, 0x00252D90, 0x002E1A60, 0x002E0DA0]
check("U0", [sizes[f] for f in F] == [263, 85, 1002, 193, 29, 71, 123, 104], "%s" % [sizes[f] for f in F])
R = B(0x00254B50)
arm = list(blob[OFF(0x00254C70):OFF(0x00254C70) + 24])
rva = struct.unpack("<6I", blob[OFF(0x00254C58):OFF(0x00254C58) + 24])
tgt = {i + 1: BASE + rva[arm[i]] for i in range(24)}
groups = collections.defaultdict(list)
for i, t in tgt.items():
    groups[t].append(i)
exp = {0x00254BFB: [1, 4], 0x00254C04: [3], 0x00254C0D: [5], 0x00254C16: [12], 0x00254C24: [24],
       0x00254C2D: [2, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}
check("U1", "0x7fff" in at(R, 0x00254B69) and dict(groups) == exp and at(R, 0x00254C37).endswith("ebp") ,
      "mask %s; arms %s; raw pass %s" % (at(R, 0x00254B69), {("%08X" % k): v for k, v in sorted(groups.items())}, at(R, 0x00254C37)))
tab = struct.unpack("<22I", blob[OFF(0x01E0C2C0):OFF(0x01E0C2C0) + 88])
un = 0
for v in tab:
    un |= v
pol = [a for a, x in R.items() if x.mnemonic == "call" and imm(x) == 0x002E0FA0]
G = B(0x00280A00)
check("U2", rip(R[0x00254B71]) == [0x02092734] and R[0x00254B71].mnemonic == "cmp" and pol and min(pol) > 0x00254B71 and R[0x00254BC1].mnemonic == "bt"
      and {at(G, 0x00280A1A), at(G, 0x00280A28)} == {"cmp qword ptr [rax + 0xb8], 0", "cmp qword ptr [rax + 0xc0], 0"} and sum(1 for v in tab if v) == 9 and un == 0x20402E,
      "latch %s before the policy call at %s; %s; root %s / %s; table non-zero %d, union %X" %
      (at(R, 0x00254B71), ["%08X" % a for a in pol], at(R, 0x00254BC1), at(G, 0x00280A1A), at(G, 0x00280A28), sum(1 for v in tab if v), un))
FIVE = {0x002E1B10, 0x002E1A60, 0x002E1AE0, 0x002E09A0, 0x002E15D0}
posts = sorted((a, m) for a, _f, m in calls[0x002E1B10])
check("U3", acc[0x0215F1A4]["w"] == FIVE and acc[0x0215F1A8]["w"] == FIVE and acc[0x0215F1A4]["r"] == {0x002E09A0} and acc[0x0215F1A8]["r"] == {0x002E09A0}
      and acc[0x0215F1A0]["w"] == FIVE and acc[0x0215F1A0]["r"] == {0x002E09A0, 0x002E12D0}
      and acc[0x0215F1A1]["w"] == {0x002E09A0, 0x002E15D0, 0x002E1690} and acc[0x0215F1A1]["r"] == {0x002E1B10, 0x002E1A60, 0x002E1AE0, 0x002E25B0}
      and posts == [(0x00253D78, "call"), (0x00253EE6, "call"), (0x00253F44, "call"), (0x00253F53, "call"), (0x0035C81E, "call"), (0x0035D750, "call"), (0x0050DAC4, "jmp")],
      "cells (writers / readers): %s; producer sites %s" % ({"%08X" % c: (sorted("%08X" % f for f in acc[c]["w"]), sorted("%08X" % f for f in acc[c]["r"]))
                                                             for c in (0x0215F1A0, 0x0215F1A1, 0x0215F1A4, 0x0215F1A8)}, ["%08X %s" % p for p in posts]))
P = B(0x002E1B10)
pc = [a for a, x in P.items() if x.mnemonic == "call" and imm(x) == 0x002E0FA0]
check("U4", at(P, 0x002E1B3C) == "mov eax, 1" and len(pc) == 1 and any(S(P[a]).startswith("cmp ecx, 2") or S(P[a]).startswith("cmp ebx, 2") or S(P[a]).startswith("cmp edi, 2")
      or (P[a].mnemonic == "cmp" and P[a].op_str.endswith(", 2")) for a in P if a < pc[0])
      and any(P[a].mnemonic in ("test", "bt") and ("1" in P[a].op_str.split(", ")[-1]) for a in P if pc[0] < a <= 0x002E1B33),
      "post returns %s; policy call %s, behind an id-2 compare, bit-0 test after" % (at(P, 0x002E1B3C), ["%08X" % a for a in pc]))
W = B(0x00252B40)
wset = {t for x in W.values() for k, o in enumerate(x.operands) if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP and is_w(x, k)
        for t in [x.address + x.size + o.mem.disp]}
rst = {t for x in R.values() for k, o in enumerate(x.operands) if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP and is_w(x, k)
       for t in [x.address + x.size + o.mem.disp]}
check("U5", {0x02092734, 0x020927D8, 0x02092730} <= wset and any("0x7fff" in S(x) for x in W.values()) and any(S(x) == "jmp 0x254740" for x in W.values())
      and not (rst & {0x02092734, 0x020927D8, 0x02092730}),
      "00252B40 writes %s and tail-jumps 00254740; the router writes %s" % (sorted("%08X" % t for t in wset), sorted("%08X" % t for t in rst)))
L = acc[0x02092734]
check("U6", L["r"] == {0x00254B50, 0x00253C70, 0x003F4E70} and 0x00253FE3 in L["ra"] and 0x00254B71 in L["ra"]
      and L["w"] <= {0x00252B40, 0x00252D90, 0x00252DE0} and {0x00252DCB, 0x00252E05} <= L["wa"],
      "readers %s; writers %s at %s" % (sorted("%08X" % f for f in L["r"]), sorted("%08X" % f for f in L["w"]), sorted("%08X" % a for a in L["wa"])))
dr = calls[0x002E09A0]
check("U7", [(a, f) for a, f, _m in dr] == [(0x0031427D, 0x00314020)] and 0x00314137 < 0x0031427D and 0x003141F2 < 0x0031427D,
      "drain call sites %s" % ["%08X in %08X" % (a, f) for a, f, _m in dr])
first_set = min(a for a, x in G.items() if x.mnemonic == "call" and imm(x) == 0x00252B40)
mounts = [rip(x)[0] for a, x in sorted(G.items()) if x.mnemonic == "lea" and rip(x) and rip(x)[0] in (0x0027FB70, 0x00280140)]
check("U8", first_set == 0x00280A60 and 0x00280A1A < first_set and 0x00280A28 < first_set and sorted(set(mounts)) == [0x0027FB70, 0x00280140],
      "root tests at 00280A1A / 00280A28, then 00252B40 at %08X; widget procs %s" % (first_set, ["%08X" % m for m in mounts]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
