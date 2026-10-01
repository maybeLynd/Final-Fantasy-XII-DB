"""fe4_ranges.py - FE-4: the battle-stats record's last unaccounted bytes, and the routes the original field scan did not
follow (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  R1 four of the five residual gaps are alignment padding, read from the widths the page's own accesses file records:
     +0x22..+0x23 lie between a word at +0x20 and a dword at +0x24; +0x4F between a byte at +0x4E and the qword-
     initialised +0x50; +0xBB between a byte at +0xBA and the dword array at +0xBC; +0x1C6..+0x1C7 between a byte at
     +0x1C5 and the 0x1C8 stride (the forming code's imul 0x1C8).
  R2 the page's +0x05C row is stale: its three accesses (00386E43, 00386E56, 00386EEC) are [r14 + r12 - 0x60] with
     r14 = stats + 0xBC + 4i (lea at 00386C90) and r12 = rdx - rsi = result - stats (00386CBE / 00386CC6), so they
     address result + 0x5C + 4i - FE-3's 2026-09-13 answer. No stats-record access at +0x5C remains.
  R3 the array seed repaired: 68 functions either read 02EBF190 and use the 0x1C8 stride, or call the record getter
     00320A40. None of them reaches the record at +0x5C..+0x63. Each access covering those displacements is classified:
     its base is a 0035D330 layout record, the battle unit (00310DEC), the unit's spawn record ([unit + 0x6A0], a 16-byte
     store at 003079F4), or it is a qword pointer-width field at +0x58 /
     +0x60, which the record cannot hold there (its +0x58 is the u16 equipment slot 4, read only as a word).
  R4 pointers stored into other objects: every 'mov R, qword [X + 0x698]' (the battle unit's stats pointer) and every
     getter result is followed forward, and into callees receiving it in rcx/rdx/r8/r9, to depth 3. Nothing touches
     +0x5C..+0x63. Positive controls on the same follower: +0x24 (max HP) and +0x64 (status word 1) are found.
  R5 the getter's result is never stored to non-stack memory at any of its call sites.
Prints PASS/FAIL per check; exit 1 on any FAIL. Takes a few minutes (R3/R4 disassemble the image).
"""
import bisect, csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
FS = sorted(SIZES)
def owner(a):
    i = bisect.bisect_right(FS, a) - 1
    return FS[i] if i >= 0 and a < FS[i] + SIZES[FS[i]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
DIS = {}
def ins(f):
    if f not in DIS:
        o = off(f); DIS[f] = list(cs.disasm(d[o:o + SIZES.get(f, 0x200)], f)) if o is not None and SIZES.get(f, 0) > 0 else []
    return DIS[f]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}

acc = list(csv.DictReader(open(DB / "08-Combat-Formula/Battle-Stats-Record/battle-stats-record-accesses.tsv", encoding="utf-8"), delimiter="\t"))
def widths(disp):
    out = set()
    for r in acc:
        if r["disp"] == disp:
            m = re.search(r"(byte|word|dword|qword|xmmword) ptr", r["instruction"])
            if m: out.add(W[m.group(1)])
    return out
w20, w24, w4e, w50, wbc = (widths(x) for x in ("0x20", "0x24", "0x4E", "0x50", "0xBC"))
def site(f, a): return next(("%s %s" % (x.mnemonic, x.op_str) for x in ins(f) if x.address == a), "")
# +0xBA and +0x1C5 were found outside the census (section 2.3b): their writers, read directly
wba = {1} if site(0x327CB0, 0x327D84) == "mov byte ptr [rdi + 0xba], bl" else set()
w1c5 = {1} if site(0x323740, 0x323779) == "mov byte ptr [r8 + 0x1c5], dl" and site(0x3236F0, 0x323729) == "mov byte ptr [r8 + 0x1c5], dl" else set()
stride = any("0x1c8" in "%s %s" % (x.mnemonic, x.op_str) for x in ins(0x320A40))
check("R1 four gaps are alignment padding (widths from the accesses file and the two writers; stride 0x1C8 in the getter)",
      2 in w20 and max(w20) <= 2 and 4 in w24 and w4e == {1} and 8 in w50 and wba == {1} and 4 in wbc and w1c5 == {1} and stride,
      "+0x20 %s +0x24 %s +0x4E %s +0x50 %s +0xBA %s +0xBC %s +0x1C5 %s" % (sorted(w20), sorted(w24), sorted(w4e), sorted(w50), sorted(wba), sorted(wbc), sorted(w1c5)))

g = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(0x386C70)}
rows5c = [r for r in acc if r["disp"] == "0x5C"]
check("R2 the +0x05C census rows are the result record's +0x5C + 4i",
      {r["site"] for r in rows5c} == {"00386E43", "00386E56", "00386EEC"} and all("[r14 + r12 - 0x60]" in r["instruction"] for r in rows5c)
      and g.get(0x386C90) == "lea r14, [rcx + 0xbc]" and g.get(0x386CBE) == "mov r12, rdx" and g.get(0x386CC6) == "sub r12, rsi"
      and g.get(0x386CA6) == "mov rsi, rcx")

RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
T0, TO, TS = [(BASE + v, ro, rs) for vs, v, rs, ro in secs if v == 0x1000][0]
tb = d[TO:TO + TS]
getter_sites = [T0 + i for i in range(len(tb) - 5) if tb[i] == 0xE8 and T0 + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == 0x320A40]
seed = set(owner(s) for s in getter_sites if owner(s))
for f in FS:
    if not (0x121000 <= f < 0x8C0000): continue
    L = ins(f)
    if not any("0x1c8" in x.op_str for x in L): continue
    for x in L:
        m = RIP.search(x.op_str)
        if m and x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) == 0x2EBF190:
            seed.add(f); break
M = re.compile(r"(byte|word|dword|qword|xmmword|ymmword) ptr \[(\w+)(?: \+ \w+(?:\*\d)?)? \+ (0x[0-9a-f]+|\d+)\]")
cover = []
for f in sorted(seed):
    for x in ins(f):
        for m in M.finditer(x.op_str):
            disp = int(m.group(3), 0); w = W[m.group(1)]
            if disp <= 0x63 and disp + w > 0x5C and m.group(2) not in ("rsp", "rbp", "rip"): cover.append(x.address)
def provenance(a):
    """what the access's base register last held: 'layout' (a 0035D330 result), 'unit' (00310DB0's rcx), else '?'"""
    f = owner(a); L = ins(f)
    k = [i for i, x in enumerate(L) if x.address == a][0]
    base = M.search(L[k].op_str).group(2)
    if f == 0x310DB0 and base == "rsi": return "unit"
    want = base
    for x in reversed(L[:k]):
        dst = x.op_str.split(",")[0].strip()
        if x.mnemonic == "call" and want == "rax": return "layout" if x.op_str == "0x35d330" else "?"
        if dst == want and x.mnemonic == "mov":
            src = x.op_str.split(",", 1)[1].strip()
            if re.fullmatch(r"qword ptr \[\w+ \+ 0x6a0\]", src): return "spawn-record"
            if re.fullmatch(r"r\w+", src): want = src; continue
            return "?"
    return "?"
prov = {a: provenance(a) for a in cover}
def by_width(a):
    """a qword access at +0x58 or +0x60: a pointer-width field, which the stats record cannot hold there (+0x58 is the
    u16 equipment slot 4, read only as a word in the accesses file)"""
    x = next(y for y in ins(owner(a)) if y.address == a)
    m = M.search(x.op_str)
    return m.group(1) == "qword" and int(m.group(3), 0) in (0x58, 0x60)
for a in list(prov):
    if prov[a] == "?" and by_width(a): prov[a] = "pointer-width"
w58 = widths("0x58")
check("R3 the repaired seed: no access to the record's +0x5C..+0x63 - every covering displacement is a 0035D330 layout record, the battle unit, its spawn record, or a qword pointer field at +0x58/+0x60 (the record's +0x58 is a u16, read only as a word)",
      len(seed) >= 60 and all(v in ("layout", "unit", "pointer-width", "spawn-record") for v in prov.values()) and "unit" in prov.values() and w58 == {2},
      "seed %d; covering sites %d, by base %s; unresolved %s" % (len(seed), len(cover), dict(__import__("collections").Counter(prov.values())), ["%08X" % a for a, v in prov.items() if v == "?"]))

