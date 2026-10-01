"""What each script verb reaches into.

This is a CALL-GRAPH FACT, not an ownership claim. The database's standing rule forbids inferring a
function's owner from its callers; nothing here assigns ownership to anything. It reports, for each
verb, which owning subsystems its begin/poll/result handlers call into -- which is a statement about
edges, not about who owns the handler.

Handlers are almost all owned by the bridge itself (1,857 of 1,888 rows), so the handler's own owner
tag answers nothing. The reach has to come from its callees.
"""
import collections, csv, io, os
import kit_paths as KP  # noqa: E402
import os

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
GRAPH = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph")
TSV = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")

def owner_of(tag):
    for part in tag.split(';'):
        if part.startswith('GFZ.V120.PrimaryOwner.'):
            return part.split('.')[-1]
    for part in tag.split(';'):
        if part.startswith('FFXII.'):
            return part[6:]
    return None

own = {}
with io.open(os.path.join(GRAPH, "functions.tsv"), encoding='utf-8', errors='replace') as fh:
    next(fh)
    for line in fh:
        p = line.rstrip('\r\n').split('\t')
        if len(p) >= 9:
            o = owner_of(p[8])
            if o:
                own[p[0].upper()] = o

edges = collections.defaultdict(set)
with io.open(os.path.join(GRAPH, "edges.tsv"), encoding='utf-8', errors='replace') as fh:
    next(fh)
    for line in fh:
        p = line.rstrip('\r\n').split('\t')
        if len(p) >= 3 and p[2] == 'false':
            edges[p[0].upper()].add(p[1].upper())

BRIDGE = 'Script_VM_Native_Bridge'

def reach(seeds, depth):
    """Owners reached within `depth` call levels, excluding the bridge itself."""
    seen, front, hits = set(seeds), set(seeds), collections.Counter()
    for _ in range(depth):
        nxt = set()
        for f in front:
            for c in edges.get(f, ()):
                if c in seen:
                    continue
                seen.add(c)
                nxt.add(c)
                o = own.get(c)
                if o and o != BRIDGE:
                    hits[o] += 1
        front = nxt
    return hits

rows = list(csv.DictReader(io.open(TSV, encoding='utf-8', errors='replace'), delimiter='\t'))
print("verb rows: %d" % len(rows))

per_depth = {}
for depth in (1, 2, 3):
    named = 0
    subsys = collections.Counter()
    for r in rows:
        seeds = [ (r.get(k) or '').strip().upper() for k in ('begin', 'poll', 'result') ]
        seeds = [s for s in seeds if s]
        if not seeds:
            continue
        h = reach(seeds, depth)
        if h:
            named += 1
            subsys[h.most_common(1)[0][0]] += 1
    per_depth[depth] = (named, subsys)
    print("\ndepth %d: %d of %d verbs reach a named non-bridge subsystem" % (depth, named, len(rows)))
    for k, v in subsys.most_common(14):
        print("   %5d  %s" % (v, k))

# ---- positive control: does depth-1 reach agree with what the verb NAME says? ----
# 'se' was here and matched inside set/use/release, scoring setvelr and setrect as Audio.
# Two-letter tokens are removed; every remaining token is >=3 chars and unambiguous.
EXPECT = [
    ('move',  'Movement'), ('walk', 'Movement'), ('turn', 'Movement'), ('pos', 'Movement'),
    ('bgm',   'Audio'),    ('voice','Audio'),    ('sound','Audio'),
    ('camera','Presentation'), ('fade','Presentation'),
    ('party', 'Party'),    ('member','Party'),
]
agree = dis = nohit = 0
examples = []
for r in rows:
    v = (r.get('verb') or '').lower()
    exp = next((o for k, o in EXPECT if k in v), None)
    if not exp:
        continue
    seeds = [(r.get(k) or '').strip().upper() for k in ('begin','poll','result')]
    seeds = [s for s in seeds if s]
    if not seeds:
        continue
    h = reach(seeds, 1)
    if not h:
        nohit += 1
        continue
    top = h.most_common(1)[0][0]
    if top == exp:
        agree += 1
    else:
        dis += 1
        if len(examples) < 12:
            examples.append((r.get('verb'), exp, top))
print("\n=== CONTROL: verb name vs depth-1 reach ===")
print("name implies a subsystem and reach agrees   : %d" % agree)
print("name implies a subsystem and reach disagrees: %d" % dis)
print("name implies a subsystem, no reach at all   : %d" % nohit)
for v, e, t in examples:
    print("   %-28s name says %-14s reach says %s" % (v, e, t))

# ---- refinement: a callee that everything calls says nothing about any one caller ----
indeg = collections.Counter()
for f, cs in edges.items():
    for c in cs:
        indeg[c] += 1

def reach1_filtered(seeds, max_indeg):
    hits = collections.Counter()
    for f in seeds:
        for c in edges.get(f, ()):
            if indeg[c] > max_indeg:
                continue
            o = own.get(c)
            if o and o != BRIDGE:
                hits[o] += 1
    return hits

print("\n=== depth-1 reach, discounting shared callees by in-degree ===")
for cap in (10**9, 50, 20, 10, 5):
    named = 0; agree = dis = 0
    subsys = collections.Counter()
    for r in rows:
        seeds = [(r.get(k) or '').strip().upper() for k in ('begin','poll','result')]
        seeds = [s for s in seeds if s]
        if not seeds: continue
        h = reach1_filtered(seeds, cap)
        if h:
            named += 1
            subsys[h.most_common(1)[0][0]] += 1
            v=(r.get('verb') or '').lower()
            exp=next((o for k,o in EXPECT if k in v), None)
            if exp:
                if h.most_common(1)[0][0]==exp: agree+=1
                else: dis+=1
    lab = "no cap" if cap > 10**8 else "in-degree <= %d" % cap
    acc = (100.0*agree/(agree+dis)) if (agree+dis) else 0.0
    print("  %-18s verbs labelled %4d   control %3d agree / %3d disagree  (%.0f%%)"
          % (lab, named, agree, dis, acc))

OUT = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-reach.tsv")
with io.open(OUT, 'w', encoding='utf-8', newline='') as fh:
    fh.write("call_id\tverb\tshape\treach_all\treach_filtered\ttop\n")
    for r in rows:
        seeds = [(r.get(k) or '').strip().upper() for k in ('begin','poll','result')]
        seeds = [s for s in seeds if s]
        a = reach(seeds, 1) if seeds else collections.Counter()
        f = reach1_filtered(seeds, 20) if seeds else collections.Counter()
        fh.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (
            r.get('call_id',''), r.get('verb',''), r.get('shape',''),
            ",".join("%s:%d" % kv for kv in a.most_common()),
            ",".join("%s:%d" % kv for kv in f.most_common()),
            f.most_common(1)[0][0] if f else ""))
print("\nwrote", OUT)
