"""sd162_award_path.py - SD-162: where the Trial Mode award calls sit in their stage scripts (SWE2-ORACLE, 2026-09-30).

Script-corpus evidence (the shipped .ebp bytecode), plus one static read of the image's kind-5 path table to pair each
tri_* file with its field number. Nothing here is native execution or a run-time observation.

For every call of script verb 0x5AD (unkCall_5ad) in every shipped .ebp:
  1. the site is re-found with FABLE's decoder (gen_req_channel_census.py) exactly as script_award_verb_census.py does,
     and the totals are checked against that census (900 x index 39, 900 x index 40 in tri_*, 9 x index 33);
  2. the enclosing script and function are named from the directory entry (+0x00 name, +0x08 start, +0x10 function
     table, +0x14 jump table; BW-5 in section-000-bytecode.md);
  3. the function is cut into basic blocks (jump immediates index the script's jump table; conditional jumps are
     0x52-0x57, 0x5B, 0x5C; unconditional 0x51, 0x5A, 0x60; returns 0x2D-0x30; bf1-opcode-semantics README), the
     dominator tree is built, and every branch that every path to the award must take is recorded with its test,
     rebuilt from the block's own stack code;
  4. the waitv call that dominates the award is found and its variable reference resolved through the file's
     descriptor table (header +0x28; script-variables page 2.2);
  5. each file's field number comes from the kind-5 path table (01E50B70, index 3 x field, 0032FD44), and the
     guards are evaluated with nowmap() equal to it.
Controls: see the CHECK lines. Output: sd162_award_path.out (this script's stdout) and sd162-award-sites.tsv.
Run from anywhere: python sd162_award_path.py > sd162_award_path.out
"""
import collections, hashlib, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))           # Database/FFXII TZA
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
sys.path.insert(0, os.path.join(DB, "_index", "candidates", "swe2contract-ddres-b1-0930"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))               # repository root: the decoder's relative paths
import gen_req_channel_census as G  # noqa: E402
import block_writer_disjoint as IMG  # noqa: E402  (certified image reader, BASE 0x120000)

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
I32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
FAILS = []


def check(tag, ok, msg):
    print("CHECK %-4s %s  %s" % (tag, "PASS" if ok else "FAIL", msg))
    if not ok:
        FAILS.append(tag)


V_WAITV, V_NOWMAP, V_AWARD, V_ITEMMES, V_GAUGEOPEN, V_EVGROUP = 0x005, 0x090, 0x5AD, 0x480, 0x3CA, 0x3030
COND = set(range(0x52, 0x58)) | {0x5B, 0x5C}
UNCOND = {0x51, 0x5A, 0x60}
RETS = {0x2D, 0x2E, 0x2F, 0x30}
CALLS = {0x58, 0x59, 0x5D, 0x5E}
BINSYM = {0x05: "||", 0x06: "&&", 0x07: "|", 0x08: "^", 0x09: "&", 0x0A: "==", 0x0B: "!=", 0x0C: ">", 0x0D: "<",
          0x0E: ">=", 0x0F: "<=", 0x10: "<<", 0x11: ">>", 0x12: "+", 0x13: "-", 0x14: "*", 0x15: "/", 0x16: "%"}
verbs = G.load_verbs()


def cstr(sec, o):
    return sec[o:sec.find(b"\0", o)].decode("cp932", "replace")


def parse(sec):
    """The script directory: [(name, start, end, funcs[(name, off)], jumps[off])]; offsets inside the script."""
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    pool = U32(sec, 0x4C)
    out = []
    for s in range(cnt):
        e = diroff + 4 + s * 0x30
        ft, jt = U32(sec, e + 0x10), U32(sec, e + 0x14)
        funcs = [(cstr(sec, pool + U32(sec, ft + 4 + 8 * i)), U32(sec, ft + 8 + 8 * i)) for i in range(U32(sec, ft))]
        jumps = [U32(sec, jt + 4 + 4 * i) for i in range(U32(sec, jt))]
        out.append([cstr(sec, pool + U32(sec, e)), U32(sec, e + 8), None, funcs, jumps])
    starts = sorted(set(x[1] for x in out))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for x in out:
        x[2] = min(b for b in bounds if b > x[1])
    return out


