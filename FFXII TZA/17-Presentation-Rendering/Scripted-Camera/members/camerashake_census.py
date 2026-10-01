"""Census of the camera-shake verbs in the decompiled `us` scripts.

`camerashakestart_1a3(channel, id)` is the only start form the shipped scripts use. Its handler masks the id to 24 bits
and uses it as an index into the camera object's shake bank; the top byte of every id in the corpus is printed so the
resource-type tag can be seen. Every camerashake* call is counted by verb, and the start calls by (channel, index).
Control: the per-verb counts must sum to the number of `camerashake` call sites found by a plain substring count.
"""
import os, re, collections

CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
call = re.compile(r"\b(camerashake[a-z_0-9]*)\(([^)]*)\)")
verbs = collections.Counter()
starts = collections.Counter()
tags = collections.Counter()
files = collections.defaultdict(set)
plain = 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"):
        continue
    t = open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()
    plain += len(re.findall(r"\bcamerashake[a-z_0-9]*\(", t))
    for m in call.finditer(t):
        verbs[m.group(1)] += 1
        if m.group(1) == "camerashakestart_1a3":
            a = [x.strip() for x in m.group(2).split(",")]
            if len(a) == 2:
                try:
                    ch = int(a[0], 0)
                    rid = int(a[1], 0)
                except ValueError:
                    starts[("computed", a[1])] += 1
                    continue
                starts[(ch, rid & 0xFFFFFF)] += 1
                tags[rid >> 24] += 1
                files[(ch, rid & 0xFFFFFF)].add(fn)
print("# call sites by substring %d; by parsed call %d (control: equal)" % (plain, sum(verbs.values())))
print("# id top bytes: " + ", ".join("0x%02X x%d" % kv for kv in sorted(tags.items())))
print("verb\tcalls")
for v, n in verbs.most_common():
    print("%s\t%d" % (v, n))
print("start_channel\tbank_index\tcalls\tscripts")
for (ch, idx), n in sorted(starts.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
    print("%s\t%s\t%d\t%d" % (ch, idx, n, len(files.get((ch, idx), ()))))
