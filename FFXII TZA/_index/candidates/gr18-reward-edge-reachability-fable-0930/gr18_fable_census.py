"""gr18_fable_census.py - GR-18, FABLE's own census (read-only research helper, 2026-09-30).

Can the shipped game reach the synthetic edge states SECTION-03 executed through the reward computers?
  (a) a zero-count or missing reward descriptor        (b) a high relocation base
  (c) a level-zero reward (level at/below +0x88)       (d) the 0xFF selector matching a 0xFFFF stats identity

Evidence classes: STATIC (original bytes of the pinned EXE) and DATA (shipped files on D:/FFXII_TZA_extract and the
decompiled us script corpus). Nothing is executed. Every section prints PASS/FAIL lines, counts, and its positive controls;
the last line is FAILS n.

Run: python gr18_fable_census.py  (about 3-6 minutes; the image-wide store sweep dominates)
"""
import glob, hashlib, os, re, struct, sys, collections
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))          # .../Database
EXE = os.path.join(DBROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
EXTRACT = "D:/FFXII_TZA_extract"
CORPUS = os.path.join(DBROOT, "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
sys.path.insert(0, os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts"))

fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


# ---------------------------------------------------------------- image
raw = open(EXE, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
BASE = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
SECS = []
for k in range(nsec):
    s = pe + 24 + optsz + 40 * k
    name = raw[s:s + 8].rstrip(b"\0").decode()
    vsz, va, rsz, roff = struct.unpack_from("<IIII", raw, s + 8)
    chars = struct.unpack_from("<I", raw, s + 36)[0]
    SECS.append((name, BASE + va, vsz, rsz, roff, chars))


def at(a, n):
    for name, va, vsz, rsz, roff, ch in SECS:
        if va <= a < va + max(vsz, rsz):
            o = a - va
            out = raw[roff + o: roff + min(o + n, rsz)] if o < rsz else b""
            return out + b"\0" * (n - len(out))   # virtual tail reads as zero
    return None


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def ins(a):
    return next(md.disasm(at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = ins(a)
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return a + i.size + op.mem.disp
    return None


def expect(pairs):
    """[(addr, exact instruction text)] -> list of mismatches"""
    return [(hex(a), t, txt(a)) for a, t in pairs if txt(a) != t]


check("IMG", sha == EXE_SHA and BASE == 0x120000, "sha256 %s..., image base %X" % (sha[:16], BASE))

# ================================================================ (a) zero-count / missing reward descriptor
print("\n== (a) zero-count or missing reward descriptor")
# code facts the census depends on
code_a = expect([
    # the .ard load callback binds header slot 5 (+0x24) -> binder index 3 -> 02EBF148, slot 6 (+0x28) -> index 4 -> 02EBF140,
    # and binds a slot as NULL only when the header dword is 0 (decoded 0 under base 0)
    (0x003EA7AD, "mov ecx, dword ptr [rbp + 0x24]"), (0x003EA7CA, "xor edx, edx"), (0x003EA7CC, "mov ecx, 3"),
    (0x003EA7D6, "mov ecx, dword ptr [rbp + 0x28]"), (0x003EA7F3, "xor edx, edx"), (0x003EA7F5, "mov ecx, 4"),
    (0x003EA73B, "mov ecx, dword ptr [rbp + 0x10]"), (0x003EA751, "mov ecx, dword ptr [rbp + 0x18]"),
    (0x0023A187, "lea rcx, [rip + 0x2c84fba]"), (0x0023A178, "lea rcx, [rip + 0x2c84fc1]"),
    (0x0023A196, "lea rcx, [rip + 0x2c84f83]"),
    # 003845F0 stores the slot pointer, then relocates descriptor +0xC in 32 bits only when it is nonzero
    (0x003845F4, "mov qword ptr [rcx], rdx"), (0x00384600, "mov eax, dword ptr [rdx + 0xc]"),
    (0x0038460A, "je 0x384611"), (0x0038460C, "add eax, edx"), (0x0038460E, "mov dword ptr [rdx + 0xc], eax"),
    # installer: enemy-row guard (count 0 or NULL wraps to 0xFFFFFFFF and passes) and the NULL-table fault
    (0x0023A656, "mov eax, dword ptr [rbx + 4]"), (0x0023A65B, "xor eax, eax"), (0x0023A65D, "dec eax"),
    (0x0023A662, "ja 0x23a63a"), (0x0023A69F, "xor esi, esi"), (0x0023A6B4, "movzx eax, word ptr [rsi]"),
    # the two reward guards (unsigned, count-1)
    (0x0023A738, "mov ecx, dword ptr [rax + 4]"), (0x0023A73F, "movzx eax, word ptr [rsi + 0x22]"),
    (0x0023A743, "dec ecx"), (0x0023A747, "ja 0x23a63a"),
    (0x0023A759, "mov ecx, dword ptr [rax + 4]"), (0x0023A760, "movzx eax, word ptr [rsi + 0x24]"),
    (0x0023A764, "dec ecx"), (0x0023A768, "ja 0x23a63a"),
    # the two stores: NULL descriptor or decoded-zero base -> 0; otherwise 32-bit imul/add
    (0x0023A96F, "je 0x23a9a3"), (0x0023A97C, "je 0x23a9a3"), (0x0023A99C, "imul ecx, edx"), (0x0023A99F, "add ecx, eax"),
    (0x0023A9A3, "xor ecx, ecx"), (0x0023A9A5, "mov qword ptr [rdi + 0xe70], rcx"),
    (0x0023A9E3, "imul ecx, edx"), (0x0023A9E6, "add ecx, eax"), (0x0023A9EA, "xor ecx, ecx"),
    (0x0023A9F4, "mov qword ptr [rdi + 0xe78], rcx"),
    # btlAtelSetUnit (verb 3001, 00510160) -> 0023A3B0: id 0xFF -> 0xFFFF (no unit), else id | 0x100 (kind 1)
    (0x00510173, "call 0x267e10"), (0x0051017D, "call 0x23a3b0"), (0x0023A3D9, "cmp ebx, 0xff"),
    (0x0023A3E1, "bts ebx, 8"), (0x0023A3E7, "mov ebx, 0xffff"), (0x0023A3F1, "call 0x23a570"),
])
regs = {rip(0x0023A187): "02EBF148", rip(0x0023A178): "02EBF140", rip(0x0023A196): "02EBF120"}
check("A-code", not code_a and set(regs) == {0x02EBF148, 0x02EBF140, 0x02EBF120},
      "loader slot5->02EBF148 / slot6->02EBF140 / slot2->02EBF120, NULL only for a zero header dword; guards and stores as read; mismatches %s" % code_a)

u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]


def ard_table(b, k):
    o = u32(b, 0x10 + 4 * k)
    if not o:
        return None
    if b[o:o + 4] != b"st2e":
        return ("bad", o)
    return (o, u32(b, o + 4), u16(b, o + 8), u32(b, o + 0xC))   # (offset, count, stride word, data offset)


def ard_census(b):
    """returns (enemy_rows, flags Counter, max selectors) for one .ard image"""
    c = collections.Counter()
    t2, t5, t6 = ard_table(b, 2), ard_table(b, 5), ard_table(b, 6)
    for k, t in ((2, t2), (5, t5), (6, t6)):
        if t is None:
            c["slot%d missing" % k] += 1
        elif t[0] == "bad":
            c["slot%d not st2e" % k] += 1
        else:
            if t[1] == 0:
                c["slot%d count0" % k] += 1
            if t[3] == 0:
                c["slot%d dataoff0" % k] += 1
    rows = 0
    mx = [0, 0]
    if t2 and t2[0] != "bad" and t2[1]:
        for i in range(t2[1]):
            r = t2[0] + t2[3] + i * t2[2]
            rows += 1
            for j, (sel, t) in enumerate(((u16(b, r + 0x22), t5), (u16(b, r + 0x24), t6))):
                mx[j] = max(mx[j], sel)
                if t is None or t[0] == "bad":
                    c["row->missing"] += 1
                elif t[1] == 0:
                    c["row->count0"] += 1
                elif sel > t[1] - 1:
                    c["row->oob"] += 1
                elif t[3] == 0:
                    c["row->dataoff0"] += 1
    return rows, c, mx, (t2[1] if t2 and t2[0] != "bad" else None)


ards = sorted(glob.glob(EXTRACT + "/ps2data/plan_master/*/plan_map/*/area/*.ard"))
copies = collections.defaultdict(list)
for f in ards:
    copies[f.replace("\\", "/").split("/plan_master/")[1].split("/")[0]].append(f)
area_enemy_count = {}
tot = collections.Counter()
for lang in sorted(copies):
    files = copies[lang]
    rows_l = 0
    flags_l = collections.Counter()
    mx_l = [0, 0]
    with_rows = 0
    empty_areas = []
    for f in files:
        b = open(f, "rb").read()
        rows, c, mx, n2 = ard_census(b)
        area = os.path.basename(f)[:-4]
        area_enemy_count.setdefault(lang, {})[area] = n2
        rows_l += rows
        with_rows += rows > 0
        flags_l.update(c)
        mx_l = [max(mx_l[0], mx[0]), max(mx_l[1], mx[1])]
        if not rows:
            empty_areas.append((area, dict(c)))
    tot["files"] += len(files)
    tot["rows"] += rows_l
    row_bad = {k: v for k, v in flags_l.items() if k.startswith("row->")}
    print("   copy %-3s files %d, files with enemy rows %d, enemy rows %d, max +0x22 %d, max +0x24 %d, row defects %s"
          % (lang, len(files), with_rows, rows_l, mx_l[0], mx_l[1], row_bad or "{}"))
    print("   copy %-3s files with no enemy rows: %s" % (lang, empty_areas))
    check("A-data-" + lang, not row_bad, "every enemy row selects inside a present, non-empty reward table with a nonzero data offset")
print("   total .ard files %d, total enemy rows %d" % (tot["files"], tot["rows"]))
check("A-prior", tot["rows"] == 2292, "row total %d vs the 2026-09-15 two-copy census (2,292)" % tot["rows"])

# positive controls: the census must flag each defect it claims to exclude
src = next(f for f in copies["in"] if ard_census(open(f, "rb").read())[0])
b0 = bytearray(open(src, "rb").read())
t2, t5, t6 = ard_table(b0, 2), ard_table(b0, 5), ard_table(b0, 6)
r0 = t2[0] + t2[3]
m1 = bytearray(b0); struct.pack_into("<H", m1, r0 + 0x22, t5[1])                  # index == count
m2 = bytearray(b0); struct.pack_into("<I", m2, t6[0] + 4, 0)                        # slot-6 count 0
m3 = bytearray(b0); struct.pack_into("<I", m3, 0x10 + 4 * 5, 0)                     # slot 5 missing
m4 = bytearray(b0); struct.pack_into("<I", m4, t5[0] + 0xC, 0)                      # slot-5 data offset 0
got = [dict((k, v) for k, v in ard_census(bytes(m))[1].items() if k.startswith("row->")) for m in (m1, m2, m3, m4)]
ok = got[0].get("row->oob") == 1 and got[1].get("row->count0") == t2[1] and got[2].get("row->missing") == t2[1] \
    and got[3].get("row->dataoff0") == t2[1]
check("A-ctrl", ok, "mutated %s: oob / count0 / missing / dataoff0 flagged %s" % (os.path.basename(src), got))

# script side: the only kind-1 install from script is btlAtelSetUnit(id) (verb 3001); where do the ids land?
call_re = re.compile(r"btlAtelSetUnit\(([^)]*)\)")
per_area = collections.defaultdict(list)
nonlit = 0
ntok = 0
for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
    t = open(f, encoding="latin1").read()
    ntok += t.count("btlAtelSetUnit(")
    m = re.match(r"([a-z]{3}_[a-z0-9])", os.path.basename(f))
    for a in call_re.findall(t):
        if not a.strip().isdigit():
            nonlit += 1
            continue
        per_area[m.group(1) if m else "?"].append(int(a))
ncalls = sum(len(v) for v in per_area.values())


def violations(calls, counts_by_lang):
    out = []
    for lang in sorted(counts_by_lang):
        for area, ids in sorted(calls.items()):
            n2 = counts_by_lang[lang].get(area)
            if n2 is None or not n2 or max(ids) > n2 - 1:
                out.append((lang, area, n2, max(ids)))
    return out


no_ard = sorted(a for a in per_area if all(a not in area_enemy_count[l] for l in area_enemy_count))
viol = violations({a: v for a, v in per_area.items() if a not in no_ard}, area_enemy_count)
empty4 = sorted(a for a, n in area_enemy_count.get("in", {}).items() if not n)
print("   script areas with no .ard of the same name: %d (%s ... %s), %d btlAtelSetUnit calls, id range %d..%d"
      % (len(no_ard), no_ard[0], no_ard[-1], sum(len(per_area[a]) for a in no_ard),
         min(min(per_area[a]) for a in no_ard), max(max(per_area[a]) for a in no_ard)))
plan_dirs = {os.path.basename(p) for p in glob.glob(EXTRACT + "/ps2data/plan_master/in/plan_map/*")}
print("   of those, plan_map directories that exist (script-only zones): %d; examples %s"
      % (len([a for a in no_ard if a in plan_dirs]), [a for a in no_ard if a in plan_dirs][:4]))
print("   btlAtelSetUnit calls %d (tokens %d, non-literal %d) in %d areas; id range %d..%d; id 255 used %d times"
      % (ncalls, ntok, nonlit, len(per_area), min(min(v) for v in per_area.values()), max(max(v) for v in per_area.values()),
         sum(v.count(255) for v in per_area.values())))
print("   areas with an empty enemy table: %s; btlAtelSetUnit calls there: %d" % (empty4, sum(len(per_area.get(a, [])) for a in empty4)))
check("A-script", ncalls == ntok and not nonlit and not viol and not any(per_area.get(a) for a in empty4),
      "every script-selected id in an area with its own .ard is below that area's enemy-table count in both copies; no install in the four empty-table areas; violations %s" % viol[:5])
full = next(a for a, n in sorted(area_enemy_count["in"].items()) if n)
cv = violations({"zzz_z": [0], empty4[0]: [0], full: [area_enemy_count["in"][full]]}, {"in": area_enemy_count["in"]})
check("A-script-ctrl", [v[1] for v in cv] == sorted(["zzz_z", empty4[0], full]),
      "control: an unknown area, an install into empty-table %s, and id == count in %s are all reported: %s" % (empty4[0], full, cv))

# ================================================================ (b) a high relocation base
print("\n== (b) high relocation base")
code_b = expect([(0x0020E600, "mov eax, ecx"), (0x0020E602, "add rax, qword ptr [rip + 0x1d74f27]"), (0x0020E609, "ret"),
                 (0x0020E620, "sub ecx, dword ptr [rip + 0x1d74f0a]")])
base_cell = rip(0x0020E602)
data = next(s for s in SECS if s[0] == ".data")
past_raw = base_cell >= data[1] + data[3]
chars = struct.unpack_from("<H", raw, pe + 4 + 18)[0]
dllc = struct.unpack_from("<H", raw, pe + 24 + 70)[0]
check("B-code", not code_b and base_cell == 0x01F83530 and rip(0x0020E620) == 0x01F83530 and past_raw,
      "resolver = zero-extended u32 + qword [%08X]; the cell is past .data's raw end %08X, so it is 0 at image load" % (base_cell, data[1] + data[3]))
print("   PE: LARGE_ADDRESS_AWARE=%d  DYNAMICBASE=%d  HIGH_ENTROPY_VA=%d" % (bool(chars & 0x20), bool(dllc & 0x40), bool(dllc & 0x20)))
# every rip-relative operand naming the 8 bytes of the cell, over the function list (retool's cached scan)
import retool as T  # noqa: E402
cache = T.scan()
naming = sorted((s, k) for g, v in cache["refs"].items() if 0x01F83530 <= g < 0x01F83538 for (_, s, k) in v)
check("B-refs", naming == [(0x0020E602, "R"), (0x0020E620, "R")],
      "rip operands naming 01F83530..37: %s (the two resolver reads; control: both known reads are found)" % ["%08X %s" % x for x in naming])

# ================================================================ (c) level-zero reward
print("\n== (c) level at or below the +0x88 baseline")
code_c = expect([
    (0x002F8C63, "movzx esi, byte ptr [rax + 0x1c2]"), (0x002F8C6A, "movzx eax, byte ptr [rax + 0x88]"), (0x002F8C71, "sub esi, eax"),
    (0x0030C496, "mov byte ptr [rcx + 0x1c2], dil"), (0x0030C4B1, "mov byte ptr [rcx + 0x88], r8b"),
    (0x0030C568, "mov edx, r15d"), (0x0030C56E, "call 0x30c650"),
    (0x0030C67A, "cmp edx, eax"), (0x0030C682, "cmovg r14d, eax"), (0x0030C686, "cmp ecx, r14d"), (0x0030C689, "jge 0x30c87f"),
    (0x0030C7B3, "inc eax"), (0x0030C7B8, "cmova eax, ecx"), (0x0030C7BB, "mov byte ptr [rdi + 0x1c2], al"),
    (0x0023AD37, "mov edx, 1"), (0x0023AD3C, "mov r12d, edx"), (0x0023AD8B, "mov r8d, r12d"),
    (0x0023991D, "call 0x328370"), (0x00239922, "lea ecx, [rsi + 1]"), (0x00239926, "idiv ecx"),
    (0x0023992F, "mov r8d, edi"), (0x00239932, "add edx, edi"), (0x00239934, "call 0x30c470"),
    (0x0050F928, "call 0x267e10"), (0x0050F930, "mov ebx, eax"), (0x0050F937, "mov r8d, eax"), (0x0050F93A, "mov edx, ebx"),
    (0x003069E8, "xor r8d, r8d"), (0x00316E33, "xor r8d, r8d"), (0x0031761E, "xor r8d, r8d"), (0x00239BE7, "xor r8d, r8d"),
])
grower_callers = sorted(s for _, s in cache["calls"].get(0x0030C470, ()))
check("C-code", not code_c and grower_callers == [0x00239934, 0x00239BED, 0x0023AD96, 0x003069EE, 0x00316E3D, 0x0031762C],
      "D = u8 level - u8 baseline; grower resets level 0 then grows to min(target, 99) (signed cmovg); baseline = r8 (kind 1); "
      "callers %s: enemy init (1, 1), btlAtelSetLevel (base + rand %% (n + 1), base), four with r8 = 0; mismatches %s"
      % (["%08X" % s for s in grower_callers], code_c))

# rand is non-negative: 00328370 returns ((b<<10 ^ c) << 10) ^ d with 11/10/10-bit fields -> [0, 2^31)
rand_ok = not expect([(0x0032838A, "and edx, 0x7ff"), (0x003283A6, "and r8d, 0x3ff"), (0x003283C2, "and eax, 0x3ff"),
                      (0x00328390, "shl edx, 0xa"), (0x003283B0, "shl r8d, 0xa")])
check("C-rand", rand_ok, "00328370 returns at most 31 bits, so draw % (n + 1) is >= 0 for any n != -1")


def s32(v):
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def grown_level(target):
    t = s32(target)
    t = 99 if t > 99 else t
    return t if t > 0 else 0


def d_range(base, n):
    """(Dmin, Dmax) for btlAtelSetLevel's native arguments: rdx = n (range), r8 = base; None if n + 1 == 0 (#DE)"""
    m = s32(n + 1)
    if m == 0:
        return None
    hi = abs(m) - 1
    lo_l, hi_l = grown_level(base), grown_level(base + hi)
    bl = base & 0xFF
    return lo_l - bl, hi_l - bl


# positive controls on the evaluator: it must see the clamp, the u8 truncation and the zero floor
ctrl = {(100, 0): d_range(100, 0), (300, 0): d_range(300, 0), (99, 5): d_range(99, 5), (1, 0): d_range(1, 0), (-3, 1): d_range(-3, 1)}
check("C-eval-ctrl", ctrl[(100, 0)] == (-1, -1) and ctrl[(300, 0)] == (55, 55) and ctrl[(99, 5)] == (0, 0) and ctrl[(1, 0)] == (0, 0)
      and ctrl[(-3, 1)] == (-253, -253), "evaluator controls %s" % ctrl)

lv_re = re.compile(r"btlAtelSetLevel\(([^)]*)\)")
pairs = collections.Counter()
ntok = nonlit = 0
for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
    t = open(f, encoding="latin1").read()
    ntok += t.count("btlAtelSetLevel(")
    for a in lv_re.findall(t):
        p = [x.strip() for x in a.split(",")]
        if len(p) != 2 or not all(re.fullmatch(r"-?\d+", x) for x in p):
            nonlit += 1
            continue
        pairs[(int(p[0]), int(p[1]))] += 1
ncall = sum(pairs.values())
a1 = [k[0] for k in pairs]
a2 = [k[1] for k in pairs]
print("   btlAtelSetLevel calls %d (tokens %d, non-literal %d), %d distinct pairs; script arg1 %d..%d, arg2 %d..%d"
      % (ncall, ntok, nonlit, len(pairs), min(a1), max(a1), min(a2), max(a2)))
res = {}
for order, pick in (("base=arg1,n=arg2", lambda k: (k[0], k[1])), ("base=arg2,n=arg1", lambda k: (k[1], k[0]))):
    dmin = None
    neg = zero_always = fault = 0
    lvl0 = 0
    for k, c in pairs.items():
        base, n = pick(k)
        r = d_range(base, n)
        if r is None:
            fault += c
            continue
        dmin = r[0] if dmin is None else min(dmin, r[0])
        neg += c if r[0] < 0 else 0
        zero_always += c if r == (0, 0) else 0
        lvl0 += c if grown_level(base) == 0 else 0
    res[order] = (dmin, neg, fault, zero_always, lvl0)
    print("   order %-17s: min D %d; calls that can give D < 0: %d; n = -1 faults: %d; calls pinned at D = 0: %d; calls that can grow level 0: %d"
          % (order, dmin, neg, fault, zero_always, lvl0))
top0 = sorted(((c, k) for k, c in pairs.items() if k[1] == 0), reverse=True)[:3]
print("   most frequent arg2 = 0 calls (D = 0 under base=arg1): %s" % ["btlAtelSetLevel(%d, %d) x%d" % (k[0], k[1], c) for c, k in top0])
check("C-script", ncall == ntok and not nonlit and all(v[1] == 0 and v[2] == 0 for v in res.values()),
      "no shipped btlAtelSetLevel call can give level < baseline under either argument order")

# the store sweep: every instruction whose memory destination covers +0x1C2 or +0x88 (and the spawn-record copies +0x242 /
# +0x108 of the embedded page at record+0x80), off any base register but rip / rsp; function list + linear .text sweep
txt_sec = next(s for s in SECS if s[0] == ".text")
sizes = T.sizes()
PROBE = [0x1C2, 0x88, 0x242, 0x108, 0x54]
hits = collections.defaultdict(set)
block = []


def scan_ins(i):
    if not i.operands:
        return
    if i.mnemonic.startswith(("rep", "stos", "movs")) and any(op.type == X.X86_OP_MEM and op.mem.base in (X.X86_REG_RDI, X.X86_REG_EDI) for op in i.operands):
        block.append(i.address)
    for op in i.operands:
        if op.type != X.X86_OP_MEM or not (op.access & capstone.CS_AC_WRITE):
            continue
        if op.mem.base in (X.X86_REG_RIP, X.X86_REG_RSP, X.X86_REG_INVALID):
            continue
        lo, hi = op.mem.disp, op.mem.disp + op.size
        for p in PROBE:
            if lo <= p < hi:
                hits[p].add((i.address, "%s %s" % (i.mnemonic, i.op_str)))


seen = set()
for f, n in sizes.items():
    d = at(f, n)
    if not d:
        continue
    for i in md.disasm(d, f):
        seen.add(i.address)
        scan_ins(i)
# linear sweep of the whole .text as a second route (catches code outside the function list)
a = txt_sec[1]
end = txt_sec[1] + txt_sec[2]
CH = 0x10000
nlin = 0
while a < end:
    d = at(a, min(CH + 16, end - a))
    last = a
    for i in md.disasm(d, a):
        if i.address >= a + CH:
            break
        last = i.address + i.size
        if i.address not in seen:
            nlin += 1
            scan_ins(i)
    a = last if last > a else a + 1   # stop at an undecodable byte: step over it
print("   store sweep: %d listed functions, %d instructions decoded only by the linear .text sweep" % (len(sizes), nlin))


import bisect  # noqa: E402
_starts = sorted(sizes)


def fn(addr):
    k = bisect.bisect_right(_starts, addr) - 1
    while k >= 0:
        f = _starts[k]
        if f <= addr < f + sizes[f]:
            return f
        if addr - f > 0x20000:
            break
        k -= 1
    return None


ctl_ok = 0x0023ACC2 in {s for s, _ in hits[0x54]} and \
    not any(s == 0x0023ACD5 for s, _ in hits[0x1C2]) and \
    {0x0030C496, 0x0030C7BB} <= {s for s, _ in hits[0x1C2]} and 0x0030C4B1 in {s for s, _ in hits[0x88]}
check("C-sweep-ctrl", ctl_ok, "width control: qword store 0023ACC2 [rdi+0x50] covers +0x54 (found); word store 0023ACD5 [rdi+0x1c3] does not cover +0x1C2 (not flagged); the grower's three stores found")
with open(os.path.join(HERE, "gr18_store_sweep.tsv"), "w", encoding="utf-8") as w:
    w.write("probe\tsite\tfunction\tinstruction\n")
    for p in PROBE:
        for s, t in sorted(hits[p]):
            f = fn(s)
            w.write("+0x%X\t%08X\t%s\t%s\n" % (p, s, "%08X" % f if f else "-", t))
narrow = {0x1C2: re.compile(r"(byte ptr \[\w+ \+ 0x1c2\]|(?<![dqx])word ptr \[\w+ \+ 0x1c[12]\])"),
          0x242: re.compile(r"(byte ptr \[\w+ \+ 0x242\]|(?<![dqx])word ptr \[\w+ \+ 0x24[12]\])"),
          0x88: re.compile(r"(byte ptr \[\w+ \+ 0x88\]|(?<![dqx])word ptr \[\w+ \+ 0x8[78]\])"),
          0x108: re.compile(r"(byte ptr \[\w+ \+ 0x108\]|(?<![dqx])word ptr \[\w+ \+ 0x10[78]\])")}
for p in (0x1C2, 0x242, 0x88, 0x108):
    nb = sorted((s, t) for s, t in hits[p] if narrow[p].search(t) and not re.search(r"\w+\*\d", t.split(",")[0]))
    print("   writes covering +0x%X: %d in total (all in gr18_store_sweep.tsv); byte/word-width with no index register: %d"
          % (p, len(hits[p]), len(nb)))
    if p in (0x1C2, 0x242):
        for s, t in nb:
            f = fn(s)
            print("      %08X  in %s  %s" % (s, "%08X" % f if f else "(no listed function)", t))
# classify the byte/word level stores: the grower pair, and three that are not stats records (read above, asserted here)
not_stats = expect([(0x003AF7F2, "movzx ecx, byte ptr [rax + 0x1c2]"), (0x003AF805, "dec cl"),
                    (0x003DCF97, "mov word ptr [rcx + 0x1c0], ax"), (0x003DD16F, "mov word ptr [rcx + 0x1c0], r15w"),
                    (0x0032923C, "mov rcx, rdi"), (0x0032923F, "mov r8d, 0xc0"), (0x00327CC3, "movzx eax, byte ptr [rcx + 5]"),
                    (0x00327CCE, "jne 0x327dcf")])
print("   003AF80F (003AF460, the render-block countdown +0x1C2 the OPUS census names), 003DCF9E / 003DD177 (word pairs +0x178..+0x1C2 "
      "at stride 0x18: not the stats layout): %s" % ("as read" if not not_stats else not_stats))
# +0x88: many structures use it; list the writers that sit in functions of the typed stats / spawn-record censuses
typed = set()
for tsv in ("08-Combat-Formula/Battle-Stats-Record/battle-stats-record-accesses.tsv",
            "05-Spawn-Encounter-Lifecycle/Spawn-Record/spawn-record-accesses.tsv"):
    for line in open(os.path.join(DBROOT, "FFXII TZA", tsv), encoding="utf-8").read().splitlines()[1:]:
        c0 = line.split("\t")[0]
        if re.fullmatch(r"[0-9A-Fa-f]{8}", c0):
            typed.add(int(c0, 16))
for p in (0x1C2, 0x88, 0x242, 0x108):
    hp = sorted(hits[p])
    hp_typed = [(s, t) for s, t in hp if fn(s) in typed]
    print("   writes covering +0x%X image-wide: %d in %d functions; in functions of the typed stats / spawn-record censuses (%d functions): %d"
          % (p, len(hp), len({fn(s) for s, _ in hp}), len(typed), len(hp_typed)))
    for s, t in hp_typed:
        print("      %08X  in %08X  %s" % (s, fn(s), t))
print("   string / block store instructions (rep stos / rep movs) with an rdi destination: %d (not attributed here)" % len(block))
# the byte/word +0x88 writers image-wide: does the function reach a stats record at all?
STATS_GETTERS = {0x00320A40, 0x00320AB0, 0x0031B860, 0x0031B810, 0x002367A0, 0x00236100}
rx88 = narrow[0x88]
n88 = sorted((s, t) for s, t in hits[0x88] if rx88.search(t) and not re.search(r"\w+\*\d", t.split(",")[0]))
print("   byte/word +0x88 writers image-wide (%d): does the writing function touch a stats record?" % len(n88))
linked = []
for s, t in n88:
    f = fn(s)
    body = list(md.disasm(at(f, sizes[f]), f)) if f else []
    loads698 = any(re.search(r"\[\w+ \+ 0x698\]", i.op_str) for i in body)
    callees = {i.operands[0].imm for i in body if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM}
    g = sorted("%08X" % c for c in callees & STATS_GETTERS)
    tag = ("typed-census " if f in typed else "") + ("loads +0x698 " if loads698 else "") + ("calls %s" % ",".join(g) if g else "")
    if tag:
        linked.append(s)
    print("      %08X  in %s  %-40s %s" % (s, "%08X" % f if f else "-", t, tag or "-"))
print("   of those, in a function with any stats-record link: %d (%s)" % (len(linked), " ".join("%08X" % s for s in linked)))

print("\n== (d) the 0xFF selector against a 0xFFFF stats identity")
code_d = expect([
    (0x002F8C96, "call 0x31b810"), (0x002F8CE2, "cmp ebx, 4"),
    (0x0031B81E, "lea ecx, [r8 + 0x17]"), (0x0031B822, "call 0x322c50"), (0x0031B82B, "mov al, 0xff"),
    (0x0031B841, "movzx eax, byte ptr [rax + rbx*2 + 0x5a5a]"),
    (0x002367B8, "lea ecx, [r8 + 2]"), (0x002367BC, "call 0x322c50"), (0x002367C3, "je 0x236803"),
    (0x002367E3, "cmp edi, 0xff"), (0x002367E9, "mov ecx, 0xffff"), (0x002367EE, "cmovne ecx, edi"),
    (0x00322C9A, "mov rcx, qword ptr [rip + 0x2b9c48f]"), (0x00322CA1, "xor eax, eax"), (0x00322CAC, "mov ecx, dword ptr [rcx + 4]"),
    (0x0032302E, "cmp ebx, edx"), (0x00323030, "jl 0x322c8d"), (0x00323036, "lea eax, [rcx - 1]"), (0x0032303B, "jg 0x322c8d"),
    (0x00322FAF, "mov ecx, 9"),
    (0x00236DA0, "lea rcx, [rip + 0x2c88389]"), (0x00236DA7, "movsxd rdx, dword ptr [rax + 0x44]"), (0x00236DAB, "call 0x3845f0"),
])
cls = lambda k: BASE + struct.unpack("<I", at(BASE + 0x203054 + 4 * (k - 1), 4))[0]
slot130 = sorted((s, k) for g, v in cache["refs"].items() if 0x02EBF130 <= g < 0x02EBF138 for (_, s, k) in v if k in ("W", "lea"))
readers130 = sorted(s for g, v in cache["refs"].items() if 0x02EBF130 <= g < 0x02EBF138 for (_, s, k) in v)
check("D-code", not code_d and cls(2) == 0x00322C9A and cls(0x17) == 0x00322FAF and rip(0x00322C9A) == 0x02EBF130
      and rip(0x00236DA0) == 0x02EBF130 and slot130 == [(0x00236DA0, "lea")],
      "0xFF only for an empty member byte; 002367A0(0xFF) matches 0xFFFF only if class 2 admits 0xFF, i.e. [02EBF130]+4 >= 256; "
      "02EBF130 is bound once, from battle_pack +0x44 (00236DA0, its only lea/store; %d rip references in all); mismatches %s"
      % (len(readers130), code_d))
counts = {}
for bp in sorted(glob.glob(EXTRACT + "/ps2data/image/ff12/test_battle/*/binaryfile/battle_pack.bin")):
    b = open(bp, "rb").read()
    o = u32(b, 0x44)
    lang = bp.replace("\\", "/").split("/test_battle/")[1].split("/")[0]
    counts[lang] = (b[o:o + 4] == b"st2e", u32(b, o + 4))
print("   chr_data (battle_pack +0x44) per language: %s" % {k: v[1] for k, v in counts.items()})
admits = lambda n: 0 <= 0xFF <= n - 1
check("D-data", len(counts) == 9 and all(v[0] for v in counts.values()) and not any(admits(v[1]) for v in counts.values()),
      "all nine packs: st2e table with count %s; 0xFF admitted by none" % sorted({v[1] for v in counts.values()}))
check("D-ctrl", admits(256) and not admits(255) and not admits(40), "bound control: count 256 admits 0xFF (SECTION-03's fixture), 255 and 40 do not")

print("\nFAILS %d" % fails)