# ---- expressions: tuples, evaluated with nowmap() bound ----
def show(n):
    k = n[0]
    if k == "c":
        return ("0x%04x" % n[1]) if abs(n[1]) > 9 else str(n[1])
    if k == "call":
        return "%s(%s)" % (n[1], ", ".join(show(a) for a in n[2]))
    if k == "bin":
        return "(%s %s %s)" % (show(n[2]), n[1], show(n[3]))
    if k == "un":
        return "%s%s" % (n[1], show(n[2]))
    return n[1] if len(n) > 1 else "?"


def ev(n, nm):
    k = n[0]
    if k == "c":
        return n[1]
    if k == "call" and n[1] == "nowmap" and not n[2]:
        return nm
    if k == "un":
        v = ev(n[2], nm)
        return None if v is None else (int(not v) if n[1] == "!" else ~v)
    if k == "bin":
        a, b = ev(n[2], nm), ev(n[3], nm)
        op = n[1]
        if op == "||" and (a or b):
            return 1
        if op == "&&" and (a == 0 or b == 0):
            return 0
        if a is None or b is None:
            return None
        return int({"||": a or b, "&&": a and b, "==": a == b, "!=": a != b, ">": a > b, "<": a < b, ">=": a >= b,
                    "<=": a <= b}.get(op, 0)) if op in ("||", "&&", "==", "!=", ">", "<", ">=", "<=") else None
    return None


def symexec(ins, sec, ipool, vtab):
    """Stack-evaluate one block; return (condition node for its closing branch or None, [(pc, verb, args)])."""
    st, regs, calls = [], {"A": ("r", "A"), "X": ("r", "X"), "Y": ("r", "Y")}, []
    pop = lambda: st.pop() if st else ("?", "?")
    def var(i):
        d = U32(sec, vtab + 4 + i * 8)
        return ("v", "var[cls%d@0x%x]" % ((d >> 24) & 7, d & 0xFFFFFF)), d
    cond = None
    for pc, op, imm in ins:
        if op == 0x4F:
            st.append(("c", imm - 0x10000 if imm & 0x8000 else imm))
        elif op == 0x4E:
            st.append(("c", I32(sec, ipool + 4 + imm * 4)))
        elif 0x3E <= op <= 0x41:
            st.append(regs.get("I%d" % (op - 0x3E), ("r", "I%d" % (op - 0x3E))))
        elif 0x42 <= op <= 0x45 or op == 0x50:
            st.append(("r", "float"))
        elif op in (0x1B, 0x1D, 0x1E):
            st.append(regs[{0x1B: "A", 0x1D: "X", 0x1E: "Y"}[op]])
        elif op in (0x1C, 0x1F, 0x20):
            regs[{0x1C: "A", 0x1F: "X", 0x20: "Y"}[op]] = pop()
        elif 0x36 <= op <= 0x39:
            regs["I%d" % (op - 0x36)] = pop()
        elif 0x3A <= op <= 0x3D or op in (0x46, 0x49):
            pop()
        elif op == 0x48:
            st.append(var(imm)[0])
        elif op == 0x4B:
            st.append(("ref", "&" + var(imm)[0][1], imm))
        elif op in (0x4A, 0x4C, 0x4D):
            st.append(("r", "op%02x[%d]" % (op, imm)))
        elif op in BINSYM:
            b, a = pop(), pop()
            st.append(("bin", BINSYM[op], a, b))
        elif op in (0x17, 0x18):
            st.append(("un", "!" if op == 0x17 else "~", pop()))
        elif op in CALLS:
            ar, pu, nm = verbs.get(imm, (None, 0, "call_%x" % imm))
            ar = ar or 0
            args = [pop() for _ in range(ar)][::-1]
            if op in (0x59, 0x5E):
                pop()
            calls.append((pc, imm, args))
            res = ("call", nm, args)
            if pu and op in (0x58, 0x59):
                st.append(res)
            elif op in (0x5D, 0x5E):
                regs["A"] = res
        elif op == 0x5C:
            cond = ("un", "!", pop())         # taken when zero: the taken edge carries !c, fall-through c
        elif op == 0x5B:
            cond = pop()                      # taken when non-zero
        elif op in (0x52, 0x53, 0x54, 0x55, 0x56):
            cond = ("bin", {0x52: "==", 0x53: ">", 0x54: ">=", 0x55: "<", 0x56: "<="}[op], pop(), regs["Y"])
        elif op == 0x57:
            b, a = pop(), pop()
            cond = ("bin", "between", ("bin", ",", a, b), regs["Y"])
        elif op == 0x5A:
            regs["X"] = pop()
        elif op in G.CHANNEL_OPS or op in G.DESCRIPTOR_CONSUMERS:
            for _ in range(G.NARGS.get(op, 3)):
                pop()
    return cond, calls


