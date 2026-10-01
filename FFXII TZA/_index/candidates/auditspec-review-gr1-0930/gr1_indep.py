"""gr1_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the GR-1 review (2026-09-30).
pefile + capstone only (img.py), certified image, sha asserted. Does NOT use retool / structflow / the package's census.

  T1  the native-command table install 003DC2D0 and the three getters 003DC240 / 003DC270 / 003DC2A0, decoded from the
      bytes: pointer-array address, which table goes in which family slot, entry stride, which qword each getter returns,
      the bound test.
  T2  every table: count dword, handler qwords; unique non-null handlers; each slot's DIR64 relocation; handlers that are
      not a .pdata function start.
  T3  image-wide references (rip-relative and image-base-relative disp32) to the pointer array and the five tables, and
      stored pointers (DIR64 slots) naming them: who else could install a table.
  L1  the lifecycle 002621D0: the phase byte, which getter runs on which phase, where the phase is written.
  A1  image-wide: every qword load r <- [X + 0xA8] (mov / add) in a .pdata function, followed (linear, until r is
      rewritten, 30 instructions) by a NON-indexed access [r + d] whose width covers d mod 0x28 = 0x27, or an imul/shl
      stride formation of 0x28 - the forms S1/S2 (indexed only) cannot see.
"""
import re, struct, sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import img as I

md0 = Cs(CS_ARCH_X86, CS_MODE_64)   # no detail: regex over op_str
IB = I.IB
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
out = []


def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)


def rip_target(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+|\d+)\]", i.op_str)
    if not m:
        return None
    d = int(m.group(2), 0)
    return i.address + i.size + (d if m.group(1) == "+" else -d)


# relocations
I.pe.parse_data_directories(directories=[5])
DIR64 = set()
for blk in getattr(I.pe, "DIRECTORY_ENTRY_BASERELOC", []):
    for e in blk.entries:
        if e.type == 10:
            DIR64.add(IB + e.rva)
PDATA = I.pdata()
STARTS = {b for b, e in PDATA}
P("image sha256 asserted; DIR64 relocations %d; .pdata entries %d" % (len(DIR64), len(PDATA)))

# ---------------- T1
P("\n== T1 table install and getters")
ins = I.dis(0x003DC2D0, 0x59)
arr, fam_tbl, default = None, {}, None
last_lea = None
for i in ins:
    t = rip_target(i)
    if i.mnemonic == "lea" and t is not None:
        last_lea = t
        if i.op_str.startswith("rdi"):
            arr = t
        elif i.op_str.startswith("rax") and default is None:
            default = t
    if i.mnemonic == "mov" and t is not None and i.op_str.startswith("qword ptr [rip"):
        fam_tbl[t] = last_lea
    P("  %08X  %-7s %s%s" % (i.address, i.mnemonic, i.op_str, ("   ; -> %08X" % t) if t is not None else ""))
    if i.mnemonic == "ret":
        break
FAMS = {0: None}
P("pointer array %08X, rep stosq count 0x10 of default table %08X" % (arr, default))
tbls = {"def": default}
for slot, tb in sorted(fam_tbl.items()):
    fam = (slot - arr) // 8
    tbls[fam] = tb
    P("  family %d (array+0x%X) <- table %08X" % (fam, slot - arr, tb))
for g in (0x003DC240, 0x003DC270, 0x003DC2A0):
    gi = I.dis(g, 0x28)
    txt = "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in gi[:9] if i.mnemonic != "int3")
    base = [rip_target(i) for i in gi if rip_target(i)][0]
    P("  getter %08X base %08X: %s" % (g, base, txt))

# ---------------- T2
P("\n== T2 tables")
cmds = []
allh = set()
nonstart = set()
unreloc = []
for fam, tb in tbls.items():
    n = I.d32(tb)
    h = []
    for N in range(n):
        b, p, r = (I.q(tb + 32 * N + o) for o in (8, 0x10, 0x20))
        for o, v in ((8, b), (0x10, p), (0x20, r)):
            if v:
                allh.add(v)
                if v not in STARTS:
                    nonstart.add(v)
                if (tb + 32 * N + o) not in DIR64:
                    unreloc.append("%08X" % (tb + 32 * N + o))
        cmds.append((fam, N, b, p, r))
    # the qword at +0x18 of each entry and the dword pair at +0 - what are they
    x18 = collections.Counter(I.q(tb + 32 * N + 0x18) != 0 for N in range(n))
    P("  family %s table %08X count %d; entries with non-null +0x18 qword: %d" % (fam, tb, n, x18[True]))
P("commands %d; unique non-null handler pointers %d; not a .pdata start: %d %s; slots without DIR64: %d %s"
  % (len(cmds), len(allh), len(nonstart), sorted("%08X" % x for x in nonstart)[:10], len(unreloc), unreloc[:10]))
nb = sum(1 for c in cmds if c[2]); np_ = sum(1 for c in cmds if c[3]); nr = sum(1 for c in cmds if c[4])
P("commands with begin %d / poll %d / result %d; poll or result without begin: %d"
  % (nb, np_, nr, sum(1 for c in cmds if not c[2] and (c[3] or c[4]))))

