"""rc5_paths.py - RC-5 (ORACLE, 2026-09-30).  Which (kind, id) path can the manager resource-set load 0032FCA0 hand the
name-classifying setter (0032FD64 -> 001EC660 -> 0020AC30), and which of those can pass the setter's regex?

1. Replays ResourcePath_Init 002DF9A0's own instruction stream for every region argument (ecx = 0..12): the prologue
   stores, then the jump-table arm for (ecx-1) <= 10 (table at 002E04B0), else the default arm at 002DFF32, up to the
   join at 002DFF7F.  Records g_pathTables[kind] = array VA for kinds 1, 5 and 8 (the three kinds 0032FCA0 selects).
2. Row formula, read from 0032FCA0 (0032FD19..0032FD44), manager index m (ecx), set id s (edx):
      m <= 0 or m >= 5 -> kind 5, row 3*s ;  1 <= m <= 3 -> kind 8, row 4*s ;  m == 4 -> kind 1, row s + 0x6B.
3. Walks each array.  The arrays have no terminator (area-nmb-index.md): the in-array walk is bounded by the next
   installed array start (every g_pathTables slot of every region).  Rows at or above 0x400 are reported separately
   (0032E400 serves rows < 0x400 from its size table and sends the rest to 0046DE70).  For kind 1 the formula's rows
   (>= 0x6B) lie past every region's array, so rows 0x6B .. 0x6B+2047 are also read raw, past the bound.
4. Applies the setter's regex (literal at 00905958, read from the image) and the extractor 0020AA50's rule (the text
   between the last '\' and the last '.', 0020AB60..0020ABE5) to every row the formula can select, and classifies the
   stem as the setter does (sum_ -> flag A only with 0001; spc_ without sum_ -> flag B).
5. Checks each matching path against the shipped archive's index (vbfextract), as a stand-in for 0032E400's size gate.
Output rc5_paths.tsv (every selectable row with a string, region 1 = 'us' only; written only when run directly) and a summary on stdout.
Controls: the regex literal read back from 00905958 must equal the page's text; kind 5 row 0 of region 0 must end in
tst_a01.ebp (area-nmb-index.md's first-entries table); the setter's own flag stores 0020ADD6 / 0020AE16 must be
decoded as byte stores to 01F832E8 / 01F832E9."""
import collections, io, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img

HERE = os.path.dirname(os.path.abspath(__file__))
PT = 0x0215F000
FN = 0x002DF9A0
JOIN = 0x002DFF7F
DEFAULT = 0x002DFF32
JT = 0x002E04B0
FAILS = []
sys.path.insert(0, os.path.join(os.path.dirname(img.EXE), "..", "..", "..", "..", "agent_flow", "tools"))
import vbfextract
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"