def cfg(ins, fo, jumps):
    """Blocks of one function. ins pcs are function-relative; jump targets come from the script's jump table."""
    tgt = lambda imm: jumps[imm] - fo if imm < len(jumps) else None
    leaders = {0}
    bad = 0
    for k, (pc, op, imm) in enumerate(ins):
        if op in COND or op in UNCOND:
            t = tgt(imm)
            if t is None or not any(p == t for p, _, _ in ins):
                bad += 1
            else:
                leaders.add(t)
        if (op in COND or op in UNCOND or op in RETS) and k + 1 < len(ins):
            leaders.add(ins[k + 1][0])
    order = sorted(l for l in leaders if any(p == l for p, _, _ in ins))
    idx = {p: k for k, (p, _, _) in enumerate(ins)}
    blocks = []
    for b, l in enumerate(order):
        e = order[b + 1] if b + 1 < len(order) else None
        blocks.append([i for i in ins[idx[l]:] if e is None or i[0] < e])
    bid = {bl[0][0]: b for b, bl in enumerate(blocks)}
    succ = []
    for b, bl in enumerate(blocks):
        pc, op, imm = bl[-1]
        ft = [b + 1] if b + 1 < len(blocks) else []
        t = tgt(imm) if (op in COND or op in UNCOND) else None
        if op in COND:
            succ.append([("f", ft[0]) if ft else None, ("t", bid.get(t))])
        elif op in UNCOND:
            succ.append([("t", bid.get(t))])
        elif op in RETS:
            succ.append([])
        else:
            succ.append([("f", x) for x in ft])
        succ[-1] = [s for s in succ[-1] if s and s[1] is not None]
    return blocks, succ, bad


def dominators(n, succ):
    preds = [[] for _ in range(n)]
    for b in range(n):
        for _, s in succ[b]:
            preds[s].append(b)
    reach, work = {0}, [0]
    while work:
        b = work.pop()
        for _, s in succ[b]:
            if s not in reach:
                reach.add(s)
                work.append(s)
    dom = {b: set(reach) for b in reach}
    dom[0] = {0}
    changed = True
    while changed:
        changed = False
        for b in sorted(reach - {0}):
            ps = [p for p in preds[b] if p in reach]
            new = set.intersection(*[dom[p] for p in ps]) | {b} if ps else {b}
            if new != dom[b]:
                dom[b], changed = new, True
    return dom, reach, preds


def reaches(src, dst, succ, avoid):
    seen, work = {src}, [src]
    while work:
        b = work.pop()
        if b == dst:
            return True
        for _, s in succ[b]:
            if s != avoid and s not in seen:
                seen.add(s)
                work.append(s)
    return False


