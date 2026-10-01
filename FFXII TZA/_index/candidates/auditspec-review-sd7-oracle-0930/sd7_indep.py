"""sd7_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the SD-7 review (ORACLE-REQ-AUDITSPEC-SD7-0930,
2026-09-30). pefile + capstone over the certified image (sha256 asserted); none of the package's or kit's census code.
Canonical VAs (image base 0x120000 included).

  A  raw byte sweep of every executable section for FF /2 (call) and FF /4 (jmp) with a memory operand whose displacement
     is exactly 0x78 (disp8 or disp32, any base incl. rbp/rsp/r13, with or without SIB/index, optional REX), each
     candidate confirmed by decoding it; then kept only if it lies on an instruction boundary of a linear decode of its
     .pdata function range. Candidates outside every .pdata range are listed. Compared site by site with the package's
     192 (pkg_rows.json, written by dump_pkg_rows.py).
     Control A0: the sweep must find OPUS's slot-30 application call 0079C23A (+0xF0) when the displacement is 0xF0.
  B  GameApplication: its vtable 008C5760 length (qwords into executable sections, then the next qword), the RTTI
     type descriptor, and every base-class descriptor in the image naming that descriptor - i.e. whether any class
     derives from GameApplication (a derived class could have more than 31 slots and still inherit slot 15).
  C  E1 probe: every E1 row whose regval terms include a load based on rbp in a function that makes rbp a frame
     pointer (lea rbp,[rsp+k] / mov rbp,rsp), or on a register set by lea r,[rsp+k] - stack slots E1's rsp exemption
     does not see. Also E1 rows whose only exclusion is an indexed load, and the displacement histogram of E1 loads.
  D  E4 windows: for the 10 E4 rows, the instructions from the vtable load to the >= slot-31 dispatch, printed, with an
     automated check that the object register and the vtable register are not written in between (linear) and no
     call intervenes.
  E  E3 constructors 001FBB40 / 001FB870: the vtable immediates they store at [rax/rcx], and those vtables' RTTI names.
  F  E2 sample: the method's vtable memberships recomputed from raw aligned qwords + COL, for all 13 E2 rows.
"""
import collections, hashlib, json, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n] if o is not None else b""


def q(va):
    b = rd(va, 8)
    return struct.unpack("<Q", b)[0] if len(b) == 8 else None


def is_exec(va):
    return any(v <= va < v + vs and x for n, v, vs, p, rs, x in SECS)


def one(va):
    for i in md.disasm(rd(va, 16), va, 1):
        return i
    return None


def txt(i):
    return "%08X %s %s" % (i.address, i.mnemonic, " ".join(i.op_str.split()))


