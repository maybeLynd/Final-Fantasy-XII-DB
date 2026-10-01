"""sample_read.py X OUT - random sample of admitted bodies per Phyre family (seed 20260930), with the evidence a reader
needs to judge each against the row's description: size, census tag, RTTI slots, callers (with their own tag and
whether they are members of the same family before/after), callees (tag), and .rdata strings the body leas."""
import collections, os, random, re, struct, subprocess, sys
X, OUT = sys.argv[1], sys.argv[2]
DB = os.path.join(X, "Database", "FFXII TZA")
W = "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work"
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
tags, sizes = {}, {}
for l in open(W + "/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    if p[0] == "entry": continue
    try:
        a = int(p[0], 16); sizes[a] = int(p[2]); tags[a] = p[8] if len(p) > 8 else ""
    except Exception: pass
rtti = collections.defaultdict(set)
for l in open(W + "/rtti/methods.tsv", encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    try: rtti[int(p[0], 16)].add(p[1])
    except Exception: pass
callers, callees = collections.defaultdict(set), collections.defaultdict(set)
for l in open(W + "/graph/edges.tsv", encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    try: a, b = int(p[0], 16), int(p[1], 16)
    except Exception: continue
    callers[b].add(a); callees[a].add(b)
d = open(W + "/exe/FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8); secs.append((0x120000 + va, rs, ro))
def off(a):
    for va, rs, ro in secs:
        if va <= a < va + rs: return ro + (a - va)
rx = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
def strings(e):
    out = []
    o = off(e)
    if o is None: return out
    for x in md.disasm(d[o:o + sizes.get(e, 0)], e):
        m = rx.search(x.op_str)
        if not m or x.mnemonic != "lea": continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        to = off(t)
        if to is None: continue
        s = d[to:to + 48].split(b"\0")[0]
        if len(s) >= 4 and all(32 <= c < 127 for c in s): out.append(s.decode())
    return out
def members(rev_or_path):
    s = set()
    for l in rev_or_path.splitlines():
        x = l.split("#")[0].strip().split()
        if x and re.fullmatch(r"[0-9A-Fa-f]{6,8}", x[0]): s.add(int(x[0], 16))
    return s
M = os.path.join(DB, "22-Middleware-PhyreEngine", "members")
short = lambda t: t.replace("GFZ.V121.CodeDomain.", "")[:60]
rnd = random.Random(20260930)
with open(OUT, "w", encoding="utf-8") as o:
    for f in sorted(os.listdir(M)):
        if not (f.startswith("phyre-") and f.endswith(".tsv")): continue
        old = members(subprocess.run(["git", "-C", DB, "show", "HEAD:22-Middleware-PhyreEngine/members/" + f], capture_output=True, text=True).stdout)
        new = members(open(os.path.join(M, f), encoding="utf-8").read())
        adm = sorted(new - old)
        if not adm: continue
        k = 25 if f == "phyre-phyrecore.tsv" else 5
        smp = sorted(rnd.sample(adm, min(k, len(adm))))
        o.write("\n=== %s: %d -> %d, admitted %d, sample %d\n" % (f, len(old), len(new), len(adm), len(smp)))
        tagc = collections.Counter(short(tags.get(a, "")).split(".")[0] for a in adm)
        o.write("admitted by census-tag domain: %s\n" % dict(tagc.most_common()))
        for a in smp:
            o.write("-- %08X  %d B  tag=%s  rtti=%s\n" % (a, sizes.get(a, 0), short(tags.get(a, "")), sorted(rtti.get(a, ()))[:2]))
            for c in sorted(callers[a])[:6]:
                st = "member" if c in new else ("member-old" if c in old else "other")
                o.write("     caller %08X [%s] %s rtti=%s\n" % (c, st, short(tags.get(c, "")), sorted(rtti.get(c, ()))[:1]))
            if len(callers[a]) > 6: o.write("     (+%d callers)\n" % (len(callers[a]) - 6))
            o.write("     callees: %s\n" % " ".join("%08X:%s" % (t, short(tags.get(t, "")).split(".")[0]) for t in sorted(callees[a])[:8]))
            s = strings(a)
            if s: o.write("     strings: %s\n" % s[:4])
print("wrote", OUT)