def guards(target, blocks, succ, dom, conds):
    """Every conditional branch that all paths from the entry to `target` must take, in pc order."""
    out = []
    for d in sorted(dom[target] - {target}):
        c = conds[d]
        if c is None or len(succ[d]) != 2:
            continue
        ok = [kind for kind, s in succ[d] if s == target or reaches(s, target, succ, d)]
        if len(ok) == 1:
            out.append((blocks[d][-1][0], c if ok[0] == "t" else ("un", "!", c)))
    return out


def simp(n):
    """!(!x) -> x, !(a != b) -> a == b, !(a == b) -> a != b."""
    if n[0] == "un" and n[1] == "!":
        m = n[2]
        if m[0] == "un" and m[1] == "!":
            return simp(m[2])
        if m[0] == "bin" and m[1] in ("==", "!="):
            return ("bin", "!=" if m[1] == "==" else "==", m[2], m[3])
    return n


# ---- the image: field number -> script file, from the kind-5 path table ----
at = IMG.load()
KIND5 = 0x01E50B70


def kind5_ebp(field):
    q = struct.unpack("<Q", at(KIND5 + 8 * 3 * field, 8))[0]
    if not q:
        return None
    d = at(q, 160) or b""
    return d.split(b"\0")[0].decode("latin1").split("\\")[-1]


field_of = {}
for fld in range(0, 1400):
    n = kind5_ebp(fld)
    if n and n.endswith(".ebp"):
        field_of.setdefault(n[:-4], fld)
# the table's slot 3N is the field's .ebp (0032FD3F-0032FD44: kind 5, index r15 + r15*2); controls from outside Trial Mode
check("M1", kind5_ebp(0) == "tst_a01.ebp", "kind-5 slot 0 = tst_a01.ebp (the table's first entry, vbf-archive page UQ-72)")
check("M2", field_of.get("slm_a01") == 701, "slm_a01 (the only other unkCall_5ad file) sits at field 701 = 0x2bd, "
      "inside the 701-708 Lowtown run (North Sprawl, South Sprawl) of the field-record page C-10: got %s" % field_of.get("slm_a01"))
tri_fields = {k: v for k, v in field_of.items() if k.startswith("tri_")}
exp = {"tri_%s%02d" % (chr(97 + g), s + 1): 0x483 + 8 * g + s for g in range(20) for s in range(5)}
check("M3", tri_fields == exp, "the 100 tri_* files occupy fields 0x483 + 8*group + (stage-1), groups a..t, stages 01..05 "
      "(%d of 100 match); tri_a01 = 0x483 (the Trial Mode load field, FV-1), tri_j05 = 0x%x, tri_t05 = 0x%x"
      % (sum(tri_fields.get(k) == v for k, v in exp.items()), tri_fields.get("tri_j05", -1), tri_fields.get("tri_t05", -1)))
stage_no = {k: 5 * (ord(k[4]) - 97) + int(k[5:7]) for k in exp}      # a01 = 1 ... t05 = 100

