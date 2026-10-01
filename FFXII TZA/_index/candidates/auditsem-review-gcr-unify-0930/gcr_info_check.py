"""SWE2-AUDIT-SEM GCR-UNIFY information-column check (own code).
For every member, read its body (linear decode from its start over the TSV's byte count) and collect its direct call
targets; a target is GUARDED-FORM when its own body calls _Init_thread_header 008092FC, _Init_thread_footer 0080929C
and the atexit wrapper 00808B90 (bodies bounded by .pdata chain extent, else 0x2000 B). Compare, per member, the set
of guarded-form callees (other than itself) with the TSV's last column. Also the member size range."""
import os, re, struct, bisect
import img

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = next(p for p in (
    os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "members",
                 "guarded-class-registration-stubs.tsv"),
    os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                 "members", "guarded-class-registration-stubs.tsv")) if os.path.exists(p))
mem = []
for l in open(TSV, encoding="utf-8"):
    if l.startswith("#") or not l.strip():
        continue
    f = l.rstrip("\r\n").split("\t")
    if re.fullmatch(r"[0-9A-Fa-f]{8}", f[0]):
        mem.append((int(f[0], 16), int(f[1]), f[-1].strip()))
pd = [s for s in img.secs if s[0].startswith(".pdata")][0]
fl = sorted((img.BASE + struct.unpack_from("<I", img.raw, pd[3] + i)[0],
             img.BASE + struct.unpack_from("<I", img.raw, pd[3] + i + 4)[0]) for i in range(0, pd[2], 12)
            if struct.unpack_from("<I", img.raw, pd[3] + i)[0])
fs = [f[0] for f in fl]
def extent(a):
    k = bisect.bisect_left(fs, a)
    if k < len(fl) and fl[k][0] == a:
        return fl[k][1] - a
    return 0x2000
def calls(a, n):
    out = set()
    for x in img.md.disasm(img.rd(a, n), a):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            out.add(int(x.op_str, 16))
        if x.mnemonic == "int3" and x.address > a:
            break
    return out
GUARD = {0x008092FC, 0x0080929C, 0x00808B90}
cache = {}
def guarded(t):
    if t not in cache:
        cache[t] = GUARD <= calls(t, extent(t))
    return cache[t]
agree = disagree = 0
bad = []
for a, n, col in mem:
    got = sorted(t for t in calls(a, n) if not (a <= t < a + n) and t not in GUARD and guarded(t))
    listed = sorted(int(x, 16) for x in re.findall(r"[0-9A-Fa-f]{8}", col))
    if set(got) == set(listed):
        agree += 1
    else:
        disagree += 1
        bad.append((a, ["%08X" % v for v in got], ["%08X" % v for v in listed]))
print("members %d; size range %d..%d B" % (len(mem), min(m[1] for m in mem), max(m[1] for m in mem)))
print("information column: non-empty %d; agrees with the recomputed guarded-form callee set for %d, differs for %d" % (
    sum(1 for m in mem if re.search(r"[0-9A-Fa-f]{8}", m[2])), agree, disagree))
for a, g, l in bad[:20]:
    print("   %08X recomputed %s | column %s" % (a, g, l))
