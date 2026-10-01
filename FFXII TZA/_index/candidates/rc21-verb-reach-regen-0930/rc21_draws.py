"""rc21_draws.py - RC-21 tie-break control (ORACLE, 2026-09-30). Runs the page's own generator logic
(Tools/analysis-kit/gfz-scripts/census_verb_reach.py: set-valued edges, Counter.most_common(1)) verbatim at depth 1
under PYTHONHASHSEED = 0..N-1, on the current census, and tallies the depth-1 partition per seed.

Question it settles: is the page's GN160 table (and its five "drifting" rows) one draw of the generator's tie-break,
which follows Python's per-process string-hash seed, rather than a snapshot difference?
Usage: python rc21_draws.py [N]      (child mode: python rc21_draws.py --child)
"""
import collections, csv, io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
G = os.path.abspath(os.path.join(DB, "..", "Tools", "work", "graph"))
TSV = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
PAGE_D1 = {"Movement": 182, "ActorEntity": 142, "Party": 51, "Presentation": 42, "Audio": 36, "Input": 35,
           "Spawn_Encounter_Lifecycle": 31, "WorldAreaField": 29, "Story_Event_Quest_Hunt": 21,
           "CoreRuntimeScheduling": 11, "UI": 8, "CombatFormula": 7, "Resource": 6,
           "Rewards_Progression_Economy": 4}
FIVE = ("ActorEntity", "Party", "WorldAreaField", "Resource", "Rewards_Progression_Economy")


def child():
    # --- verbatim logic of census_verb_reach.py (owner_of, edges as sets, reach, most_common(1)) ---
    def owner_of(tag):
        for part in tag.split(';'):
            if part.startswith('GFZ.V120.PrimaryOwner.'):
                return part.split('.')[-1]
        for part in tag.split(';'):
            if part.startswith('FFXII.'):
                return part[6:]
        return None
    own = {}
    with io.open(os.path.join(G, "functions.tsv"), encoding='utf-8', errors='replace') as fh:
        next(fh)
        for line in fh:
            p = line.rstrip('\r\n').split('\t')
            if len(p) >= 9:
                o = owner_of(p[8])
                if o:
                    own[p[0].upper()] = o
    edges = collections.defaultdict(set)
    with io.open(os.path.join(G, "edges.tsv"), encoding='utf-8', errors='replace') as fh:
        next(fh)
        for line in fh:
            p = line.rstrip('\r\n').split('\t')
            if len(p) >= 3 and p[2] == 'false':
                edges[p[0].upper()].add(p[1].upper())
    BRIDGE = 'Script_VM_Native_Bridge'

    def reach(seeds, depth):
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
    subsys = collections.Counter()
    for r in rows:
        seeds = [(r.get(k) or '').strip().upper() for k in ('begin', 'poll', 'result')]
        seeds = [s for s in seeds if s]
        if not seeds:
            continue
        h = reach(seeds, 1)
        if h:
            subsys[h.most_common(1)[0][0]] += 1
    print(json.dumps(subsys))


def main(n):
    tallies = []
    for seed in range(n):
        env = dict(os.environ, PYTHONHASHSEED=str(seed))
        out = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--child"], env=env,
                             capture_output=True, text=True, check=True).stdout
        tallies.append(collections.Counter(json.loads(out)))
    exact14 = sum(1 for t in tallies if all(t[s] == v for s, v in PAGE_D1.items()))
    print("draws: %d (PYTHONHASHSEED 0..%d), current census, depth 1" % (n, n - 1))
    print("draws reproducing all fourteen GN160 rows exactly: %d" % exact14)
    stable = [s for s in PAGE_D1 if len(set(t[s] for t in tallies)) == 1]
    print("rows identical in every draw: %d (%s)" % (len(stable), ", ".join(stable)))
    for s in PAGE_D1:
        vals = collections.Counter(t[s] for t in tallies)
        print("  %-30s page %4d  draws min %4d max %4d  page value drawn %3d times  %s" % (
            s, PAGE_D1[s], min(vals), max(vals), vals[PAGE_D1[s]], "FIVE" if s in FIVE else ""))
    print("partition totals in every draw: %s" % sorted(set(sum(t.values()) for t in tallies)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        child()
    else:
        main(int(sys.argv[1]) if len(sys.argv) > 1 else 100)
