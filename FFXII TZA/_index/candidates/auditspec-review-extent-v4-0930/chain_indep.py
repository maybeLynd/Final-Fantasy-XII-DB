"""chain_indep.py - SWE2-AUDIT-SPEC independent re-derivation of the chained-tail extents (EXTENT-V4 review, 2026-09-30).

Own PE parse (tk.py section map, no pefile), own UNWIND_INFO decode, own chain walk. Compares with:
  - the 254 pdata-chain rows committed at d20226c17 (git show d20226c17 -- ERRATA),
  - the author's rows() run against the pre-apply ledger d20226c17^ (reproduces 254 / 16 skipped / 49 beside).
Sensitivity variants: one hop only; no contiguity check; next-adjacent non-chained entries; chained triple mismatch.
"""
import os, sys, struct, subprocess, io, bisect, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "work", "FABLE", "takebacks"))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import tk
BASE = tk.BASE
ERR_REL = "Database/FFXII TZA/_index/FUNCTION-EXTENT-ERRATA.tsv"

def git_show(rev):
    return subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (rev, ERR_REL)], capture_output=True).stdout.decode("utf-8")

# ---- own .pdata / UNWIND_INFO parse
PVA, PVS, PRS, PRO = tk.secs[".pdata"]
ent = {}
for j in range(0, min(PVS, PRS) - 11, 12):
    b, e, u = struct.unpack_from("<III", tk.d, PRO + j)
    if b:
        ent[BASE + b] = (BASE + e, BASE + u)
def uinfo(u):
    o = tk.off(u)
    ver_flags, prolog, count, fr = tk.d[o], tk.d[o + 1], tk.d[o + 2], tk.d[o + 3]
    flags = ver_flags >> 3
    if flags & 0x4:
        c = o + 4 + 2 * (count + (count & 1))
        return struct.unpack_from("<III", tk.d, c)
    return None
parent, triple_bad = {}, []
for b, (e, u) in ent.items():
    t = uinfo(u)
    if t:
        pb, pe_, pu = BASE + t[0], BASE + t[1], BASE + t[2]
        parent[b] = pb
        if pb not in ent or ent[pb] != (pe_, pu):
            triple_bad.append((b, pb))
def root_of(b, hops=None):
    seen, r, n = set(), b, 0
    while r in parent and r not in seen and (hops is None or n < hops):
        seen.add(r); r = parent[r]; n += 1
    return r
def build(hops=None):
    g = collections.defaultdict(list)
    for b in ent:
        g[root_of(b, hops)].append((b, ent[b][0]))
    return {r: sorted(v) for r, v in g.items() if len(v) > 1}

