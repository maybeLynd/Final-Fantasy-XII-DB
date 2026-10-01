"""SWE2-AUDIT-SEM: independent re-derivation for the review of SWE2-DATA's DD owner read batch 4 (4415dba48).
Static only: the shipping image (SHA-256 73461d08...d89721f8, checked) and the register / pages as git blobs.
Cross-references come from retool.scan() (OPUS's cached rip/call index over the v4 extents), NOT from the producer's
pe.raw_rip_refs, so the census side is a second implementation. Disassembly uses the same capstone build.

  R1  register at parent / commit / HEAD: new SD rows, and every id that appears twice
  M1  _set_new_mode: the IAT slot's only reference is the thunk 00862046; the thunk's only caller is 00808D5C (tail jmp);
      00808D5C = call 00809B44 (lea rcx, handler; jmp [SetUnhandledExceptionFilter]) ; call 005C5230 (xor eax,eax; ret);
      mov ecx, eax ; jmp thunk. 008C31D0 is a null qword whose address the startup body 00808D78 passes (lea) and
      008C31D8 holds 00808D5C: the MSVC pre_cpp_initialization shape, first entry after the null table start
  M2  _Xbad_alloc: call/jmp references through its IAT slot, and the number of containing functions
  N1  00408F30 compares eight dwords (+0..+0x1C) and returns 0 on a full match, 1 at the first mismatch; its only
      callers are 00408FA0's two sites, each followed by test rax,rax / jne hit; 00408FA0's only caller is 00408F90,
      whose four callers pass r8d = 0 and edx = '@FRM'
  E1  0026D910's rip-relative stores hit exactly 02099DA8, 02099DAC, 02099DB0, 02099DBC
  E2  the environment page at the commit still carries an unstruck "publish five globals" line
  S1  003171C0 reaches the bestiary counter (thunk 00253750 -> 00315820) only when [unit+0x698]+5 == 1, the actor's
      free-target type != 3 and the class word +0x52 != 0xFFFF; 00315820 also refuses id >= 0x200 and counts only
      when 00315D50(id) == -1
  S2  every .text instruction whose memory displacement lies in 0x3844..0x386B (the achievement block), by owner:
      the updater's store 00316BF0 writes the clamped sum; 00316810 writes only 0x7FFFFFFE / 0x7FFE; 00316C60 writes
      99,999 (0x1869F); so no displacement-addressed writer stores a negative into a kind-4 counter
  S3  00316A50's kind-4 arm: sum >= 0 or 0 (00316B9D add / 00316B9F jns / 00316BA1 xor)
  H1  0036C5A0(id, fn) stores fn at 022D7FD0 + id*0xA8 + 0xA0; its only callers pass (6, 002E6D60) and (0xA, 002E6D60);
      the arena initializer 00369D30 stores a zeroed r8 there (00369E36); 0036BFE0 calls [desc+0xA0] (0036C03B)
  H2  002E6D60 has one ret and every path to it passes 002E6E1E xor eax, eax: it always answers 0
  H3  handle-issuing entries: direct call sites of 0036B160 and of 0036B970 (-> 0036B980), counted with their bodies
  H4  RC-11's census of the 135 arena-push sites (arena_sites.tsv at the parent) contains no arena 7
  K1  the byte kernel 00432300 that SD-140 leaves unread: its direct call sites and bodies (includes both emit paths)
Usage: python dd4_sem.py
"""
import hashlib, os, re, subprocess, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool  # noqa: E402
from pe import d, off, dis, u64, funcs, owner, text_range, containing_ins, BASE  # noqa: E402

C = "4415dba48"
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True).stdout.decode("utf-8", "replace")


EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
check("image SHA-256", hashlib.sha256(open(EXE, "rb").read()).hexdigest().startswith("73461d08"))
X = retool.scan()
refs, calls = X["refs"], X["calls"]