# ---- .pdata
ed = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
PD = []
for k in range(ed.Size // 12):
    b, e, u = struct.unpack_from("<III", raw, off(IB + ed.VirtualAddress) + 12 * k)
    if b:
        PD.append((IB + b, IB + e))
PD.sort()
print("pdata entries: %d" % len(PD))
import bisect
PDB = [b for b, e in PD]


def pd_of(va):
    k = bisect.bisect_right(PDB, va) - 1
    return PD[k] if k >= 0 and PD[k][0] <= va < PD[k][1] else None


_bound = {}


def boundaries(rng):
    if rng not in _bound:
        b, e = rng
        _bound[rng] = {i.address for i in md.disasm(rd(b, e - b), b)}
    return _bound[rng]


def sweep(disp):
    hits = []
    for n, v, vs, p, rs, x in SECS:
        if not x:
            continue
        data = raw[p:p + min(vs, rs)]
        for pos in range(len(data) - 3):
            if data[pos] != 0xFF:
                continue
            m = data[pos + 1]
            reg, mod, rm = (m >> 3) & 7, m >> 6, m & 7
            if reg not in (2, 4) or mod not in (1, 2):
                continue
            dp = pos + 2 + (1 if rm == 4 else 0)
            if mod == 1:
                if dp >= len(data) or data[dp] != disp:
                    continue
            else:
                if dp + 4 > len(data) or struct.unpack_from("<i", data, dp)[0] != disp:
                    continue
            for st in (pos - 1, pos) if pos > 0 and 0x40 <= data[pos - 1] <= 0x4F else (pos,):
                va = v + st
                i = one(va)
                if i and i.mnemonic in ("call", "jmp") and i.size == (dp - st) + (1 if mod == 1 else 4) and \
                        i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp == disp:
                    hits.append(i)
                    break
    return hits


pkg = json.load(open(os.path.join(HERE, "pkg_rows.json")))
PKG = {int(r["site"], 16): r for r in pkg}

print("\n== A: raw sweep, displacement 0x78")
hits = sweep(0x78)
inb, outpd, notb = [], [], []
for i in hits:
    r = pd_of(i.address)
    if r is None:
        outpd.append(i)
    elif i.address in boundaries(r):
        inb.append(i)
    else:
        notb.append(i)
print("decoded candidates %d: on a .pdata-range instruction boundary %d, inside a range but off-boundary %d, outside .pdata %d"
      % (len(hits), len(inb), len(notb), len(outpd)))
forms = collections.Counter()
for i in inb:
    mem = i.operands[0].mem
    forms["%s base=%s index=%s" % (i.mnemonic, md.reg_name(mem.base) if mem.base else "-", md.reg_name(mem.index) if mem.index else "-")] += 1
for k, c in sorted(forms.items()):
    print("  form %-40s %d" % (k, c))
mine = {i.address for i in inb}
print("package 192 sites: %d; mine on boundary: %d; in both: %d" % (len(PKG), len(mine), len(mine & set(PKG))))
for a in sorted(mine - set(PKG)):
    i = one(a)
    print("  MINE-ONLY %s  func %s" % (txt(i), "%08X-%08X" % pd_of(a)))
for a in sorted(set(PKG) - mine):
    print("  PKG-ONLY  %s" % txt(one(a)))
for i in outpd:
    ctx = list(md.disasm(rd(i.address - 24, 40), i.address - 24))
    print("  OUTSIDE-PDATA %s   (preceding decode: %s)" % (txt(i), " | ".join(txt(c) for c in ctx if c.address < i.address)[-160:]))
print("  (off-boundary candidates are byte coincidences inside other instructions: %d)" % len(notb))
print("functions (pdata begin) holding the %d: %d" % (len(mine), len({pd_of(a)[0] for a in mine})))

print("\n== A0 control: same sweep at displacement 0xF0 must contain 0079C23A")
h2 = {i.address for i in sweep(0xF0)}
print("  0079C23A found: %s   (%d decoded 0xF0 candidates)" % (0x0079C23A in h2, len(h2)))

# ---- RTTI
print("\n== B: GameApplication vtable and derivation")
APPVT = 0x008C5760


def col_of(vt):
    c = q(vt - 8)
    d = rd(c, 0x18) if c else b""
    if len(d) < 0x18 or struct.unpack_from("<I", d, 0)[0] != 1:
        return None
    return c


def td_name(td):
    return rd(td + 0x10, 200).split(b"\0")[0].decode("latin1")


def cls_of_vt(vt):
    c = col_of(vt)
    if not c:
        return None
    return td_name(IB + struct.unpack_from("<I", rd(c, 0x18), 0x0C)[0])


n = 0
while is_exec(q(APPVT + 8 * n) or 0):
    n += 1
nxt = q(APPVT + 8 * n)
print("  vtable %08X class %s: %d consecutive code pointers; next qword %s (a COL: %s)"
      % (APPVT, cls_of_vt(APPVT), n, "%08X" % nxt if nxt else None, bool(col_of(APPVT + 8 * n + 8))))
print("  slot 15 = %08X; slot 30 = %08X" % (q(APPVT + 0x78), q(APPVT + 0xF0)))
c = col_of(APPVT)
tdrva = struct.unpack_from("<I", rd(c, 0x18), 0x0C)[0]
print("  type descriptor RVA %#x name %s" % (tdrva, td_name(IB + tdrva)))
# every base class descriptor naming this TD: BCD = {TD rva, numContained, PMD(3 dwords), attributes, CHD rva} (28 bytes)
bcds = []
for n_, v, vs, p, rs, x in SECS:
    if x:
        continue
    data = raw[p:p + min(vs, rs)]
    for o in range(0, len(data) - 28, 4):
        if struct.unpack_from("<I", data, o)[0] == tdrva:
            bcds.append(v + o)
print("  dwords equal to the TD RVA in data sections: %d at %s" % (len(bcds), " ".join("%08X" % b for b in bcds)))
# which class hierarchy descriptors' base-class arrays contain those BCDs
bcdrvas = {b - IB for b in bcds}
chd_hits = []
for n_, v, vs, p, rs, x in SECS:
    if x:
        continue
    data = raw[p:p + min(vs, rs)]
    for o in range(0, len(data) - 16, 4):
        sig, attr, nb, arr = struct.unpack_from("<IIII", data, o)
        if sig != 0 or not (1 <= nb <= 64) or not arr:
            continue
        ao = off(IB + arr)
        if ao is None:
            continue
        elems = struct.unpack_from("<%dI" % nb, raw, ao) if ao + 4 * nb <= len(raw) else ()
        if bcdrvas & set(elems):
            first_td = struct.unpack_from("<I", raw, off(IB + elems[0]))[0] if off(IB + elems[0]) else None
            chd_hits.append((v + o, nb, td_name(IB + first_td) if first_td else None))
for a, nb, nm in chd_hits:
    print("  CHD %08X numBases %d most-derived %s" % (a, nb, nm))

# ---- C: E1 probe
print("\n== C: E1 rule probe")


def frame_regs(func):
    """registers made to point into the frame in the first 40 instructions (lea r,[rsp+k] / mov r,rsp)"""
    out = set()
    for k, i in enumerate(md.disasm(rd(func, 0x200), func)):
        if k > 40:
            break
        s = " ".join(i.op_str.split())
        m = re.match(r"(\w+), \[rsp(?: [+-] 0x[0-9a-f]+)?\]$", s)
        if i.mnemonic == "lea" and m:
            out.add(m.group(1))
        if i.mnemonic == "mov" and re.match(r"(\w+), rsp$", s):
            out.add(s.split(",")[0])
    return out


hist = collections.Counter()
flag = []
idx_only = 0
for r in pkg:
    if r["class"] != "E1":
        continue
    f = int(r["func"], 16)
    fr = frame_regs(f)
    kinds = set()
    for t in r["terms"]:
        if t[0] != "M":
            kinds.add(t[0])
            continue
        mem = re.search(r"\[([^\]]+)\]", t[1]).group(1).replace(" ", "")
        base = re.match(r"(\w+)", mem).group(1)
        dm = re.search(r"([+-]0x[0-9a-f]+|[+-]\d+)$", mem)
        d = int(dm.group(1), 0) if dm and "*" not in mem.split(dm.group(1))[-1] else 0
        hist["idx" if "*" in mem else "%#x" % d] += 1
        kinds.add("idx" if "*" in mem else "disp")
        if base in fr:
            flag.append((r["func"], r["site"], t[1], sorted(fr)))
    if kinds <= {"idx", "C", "R"} and "idx" in kinds:
        idx_only += 1
print("  E1 rows: %d; load-displacement histogram: %s" % (sum(1 for r in pkg if r["class"] == "E1"),
                                                      dict(sorted(hist.items(), key=lambda kv: -kv[1]))))
print("  E1 rows excluded by indexed loads / resolver / 0 only: %d" % idx_only)
print("  E1 loads based on a frame register (stack slot E1's rsp exemption does not cover): %d" % len(flag))
for fl in flag:
    print("    %s %s %s  frame regs %s" % fl)

# ---- D: E4 windows
print("\n== D: E4 windows")
for r in pkg:
    if r["class"] != "E4":
        continue
    f, s, vl = int(r["func"], 16), int(r["site"], 16), int(r["vtload"], 16)
    ins = list(md.disasm(rd(vl, 0x400), vl))
    obj = r["obj"]
    # find the next load mov V2,[obj] and dispatch at >= 0xF8 through V2 after vl, before obj is written
    OBJF = {"rcx": "cx", "rdx": "dx", "rbx": "bx", "rsi": "si", "rdi": "di", "rax": "ax", "rbp": "bp"}.get(obj, obj)
    ok = None
    wr = []
    for k, i in enumerate(ins):
        if k and any(md.reg_name(x).endswith(OBJF) or md.reg_name(x).startswith(obj) for x in i.regs_access()[1]):
            wr.append(txt(i))
            if not (i.mnemonic == "call" and obj not in ("rcx", "rdx", "r8", "r9", "r10", "r11", "rax")):
                break
        if i.mnemonic in ("call", "jmp") and i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp >= 0xF8 \
                and i.address > s:
            ok = i
            break
    if ok is None:  # the big dispatch may precede the +0x78 site
        ok_txt = "big dispatch precedes the site or not reached linearly"
    else:
        ok_txt = txt(ok)
    print("  %s site %s obj %s vtload %s -> %s ; obj writes before it: %s" % (r["func"], r["site"], obj, r["vtload"], ok_txt, wr[:2]))

# ---- E: constructors
print("\n== E: E3 constructors")
for ctor in (0x001FBB40, 0x001FB870):
    for i in md.disasm(rd(ctor, 0x200), ctor):
        if i.mnemonic == "lea" and "rip" in i.op_str:
            tgt = i.address + i.size + i.operands[1].mem.disp
            nm = cls_of_vt(tgt)
            if nm:
                print("  %08X: %s -> vtable %08X %s" % (ctor, txt(i), tgt, nm))
        if i.mnemonic == "ret":
            break

# ---- F: E2 classes
print("\n== F: E2 method vtable memberships (raw aligned qwords)")
e2f = {}
for r in pkg:
    if r["class"] == "E2":
        m = re.search(r"argument rcx of (\w+)", " ".join(" ".join(t) for t in r["terms"]))
        e2f[int(m.group(1), 16)] = r
want = set(e2f)
sites = collections.defaultdict(list)
for n_, v, vs, p, rs, x in SECS:
    if x:
        continue
    data = raw[p:p + min(vs, rs)]
    for o in range(0, len(data) - 7, 8):
        val = struct.unpack_from("<Q", data, o)[0]
        if val in want:
            sites[val].append(v + o)
for fn in sorted(want):
    names = []
    for sa in sites[fn]:
        nm = None
        for k in range(200):
            nm = cls_of_vt(sa - 8 * k)
            if nm:
                break
        names.append(nm)
    print("  %08X (site %s): qwords %d, classes %s" % (fn, e2f[fn]["site"], len(sites[fn]), sorted(set(map(str, names)))))

# ---- G: argument chains through address-taken functions
print("\n== G: rows whose regval terms were collected in callers, where a function in the chain is address-taken")
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
qref = collections.Counter()
for n_, v, vs, p, rs, x in SECS:
    if x:
        continue
    data = raw[p:p + min(vs, rs)]
    for o in range(0, len(data) - 7, 8):
        qref[struct.unpack_from("<Q", data, o)[0]] += 1
learef = collections.Counter()
for n_, v, vs, p, rs, x in SECS:
    if not x:
        continue
    data = raw[p:p + min(vs, rs)]
    for pos in range(1, len(data) - 6):
        if data[pos] == 0x8D and (data[pos + 1] & 0xC7) == 0x05 and 0x48 <= data[pos - 1] <= 0x4F:
            learef[v + pos + 6 + struct.unpack_from("<i", data, pos + 2)[0]] += 1


def fstart(va):
    r = pd_of(va)
    return r[0] if r else None


def taken(fn):
    return qref.get(fn, 0) + learef.get(fn, 0)


risk = []
for r in pkg:
    if r["class"] == "RESIDUE":
        continue
    f = int(r["func"], 16)
    outside = [t for t in r["terms"] if t[0] == "M" and re.match(r"[0-9A-F]{8} ", t[1])
               and fstart(int(t[1][:8], 16)) != fstart(int(r["site"], 16))]
    if not outside:
        continue
    chain, frontier = {fstart(int(r["site"], 16)) or f}, {fstart(int(r["site"], 16)) or f}
    for _ in range(3):
        nxt = set()
        for g in frontier:
            for cs in RAW.get("%X" % g, ()):
                s = fstart(int(cs, 16))
                if s and s not in chain:
                    nxt.add(s)
        chain |= nxt
        frontier = nxt
    tk = sorted("%08X(q%d,lea%d)" % (g, qref.get(g, 0), learef.get(g, 0)) for g in chain if taken(g))
    if tk:
        risk.append((r["class"], r["func"], r["site"], len(chain), tk))
print("  non-residue rows with caller-side terms: %d; with an address-taken function among their <=3-level direct-caller chain: %d"
      % (sum(1 for r in pkg if r["class"] != "RESIDUE" and any(t[0] == "M" and re.match(r"[0-9A-F]{8} ", t[1]) and
             fstart(int(t[1][:8], 16)) != fstart(int(r["site"], 16)) for t in r["terms"])), len(risk)))
for x in risk:
    print("    %s %s %s chain %d taken %s" % x)

# ---- C2: E1 load bases
print("\n== C2: E1 load base registers, and rbp bases in rbp-frame functions")
bh = collections.Counter()
for r in pkg:
    if r["class"] != "E1":
        continue
    for t in r["terms"]:
        if t[0] != "M":
            continue
        base = re.search(r"\[(\w+)", t[1]).group(1)
        bh[base] += 1
        if base == "rbp":
            fs = fstart(int(t[1][:8], 16))
            print("    rbp-based E1 load %s in %08X; frame regs %s" % (t[1], fs or 0, sorted(frame_regs(fs)) if fs else "?"))
print("  bases: %s" % dict(bh))