fns = {}
for line in io.open(tk.FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: fns[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
starts = sorted(fns)
def short(ch, contig=True):
    out = {}
    for r, fs in ch.items():
        if r not in fns: continue
        if contig and any(fs[k][0] != fs[k - 1][1] for k in range(1, len(fs))): continue
        cend = max(e for _, e in fs)
        if cend > r + fns[r]:
            out[r] = cend
    return out

ch = build()
nonc = [r for r, fs in ch.items() if any(fs[k][0] != fs[k - 1][1] for k in range(1, len(fs)))]
sh = short(ch)
nb = sum(c - (r + fns[r]) for r, c in sh.items())
print("own parse: pdata entries %d, chained entries %d, chained triple != its pdata entry: %d" % (len(ent), len(parent), len(triple_bad)))
print("own: chained roots %d; non-contiguous %d; roots ending before chain %d; bytes %d" % (len(ch), len(nonc), len(sh), nb))
roots_notlisted = [r for r in ch if r not in fns]
print("own: chained roots not a listed function start: %d" % len(roots_notlisted))
chain_depth = collections.Counter()
for b in parent:
    n, r = 0, b
    while r in parent: r = parent[r]; n += 1
    chain_depth[n] += 1
print("own: chain depth histogram (fragment -> hops to root):", dict(sorted(chain_depth.items())))
# overlap with next listed entry
ov = [r for r, c in sh.items() if bisect.bisect_right(starts, r) < len(starts) and starts[bisect.bisect_right(starts, r)] < c]
print("own: short roots whose chain end overlaps the next listed entry: %d" % len(ov))

# ---- committed rows at d20226c17 (the 254) vs own
def pdrows(txt):
    s = {}
    for i, line in enumerate(txt.splitlines()):
        p = line.split("\t")
        if i and len(p) >= 15 and p[14].strip() == "pdata-chain":
            s[int(p[0], 16)] = int(p[12], 16)
    return s
def urows(txt):
    s = collections.defaultdict(set)
    for i, line in enumerate(txt.splitlines()):
        p = line.split("\t")
        if i and len(p) >= 15 and p[13].startswith("underrun-extend") and p[12]:
            s[int(p[0], 16)].add(int(p[12], 16))
    return s
post, pre = git_show("d20226c17"), git_show("d20226c17^")
com = pdrows(post)
print("committed pdata-chain rows at d20226c17: %d; head: %d" % (len(com), len(pdrows(io.open(os.path.join(ROOT, ERR_REL), encoding="utf-8").read()))))
pre_u = urows(pre)
same = {r for r, c in sh.items() if c in pre_u.get(r, ())}
beside = {r for r, c in sh.items() if r in pre_u and c not in pre_u[r] and max(pre_u[r]) < c}
past = {r for r, c in sh.items() if r in pre_u and max(pre_u[r]) > c}
mine254 = {r: c for r, c in sh.items() if r not in same and r not in past}
print("own vs pre-apply ledger: same-end skip %d, beside %d, ledger past chain %d, rows to emit %d" % (len(same), len(beside), len(past), len(mine254)))
print("own rows == committed 254 (start and end): %s; diff own-com %d com-own %d" % (
    mine254 == com, len(set(mine254.items()) - set(com.items())), len(set(com.items()) - set(mine254.items()))))
# ---- author's own rows() on the pre-apply ledger
import chained_tail_errata as cte
tmp = os.path.join(r"C:\t\auditspec", "errata_pre_d20226c17.tsv")
os.makedirs(os.path.dirname(tmp), exist_ok=True)
io.open(tmp, "w", encoding="utf-8", newline="").write(pre)
out, refused, skipped, conflicts, noncontig, wider = cte.rows(cte.chains(), cte.listed(), cte.existing(tmp))
os.remove(tmp)
print("author rows() on d20226c17^ ledger: emit %d, beside %d, skipped %d, conflicts %d, refused %d" % (len(out), len(wider), len(skipped), len(conflicts), len(refused)))
print("author emitted rows identical to committed: %s" % ({int(r[0], 16): int(r[12], 16) for r in out} == com))

# ---- sensitivity variants
v1 = build(hops=1); s1 = short(v1)
print("VARIANT one hop only: chained roots %d, short %d, bytes %d" % (len(v1), len(s1), sum(c - (r + fns[r]) for r, c in s1.items() if r in fns)))
s2 = short(ch, contig=False)
print("VARIANT no contiguity check: short %d (same as contig: %s)" % (len(s2), s2 == sh))
# extension applied to NON-chained entries: listed functions whose next .pdata entry (non-chained root) starts at the listed end
pstarts = sorted(ent)
adj = 0
for r, sz in fns.items():
    if r in parent or r in ch: continue
    k = bisect.bisect_left(pstarts, r + sz)
    if k < len(pstarts) and pstarts[k] == r + sz and pstarts[k] not in parent and r in ent:
        adj += 1
print("VARIANT non-chained: listed .pdata roots immediately followed by another non-chained entry (would grow if merged): %d" % adj)
# spot rows for byte reads
import random
random.seed(7)
pick = sorted(random.sample(sorted(com), 5))
for r in pick:
    print("SPOT %08X listed_end %08X chain_end %08X frags %s" % (r, r + fns[r], com[r], " ".join("%08X-%08X" % f for f in ch[r])))