def rrefs(lo, hi=None):
    hi = lo if hi is None else hi
    return sorted((g, f, a, k) for g, s in refs.items() if lo <= g <= hi for (f, a, k) in s)


def callers(t):
    return sorted(calls.get(t, set()))


def ops(fn, n=None):
    return {x.address: (x.mnemonic, x.op_str) for x in dis(fn, n)}


# ---- R1 register duplicates
REG = "Database/FFXII TZA/_index/OPEN-QUESTIONS.md"
for label, rev in (("parent", C + "^"), ("commit", C), ("HEAD", "HEAD")):
    t = git("show", "%s:%s" % (rev, REG))
    ids = re.findall(r"^\|\s*([A-Z][A-Za-z0-9/\-]*-\d+)\s*\|", t, re.M)
    seen, dup = set(), []
    for i in ids:
        if i in seen:
            dup.append(i)
        seen.add(i)
    sd = sorted(set(i for i in ids if re.fullmatch(r"SD-1[46]\d", i)), key=lambda s: int(s[3:]))
    print("   register %-6s: SD-14x/16x ids %s; duplicated ids %s" % (label, " ".join(sd), " ".join(dup) or "none"))
    if label == "commit":
        check("R1 the commit registers SD-160..SD-169 twice each (20 rows, 10 ids)",
              sorted(dup, key=lambda s: int(s[3:])) == ["SD-%d" % k for k in range(160, 170)])
    if label == "parent":
        check("R1 control: the parent already had SD-140 and SD-141 (b47a560bd) and no duplicate", sd == ["SD-140", "SD-141"] and not dup)


# ---- M1 _set_new_mode
def imports():
    pe_ = struct.unpack_from("<I", d, 0x3C)[0]
    imp_rva = struct.unpack_from("<I", d, pe_ + 24 + 112 + 8)[0]
    out, o = {}, off(BASE + imp_rva)
    while True:
        oft, _, _, name, ft = struct.unpack_from("<IIIII", d, o)
        if name == 0:
            break
        i = 0
        while True:
            th = struct.unpack_from("<Q", d, off(BASE + (oft or ft)) + 8 * i)[0]
            if th == 0:
                break
            if not th >> 63:
                hn = off(BASE + (th & 0x7FFFFFFF)) + 2
                out[BASE + ft + 8 * i] = d[hn:d.index(b"\0", hn)].decode()
            i += 1
        o += 20
    return out


IMP = imports()
slot = {v: k for k, v in IMP.items()}
snm = rrefs(slot["_set_new_mode"])
th = ops(0x00862046, 6)
st = ops(0x00808D5C, 0x19)
k9 = ops(0x00809B44, 14)
print("   _set_new_mode slot %08X refs %s; 00809B4B jumps through %s" % (
    slot["_set_new_mode"], ["%08X in %08X" % (a, f) for g, f, a, k in snm], IMP.get(0x008C2250)))
check("M1 slot referenced only by the thunk 00862046, whose only caller is 00808D5C's tail jmp",
      [a for g, f, a, k in snm] == [0x00862046] and callers(0x00862046) == [(0x00808D5C, 0x00808D70)])
check("M1 00808D5C = SetUnhandledExceptionFilter(handler); _set_new_mode(005C5230() = 0) - MSVC pre_cpp_initialization",
      st[0x00808D60] == ("call", "0x809b44") and st[0x00808D65] == ("call", "0x5c5230")
      and st[0x00808D6A] == ("mov", "ecx, eax") and st[0x00808D70] == ("jmp", "0x862046")
      and k9[0x00809B4B][0] == "jmp" and IMP.get(0x008C2250) == "SetUnhandledExceptionFilter"
      and [(x.mnemonic, x.op_str) for x in dis(0x005C5230, 3)] == [("xor", "eax, eax"), ("ret", "")])
