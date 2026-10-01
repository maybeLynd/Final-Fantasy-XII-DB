# rc13_channels.py - RC-13: what each actor request channel means to a script author. Authored-data census over the shipped
# decompiled scripts (corpus/us/*.txt, 1,114 scripts): every call of the REQ family written with a literal channel,
#   sysReq / sysReqsw / sysReqew / sysReqi / sysReqewi / sysReqall / sysReqiall / sysReqwait... (channel, Target::function)
# tallies, per channel, the functions requested on it (by function name, the part after '::'), and the verb forms.
# Control: the per-verb totals by channel must match a plain regex count (printed side by side).
import os, re, collections
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
call = re.compile(r"\b(sysReq[a-z]*)\((\-?\d+),\s*([^\s,()]+?)::([^\s,()]+)\)")
anycall = re.compile(r"\bsysReq[a-z]*\((\-?\d+),")
by_ch = collections.defaultdict(collections.Counter)
verbs = collections.defaultdict(collections.Counter)
scripts = collections.defaultdict(set)
plain = collections.Counter()
parsed = collections.Counter()
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    for m in anycall.finditer(t):
        plain[int(m.group(1))] += 1
    for m in call.finditer(t):
        ch = int(m.group(2))
        parsed[ch] += 1
        by_ch[ch][m.group(4)] += 1
        verbs[ch][m.group(1)] += 1
        scripts[ch].add(fn)
print("channel  calls(parsed/plain)  scripts  top verbs | top requested functions")
for ch in sorted(set(plain) | set(parsed)):
    top = ", ".join("%s %d" % kv for kv in by_ch[ch].most_common(12))
    vb = ", ".join("%s %d" % kv for kv in verbs[ch].most_common(4))
    print("%3d  %6d/%6d  %5d  %s | %s" % (ch, parsed[ch], plain[ch], len(scripts[ch]), vb, top))
# naming families: share of requests on each channel whose function name starts with a common prefix
fam = collections.defaultdict(collections.Counter)
for ch, c in by_ch.items():
    for name, n in c.items():
        p = re.match(r"[a-z]+", name.lower())
        fam[ch][p.group(0) if p else name] += n
print()
for ch in sorted(fam):
    tot = sum(fam[ch].values())
    print("%3d  name-prefix shares: %s" % (ch, ", ".join("%s %.0f%%" % (k, 100.0 * v / tot) for k, v in fam[ch].most_common(8))))
