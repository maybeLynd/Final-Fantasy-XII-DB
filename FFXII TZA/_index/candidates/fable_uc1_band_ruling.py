# fable_uc1_band_ruling.py - FABLE (Claude Opus 5.5), 2026-09-25, for FRONTIER-REQ-FABLE-UC1-BAND-RULING.
#
# Part A: is the body-shape gate (a linear decode reaching the last byte) sensitive to DATA, and to a
#         WRONG BOUNDARY? Negative controls: N1 the `table` rows (known data), N2 .rdata windows drawn
#         with the admitted rows' size distribution (known data), N3 listed bodies entered at +1 (known
#         code, wrong boundary).
# Part B: boundary signals per admitted `body` row against the listed control:
#   aligned16    start % 16 == 0
#   referenced   the admissions TSV's pass-6-admissible reference column
#   multi        an unreached terminator before the last instruction followed by non-padding code:
#                more than one straight-line body in the block. Known positive: 00125743.
#   pred_branch  the listed predecessor branches (jcc/jmp rel, never call) into [start, start+n)
# and writes the per-row TSV of the 1-64 B band: uc1-band-1-64-fable-2026-09-25.tsv.
# Read-only on its inputs: the EXE, functions.tsv and unlisted-body-admissions.tsv.
import io, os, random, struct, sys, collections
import capstone

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
ADM = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code", "unlisted-body-admissions.tsv")
OUT = os.path.join(DB, "_index", "candidates", "uc1-band-1-64-fable-2026-09-25.tsv")

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + 40 * i
    name = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, 0x120000 + va, vs, rs, ro))


def off(v):
    for name, va, vs, rs, ro in secs:
        if va <= v < va + min(vs, rs):
            return ro + v - va
    return None


md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
TERM = {"ret", "jmp", "int3", "ud2", "hlt", "repz ret"}
BANDS = [(1, 64), (65, 256), (257, 1024), (1025, 1 << 30)]


def band(n):
    return next((b for b in BANDS if b[0] <= n <= b[1]), None)


def dis(v, n):
    o = off(v)
    return list(md.disasm(d[o:o + n], v)) if o is not None and n > 0 else []


def shape(v, n):
    ins = dis(v, n)
    full = bool(ins) and ins[-1].address + ins[-1].size == v + n
    return full, full and ins[-1].mnemonic in TERM


def multi(v, n):
    ins = dis(v, n)
    for k, i in enumerate(ins[:-1]):
        if i.mnemonic not in ("ret", "repz ret", "jmp"):
            continue
        rest = ins[k + 1:]
        if not any(r.mnemonic not in ("int3", "nop") for r in rest):
            continue
        if i.mnemonic == "jmp" and i.op_str.startswith("0x") and v <= int(i.op_str, 16) < v + n:
            continue                      # an internal branch, not an end
        targets = {int(x.op_str, 16) for x in ins[:k + 1]
                   if x.mnemonic.startswith("j") and x.op_str.startswith("0x")}
        if any(rest[0].address <= t < v + n for t in targets):
            continue                      # the code after it is reached from the block itself
        return True
    return False


def branches_into(pv, pn, lo, hi):
    for i in dis(pv, pn):
        if i.mnemonic.startswith("j") and i.op_str.startswith("0x") and lo <= int(i.op_str, 16) < hi:
            return True
    return False


