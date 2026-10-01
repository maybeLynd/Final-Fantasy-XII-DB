"""Audit: rip-relative WRITE targets in .data/.bss not covered by any declared STATIC/ARRAY span, clustered (gap <= 0x40),
ranked by number of distinct writing functions. Uses data_xref_scan's section/entry helpers and capstone access flags."""
import collections
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import reg_tracking as RT
import csv
import io
import re
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import data_xref_scan as X  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
G = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
TY = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_types\types.tsv"
spans = []
for r in csv.DictReader(io.open(TY, encoding="utf-8"), delimiter="\t"):
    m = re.match(r"(STATIC|ARRAY|PTR) 0x([0-9A-Fa-f]+)", r.get("route") or "")
    if not m:
        continue
    b = int(m.group(2), 16)
    if m.group(1) == "PTR":
        spans.append((b, b + 8))
        continue
    try:
        sz = int(r["size"], 16)
    except ValueError:
        continue
    mm = re.search(r"count=(\d+)", r["route"])
    st = re.search(r"stride=0x([0-9A-Fa-f]+)", r["route"])
    if mm and st:
        sz = int(st.group(1), 16) * int(mm.group(1))
    spans.append((b, b + sz))
spans.sort()
blob = open(EXE, "rb").read()
secs = X.sections_of(blob)


def off(va):
    for _n, ro, sz, v in secs:
        if v <= va < v + sz:
            return ro + (va - v)


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
writes = collections.defaultdict(set)
DLO, DHI = 0x01C00000, 0x03000000
for fva, fsize in X.entries(G):
    o = off(fva)
    if o is None or fsize <= 0:
        continue
    for i in md.disasm(blob[o:o + fsize], fva):
        for oi, op in enumerate(i.operands):
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and RT.op_kind(i, op, oi) in ("w", "rw"):
                t = i.address + i.size + op.mem.disp
                if DLO <= t < DHI:
                    writes[t].add(fva)
import bisect  # noqa: E402
starts = [s for s, _ in spans]


def covered(a):
    k = bisect.bisect_right(starts, a) - 1
    while k >= 0 and spans[k][0] <= a:
        if a < spans[k][1]:
            return True
        k -= 1
        if k < 0 or a - spans[k][0] > 0x100000:
            break
    return False


unc = sorted(a for a in writes if not covered(a))
clusters, cur = [], []
for a in unc:
    if cur and a - cur[-1] > 0x40:
        clusters.append(cur)
        cur = []
    cur.append(a)
if cur:
    clusters.append(cur)
rank = sorted(clusters, key=lambda c: -len(set().union(*(writes[a] for a in c))))
print("write targets:", len(writes), " uncovered:", len(unc), " clusters:", len(clusters))
for c in rank:
    fns = set().union(*(writes[a] for a in c))
    print("%08X..%08X  cells %3d  writers %3d  e.g. %s" % (c[0], c[-1], len(c), len(fns), ",".join("%08X" % f for f in sorted(fns)[:4])))
