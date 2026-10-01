"""pdata_pefile.py - SWE2-AUDIT-SPEC second independent re-derivation of the chained-tail rows (EXTENT-V4 review).

Uses pefile's own exception-directory parser (RUNTIME_FUNCTION + UNWIND_INFO, UNW_FLAG_CHAININFO -> FunctionEntry),
not tk.py and not the author's chains(). Asserts the certified image sha256. Reports:
  - entries, entries whose UnwindData has bit 0 set (the indirect form neither the author nor chain_indep.py decodes),
  - chained roots / non-contiguous / short roots / bytes (controls 3828 / 0 / 270 / 16361),
  - agreement with the HEAD ledger: the 254 pdata-chain rows + the 16 same-end instruction-scan rows = the 270,
  - where the 16,361 tail bytes land in the v3 byte classes (another population body incl. UC-1 frontier and
    extensions, funclet, held row, fill) - the author's overlap guard checks only the next functions.tsv entry.
"""
import os, sys, io, hashlib, bisect, collections
import pefile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
ERR = os.path.join(ROOT, "Database", "FFXII TZA", "_index", "FUNCTION-EXTENT-ERRATA.tsv")
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
assert hashlib.sha256(open(EXE, "rb").read()).hexdigest() == SHA, "image sha mismatch"
print("image sha256 ok")

pe = pefile.PE(EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
B = pe.OPTIONAL_HEADER.ImageBase
ex = pe.DIRECTORY_ENTRY_EXCEPTION
exdir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
print("pefile: exception dir size %d -> %d slots; parsed entries %d; warnings: %d 'Chained function entry cannot be changed' "
      "(pefile's back-link on a SHARED UNWIND_INFO; this script reads ui.FunctionEntry itself), %d other" % (
    exdir.Size, exdir.Size // 12, len(ex), sum(1 for w in pe.get_warnings() if "cannot be changed" in w),
    sum(1 for w in pe.get_warnings() if "cannot be changed" not in w)))
odd = sum(1 for e in ex if e.struct.UnwindData & 1)
nui = sum(1 for e in ex if e.unwindinfo is None)
print("entries with UnwindData bit0 set (indirect chain form): %d; entries without unwindinfo: %d" % (odd, nui))

rng = {B + e.struct.BeginAddress: B + e.struct.EndAddress for e in ex if e.struct.BeginAddress}
par = {}
for e in ex:
    ui = e.unwindinfo
    if ui is not None and ui.Flags & 4:
        par[B + e.struct.BeginAddress] = B + ui.FunctionEntry
print("chained entries (UNW_FLAG_CHAININFO): %d" % len(par))

def root(b):
    seen = set()
    while b in par and b not in seen:
        seen.add(b); b = par[b]
    return b
grp = collections.defaultdict(list)
for b in rng:
    grp[root(b)].append((b, rng[b]))
ch = {r: sorted(v) for r, v in grp.items() if len(v) > 1}
nonc = [r for r, fs in ch.items() if any(fs[k][0] != fs[k - 1][1] for k in range(1, len(fs)))]

fns, funclets = {}, []
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i == 0 or len(p) < 3: continue
    try: e, z = int(p[0], 16), int(p[2])
    except ValueError: continue
    fns[e] = z
    if p[1].startswith(("Unwind@", "Catch_All@")): funclets.append((e, z))
short = {r: fs[-1][1] for r, fs in ch.items() if r in fns and r not in nonc and fs[-1][1] > r + fns[r]}
nb = sum(c - (r + fns[r]) for r, c in short.items())
print("chained roots %d; non-contiguous %d; roots not in functions.tsv %d; short roots %d; bytes %d" % (
    len(ch), len(nonc), sum(1 for r in ch if r not in fns), len(short), nb))
print("controls 3828/0/270/16361 reproduced: %s" % ((len(ch), len(nonc), len(short), nb) == (3828, 0, 270, 16361)))

# ---- HEAD ledger
rows = collections.defaultdict(list)
for i, line in enumerate(io.open(ERR, encoding="utf-8")):
    p = line.rstrip("\r\n").split("\t")
    if i and len(p) >= 15 and p[13].startswith("underrun") and p[12]:
        rows[int(p[0], 16)].append((int(p[12], 16), p[14].strip()))
pdc = {e: c for e, v in rows.items() for c, d in v if d == "pdata-chain"}
same_other = {r for r, c in short.items() if any(cc == c and d != "pdata-chain" for cc, d in rows.get(r, []))}
print("HEAD ledger: pdata-chain rows %d; == own short roots minus same-end instruction-scan rows: %s (same-end %d)" % (
    len(pdc), pdc == {r: c for r, c in short.items() if r not in same_other}, len(same_other)))
furthest = {e: max(c for c, _ in v) for e, v in rows.items()}
past = [r for r, c in short.items() if furthest.get(r, 0) > c]
print("short roots whose furthest ledger end runs past the chain end: %d" % len(past))
print("roots in the 270 not covered at their chain end by the furthest ledger end: %d" % sum(1 for r, c in short.items() if furthest.get(r) != c))

# ---- where the tail bytes land (v3 classes, uc1_band population)
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import uc1_band
band = uc1_band.load()
fset = set(funclets)
pop, _ = uc1_band.apply({e: z for e, z in fns.items() if (e, z) not in fset}, band)
iv = []
for e, z in pop.items(): iv.append((e, e + z, "frontier" if e in band["frontier"] else "listed", e))
for e, z in funclets: iv.append((e, e + z, "funclet", e))
for s, t in band["held"]: iv.append((s, t, "held", s))
tails = sorted((r + fns[r], c, r) for r, c in short.items())
tst = [t[0] for t in tails]
cov = {}   # tail byte -> class of another body covering it (listed < frontier < funclet < held)
prio = {"listed": 0, "frontier": 1, "funclet": 2, "held": 3}
who = collections.defaultdict(set)
for s_, t_, kind, owner in iv:
    j = max(bisect.bisect_right(tst, s_) - 1, 0)
    while j < len(tails) and tails[j][0] < t_:
        a0, a1, r = tails[j]
        lo_, hi_ = max(a0, s_), min(a1, t_)
        if owner != r and lo_ < hi_:
            who[kind].add((r, owner, hi_ - lo_))
            for a in range(lo_, hi_):
                if a not in cov or prio[kind] < prio[cov[a]]:
                    cov[a] = kind
        j += 1
land = collections.Counter()
tsec = next(s for s in pe.sections if s.Name.startswith(b".text"))
tdata = tsec.get_data(); tlo = B + tsec.VirtualAddress
for a0, a1, r in tails:
    for a in range(a0, a1):
        land[cov[a] if a in cov else ("fill" if tdata[a - tlo] in (0xCC, 0x90) else "no-body")] += 1
print("tail bytes by v3 class: %s (total %d)" % (dict(land), sum(land.values())))
for k in ("listed", "frontier", "funclet", "held"):
    if who[k]:
        print("  %s (root <- other body, bytes): %s" % (k, " ".join("%08X<-%08X:%d" % x for x in sorted(who[k]))))
