"""consumer_sensitivity.py - SWE2-AUDIT-SPEC: does each consumer wired at d20226c17 actually apply the chained-tail extents?

Sensitivity control per consumer: the same consumer, the same image and function list, with the errata ledger swapped for
a scratch copy (C:\\t\\auditspec) that lacks (a) all 254 pdata-chain rows or (b) ONE pdata-chain row. The swap is done by
setting uc1_band.ERRATA_TSV (the module constant every consumer's apply_extents()/errata_extends() default reads) or by
passing the path (build_views.text_intervals). No kit file is edited; outputs go to this folder or C:\\t\\auditspec.

  views  build_views.text_intervals: byte classes v3 (no errata) / v4 / v4 without chain rows / v4 without one row
  rfc    receiver_flow_census.check_extent_against_graph(root, chain end): accepted with the row, refused without it
  fds    field_disp_scan: (1) census of field_disp_scan-eligible displacement sites decoded INSIDE the 254 tails, split by
         tail kind (jump table vs other); (2) a real run pair on one row: the tail site appears only with the row
  pc     program_coverage: full report with / without the chain rows, diffed
"""
import os, sys, io, struct, collections, contextlib, runpy, hashlib, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
K = os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts")
DASH = os.path.join(ROOT, "Database", "Tools", "dashboard")
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
ERR = os.path.join(ROOT, "Database", "FFXII TZA", "_index", "FUNCTION-EXTENT-ERRATA.tsv")
SCR = r"C:\t\auditspec"
assert hashlib.sha256(open(EXE, "rb").read()).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
sys.path.insert(0, K); sys.path.insert(0, DASH)
import uc1_band
os.makedirs(SCR, exist_ok=True)
ONE = 0x00729920   # the ruling's own example row (pdata-chain detector)

lines = io.open(ERR, encoding="utf-8", newline="").read().splitlines(True)
chain_rows = {}
for i, l in enumerate(lines):
    p = l.rstrip("\r\n").split("\t")
    if i and len(p) >= 15 and p[14].strip() == "pdata-chain":
        chain_rows[int(p[0], 16)] = (int(p[3], 16), int(p[12], 16))
def write_copy(name, drop):
    path = os.path.join(SCR, name)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        for i, l in enumerate(lines):
            p = l.rstrip("\r\n").split("\t")
            if i and len(p) >= 15 and p[14].strip() == "pdata-chain" and drop(int(p[0], 16)):
                continue
            f.write(l)
    return path
NOCHAIN = write_copy("errata_nochain.tsv", lambda e: True)
NOONE = write_copy("errata_no_%08X.tsv" % ONE, lambda e: e == ONE)
le1, ce1 = chain_rows[ONE]
other = [l for l in lines[1:] if l.startswith("%08X\t" % ONE) and "pdata-chain" not in l]
print("pdata-chain rows at HEAD %d; row %08X listed end %08X chain end %08X (+%d); other ledger rows for it: %d" % (
    len(chain_rows), ONE, le1, ce1, ce1 - le1, len(other)))
mode = sys.argv[1] if len(sys.argv) > 1 else "all"

if mode in ("views", "all"):
    import build_views as BV
    bands = uc1_band.BAND_TSVS
    res = {}
    for k, p in (("v3", None), ("v4", ERR), ("v4-nochain", NOCHAIN), ("v4-no-one", NOONE)):
        iv = BV.text_intervals(FUNCS, bands, EXE, p)
        res[k] = iv
        print("VIEWS %-10s bytes %s overlap %d extents %s" % (k, iv["bytes"], iv["overlap"], iv["extents"]))
    for a, b in (("v3", "v4"), ("v4-nochain", "v4"), ("v4-no-one", "v4")):
        d = {c: res[b]["bytes"][c] - res[a]["bytes"][c] for c in res[a]["bytes"]}
        print("VIEWS delta %s -> %s: %s; overlap %+d" % (a, b, d, res[b]["overlap"] - res[a]["overlap"]))

if mode in ("rfc", "all"):
    import receiver_flow_census as RFC
    for k, p in (("with row", ERR), ("without row", NOONE)):
        uc1_band.ERRATA_TSV = p
        try:
            RFC.check_extent_against_graph(ONE, ce1, False); r = "ACCEPTED"
        except SystemExit as e:
            r = "REFUSED: " + str(e)[:110]
        print("RFC %s: extent %08X..%08X -> %s" % (k, ONE, ce1, r))
    uc1_band.ERRATA_TSV = ERR
    try:
        RFC.check_extent_against_graph(ONE, ce1 - 1, False); r = "ACCEPTED"
    except SystemExit as e:
        r = "REFUSED"
    print("RFC control: an end one byte short of the chain (%08X) with the row -> %s" % (ce1 - 1, r))