# ---- the corpus ----
f = io.open(G.VBF, "rb")
names, blocks_idx = G.V.load_index(f)
award_rows, other_awards, calls_total = [], [], 0
per_file = collections.Counter()
ctrl_item, ctrl_gauge = [], []
fn_hash = collections.Counter()
popv_s1_6 = 0
evgroup = collections.Counter()
filegroups = collections.defaultdict(collections.Counter)
jump_bad = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks_idx, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18)
    if U32(sec, diroff) > 0x400 or diroff + 4 + U32(sec, diroff) * 0x30 > len(sec):
        continue
    istri = "/tri_" in path
    ipool, vtab = U32(sec, 0x20), U32(sec, 0x28)
    seen = set()
    for sname, start, end, funcs, jumps in parse(sec):
        if start in seen:                     # duplicate directory entries share one body
            continue
        seen.add(start)
        fs = sorted(funcs, key=lambda x: x[1])
        for fi, (fname, fo) in enumerate(fs):
            fe = fs[fi + 1][1] if fi + 1 < len(fs) else end - start
            if fe <= fo:
                continue
            ins, _ = G.decode(sec[start + fo:start + fe])
            ops = [op for _, op, _ in ins]
            calls_total += sum(1 for o in ops if o in CALLS)
            if istri:
                for pc, op, imm in ins:
                    if op == 0x49:
                        d = U32(sec, vtab + 4 + imm * 8)
                        popv_s1_6 += ((d >> 24) & 7) == 4 and (d & 0xFFFFFF) == 6
                    if op in CALLS and imm == V_EVGROUP:
                        k = [i for i, x in enumerate(ins) if x[0] == pc][0]
                        a, stt = G.resolve_args(ins, k, 2 + (op in (0x59, 0x5E)), verbs)
                        grp = a[0] if stt == "ok" else None           # (group, mode[, actor]): the group is pushed first
                        key = ("g%d" % grp[1]) if grp and grp[0] == "PUSHII" else ("non-constant:%s" % (grp or stt,))
                        evgroup[key] += 1
                        filegroups[(path.split("/")[-1][:-4], path.split("/")[2])][key] += 1
            want = [(pc, imm) for pc, op, imm in ins if op in CALLS and imm in (V_AWARD, V_ITEMMES, V_GAUGEOPEN)]
            if not any(v == V_AWARD for _, v in want) and not (istri and want):
                continue
            blocks, succ, bad = cfg(ins, fo, jumps)
            jump_bad += bad
            dom, reach, preds = dominators(len(blocks), succ)
            conds, bcalls = [], []
            for bl in blocks:
                c, cl = symexec(bl, sec, ipool, vtab)
                conds.append(c)
                bcalls.append(cl)
            where = {pc: bi for bi, bl in enumerate(blocks) for pc, _, _ in bl}
            waits = [(bi, pc, args) for bi, cl in enumerate(bcalls) for pc, v, args in cl if v == V_WAITV]
            for pc, v in want:
                bi = where[pc]
                args = [a for p, vv, a in bcalls[bi] if p == pc][0]
                g = [(gpc, simp(c)) for gpc, c in guards(bi, blocks, succ, dom, conds)]
                w = [(wpc, a) for wb, wpc, a in waits if wb in dom.get(bi, ()) and (wb != bi or wpc < pc)]
                wref = w[0][1][0] if w and w[0][1] else None
                wdesc = None
                if wref and wref[0] == "ref":
                    d = U32(sec, vtab + 4 + wref[2] * 8)
                    wdesc = ((d >> 24) & 7, d & 0xFFFFFF)
                row = dict(tri=istri, path=path, file=path.split("/")[-1][:-4], lang=path.split("/")[2], script=sname, func=fname,
                           pc=start + fo + pc, arg=show(args[0]) if args else "", argv=ev(args[0], 0) if args else None,
                           guards=g, waitv=wdesc, reach=bi in reach,
                           loop=any(bi in dom.get(p, ()) for p in preds[bi]))
                if v == V_AWARD and istri:
                    award_rows.append(row)
                    per_file[(row["file"], row["lang"], row["argv"])] += 1
                    fn_hash[hashlib.sha1(sec[start + fo:start + fe]).hexdigest()[:12]] += 1
                elif v == V_AWARD:
                    other_awards.append(row)
                elif v == V_ITEMMES:
                    ctrl_item.append(row)
                elif v == V_GAUGEOPEN:
                    ctrl_gauge.append(row)

if calls_total == 0:
    sys.exit("REFUSE: control failed - no CALL-family site decoded")
print("CALL-family sites decoded (function-sliced): %d" % calls_total)

# ---- census agreement ----
by = collections.Counter(r["argv"] for r in award_rows)
census = [l.split("\t") for l in io.open(os.path.join(DB, "20-Platform-Online-Achievements", "members",
                                                          "script-award-verb-census.tsv"), encoding="utf-8").read().splitlines()[1:]]