ACC = re.compile(r"(byte|word|dword|qword|xmmword|ymmword) ptr \[(r\w+) \+ (0x[0-9a-f]+|\d+)\]")
LOAD = re.compile(r"^(r\w+), qword ptr \[\w+(?: \+ \w+(?:\*\d)?)? \+ 0x698\]$")
ARGS = ("rcx", "rdx", "r8", "r9"); NV = ("rbx", "rsi", "rdi", "rbp", "r12", "r13", "r14", "r15")
R32 = {"rax": "eax", "rbx": "ebx", "rcx": "ecx", "rdx": "edx", "rsi": "esi", "rdi": "edi", "rbp": "ebp", "r8": "r8d", "r9": "r9d",
       "r10": "r10d", "r11": "r11d", "r12": "r12d", "r13": "r13d", "r14": "r14d", "r15": "r15d"}
def follow(L, k0, regs, depth, lo, hi, hits, seen):
    regs = set(regs)
    for y in L[k0:k0 + 80]:
        for a in ACC.finditer(y.op_str):
            if a.group(2) in regs:
                disp = int(a.group(3), 0); w = W[a.group(1)]
                if disp <= hi and disp + w > lo: hits.add(y.address)
        m = re.match(r"(r\w+), (r\w+)$", y.op_str)
        if y.mnemonic == "mov" and m and m.group(2) in regs: regs.add(m.group(1)); continue
        if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"):
            t = int(y.op_str, 16); passed = [r for r in ARGS if r in regs]
            if passed and depth > 0 and t in SIZES and (t, tuple(passed), lo) not in seen:
                seen.add((t, tuple(passed), lo)); follow(ins(t), 0, passed, depth - 1, lo, hi, hits, seen)
            if y.mnemonic == "jmp": return
            regs = {r for r in regs if r in NV}
            if not regs: return
            continue
        if y.mnemonic == "ret": return
        dst = y.op_str.split(",")[0].strip()
        for r in list(regs):
            if dst in (r, R32.get(r)) and y.mnemonic in ("mov", "lea", "movzx", "movsx", "xor", "pop", "add", "sub", "imul", "and", "or"):
                regs.discard(r)
        if not regs: return
sources = []
for f in FS:
    if not (0x121000 <= f < 0x8C0000): continue
    L = ins(f)
    for k, x in enumerate(L):
        if x.mnemonic == "mov":
            m = LOAD.match(x.op_str)
            if m: sources.append((L, k + 1, m.group(1)))
        if x.mnemonic == "call" and x.op_str == "0x320a40": sources.append((L, k + 1, "rax"))
res = {}
for lo, hi in ((0x5C, 0x63), (0x24, 0x27), (0x64, 0x67)):
    hits = set(); seen = set()
    for L, k, r in sources: follow(L, k, [r], 3, lo, hi, hits, seen)
    res[(lo, hi)] = len(hits)
check("R4 the unit's +0x698 pointer and the getter's result, followed to depth 3: nothing at +0x5C..+0x63; controls found",
      res[(0x5C, 0x63)] == 0 and res[(0x24, 0x27)] >= 3 and res[(0x64, 0x67)] >= 100 and len(sources) >= 500,
      "sources %d; hits +0x5C..+0x63 %d, control +0x24 %d, control +0x64 %d" % (len(sources), res[(0x5C, 0x63)], res[(0x24, 0x27)], res[(0x64, 0x67)]))

stores = 0
for s in getter_sites:
    f = owner(s); L = ins(f)
    k = [i for i, x in enumerate(L) if x.address == s]
    if not k: continue
    regs = {"rax"}
    for y in L[k[0] + 1:k[0] + 30]:
        m = re.match(r"(r\w+), (r\w+)$", y.op_str)
        if y.mnemonic == "mov" and m and m.group(2) in regs: regs.add(m.group(1))
        m2 = re.match(r"qword ptr \[(\w+)[^\]]*\], (r\w+)$", y.op_str)
        if y.mnemonic == "mov" and m2 and m2.group(2) in regs and m2.group(1) != "rsp": stores += 1
        if y.mnemonic == "call": regs = {r for r in regs if r in NV}
check("R5 the getter's result is never stored to non-stack memory", stores == 0 and len(getter_sites) >= 20, "%d call sites" % len(getter_sites))
print("FAILS", fails)
sys.exit(1 if fails else 0)
