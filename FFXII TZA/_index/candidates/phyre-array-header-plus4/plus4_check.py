"""The PArray / PSharray header dword at +0x4 (OPUS, 2026-09-27, OPUS-STRUCT-PHYRE-ARRAY-PLUS4).
Question: is +0x4 a field some path reads or writes, or unused bytes between the u32 count and the 8-aligned pointer?
  Q1 the member vtables: slots 4/6/7 (count / element accessors) are shared by every instantiation; slots 5 and 8
     (resize / set-from-buffer) are PER ELEMENT TYPE - so "the" resize/adopt of a family is not one function
  Q2 every slot-5/8 entry of the 59 PhyreArray and 10 PhyreSharray vtables, their tail-jump targets and direct callees:
     no operand at [reg + 4]; POSITIVE control: the same scan sees the +8 pointer store in 0062A870
  Q3 image-wide: 812-ish dword loads followed by btr 0x1f (a Phyre-style count); accesses at [same base + 4] within
     24 instructions land only in the four known non-array functions (an item-record bitfield merge, a tagged-chunk
     walker); POSITIVE control: most of those loads have a +8 access nearby
  Q4 the cluster-load array fix-up 0059C250 writes the header as a QWORD zero at the field (0059C5E8, r12 = 0 from
     0059C286), the field being object + member[+0x48] - class[+0xF4], and only then calls the member's slot-8 setter
     (0059C5FC): after a load, +4 is 0 - the dword is cleared with the count, never written on its own
  Q5 the by-value setter 00672F30 (PSharray<PDataBlockBufferD3D11>) copies the 0x48-byte element inline at count one
     and stores the TAsyncUpdate<PDataBlockD3D11> vtable 00D68DD0 at element +0x28 (corroborates 3d95e439c)
  S  REGRESSION: both +0x4 rows state the zeroing fix-up and the reach; the PSharray m_u row and page section 20 no
     longer present one resize/adopt pair as the family's (FAILS before)
Not claimed: that +4 is compiler padding (a reading consistent with every observation, not proven: indirect accesses
and untraced code are outside the reach); the value on the create path (copied from each class's default instance).
"""
import os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
SZ = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    try: SZ[int(c[0], 16)] = int(c[2])
    except: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size=None): return list(cs.disasm(d[off(a):off(a) + (size or SZ.get(a, 0x200))], a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

# Q1 vtable slots
VT = {"PhyreArray": [], "PhyreSharray": []}
for l in open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "members", "rtti-class-vtables.tsv"), encoding="utf-8"):
    r = l.rstrip("\n").split("\t")
    m = re.match(r"\.\?AV\?\$PClassDataMember(PhyreArray|PhyreSharray)@", r[0])
    if m and len(r) > 2 and r[2]:
        v = int(r[2], 16); VT[m.group(1)].append([struct.unpack_from("<Q", d, off(v) + 8 * i)[0] for i in range(9)])
def distinct(fam, s): return sorted({q[s] for q in VT[fam]})
shared = all(len(distinct(f, s)) == 1 for f in VT for s in (4, 6, 7))
nv = {f: [len(distinct(f, s)) for s in (5, 8)] for f in VT}
check("Q1 59 + 10 member vtables: slots 4/6/7 shared, slots 5/8 per element type",
      len(VT["PhyreArray"]) == 59 and len(VT["PhyreSharray"]) == 10 and shared
      and nv["PhyreSharray"] == [5, 5] and nv["PhyreArray"][0] > 1 and nv["PhyreArray"][1] > 1,
      "resize/set variants: PArray %s, PSharray %s" % (nv["PhyreArray"], nv["PhyreSharray"]))

