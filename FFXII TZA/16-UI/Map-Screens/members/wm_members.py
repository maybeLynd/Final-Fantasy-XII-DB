"""wm_members.py: members TSV for the map-data widget family (02B457E0 closure, wm_family.json) with, per member, which
map screens reach it. Screens are rooted at the widget procedures identified by their layout-key readers:
  track    002B7590 (container 0209E5C0) / 002B7B80 (page) / 002B8EE0 (TrackMap* reader)
  location 002BA700 (container 0209E5F0) / 002BAF80 (page) / 002BCB00 (LocaMap* reader) / 002BA040 (opener)
  world    00552250 (widget 02CA8F38) / 005528C0 / 00550A00 / 00553AE0 (WorldMap* readers)
  field    003CB650 (container 02B47760) / 003CB4F0 (page) / 003CB440 (creator)
  child    002BA240, the child widget procedure all three containers install
The page helpers 002B7460 / 00402A40 / 00402250 / 00403970 (called from both page procedures) count for track AND location;
world also takes the widgets 005542D0 / 00553F40 and the helpers 00550820 / 00550690 / 00551800 / 005632C0 / 002901D0 under it.
A member is tagged with a screen when a caller chain of at most 4 hops, staying inside the family, reaches that
screen's root functions (direct callers outside the family are matched against the roots and their callees)."""
import json, bisect, collections
raw = json.load(open("tools/rawcalls.json"))
sizes, names = {}, {}
for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
ks = sorted(sizes)
def own(s):
    i = bisect.bisect_right(ks, s) - 1
    return ks[i] if i >= 0 and ks[i] <= s < ks[i] + sizes[ks[i]] else None
callers = collections.defaultdict(set)
for tgt, sites in raw.items():
    for s in sites:
        f = own(int(s, 16))
        if f is not None: callers[int(tgt, 16)].add(f)
W = json.load(open("wm_family.json")); fam = set(int(x, 16) for x in W["family"]); seed = set(int(x, 16) for x in W["seed"])
roots = {"track": [0x2B7590, 0x2B7B80, 0x2B8EE0, 0x2B6350, 0x2B6220, 0x2B7460, 0x402A40, 0x402250, 0x403970, 0x402C30, 0x402D20], "location": [0x2BA700, 0x2BAF80, 0x2BCB00, 0x2BA040, 0x2B9D30, 0x2B7460, 0x402A40, 0x402250, 0x403970, 0x402C30, 0x402D20],
         "world": [0x552250, 0x5528C0, 0x550A00, 0x553AE0, 0x550400, 0x551F00, 0x551E00, 0x550820, 0x550690, 0x5542D0, 0x551800, 0x551930, 0x551B30, 0x553F40, 0x5632C0, 0x2901D0], "field": [0x3CB650, 0x3CB4F0, 0x3CB440], "child": [0x2BA240]}
front = set(int(l.split()[0], 16) for f in ("arch_frontier.txt", "c_frontier.txt") for l in open(f) if l.strip())
def screens(m):
    seen = {m}; frontier = {m}; hit = set(); ext = set()
    for _ in range(4):
        nxt = set()
        for f in frontier:
            for c in callers[f]:
                for k, r in roots.items():
                    if c in r: hit.add(k)
                if c in fam and c not in seen: nxt.add(c); seen.add(c)
                elif c not in fam and not any(c in r for r in roots.values()): ext.add(c)
        frontier = nxt
    return hit, ext
rows = []
cnt = collections.Counter()
for m in sorted(fam):
    hit, ext = screens(m)
    tag = ",".join(sorted(hit)) or "-"
    cnt[tag] += 1
    rows.append("%08X\t%d\t%s\t%s\t%s\t%s\t%s" % (m, sizes[m], names.get(m, ""), "singleton" if m in seed else "closure",
                                             "yes" if m in front else "no", tag, " ".join("%08X" % c for c in sorted(ext)[:6])))
with open("wm_members.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("address\tsize\tname\tmembership\tfrontier\tscreens\tother_callers\n")
    f.write("\n".join(rows) + "\n")
print(len(rows), dict(cnt))