# ---------------- decode every .pdata function once (no detail)
P("\n== image-wide decode of .pdata functions")
INS = []
seen = set()
for b, e in PDATA:
    if b in seen:
        continue
    seen.add(b)
    d = I.rd(b, e - b)
    if not d:
        continue
    fl = list(md0.disasm(d, b))
    INS.append((b, fl))
P("functions decoded %d, instructions %d" % (len(INS), sum(len(x) for _, x in INS)))

# ---------------- T3
P("\n== T3 references to the pointer array and the tables")
ranges = [("ptrarray", arr, arr + 0x80)] + [("tbl_%s" % f, t, t + 8 + 32 * I.d32(t) + 8) for f, t in tbls.items()]
hits = collections.defaultdict(list)
for f, fl in INS:
    for i in fl:
        t = rip_target(i)
        cands = []
        if t is not None:
            cands.append(("rip", t))
        for m in re.finditer(r"\[(\w+)(?: \+ \w+\*\d)? \+ (0x[0-9a-f]{6,8})\]", i.op_str):
            if m.group(1) != "rip":
                cands.append(("ib", IB + int(m.group(2), 16)))
        for form, t in cands:
            for nm, lo, hi in ranges:
                if lo <= t < hi:
                    hits[nm].append("%08X %s %s %s [%s +0x%X]" % (i.address, form, i.mnemonic, i.op_str, nm, t - lo))
stored = collections.defaultdict(list)
for va in DIR64:
    for nm, lo, hi in ranges:
        v = I.q(va)
        if v is not None and lo <= v < hi:
            stored[nm].append("%08X" % va)
for nm, lo, hi in ranges:
    P("  %s %08X..%08X: code refs %d; stored pointers %d" % (nm, lo, hi, len(hits[nm]), len(stored[nm])))
    for s in hits[nm][:12]:
        P("     ", s)
    for s in stored[nm][:6]:
        P("      stored at", s)

# ---------------- L1
P("\n== L1 lifecycle 002621D0 (phase byte, getter by phase)")
for i in I.dis(0x002621D0, 0x1D0):
    s = "%s %s" % (i.mnemonic, i.op_str)
    if "0x15]" in s or "0x3dc2" in s or "0x3dc240" in s or s.startswith("call rax") or ("rdi + 0x18" in s) \
            or (i.mnemonic in ("cmp", "je", "jne", "jae", "test") and 0x00262240 <= i.address <= 0x00262310) \
            or "rdi + 0xc]" in s:
        P("  %08X  %s" % (i.address, s))
    if i.mnemonic == "ret":
        break

# ---------------- A1
P("\n== A1 non-indexed / non-lea-x5 uses of a [X + 0xA8] qword load, image-wide")
WAIT7 = {0x0025B400, 0x0025DF00, 0x0025E4C0, 0x002651A0, 0x0026B4C0, 0x0026B4E0, 0x003DBDC0}
FAM = {}
for fam in (("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
            ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl")):
    for r in fam:
        FAM[r] = fam[0]
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (n, suf)] = "r%d" % n
loads = 0
direct, strided, fn_with = [], [], set()
for f, fl in INS:
    for k, i in enumerate(fl):
        m = re.match(r"(r\w+), qword ptr \[(\w+) \+ 0xa8\]$", i.op_str)
        if not (m and i.mnemonic in ("mov", "add")):
            continue
        loads += 1
        r = FAM.get(m.group(1), m.group(1))
        for j in fl[k + 1:k + 31]:
            ops = j.op_str.split(", ")
            dst = FAM.get(ops[0], ops[0]) if ops else ""
            mm = re.search(r"(byte|word|dword|qword|xmmword) ptr \[(\w+) \+ (0x[0-9a-f]+|\d+)\]", j.op_str)
            if mm and FAM.get(mm.group(2), mm.group(2)) == r:
                d, w = int(mm.group(3), 0), W[mm.group(1)]
                if any((d + x) % 0x28 == 0x27 for x in range(w)):
                    direct.append((f, "%08X %s %s" % (j.address, j.mnemonic, j.op_str)))
            if j.mnemonic == "imul" and ("0x28" in j.op_str):
                strided.append((f, "%08X %s %s" % (j.address, j.mnemonic, j.op_str)))
            if dst == r and j.mnemonic in ("mov", "lea", "xor", "pop", "movzx", "movsxd", "call") and "[%s" % r not in j.op_str:
                break
            if j.mnemonic in ("ret", "call") and r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                break
P("qword loads/adds of [X + 0xA8]: %d" % loads)
P("non-indexed accesses through the loaded register whose width covers +0x27 (mod 0x28): %d" % len(direct))
for f, s in direct:
    P("   in %08X%s: %s" % (f, " (one of the seven)" if f in WAIT7 else "", s))
P("imul by 0x28 within 30 instructions of such a load: %d" % len(strided))
for f, s in strided:
    P("   in %08X%s: %s" % (f, " (one of the seven)" if f in WAIT7 else "", s))

open(sys.argv[1] if len(sys.argv) > 1 else "gr1_indep.out", "w").write("\n".join(out) + "\n")