cen = collections.Counter((("tri" if "/tri_" in c[0] else "other"), c[5]) for c in census if c[2] == "unkCall_5ad")
check("C1", by == {39: 900, 40: 900}, "tri_* award sites by index: %s (page table: 900 and 900)" % dict(by))
check("C2", cen[("tri", "PUSHII:39")] == 900 and cen[("tri", "PUSHII:40")] == 900 and len(award_rows) == 1800,
      "the published census TSV agrees: %s" % dict(cen))
check("C3", sorted(collections.Counter(r["argv"] for r in other_awards).items()) == [(33, 9)],
      "non-tri unkCall_5ad sites: %s (slm_a01 index 33, 9 languages)" % dict(collections.Counter(r["argv"] for r in other_awards)))
files = collections.Counter((r["file"], r["lang"]) for r in award_rows)
langs = collections.Counter(r["lang"] for r in award_rows)
check("C4", len(files) == 900 and set(files.values()) == {2} and set(per_file.values()) == {1}
      and len(set(r["file"] for r in award_rows)) == 100 and set(langs.values()) == {200},
      "900 = 100 stage files x 9 language copies; each file holds exactly one index-39 and one index-40 call "
      "(files %d, per-language %s)" % (len(files), sorted(set(langs.values()))))
where = collections.Counter((r["script"], r["func"]) for r in award_rows)
check("C5", list(where) == [("トライアル監督", "main")], "every site is in actor トライアル監督 (trial director), function main: %s"
      % dict(where))
print("      director main() bodies: %d distinct byte strings over the 900 files, so the guards below are rebuilt "
      "from each file's own bytes, not copied from one" % len(fn_hash))
check("C6", jump_bad == 0, "every jump immediate in the analysed functions indexes the script's jump table and lands on "
      "an instruction of the same function (%d misses)" % jump_bad)

# ---- the guards ----
def gsig(r):
    return tuple(show(c) for _, c in r["guards"])


for ix in (39, 40):
    rs = [r for r in award_rows if r["argv"] == ix]
    sigs = collections.Counter(gsig(r) for r in rs)
    print("\nindex %d: %d sites, %d distinct guard lists" % (ix, len(rs), len(sigs)))
    for s, n in sigs.items():
        print("   %4d x  guards (outermost first):" % n)
        for c in s:
            print("            %s" % c)
    wd = collections.Counter(r["waitv"] for r in rs)
    check("W%d" % ix, wd == {(4, 6): len(rs)} and all(r["reach"] for r in rs) and not any(r["loop"] for r in rs),
          "index %d: every site is reachable from main's entry, not inside a loop, and dominated by one waitv whose "
          "argument is a reference to scratch1 (class 4) offset 0x06: %s" % (ix, dict(wd)))

# evaluate every guard with nowmap() = the file's field
live = collections.defaultdict(set)
undecided = 0
for r in award_rows:
    fld = tri_fields[r["file"]]
    vals = [ev(c, fld) for _, c in r["guards"]]
    if any(v is None for v in vals):
        undecided += 1
    if all(v for v in vals):
        live[r["argv"]].add(r["file"])
check("E0", undecided == 0, "every guard is decided by nowmap() alone (%d sites carry any other test)" % undecided)
check("E39", live[39] == {"tri_j05"}, "index 39 is on a live branch only in %s (stage %s, field 0x%x); in the other 99 stage "
      "files its guard is false for that file's own field" % (sorted(live[39]), [stage_no[x] for x in sorted(live[39])],
                                                             tri_fields.get("tri_j05")))
check("E40", live[40] == {"tri_t05"}, "index 40 is on a live branch only in %s (stage %s, field 0x%x)"
      % (sorted(live[40]), [stage_no[x] for x in sorted(live[40])], tri_fields.get("tri_t05")))