def is_jt(r, le, ce, blob, off):
    a = le
    while a < ce and (a & 3): a += 1
    n, lead = (ce - a) // 4, 0
    while lead < n and r <= 0x120000 + struct.unpack_from("<I", blob, off(a) + 4 * lead)[0] < ce: lead += 1
    return lead >= 2

if mode in ("fds", "all"):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP
    import pefile
    pe = pefile.PE(EXE, fast_load=True); blob = open(EXE, "rb").read()
    def off(va): return pe.get_offset_from_rva(va - 0x120000)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    fn = {}
    for i, l in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
        p = l.rstrip("\n").split("\t")
        if i and len(p) > 2:
            try: fn[int(p[0], 16)] = int(p[2])
            except ValueError: pass
    grown, _ = uc1_band.apply_extents(fn)
    hits = collections.Counter(); rows_hit = collections.Counter(); small = collections.Counter(); pick = None
    for r, (le, ce) in sorted(chain_rows.items()):
        kind = "jtable" if is_jt(r, le, ce, blob, off) else "other"
        z = grown[r]
        body, tail = [], []
        for ins in md.disasm(blob[off(r):off(r) + z], r):   # field_disp_scan's own decode: linear from the entry
            for oi, op in enumerate(ins.operands):
                if op.type == X86_OP_MEM and op.mem.base not in (X86_REG_RIP, X86_REG_RSP, X86_REG_RBP) and op.mem.disp > 0:
                    (tail if ins.address >= le else body).append((ins.address, op.mem.disp, ins.mnemonic + " " + ins.op_str,
                                                                   oi == 1 and ins.mnemonic in ("mov", "movzx", "movsx", "movsxd", "cmp", "movss", "movsd")))
                    break
        hits[kind] += len(tail)
        if tail: rows_hit[kind] += 1
        small[kind] += sum(1 for x in tail if x[1] < 0x2000)
        rd = [x for x in body if x[3]]
        if pick is None and kind == "jtable" and tail and rd:
            bd = {x[1] for x in body}
            t = next((x for x in tail if x[1] not in bd), None)
            if t: pick = (r, le, ce, t, rd[0])
    print("FDS tail sites field_disp_scan would emit (non rip/rsp/rbp base, disp > 0), by tail kind: %s; rows with any: %s; "
          "with disp < 0x2000: %s" % (dict(hits), dict(rows_hit), dict(small)))
    r, le, ce, t, b = pick
    print("FDS pair row %08X (listed end %08X, chain end %08X, jump-table tail): tail site %08X disp 0x%x '%s'; control %08X disp 0x%x '%s'" % (
        r, le, ce, t[0], t[1], t[2], b[0], b[1], b[2]))
    nopick = write_copy("errata_no_%08X.tsv" % r, lambda e: e == r)
    for k, p in (("with row", ERR), ("without row", nopick)):
        uc1_band.ERRATA_TSV = p
        out = os.path.join(SCR, "fds_%s.tsv" % k.replace(" ", "_"))
        sys.argv = ["field_disp_scan.py", "--funcs", FUNCS, "--disp", "0x%x" % t[1], "0x%x" % b[1],
                    "--control", "0x%x:%08X:r" % (b[1], r), "--out", out]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path(os.path.join(K, "field_disp_scan.py"), run_name="__main__")
        except SystemExit as e:
            buf.write("SystemExit %s\n" % e)
        rowsout = [l.split("\t") for l in io.open(out, encoding="utf-8").read().splitlines()[1:]]
        insite = [x for x in rowsout if x[1] == "%08X" % t[0]]
        print("FDS %s: %s | tail site %08X in output: %s" % (k, " / ".join(buf.getvalue().strip().splitlines()[:5]), t[0], insite))
    uc1_band.ERRATA_TSV = ERR

if mode in ("pc", "all"):
    outs = {}
    for k, p in (("with", ERR), ("nochain", NOCHAIN)):
        uc1_band.ERRATA_TSV = p
        out = os.path.join(HERE, "pc_%s.md" % k)
        sys.argv = ["program_coverage.py", "--db", os.path.join(ROOT, "Database", "FFXII TZA"), "--out", out]
        sys.modules.pop("program_coverage", None)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                runpy.run_path(os.path.join(K, "program_coverage.py"), run_name="__main__")
        except SystemExit as e:
            print("PC %s: program_coverage exit %s" % (k, e.code))
        outs[k] = io.open(out, encoding="utf-8").read().splitlines()
    uc1_band.ERRATA_TSV = ERR
    d = [l for l in difflib.unified_diff(outs["nochain"], outs["with"], "nochain", "with", n=0, lineterm="") if not l.startswith(("---", "+++", "@@"))]
    print("PC report lines %d / %d; differing lines %d:" % (len(outs["with"]), len(outs["nochain"]), len(d)))
    for l in d: print("  " + l[:400])
