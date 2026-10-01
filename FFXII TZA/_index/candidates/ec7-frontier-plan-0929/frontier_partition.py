# frontier_partition.py - one row per frontier function (check_dispositions' own frontier_set) with
# reproducible partition keys. Read-only; writes work/SWE2-EC7/frontier-partition-0929.tsv.
#
# keys: size band; UC-1 band member; list name (named / FUN_); owner + CodeDomain head (audit_crossrefs'
# own loader); decoded shape class (capstone, whole body); vtable-slot target (rtti/methods.tsv) and the
# slot classes' top namespace; library span (the span constants the family selectors use); citation
# state (check_dispositions.measure_a: entry-only on an evidence-bearing page / interior on a
# non-bearing page / mentioned nowhere); selector would-admit (the 2026-09-29 selector-drift record);
# contiguous frontier run length; ghidra call-graph in/out degree (edges.tsv - no jcc/jmp-table edges).
import os, sys, io, re, csv, struct, bisect, collections
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
GS = ROOT + r"\Database\Tools\analysis-kit\gfz-scripts"
sys.path.insert(0, GS)
import check_dispositions as CD, uc1_band, audit_crossrefs as AC
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
DB = ROOT + r"\Database\FFXII TZA"
WK = ROOT + r"\Database\Tools\work"
OUT = WK + r"\SWE2-EC7\frontier-partition-0929.tsv"

sizes = CD.load_functions()
r = CD.evaluate(DB, sizes)
front = sorted(r["frontier_set"])
a_set, entry_only, any_interior, documented_any = CD.measure_a(DB, sizes)
# every address mentioned anywhere in a scanned document (entry or interior, any status)
mentioned = set()
ents = sorted(sizes)
for p in CD.docs(DB):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    for h in CD.CITE.findall(t):
        v = int(h, 16)
        i = bisect.bisect_right(ents, v) - 1
        if i >= 0 and ents[i] <= v < ents[i] + sizes[ents[i]]:
            mentioned.add(ents[i])
uc1f = uc1_band.frontier_starts()
fn = AC.load_functions(WK + r"\graph\functions.tsv")

d = open(WK + r"\exe\FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((0x120000 + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs:
            return ro + (a - va)
md = Cs(CS_ARCH_X86, CS_MODE_64)

slots = collections.defaultdict(set)
for row in csv.DictReader(open(WK + r"\rtti\methods.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
    try:
        slots[int(row["address"], 16)].add(row["class"])
    except (ValueError, KeyError, TypeError):
        pass
indeg, outdeg = collections.Counter(), collections.Counter()
for row in csv.DictReader(open(WK + r"\graph\edges.tsv", encoding="utf-8"), delimiter="\t"):
    try:
        c, e = int(row["caller"], 16), int(row["callee"], 16)
    except (ValueError, TypeError):
        continue
    outdeg[c] += 1; indeg[e] += 1

# library spans, as the declaring selectors state them (half-open)
SPANS = [(0x6DA880, 0x7911E0, "PPFX span"), (0x7A4380, 0x7F41A0, "SEAD span"), (0x7F41A0, 0x7FFBC0, "Tremor/vorbisfile span"),
         (0x8800C0, 0x8958B0, "libvorbis span"), (0x16DDD0, 0x17C890, "libvpx span"), (0x121000, 0x125740, "CRI HCA span")]
def span_of(e):
    for lo, hi, nm in SPANS:
        if lo <= e < hi:
            return nm
    return ""

drift = collections.defaultdict(list)
dp = DB + r"\_index\candidates\ec7-refused-family-repair-0929\selector-drift.tsv"
if os.path.exists(dp):
    for row in csv.DictReader(open(dp, encoding="utf-8"), delimiter="\t"):
        if row["change"] == "would-admit":
            drift[int(row["address"], 16)].append(row["family"])

def shape(e):
    sz = sizes[e]
    o = off(e)
    if o is None:
        return "no-bytes", 0, 0
    ins = list(md.disasm(d[o:o + sz], e))
    if not ins:
        return "undecodable", 0, 0
    mn = [x.mnemonic for x in ins]
    calls = sum(1 for m in mn if m == "call")
    last = mn[-1]
    back = any(x.mnemonic.startswith("j") and x.op_str.startswith("0x") and int(x.op_str, 16) < x.address
               and int(x.op_str, 16) >= e for x in ins)
    if len(ins) == 1 and last == "jmp":
        k = "jmp-only"
    elif len(ins) == 1 and last in ("ret", "int3"):
        k = "ret-only"
    elif len(ins) <= 3 and last == "ret" and calls == 0:
        k = "const/trivial-return"
    elif last == "jmp" and calls == 0 and len(ins) <= 6:
        k = "short tail-forwarder"
    elif calls == 0 and not back:
        k = "leaf, straight-line" if sz <= 64 else "leaf, branchy/large"
    elif calls == 0:
        k = "leaf with loop"
    elif calls == 1 and len(ins) <= 12:
        k = "one-call adapter"
    else:
        k = "caller"
    return k, len(ins), calls

runs = {}
fs = set(front)
i = 0
while i < len(ents):
    if ents[i] in fs:
        j = i
        while j + 1 < len(ents) and ents[j + 1] in fs:
            j += 1
        for k in range(i, j + 1):
            runs[ents[k]] = j - i + 1
        i = j + 1
    else:
        i += 1

def band(s):
    return "0-16" if s <= 16 else "17-64" if s <= 64 else "65-256" if s <= 256 else "257-1024" if s <= 1024 else "1025+"

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    cols = ["entry", "bytes", "size_band", "uc1", "named", "owner", "domain_head", "shape", "insns", "calls",
            "vtable_slot_ns", "library_span", "cite_state", "selector_would_admit", "run_len", "in_deg", "out_deg"]
    f.write("\t".join(cols) + "\n")
    for e in front:
        rec = fn.get("%08X" % e) or {}
        k, ni, nc = shape(e)
        ns = sorted({c.split("::")[0] if "::" in c else "(global)" for c in slots.get(e, ())})
        cite = ("entry-only, evidence-bearing page" if e in entry_only else
                "cited (other)" if e in mentioned else "mentioned nowhere")
        dom = rec.get("domains") or []
        f.write("\t".join(map(str, [
            "%08X" % e, sizes[e], band(sizes[e]), "Y" if e in uc1f else "", "" if (rec.get("name", "FUN_").startswith(("FUN_", "UC1-"))) else "Y",
            rec.get("owner", ""), dom[0].split(".")[0] if dom else "", k, ni, nc, "/".join(ns)[:60], span_of(e), cite,
            "/".join(drift.get(e, [])), runs.get(e, 0), indeg[e], outdeg[e]])) + "\n")
print("frontier", len(front), "->", OUT)
