"""CY-4: does any verb's recorded shape contradict which dispatch slots it actually has?
CY-1: split the verbs the reach map cannot label into 'thin handler' and 'untagged callees'.

Both are joins over files already in the tree; neither needs the binary.
"""
import collections, csv, io, os
import kit_paths as KP  # noqa: E402
import os

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
GRAPH = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph")
VT = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")

def owner_of(tag):
    for part in tag.split(';'):
        if part.startswith('GFZ.V120.PrimaryOwner.'):
            return part.split('.')[-1]
    for part in tag.split(';'):
        if part.startswith('FFXII.'):
            return part[6:]
    return None

own, known = {}, set()
with io.open(os.path.join(GRAPH, "functions.tsv"), encoding='utf-8', errors='replace') as fh:
    next(fh)
    for line in fh:
        p = line.rstrip('\r\n').split('\t')
        if len(p) >= 9:
            known.add(p[0].upper())
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

rows = list(csv.DictReader(io.open(VT, encoding='utf-8', errors='replace'), delimiter='\t'))
BRIDGE = 'Script_VM_Native_Bridge'

# ---------------- CY-4 : shape vs slots ----------------
print("=== CY-4: recorded shape against the slots actually present ===")
combo = collections.Counter()
for r in rows:
    shape = (r.get('shape') or '').strip()
    have = tuple(k for k in ('begin', 'poll', 'result') if (r.get(k) or '').strip())
    combo[(shape, have)] += 1
for (shape, have), n in sorted(combo.items(), key=lambda kv: -kv[1]):
    print("  %-16s %-28s %5d" % (shape or '(blank)', '+'.join(have) or '(none)', n))

print()
print("  contradictions by the natural reading:")
dur_no_poll = [r for r in rows if (r.get('shape') or '').strip() == 'durative'
               and not (r.get('poll') or '').strip()]
inst_with_poll = [r for r in rows if (r.get('shape') or '').strip() == 'instantaneous'
                  and (r.get('poll') or '').strip()]
print("    durative verbs with NO poll slot      : %d" % len(dur_no_poll))
for r in dur_no_poll[:10]:
    print("        %s %-24s begin=%s result=%s" % (r['call_id'], r['verb'],
          (r.get('begin') or '-'), (r.get('result') or '-')))
print("    instantaneous verbs WITH a poll slot  : %d" % len(inst_with_poll))
for r in inst_with_poll[:10]:
    print("        %s %-24s poll=%s" % (r['call_id'], r['verb'], r.get('poll')))

# ---------------- CY-1 : why a verb is unlabelled ----------------
print()
print("=== CY-1: why the reach map cannot label a verb ===")
cat = collections.Counter()
for r in rows:
    seeds = [(r.get(k) or '').strip().upper() for k in ('begin', 'poll', 'result')]
    seeds = [s for s in seeds if s]
    if not seeds:
        cat['no handler at all'] += 1
        continue
    callees = set()
    for s in seeds:
        callees |= edges.get(s, set())
    hits = {own[c] for c in callees if c in own and own[c] != BRIDGE}
    if hits:
        cat['labelled'] += 1
    elif not callees:
        cat['handler calls nothing (inline body)'] += 1
    elif all(c not in own for c in callees):
        cat['every callee is untagged'] += 1
    else:
        cat['all tagged callees are bridge-owned'] += 1
for k, v in cat.most_common():
    print("  %-40s %5d" % (k, v))