check("M1 008C31D0 is a null qword passed by 00808D78 (lea); 008C31D8 holds 00808D5C, the first initializer",
      u64(0x008C31D0) == 0 and u64(0x008C31D8) == 0x00808D5C
      and [(f, a, k) for g, f, a, k in rrefs(0x008C31D0)] == [(0x00808D78, 0x00808DF5, "lea")])

# ---- M2 _Xbad_alloc
xb = [(f, a) for g, f, a, k in rrefs(slot["?_Xbad_alloc@std@@YAXXZ"])]
xs = [a for f, a in xb if (containing_ins(a)[0] or dis(f)[0]).mnemonic in ("call", "jmp")]
print("   _Xbad_alloc slot %08X: %d references (%d call/jmp) in %d functions" % (
    slot["?_Xbad_alloc@std@@YAXXZ"], len(xb), len(xs), len(set(f for f, a in xb))))
check("M2 23 call/jmp sites in 14 functions (second implementation)", len(xs) == 23 and len(set(f for f, a in xb)) == 14)

# ---- N1 NameEquals / FindEntry
ne = dis(0x00408F30, 0x47)
cmp_disp = [x.op_str for x in ne if x.mnemonic == "cmp"]
check("N1 00408F30: eight dword compares +0..+0x1C, 0 on full match, 1 on mismatch",
      len(cmp_disp) == 8 and cmp_disp[0] == "dword ptr [rcx], eax" and cmp_disp[-1] == "dword ptr [rcx + 0x1c], eax"
      and ops(0x00408F30, 0x47)[0x00408F6E] == ("xor", "eax, eax") and ops(0x00408F30, 0x47)[0x00408F71] == ("mov", "eax, 1"))
fe = ops(0x00408FA0)
tc = callers(0x00408F90)
args = []
for f, a in tc:
    pre = [x for x in dis(f) if a - 24 <= x.address < a]
    args.append(any(x.op_str == "r8d, r8d" and x.mnemonic == "xor" for x in pre)
                and any(x.op_str == "edx, 0x4d524640" for x in pre))
check("N1 FindEntry takes a NON-zero NameEquals return as the hit; only the thunk reaches it; 4 callers, no name, '@FRM'",
      [a for f, a in callers(0x00408F30)] == [0x00409006, 0x00409066]
      and fe[0x0040900B] == ("test", "rax, rax") and fe[0x0040900E] == ("jne", "0x40907d")
      and fe[0x0040906E] == ("jne", "0x40907d") and callers(0x00408FA0) == [(0x00408F90, 0x00408F93)]
      and len(tc) == 4 and all(args) and struct.pack("<I", 0x4D524640) == b"@FRM")

# ---- E1 / E2 environment page
w = sorted(set(g for g, f, a, k in rrefs(0x02000000, 0x02FFFFFF) if f == 0x0026D910 and k == "W"))
print("   0026D910 rip stores: %s" % " ".join("%08X" % g for g in w))
check("E1 0026D910 stores exactly the four globals", w == [0x02099DA8, 0x02099DAC, 0x02099DB0, 0x02099DBC])
env = git("show", "%s:Database/FFXII TZA/03-World-Area-Field/choosing-the-field-environment-variant.md" % C)
five = [l for l in env.splitlines() if "five globals" in l and "~~" not in l]
print("   unstruck 'five globals' lines at the commit: %s" % five)
check("E2 FINDING: an unstruck 'publish five globals' line survives the four-globals correction", len(five) == 1)

# ---- S1 bestiary tally gates
k = ops(0x003171C0, 0x6A)
cnt = ops(0x00315820, 0x85)
check("S1 003171C0 tallies only if [+0x698]+5 == 1, type != 3, word +0x52 != 0xFFFF; 00315820 gates on id < 0x200 and 00315D50 == -1",
      k[0x003171F8] == ("cmp", "byte ptr [rax + 5], 1") and k[0x00317202] == ("call", "0x263c20")
      and k[0x00317207] == ("cmp", "eax, 3") and k[0x00317217] == ("cmp", "ecx, 0xffff") and k[0x0031721F] == ("call", "0x253750")
      and ops(0x00253750, 5)[0x00253750] == ("jmp", "0x315820")
      and cnt[0x00315820] == ("cmp", "ecx, 0x200") and cnt[0x00315871] == ("call", "0x315d50")
      and cnt[0x00315876] == ("cmp", "eax, -1") and cnt[0x00315879][0] == "jne"
      and cnt[0x0031588E] == ("mov", "byte ptr [rax + rsi + 0x3404], bl"))

