"""sd7_app_pointer_sites.py - can any `call [vtable + 0x78]` site in the image dispatch GameApplication slot 15 (0017D1A0)?
(SWE2-ORACLE, 2026-09-30; register SD-7, follow-up to OPUS's sd7-slot15-callers-0930). Static, certified image, through
Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py (backward value sets, depth 3). Nothing is executed.

Method, per site `call/jmp qword ptr [V + 0x78]`: find V's vtable load `mov V, qword ptr [O]`, resolve the object register
O with regval, then try to exclude the application in four independent ways:
  E1 displacement  every value of O is a load [B + d] with d outside the displacements the application pointer is ever
                   stored at (OPUS's 26 escapes: 0x0, 0x8, 0x20, 0x38, 0x78; no indexed store), a constant 0, or an
                   indexed load; the handle resolvers 007B58C0 / 007BC2B0 return exactly such an indexed load.
                   A load through a frame-pointer rbp is a stack slot and is never excluded: stack_base checks the
                   last write of the base is rsp-derived (mov B,rsp / lea B,[rsp+-k] / lea B,[X+-k] with X rsp-derived)
                   and not a pointer loaded from memory. (Repair of the auditspec-review-sd7-oracle-0930 REJECT:
                   8 PPFX rows read stack-passed arguments through the frame pointer and must not count as E1.)
  E2 class         O is the incoming rcx (this) of a method whose every vtable (RTTI) is a class outside GameApplication's
                   hierarchy {GameApplication, PApplication, PBase, PMemoryBase}
  E3 constructed   O is the return of a constructor that stores a non-application vtable (001FBB40, 001FB870)
  E4 slot range    the same object (O unchanged) is also dispatched at a vtable slot >= 31; GameApplication's vtable
                   has 31 slots (0..30), so that object is not a GameApplication
Controls:
  K1 the census reproduces OPUS's count (192 sites in 114 functions)
  K2 the window procedure's own application call 0079914C (object = [02EA5368]) is NOT excluded by E1
  K3 E2 does not exclude GameApplication's own methods (rcx of 0017D1A0 types as GameApplication)
  K4 GameApplication's vtable has 31 slots and a real application call at slot 30 (+0xF0, 0079C23A) exists, so the E4
     threshold (>= 31) is above every slot the application answers
  K5 007B58C0 / 007BC2B0 return an indexed handle-table load ([table + i*40 + 0x20]), treated as E1
  K6 00739C9D's frame-pointer load is not excluded (positive); 0074C8EC / 0074CA3D / 00771C06, whose rbp is a pointer
     loaded from a stack slot, stay E1 (negative)
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ = T.R, V.SZ
fails = 0
APPVT, APP_HIER = 0x008C5760, {"GameApplication", "Phyre::PFramework::PApplication", "Phyre::PBase", "Phyre::PMemoryBase"}
HOLD = {0x0, 0x8, 0x20, 0x38, 0x78}
RESOLVERS = {"0x7b58c0", "0x7bc2b0"}          # handle -> [table + i*40 + 0x20] (read in K5)
CTORS = {"0x1fbb40": 0x009043D8, "0x1fb870": 0x00904328}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, " ".join(i.op_str.split()))


# one pass over every aligned qword, for vtable membership
import pefile  # noqa: E402
pe = pefile.PE(R.b.EXE, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
QSITES = collections.defaultdict(list)
for s in pe.sections:
    d = s.get_data()
    for off in range(0, len(d) - 7, 8):
        v = struct.unpack_from("<Q", d, off)[0]
        if v in SZ:
            QSITES[v].append(IB + s.VirtualAddress + off)


def classes_of(fn):
    out = set()
    for site in QSITES.get(fn, ()):
        vt, cls = T.vtable_start(site)
        if cls:
            out.add(cls)
    return out


def parse(mem):
    s = re.search(r"\[([^\]]+)\]", mem).group(1).replace(" ", "")
    base, idx, d = None, None, 0
    for tok in re.findall(r"[+-]?[^+-]+", s):
        sg = -1 if tok.startswith("-") else 1
        tok = tok.lstrip("+-")
        if "*" in tok:
            idx = tok
        elif tok.startswith("0x") or tok.isdigit():
            d += sg * int(tok, 0)
        else:
            base = tok
    return base, idx, d


def stack_base(f, la, base):
    """Is `base` stack-derived at the load `la` in function f? The last write on the linear walk is `mov B, rsp`,
    `lea B, [rsp ± k]`, or the frame idiom `lea B, [X ± k]` where X's own last write before it is rsp-derived
    (`mov rax, rsp; lea rbp, [rax - k]`). A base loaded from memory - `mov rbp, [rsp+0x188]` - is a pointer, not a
    frame pointer. A base never written in the body is an incoming register, not a local frame. Linear walk of the
    body, not flow-aware (a join from another path is not seen)."""
    ins, idx, _ = V.body(f)
    k = idx.get(la)
    fam = V.canon(base)
    if k is None or fam is None:
        return False

    def last_write(reg, upto):
        w = None
        for i in ins[:upto]:
            if reg in V.writes(i):
                w = i
        return w

    def rsp_rel(w):
        if w is None or w.mnemonic not in ("mov", "lea"):
            return False
        d, s = V.ops(w)
        if w.mnemonic == "mov":
            return V.canon(s or "") == "rsp"
        m = re.match(r"\[(\w+)(?: [+-] (?:0x[0-9a-f]+|\d+))?\]$", s or "")
        if not m:
            return False
        if V.canon(m.group(1)) == "rsp":
            return True
        w2 = last_write(V.canon(m.group(1)), idx[w.address])
        if w2 and w2.mnemonic in ("mov", "lea"):
            d2, s2 = V.ops(w2)
            return V.canon(d2) == V.canon(m.group(1)) and (V.canon(s2 or "") == "rsp" or
                                                          bool(re.match(r"\[rsp", s2 or "")))
        return False

    w = last_write(fam, k)
    return bool(w and V.canon(V.ops(w)[0]) == fam and rsp_rel(w))


def e1(terms, f):
    if not terms:
        return False
    for t in terms:
        if t[0] == "C" and t[1] == 0:
            continue
        if t[0] == "R" and t[1] in RESOLVERS:
            continue
        if t[0] == "M":
            base, idx, d = parse(t[1])
            if base not in ("rip", "rsp"):
                # a load through a frame pointer is a stack slot and is never excluded (audit-spec review
                # auditspec-review-sd7-oracle-0930: a stack-passed argument read through rbp is not a holder
                # displacement, and regval does not follow it into the caller)
                if stack_base(f, int(t[1][:8], 16), base):
                    return False
                if idx or d not in HOLD:
                    continue
        return False
    return True


def e2(terms):
    cl = []
    for t in terms or ():
        m = re.match(r"argument rcx of (\w+)", str(t[1]))
        if t[0] != "U" or not m:
            return None
        cs = classes_of(int(m.group(1), 16))
        if not cs or cs & APP_HIER:
            return None
        cl.append(sorted(cs)[0])
    return cl or None


def e3(terms):
    ok = bool(terms)
    for t in terms or ():
        if t[0] == "C" and t[1] == 0:
            continue
        if not (t[0] == "R" and t[1] in CTORS):
            return None
    return [T.rtti_class(CTORS[t[1]]) for t in terms if t[0] == "R"] if ok else None


def slot_disps(f, vtl, obj):
    ins, idx, _ = V.body(f)
    k, fam = idx[vtl], V.canon(obj)
    lo = k
    while lo > 0 and fam not in V.writes(ins[lo - 1]):
        lo -= 1
    hi = k
    while hi + 1 < len(ins) and fam not in V.writes(ins[hi + 1]):
        hi += 1
    ds = []
    for j in range(lo, hi + 1):
        m = re.match(r"(\w+), qword ptr \[(\w+)\]$", ins[j].op_str)
        if ins[j].mnemonic != "mov" or not m or V.canon(m.group(2)) != fam:
            continue
        v = V.canon(m.group(1))
        for c in ins[j + 1:hi + 1]:
            mm = re.match(r"qword ptr \[(\w+)(?: \+ (0x[0-9a-f]+))?\]$", c.op_str)
            if c.mnemonic in ("call", "jmp") and mm and V.canon(mm.group(1)) == v:
                ds.append((c.address, int(mm.group(2) or "0", 16)))
            if c.mnemonic == "call" and v in V.VOLATILE:
                break
            if c.mnemonic != "call" and v in V.writes(c):
                break
    return ds


# --- census
rows = []
for f in sorted(SZ):
    ins, idx, _ = V.body(f)
    for k, i in enumerate(ins):
        m = re.match(r"qword ptr \[(\w+) \+ 0x78\]$", i.op_str)
        if i.mnemonic not in ("call", "jmp") or not m or m.group(1) in ("rip", "rsp", "rbp"):
            continue
        fam, ld = V.canon(m.group(1)), None
        for j in range(k - 1, max(-1, k - 40), -1):
            if fam in V.writes(ins[j]):
                ld = ins[j]
                break
        obj = terms = None
        if ld is not None:
            mm = re.match(r"\w+, qword ptr \[(\w+)\]$", ld.op_str)
            if ld.mnemonic == "mov" and mm:
                obj, terms = mm.group(1), V.value_at(f, ld.address, mm.group(1), 3)
        rows.append((f, i.address, ld, obj, terms))
check("K1", len(rows) == 192 and len({r[0] for r in rows}) == 114,
      "%d [vtable+0x78] dispatch sites in %d functions (OPUS: 192 / 114)" % (len(rows), len({r[0] for r in rows})))

cls = collections.Counter()
resid = []
for f, a, ld, obj, terms in rows:
    if e1(terms, f):
        cls["E1"] += 1
        continue
    c2 = e2(terms)
    if c2:
        cls["E2"] += 1
        print("      E2 %08X %08X this is %s" % (f, a, c2[0]))
        continue
    c3 = e3(terms)
    if c3:
        cls["E3"] += 1
        print("      E3 %08X %08X object built by a %s constructor" % (f, a, c3[0]))
        continue
    ds = slot_disps(f, ld.address, obj) if ld is not None and obj else []
    big = [x for x in ds if x[1] >= 31 * 8]
    if big:
        cls["E4"] += 1
        print("      E4 %08X %08X same object dispatched at +%#x (%08X)" % (f, a, big[0][1], big[0][0]))
        continue
    cls["RESIDUE"] += 1
    resid.append((f, a, ld, obj, terms))
print("      classes: %s" % dict(sorted(cls.items())))
for f, a, ld, obj, terms in resid:
    print("      RESIDUE %08X %08X obj=%s %s" % (f, a, obj, "; ".join(sorted(str(t) for t in terms)[:3]) if terms else "(no vtable load)"))

# --- controls
t_ctl = V.value_at(0x00798FF0, 0x00799145, "rcx", 3)
g = [t for t in t_ctl if t[0] == "M"]
tgt = None
if g:
    ia = int(g[0][1].split()[0], 16)
    i = next(R.md.disasm(R.at(ia, 16), ia, 1))
    tgt = i.address + i.size + i.operands[1].mem.disp
check("K2", txt(0x0079914C) == "call qword ptr [rax + 0x70]" and not e1(t_ctl, 0x00798FF0) and tgt == 0x02EA5368,
      "the window procedure's application call 0079914C (object [%s]) is not excluded by E1" % (hex(tgt) if tgt else None))
check("K3", "GameApplication" in classes_of(0x0017D1A0) and e2({("U", "argument rcx of 0017D1A0: no direct caller")}) is None,
      "E2 types 0017D1A0's this as GameApplication and does not exclude it")
n = 0
while struct.unpack("<Q", R.at(APPVT + 8 * n, 8))[0] in SZ:
    n += 1
check("K4", n == 31 and txt(0x0079C23A) == "call qword ptr [rax + 0xf0]" and T.rtti_class(APPVT) == "GameApplication",
      "GameApplication vtable = %d slots; slot 30 is called at 0079C23A, so a slot >= 31 excludes the class" % n)
check("K5", txt(0x007B58EB) == "mov rax, qword ptr [rax + rcx*8 + 0x20]" and txt(0x007BC2DB) == "mov rax, qword ptr [rax + rcx*8 + 0x20]",
      "007B58C0 / 007BC2B0 return an indexed handle-table load ([table + i*40 + 0x20]), treated as E1")
# K6: the frame-pointer rule's own controls (auditspec-review-sd7-oracle-0930 R1). 00739C9D's load is
# [rbp+0x138] with rbp = entry rsp - 0x58 - a stack slot, not excluded; 0074C8EC/0074CA3D/00771C06 load rbp
# itself from a stack slot - pointers, still excluded.
k6p = next((r for r in rows if r[1] == 0x00739C9D), None)
k6n = [r for r in rows if r[1] in (0x0074C8EC, 0x0074CA3D, 0x00771C06)]
check("K6", k6p is not None and not e1(k6p[4], k6p[0]) and len(k6n) == 3 and all(e1(r[4], r[0]) for r in k6n),
      "00739C9D's frame-pointer load is not excluded; the three loaded-pointer rbp rows stay E1")
PART = {"E1": 125, "E2": 13, "E3": 2, "E4": 10, "RESIDUE": 42}
check("S1", dict(cls) == PART and cls["RESIDUE"] == len(resid),
      "partition: E1 %d, E2 %d, E3 %d, E4 %d, residue %d (expected %s; the stack-slot rows are not excludable)" % (
          cls["E1"], cls["E2"], cls["E3"], cls["E4"], cls["RESIDUE"], PART))
print("FAILS %d" % fails)