def run(start, stop, regs, slots):
    va = start
    while va != stop:
        x = img.dis(va, 16)[0]
        if x.mnemonic == "lea" and img.ripmem(x) is not None:
            regs[x.op_str.split(",")[0].strip()] = img.ripmem(x)
        elif x.mnemonic == "mov" and img.ripmem(x) is not None and x.op_str.startswith("qword ptr [rip"):
            t = img.ripmem(x)
            if PT <= t < PT + 0x200:
                slots[(t - PT) // 8] = regs.get(x.op_str.split(",")[1].strip())
        elif x.mnemonic == "jmp":
            va = x.operands[0].imm
            continue
        elif x.mnemonic in ("ret", "call") or x.mnemonic.startswith("j"):
            break
        va = x.address + x.size
    return slots


def region_slots(ecx):
    slots = run(FN, 0x002DFBAF, {}, {})
    arm = img.BASE + img.u32(JT + 4 * (ecx - 1)) if 1 <= ecx <= 11 else DEFAULT
    return run(arm, JOIN + 7, {}, slots), arm


def cstr(va):
    try:
        b = img.rd(va, 260)
    except ValueError:
        return None
    n = b.find(b"\0")
    if n <= 0:
        return None
    s = b[:n]
    return s.decode() if all(32 <= c < 127 for c in s) else None


def stem(path):
    a = path.rfind("\\"); b = path.rfind(".")
    return path[a + 1:b] if b > a else path[a + 1:]


def classify(n):
    if len(n) < 4:
        return ""
    if "sum_" in n:
        return "A(sum_+0001)" if "0001" in n else "sum_(json only)"
    return "B(spc_)" if "spc_" in n else ""


lit = img.rd(0x00905958, 80).split(b"\0")[0].decode()
if lit != r"(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)":
    FAILS.append("regex literal " + lit)
RX = re.compile(r"(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)")
for va, tgt in ((0x0020ADD6, 0x01F832E8), (0x0020AE16, 0x01F832E9)):
    x = img.dis(va, 16)[0]
    if img.ripmem(x) != tgt or not x.op_str.startswith("byte ptr"):
        FAILS.append("flag store %08X" % va)

regions, all_starts = {}, set()
for ecx in range(0, 13):
    s, arm = region_slots(ecx)
    regions[ecx] = (s, arm)
    all_starts |= {v for v in s.values() if v}
starts = sorted(all_starts)


def bound(a):
    nxt = [b for b in starts if b > a]
    return min(nxt) if nxt else a + 0x2000


def row(a, r):
    p = struct.unpack("<Q", img.rd(a + 8 * r, 8))[0]
    return cstr(p) if p else None


if not (row(regions[0][0][5], 0) or "").endswith("tst_a01.ebp"):
    FAILS.append("kind 5 row 0 control")

vf = io.open(VBF, "rb")
arch = set(n.lower() for n in vbfextract.load_index(vf)[0])
FORM = {8: ("1..3", lambda r: r % 4 == 0, lambda r: r // 4), 5: ("0 or >=5", lambda r: r % 3 == 0, lambda r: r // 3),
        1: ("4", lambda r: r >= 0x6B, lambda r: r - 0x6B)}
rows, summ, flagged = [], collections.OrderedDict(), collections.OrderedDict()
for ecx in range(0, 13):
    s, arm = regions[ecx]
    for kind in (8, 5, 1):
        a = s.get(kind)
        n = (bound(a) - a) // 8
        rng = range(0x6B, 0x6B + 2048) if kind == 1 else range(n)
        sel = match = inarch = hi = 0
        cls = collections.Counter()
        for r in rng:
            st = row(a, r)
            mgr, ok, sid = FORM[kind]
            if st is None or not ok(r):
                continue
            sel += 1
            m = RX.match(st)
            present = st.lower().replace("\\", "/") in arch
            if m:
                match += 1; inarch += present; hi += r >= 0x400
                c = classify(stem(st)); cls[c] += 1
                if c and ecx == 0:
                    flagged.setdefault((c, stem(st)), []).append(sid(r))
            rows.append((ecx, "%08X" % arm, kind, mgr, sid(r), r, "%08X" % a, "in-array" if r < n else "PAST-ARRAY",
                         "MATCH" if m else "-", m.group(3) if m else "", stem(st) if m else "", classify(stem(st)) if m else "",
                         "yes" if present else "no", st))
        summ[(ecx, kind)] = ("%08X" % a, n, sel, match, hi, inarch, cls["A(sum_+0001)"], cls["sum_(json only)"], cls["B(spc_)"])

TSV_REGION = 1                                  # 'us'; every region's (set id, name) pairs are identical (summary below)
if __name__ == "__main__":                      # rc6_packs.py imports this module for the replay only
    with io.open(os.path.join(HERE, "rc5_paths.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("region_ecx\tarm\tkind\tmanager_index\tset_id\trow\tarray\trow_position\tregex\tlocale\tstored_name\tclass\t"
                "in_archive\tpath\n")
        for r in rows:
            if r[0] == TSV_REGION:
                f.write("\t".join(str(c) for c in r) + "\n")
print("region kind array    rows_in_array selectable regex_match match_row>=0x400 match_in_archive flagA sum_json flagB")
for (ecx, kind), v in summ.items():
    print("%6d %4d %s %13d %10d %11d %16d %16d %5d %8d %5d" % ((ecx, kind) + v))
print("region 0 classified names (class, stored name) -> set ids:")
for k, v in flagged.items():
    print("  ", k, v)
print("FAILS", len(FAILS), FAILS)
