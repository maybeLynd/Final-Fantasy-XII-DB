"""SWE2-AUDIT-SEM RC-16 re-read (own parse of the decompiled us corpus, independent of rc16_regfile_reads.py):
for every `while ((regI1 != -1 && regI0 < 64))` loop, name the enclosing function and actor, and list every earlier
line of the same actor that touches regI1 (any function), plus whether the loop is under `btlAtelGetRespawnCause() == -1`.
Also: in rbn_a03, every mention of regF0..regF3 in actor SND_WOMAN_A (all its functions)."""
import glob, re, os, collections
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
fnkind = collections.Counter()
prior = []
under = collections.Counter()
n = 0
for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
    L = open(f, encoding="utf-8", errors="replace").read().splitlines()
    actor_start = 0
    fn = "?"
    for i, line in enumerate(L):
        if re.match(r"^actor\s", line):
            actor_start = i
        m = re.match(r"^\s*(?:function|fn_\w+)\s+([^\s(]+)\s*\(", line)
        if m:
            fn = line.strip().split("(")[0]
        if "while ((regI1 != -1 && regI0 < 64))" in line:
            n += 1
            fnkind[re.sub(r"\d+$", "", fn.split()[-1]) if fn != "?" else "?"] += 1
            LOOPLINE = ("while ((regI1 != -1 && regI0 < 64))", "regI1 = btlAtelGetDeadCountMax(regI0);", "if (regI1 != -1)")
            earlier = [k for k in range(actor_start, i) if re.search(r"\bregI1\b", L[k])
                       and not L[k].strip().startswith(LOOPLINE) and "+ regI1)" not in L[k]]
            if earlier:
                prior.append((os.path.basename(f), i + 1, [(k + 1, L[k].strip()) for k in earlier][:3]))
            ctx = " ".join(L[max(actor_start, i - 4):i])
            under["RespawnCause() == -1" in ctx] += 1
print("loops found:", n)
print("enclosing function names:", dict(fnkind))
print("loop under a RespawnCause() == -1 test within 4 lines:", dict(under))
print("loops with an earlier regI1 line in the same actor, other than earlier copies of the same loop:", len(prior))
for p in prior[:10]:
    print("  ", p)
L = open(os.path.join(CORPUS, "rbn_a03.txt"), encoding="utf-8", errors="replace").read().splitlines()
inside = False
for i, line in enumerate(L):
    if re.match(r"^actor\s", line):
        inside = "SND_WOMAN_A" in line
    if inside and re.search(r"\bregF[0-3]\b", line):
        print("SND_WOMAN_A line %d: %s" % (i + 1, line.strip()))