# ---- controls ----
# positive: the tenth-stage item rewards (additemmes 0x9123..0x912b) share the award's post-waitv branch, each under its
# own nowmap() test; their live file must be stages 10, 20, ..., 90
items = collections.defaultdict(set)
for r in ctrl_item:
    if r["tri"] and r["waitv"] == (4, 6) and r["script"] == "トライアル監督":
        fld = tri_fields[r["file"]]
        if all(ev(c, fld) for _, c in r["guards"]):
            items[r["arg"]].add(stage_no[r["file"]])
check("K1", sorted((k, sorted(v)) for k, v in items.items()) == [("0x%04x" % (0x9123 + i), [10 * (i + 1)]) for i in range(9)],
      "control: the nine post-clear additemmes(0x9123..0x912b) calls resolve to stages 10..90, one each: %s"
      % sorted((k, sorted(v)) for k, v in items.items()))
j05 = [r for r in ctrl_item if r["file"] == "tri_j05" and r["lang"] == "us" and r["arg"] == "0x9127"]
a39 = [r for r in award_rows if r["file"] == "tri_j05" and r["lang"] == "us" and r["argv"] == 39]
check("K2", len(j05) == 1 and len(a39) == 1 and gsig(j05[0]) == gsig(a39[0]) and j05[0]["pc"] < a39[0]["pc"],
      "control: in tri_j05 (us) the index-39 award shares its whole guard list with additemmes(0x9127) just before it "
      "(item pc 0x%x, award pc 0x%x)" % (j05[0]["pc"] if j05 else -1, a39[0]["pc"] if a39 else -1))
# negative: bossgaugeopen() sits in main before the waitv - the dominance test must NOT credit it with the wait
g_us = [r for r in ctrl_gauge if r["lang"] == "us" and r["script"] == "トライアル監督" and r["func"] == "main"]
check("K3", len(g_us) == 100 and all(r["waitv"] is None for r in g_us),
      "negative control: the 100 (us) bossgaugeopen() calls in main precede the waitv and are classified as not "
      "dominated by it (%d sites, %d credited)" % (len(g_us), sum(r["waitv"] is not None for r in g_us)))
# the wake: nothing in the tri files writes scratch1 @0x06; the stage enemies are placed in event groups
check("K4", popv_s1_6 == 0, "no POPV in any tri_* file writes scratch1 @0x06 (%d); the wake is the engine's "
      "group-completion post (CONTRACT-group-completion-and-respawn.md, EE-9)" % popv_s1_6)
check("K5", set(evgroup) == {"g0", "g1"}, "btlAtelSetEventFlagGroup calls in tri_* files, by group: %s - group 1 is "
      "the only event group Trial Mode authors (group 0 = no event group, EE-11)" % dict(sorted(evgroup.items())))
g1 = sorted(set(c["g1"] for c in filegroups.values()))
check("K6", len(filegroups) == 900 and all(c["g1"] >= 1 for c in filegroups.values()),
      "every one of the %d stage files places at least one unit in group 1 (units per file: %s); tri_j05 (us) %s, "
      "tri_t05 (us) %s" % (len(filegroups), g1, dict(filegroups[("tri_j05", "us")]), dict(filegroups[("tri_t05", "us")])))

with io.open(os.path.join(HERE, "sd162-award-sites.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("file\tlang\tfield\tstage\tindex\tscript\tfunction\tpc\twaitv_scratch1_0x06\tlive_for_this_field\tguard_count\n")
    for r in sorted(award_rows, key=lambda r: (r["file"], r["lang"], r["argv"])):
        fld = tri_fields[r["file"]]
        w.write("%s\t%s\t0x%x\t%d\t%d\t%s\t%s\t0x%x\t%s\t%d\t%d\n" % (
            r["file"], r["lang"], fld, stage_no[r["file"]], r["argv"], r["script"], r["func"], r["pc"],
            int(r["waitv"] == (4, 6)), int(all(ev(c, fld) for _, c in r["guards"])), len(r["guards"])))
print("\nFAILS %d%s" % (len(FAILS), (" " + " ".join(FAILS)) if FAILS else ""))
