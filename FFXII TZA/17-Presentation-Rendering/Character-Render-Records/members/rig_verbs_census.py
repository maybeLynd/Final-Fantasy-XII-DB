"""Census of the three talking-head verbs in the decompiled `us` scripts: lip flap, nod, head shake.

`setkutipakustatus` (02B8) / `setkutipakustatus_4a2` (04A2), `setunazukistatus` (02F3) / `setunazukistatus_4a3` (04A3)
and `setkubifuristatus` (0494) / `setkubifuristatus_4a4` (04A4). The plain form takes one argument (on / off); the
suffixed form takes (on, frames). Counts calls and scripts by verb, the first argument by verb, and the distinct frame
counts of the timed forms.
Control: the per-verb counts must sum to the number of call sites found by a plain substring count of the three stems.
"""
import os, re, collections

CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
STEM = r"(?:setkutipakustatus|setunazukistatus|setkubifuristatus)"
call = re.compile(r"\b(" + STEM + r"(?:_[0-9a-f]+)?)\(([^()]*)\)")
plainre = re.compile(r"\b" + STEM + r"(?:_[0-9a-f]+)?\(")
verbs = collections.Counter()
scripts = collections.defaultdict(set)
first = collections.Counter()
frames = collections.Counter()
plain = 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    plain += len(plainre.findall(t))
    for m in call.finditer(t):
        v = m.group(1)
        a = [x.strip() for x in m.group(2).split(",")]
        verbs[v] += 1
        scripts[v].add(fn)
        first[(v, a[0] if a[0] in ("0", "1") else "other")] += 1
        if len(a) == 2:
            frames[(v, a[1] if re.fullmatch(r"-?\d+(\.\d+)?", a[1]) else "computed")] += 1
parsed = sum(verbs.values())
print("# call sites by substring %d; by parsed call %d; difference %d (calls whose arguments contain a nested call)"
      % (plain, parsed, plain - parsed))
print("verb\tcalls\tscripts")
for v, n in sorted(verbs.items()):
    print("%s\t%d\t%d" % (v, n, len(scripts[v])))
print("verb\tfirst_argument\tcalls")
for (v, a), n in sorted(first.items()):
    print("%s\t%s\t%d" % (v, a, n))
print("verb\tframes\tcalls")
for (v, a), n in sorted(frames.items(), key=lambda kv: (kv[0][0], -kv[1])):
    print("%s\t%s\t%d" % (v, a, n))