# Q2 register-offset trace from the field address every slot entry computes (object + member[+0x48] - class[+0xF4]),
# through register copies, lea / add displacement, tail jumps and calls (argument registers carried). A register copy
# UNIONS offsets (over-approximation); any other write kills the register, EXCEPT in a block that runs straight to `ret`
# (an epilogue restore on an early-return path must not hide the main path); calls clobber the volatile registers; two
# sweeps carry loop state. Errors lean toward reporting +4, not hiding it.
R32 = {"e" + r: "r" + r for r in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp")}
def full(r):
    if r in R32: return R32[r]
    m = re.match(r"(r\d+)[dwb]$", r)
    return m.group(1) if m else r
SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
IMM = r"(0x[0-9a-f]+|\d+)$"
ACC = []; SEEN = set()
def trace(fa, state, depth=0):
    key = (fa, frozenset((r, frozenset(v)) for r, v in state.items()))
    if key in SEEN or depth > 4 or off(fa) is None: return
    SEEN.add(key); st = {r: set(v) for r, v in state.items()}; I = ins(fa)
    epi = set(); tail = False
    for k in range(len(I) - 1, -1, -1):
        if I[k].mnemonic == "ret": tail = True
        elif I[k].mnemonic.startswith("j") or I[k].mnemonic == "call": tail = False
        if tail: epi.add(k)
    def kill(r):
        if k not in epi: st.pop(full(r), None)
    for rnd in range(2):  # a second sweep carries offsets gained late in the body back to earlier uses (loops)
        for k, x in enumerate(I):
            ops = [o.strip() for o in x.op_str.split(",")] if x.op_str else []
            for o in ops:
                m = re.search(r"(?:(byte|word|dword|qword|xmmword) ptr )?\[(\w+)(?: \+ (\w+)\*\d)?(?: ([+-]) (0x[0-9a-f]+|\d+))?\]", o)
                if m and full(m.group(2)) in st:
                    disp = int(m.group(5), 0) * (-1 if m.group(4) == "-" else 1) if m.group(5) else 0
                    for v in st[full(m.group(2))]:
                        ACC.append((x.address, x.mnemonic, v + disp, SIZE.get(m.group(1), 0), bool(m.group(3))))
            if x.mnemonic == "movsxd" and k + 1 < len(I) and any(y.mnemonic == "sub" and "[rax + 0xf4]" in y.op_str for y in I[max(0, k - 3):k]) \
                    and I[k + 1].mnemonic == "add" and I[k + 1].op_str == "%s, rdx" % ops[0]:
                st.setdefault(ops[0], set()).add(0)
            elif x.mnemonic == "add" and len(ops) == 2 and full(ops[0]) in st and re.match(IMM, ops[1]):
                st[full(ops[0])] |= {v + int(ops[1], 0) for v in st[full(ops[0])] if v < 0x100}
            elif x.mnemonic == "mov" and len(ops) == 2 and re.match(r"r\w+$", ops[0]) and re.match(r"r\w+$", ops[1]) \
                    and ops[0] == full(ops[0]) and full(ops[1]) in st:
                st.setdefault(ops[0], set()).update(st[full(ops[1])])
            elif x.mnemonic == "lea" and len(ops) == 2 and ops[0] == full(ops[0]):
                m = re.match(r"\[(\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]$", ops[1])
                if m and full(m.group(1)) in st:
                    dd = int(m.group(3), 0) * (-1 if m.group(2) == "-" else 1) if m.group(3) else 0
                    st[ops[0]] = {v + dd for v in st[full(m.group(1))]}
                else: kill(ops[0])
            elif x.mnemonic == "call" and x.op_str.startswith("0x") and int(x.op_str, 16) != 0x584730:
                args = {r: st[r] for r in ("rcx", "rdx", "r8", "r9") if r in st}
                if args: trace(int(x.op_str, 16), args, depth + 1)
            if x.mnemonic == "call":
                for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"): kill(r)
            elif x.mnemonic == "jmp" and x.op_str.startswith("0x"):
                t = int(x.op_str, 16)
                if not fa <= t < fa + SZ.get(fa, 0x200): trace(t, st, depth + 1)
            elif ops and re.match(r"[a-z]\w*$", ops[0]) and x.mnemonic not in ("cmp", "test", "push", "bt", "add", "movsxd") \
                    and not (x.mnemonic in ("mov", "lea") and len(ops) == 2 and full(ops[1].split()[0].strip("[")) in st):
                kill(ops[0])
entries = set()
for f in VT:
    for s in (4, 5, 6, 7, 8): entries |= set(distinct(f, s))
for e in entries: trace(e, {})
def overlaps4(o, s): return s and o < 8 and o + s > 4
# DETECTOR CONTROL: seed 0057DAD0's rcx at -8, so its `lea rbx,[rcx+8]` / `mov word [rbx+4]` is a header +4 write
n_real = len(ACC); trace(0x57DAD0, {"rcx": {-8}})
ctrl = [a for a, mn, o, s, ix in ACC[n_real:] if overlaps4(o, s)]; del ACC[n_real:]
check("Q2c the trace reports a seeded +4 write (0057DAD0 with rcx = header - 8)", 0x57DB76 in ctrl, str(["%08X" % a for a in ctrl[:4]]))
hit4 = sorted({"%08X %s @%+d/%d" % (a, mn, o, s) for a, mn, o, s, ix in ACC if overlaps4(o, s) and not (o == 0 and s == 8)})
q0 = sorted({"%08X" % a for a, mn, o, s, ix in ACC if o == 0 and s == 8})
seen = {(o, s) for a, mn, o, s, ix in ACC}
check("Q2 header trace from %d slot entries (%d accesses): +4 never accessed alone; controls +0 dword, +8 qword, +0x48 inline copy"
      % (len(entries), len(ACC)), not hit4 and (0, 4) in seen and (8, 8) in seen and (0x48, 8) in seen,
      "+4 hits %s; whole-qword +0 accesses %s" % (hit4[:6], q0[:6]))

# Q3 image-wide census
KNOWN = {0x57DAD0, 0x57DC30, 0x57DED0, 0x2DF070}
loads = near8 = 0; hits4 = set()
for fa, fsz in SZ.items():
    if fsz <= 0 or fsz > 30000 or off(fa) is None: continue
    I = ins(fa, fsz)
    for i, x in enumerate(I):
        m = re.match(r"(e\w\w|r\d+d), dword ptr \[(r\w+)(?: \+ (0x[0-9a-f]+))?\]$", x.op_str)
        if x.mnemonic != "mov" or not m: continue
        if not any(y.mnemonic == "btr" and y.op_str == m.group(1) + ", 0x1f" for y in I[i + 1:i + 4]): continue
        base, h = m.group(2), int(m.group(3) or "0", 16); loads += 1
        win = I[max(0, i - 24):i + 24]
        if any("[%s + 0x%x]" % (base, h + 8) in y.op_str for y in win): near8 += 1
        if any("[%s + 0x%x]" % (base, h + 4) in y.op_str for y in win): hits4.add(fa)
check("Q3 image census: +4 accesses only in the four non-array functions", loads > 700 and near8 > loads // 2 and hits4 == KNOWN,
      "loads %d, +8 nearby %d, +4 functions %s" % (loads, near8, sorted("%08X" % a for a in hits4)))

# Q4 the load fix-up
F = {x.address: (x.mnemonic, x.op_str) for x in ins(0x59C250)}
check("Q4 0059C250 clears the header as a qword before the slot-8 setter",
      F.get(0x59C286) == ("xor", "r12d, r12d") and F.get(0x59C591) == ("mov", "ecx, dword ptr [rbx + 0x48]")
      and F.get(0x59C598) == ("sub", "ecx, dword ptr [rax + 0xf4]") and F.get(0x59C5A1) == ("add", "rsi, rdx")
      and F.get(0x59C5E8) == ("mov", "qword ptr [rsi], r12") and F.get(0x59C5FC) == ("call", "qword ptr [rax + 0x40]")
      and all(F.get(a, ("", ""))[1].find("r12") < 0 or F[a][0] in ("mov", "cmovne", "lea", "xor") for a in F if 0x59C286 < a < 0x59C5E8))

# Q5 the by-value setter
G = {x.address: (x.mnemonic, x.op_str) for x in ins(0x672F30, 243)}
vt = 0x672FBD + 0x6F5E13
col = struct.unpack_from("<Q", d, off(vt - 8))[0]; td = B + struct.unpack_from("<I", d, off(col) + 12)[0]
name = d[off(td) + 16:off(td) + 90].split(b"\0")[0]
check("Q5 00672F30 copies the 0x48-byte element inline; element +0x28 gets the TAsyncUpdate<PDataBlockD3D11> vtable",
      G.get(0x672F89) == ("lea", "rdx, [rbx + 8]") and G.get(0x672FCF) == ("mov", "rax, qword ptr [rdi + 0x40]")
      and G.get(0x672FD3) == ("mov", "qword ptr [rdx + 0x40], rax") and G.get(0x672FBD) == ("mov", "qword ptr [rdx + 0x28], rax")
      and vt == 0xD68DD0 and name == b".?AV?$TAsyncUpdate@VPDataBlockD3D11@PGeometry@Phyre@@@@", name.decode())

rows = {(l.split("\t")[0], l.split("\t")[1]): l for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")}
page = open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "member-registration-and-the-recovered-field-schema.md"), encoding="utf-8").read()
live = re.sub(r"~~.*?~~", "", page, flags=re.S)
MK = "ZEROED WITH THE COUNT BY THE LOAD FIX-UP"
check("S the +4 rows, the m_u row and page section 20 follow",
      MK in rows[("PArray", "0x0004")] and MK in rows[("PSharray", "0x0004")] and "PER ELEMENT TYPE" in rows[("PSharray", "0x0008")]
      and "the resizes `005C8BF0` / `006C7A40` and the adopts `0062A870` / `006A5950` call" not in live)
print("FAILS", fails)
sys.exit(1 if fails else 0)