# ---- S2 achievement-block displacement census (raw, function-list independent)
t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
hits = {}
for disp in range(0x3844, 0x386C):
    pat = struct.pack("<i", disp)
    p = blob.find(pat)
    while p >= 0:
        x, how = containing_ins(t0 + p)
        if x is not None and re.search(r"\+ 0x%x\]" % disp, x.op_str):
            hits.setdefault(owner(x.address), set()).add((x.address, x.mnemonic, x.op_str))
        p = blob.find(pat, p + 1)
print("   bodies with a displacement in 0x3844..0x386B: %s" % " ".join(
    "%08X(%d)" % (f or 0, len(s)) for f, s in sorted(hits.items(), key=lambda t: t[0] or 0)))
fam = {0x003162E0, 0x003166F0, 0x00316810, 0x00316BF0, 0x00316C60}
lea384c = sorted(f for f, s in hits.items() if any(m == "lea" and "0x384c" in o for a, m, o in s))
print("   bodies forming base+0x384C (counter block) with lea: %s" % " ".join("%08X" % f for f in lea384c))
check("S2 the counter block base (+0x384C) is formed only by the accessor family the page's 2026-09-18 census names",
      set(lea384c) <= fam and set(lea384c) >= {0x00316810, 0x00316BF0, 0x00316C60})
n = ops(0x00316810, 0x100)
c6 = ops(0x00316C60, 0x65)
check("S2 00316810 stores only 0x7FFFFFFE (kind 4) / 0x7FFE, 0xFFFE (kind 2); 00316C60 stores 99,999",
      n[0x0031689D] == ("mov", "dword ptr [rax], 0x7ffffffe") and n[0x003168F0] == ("mov", "dword ptr [rax], ebp")
      and n[0x00316838] == ("mov", "ebp, 0x7ffe") and n[0x0031683D] == ("lea", "r15d, [rsi - 2]")
      and n[0x00316868] == ("cmp", "eax, 0x7fffffff")
      and c6[0x00316CA3] == ("mov", "dword ptr [rax], 0x1869f"))
u = ops(0x00316A50, 0x19B)
check("S3 kind-4 arm: add, then jns keeps it, else 0 (and INT_MAX saturation above)",
      u[0x00316BA5] == ("cmp", "al, 4") and u[0x00316BB2] == ("jl", "0x316b9d") and u[0x00316B9D] == ("add", "ebx, edi")
      and u[0x00316B9F] == ("jns", "0x316bbd") and u[0x00316BA1] == ("xor", "ebx, ebx")
      and u[0x00316BC1] == ("call", "0x315e90") and u[0x00316BCC] == ("call", "0x316bf0"))

# ---- H1 / H2 callback slot
s5 = ops(0x0036C5A0, 0x29)
cs = callers(0x0036C5A0)
pre = {a: [x for x in dis(f) if a - 16 <= x.address < a] for f, a in cs}
setp = sorted((next(x.op_str for x in pre[a] if x.mnemonic == "mov" and x.op_str.startswith("ecx")),
               next(retool.ann(x) for x in pre[a] if x.mnemonic == "lea" and x.op_str.startswith("rdx"))) for f, a in cs)