listed = []
for line in io.open(FUNCS, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    try:
        listed.append((int(p[0], 16), int(p[2])))
    except (ValueError, IndexError):
        pass
listed.sort()
if not listed:
    sys.exit("functions.tsv parse failed")
sizes = dict(listed)
rows = [l.rstrip("\n").split("\t") for l in io.open(ADM, encoding="utf-8") if not l.startswith("#")][1:]
body = [(int(r[0], 16), int(r[1])) for r in rows if r[8] == "body"]
table = [(int(r[0], 16), int(r[1])) for r in rows if r[8] == "table"]

# ---------------- Part A
print("Part A - body-shape gate sensitivity (listed parsed %d, body %d, table %d)" % (len(listed), len(body), len(table)))
rd = [s for s in secs if s[0] == ".rdata"][0]
random.seed(1)
n2 = [(rd[1] + random.randrange(0, min(rd[2], rd[3]) - n), n) for _, n in body * 20]
n3 = [(v + 1, n - 1) for v, n in listed if n > 1]
for label, pop in (("ADMITTED body", body), ("LISTED (control +)", listed), ("N1 table rows (data)", table),
                   ("N2 .rdata windows (data)", n2), ("N3 listed entered at +1", n3)):
    agg = collections.defaultdict(lambda: [0, 0, 0])
    for v, n in pop:
        b = band(n)
        if b is None or b[0] > 1024 or off(v) is None:
            continue
        full, term = shape(v, n)
        a = agg[b]
        a[0] += 1; a[1] += full; a[2] += term
    for b in BANDS[:3]:
        a = agg[b]
        if a[0]:
            print("  %-26s %4d-%-5d n=%6d  decodes_to_end %5.1f%%  ends_in_terminator %5.1f%%"
                  % (label, b[0], b[1], a[0], 100.0 * a[1] / a[0], 100.0 * a[2] / a[0]))

# ---------------- Part B
print("Part B - boundary signals")
print("  known positive multi(00125743, 33):", multi(0x125743, 33))
agg = collections.defaultdict(collections.Counter)
outrows = []
for r in rows:
    if r[8] != "body":
        continue
    v, n, pv = int(r[0], 16), int(r[1]), int(r[2], 16)
    b = band(n)
    c = agg[("body",) + b]
    al, ref = v % 16 == 0, r[4] == "yes"
    m = multi(v, n)
    pb = branches_into(pv, sizes.get(pv, 0), v, v + n)
    c["n"] += 1; c["aligned16"] += al; c["referenced"] += ref; c["multi"] += m; c["pred_branch"] += pb
    c["unaligned_unreferenced"] += (not al) and (not ref)
    clean = (not m) and (not pb) and (al or ref)
    c["clean"] += clean
    if b == (1, 64):
        ruling = "admit" if clean else ("extend-predecessor" if pb else ("split" if m else "hold-ambiguous"))
        outrows.append((r[0], n, r[2], "yes" if al else "no", "yes" if ref else "no", "yes" if m else "no",
                        "yes" if pb else "no", r[7], ruling))
for k, (v, n) in enumerate(listed):
    if n <= 0:
        continue
    c = agg[("listed",) + band(n)]
    c["n"] += 1; c["aligned16"] += v % 16 == 0; c["multi"] += multi(v, n)
    if k:
        c["pred_branch"] += branches_into(listed[k - 1][0], listed[k - 1][1], v, v + n)
for key in sorted(agg):
    c = agg[key]
    print("  %-8s %4d-%-10d n=%5d " % (key[0], key[1], key[2], c["n"]) + " ".join(
        "%s=%d (%.1f%%)" % (f, c[f], 100.0 * c[f] / c["n"])
        for f in ("aligned16", "referenced", "multi", "pred_branch", "unaligned_unreferenced", "clean")
        if f in c))
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("# UC-1 1-64 B band, one line per admitted `body` row (FABLE, Claude Opus 5.5, 2026-09-25).\n"
            "# Generated by fable_uc1_band_ruling.py from unlisted-body-admissions.tsv. ruling: admit = 16-aligned\n"
            "# or referenced, one straight-line body, not branched into by its predecessor; extend-predecessor = a\n"
            "# jcc/jmp of the listed predecessor targets it (the 2026-09-13 tail rule); split = more than one body;\n"
            "# hold-ambiguous = unaligned and unreferenced with neither of those shapes.\n")
    f.write("start_va\tbytes\tprev_entry\taligned16\treferenced\tmulti\tpred_branch\tdecodes_to_end\truling\n")
    for r in outrows:
        f.write("\t".join(str(x) for x in r) + "\n")
print("per-row rulings, 1-64 B:", dict(collections.Counter(r[-1] for r in outrows)))
for r in outrows:
    if r[-1] != "admit":
        print("  ", "\t".join(str(x) for x in r))