print("   0036C5A0 callers %s -> %s" % (["%08X@%08X" % c for c in cs], setp))
bf = ops(0x0036BFE0, 0x110)
init = ops(0x00369D30)
check("H1 setter 0036C5A0 writes desc+0xA0; only callers set arenas 6 and 10 to 002E6D60; init zeroes it; 0036BFE0 calls it",
      s5[0x0036C5B6] == ("mov", "qword ptr [rcx + rax + 0xa0], rdx") and [f for f, a in cs] == [0x002EA320, 0x002EA320]
      and [e for e, _ in setp] == ["ecx, 0xa", "ecx, 6"] and all("002E6D60" in t for _, t in setp)
      and init[0x00369D57] == ("xor", "r8d, r8d") and init[0x00369E36] == ("mov", "qword ptr [rbx + 0xa0], r8")
      and not any(a2 for a2 in init if 0x00369D57 < a2 < 0x00369E36 and init[a2][1].startswith(("r8,", "r8d,", "r8b,")))
      and bf[0x0036C02D] == ("mov", "rax, qword ptr [rdx + 0xa0]") and bf[0x0036C03B] == ("call", "rax"))
cb = dis(0x002E6D60, 0xC5)
rets = [x.address for x in cb if x.mnemonic == "ret"]
check("H2 002E6D60: one ret (002E6E24), reached only through 002E6E1E xor eax, eax - it always answers 0",
      rets == [0x002E6E24] and ops(0x002E6D60, 0xC5)[0x002E6E1E] == ("xor", "eax, eax")
      and all(not (m in ("jmp",) or m.startswith("j")) or int(o, 16) <= 0x002E6E1E or int(o, 16) > 0x002E6E24
              for m, o in [(x.mnemonic, x.op_str) for x in cb if x.mnemonic.startswith("j") and x.op_str.startswith("0x")])
      and ops(0x002E6D60, 0xC5)[0x002E6E20][0] == "add")

# ---- H3 handle-issuing entries
b160, b970 = callers(0x0036B160), callers(0x0036B970)
print("   0036B160: %d sites in %d bodies %s" % (len(b160), len(set(f for f, a in b160)), sorted(set("%08X" % f for f, a in b160))))
print("   0036B970 (-> 0036B980): %d sites in %d bodies %s" % (len(b970), len(set(f for f, a in b970)), sorted(set("%08X" % f for f, a in b970))))
ov40 = git("show", "%s^:Database/FFXII TZA/_index/candidates/ov40-reregistration-fable/reregister.py" % C)
check("H3 the handle entries have 15 sites in 11 bodies; OV-40's record already traces 003DC5B0 and 002E6EB0 as handle takers",
      len(b160) == 13 and len(b970) == 2 and callers(0x0036B980) == [(0x0036B970, 0x0036B97B)]
      and (0x003DC5B0, 0x003DC62D) in b160 and (0x002E6EB0, 0x002E6F4D) in b160
      and "0036B160 allocates, the handle goes to slot +0" in ov40 and "002E6EED-002E7001" in ov40)

# ---- H4 RC-11 push census
tsv = git("show", "%s^:Database/FFXII TZA/_index/candidates/rc11-arena-ten-0930/arena_sites.tsv" % C).splitlines()
vals = set()
for l in tsv[1:]:
    c = l.split("\t")
    if len(c) > 2:
        vals |= set(v for v in c[2].split(",") if v.isdigit())
print("   RC-11 arena values over %d push sites: %s" % (len(tsv) - 1, sorted(vals, key=int)))
check("H4 RC-11's 135-site push census (at the parent) selects no arena 7", len(tsv) - 1 == 135 and "7" not in vals)

# ---- K1 the SD-140 byte kernel
kc = callers(0x00432300)
print("   00432300: %d sites in %d bodies %s" % (len(kc), len(set(f for f, a in kc)), sorted(set("%08X" % f for f, a in kc))))
check("K1 the byte kernel 00432300 is shared: both consumers and both emit paths (00437130, 00438860) call it",
      {0x00434CD0, 0x00435050, 0x00437130, 0x00438860} <= set(f for f, a in kc))

print("FAILS %d" % FAILS)
