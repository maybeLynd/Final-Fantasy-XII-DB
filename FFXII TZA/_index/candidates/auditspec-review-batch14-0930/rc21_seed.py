"""rc21_seed.py - SWE2-AUDIT-SPEC (2026-09-30), independent of rc21_reach.py / rc21_draws.py.

Tests RC-21's tie-break claim directly: census_verb_reach.py's depth-1 label is Counter.most_common(1) over hits
inserted in Python set-iteration order, so among tied owners the label depends on PYTHONHASHSEED. Written from the
generator's text (owner = GFZ.V120.PrimaryOwner tag else first FFXII. tag; non-external edges; seeds begin/poll/result;
bridge callees count for nobody). Depth 1 only.
Parent: runs itself as a child under seeds 0..11 and prints each subsystem's min..max, plus the deterministic
alphabetical-tie-break count and the number of tied verbs. Sensitivity: if ties did not exist or were broken
deterministically, every row would print a single value (min == max) across the seeds.
Also run a child under a FIXED seed twice: both runs must agree (the variation is the seed, not other noise).
"""
import collections, csv, io, json, os, subprocess, sys
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
GRAPH = os.path.join(ROOT, "Database", "Tools", "work", "graph")
TSV = os.path.join(ROOT, "Database", "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
BRIDGE = "Script_VM_Native_Bridge"


def load():
    own = {}
    with io.open(os.path.join(GRAPH, "functions.tsv"), encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\r\n").split("\t")
            if len(p) < 9:
                continue
            tags = p[8].split(";")
            o = next((t.split(".")[-1] for t in tags if t.startswith("GFZ.V120.PrimaryOwner.")), None)
            if o is None:
                o = next((t[6:] for t in tags if t.startswith("FFXII.")), None)
            if o:
                own[p[0].upper()] = o
    edges = collections.defaultdict(set)
    with io.open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3 and p[2] == "false":
                edges[p[0].upper()].add(p[1].upper())
    rows = list(csv.DictReader(io.open(TSV, encoding="utf-8", errors="replace"), delimiter="\t"))
    return own, edges, rows


def hits1(seeds, own, edges):
    seen, h = set(seeds), collections.Counter()
    for f in set(seeds):
        for c in edges.get(f, ()):
            if c in seen:
                continue
            seen.add(c)
            o = own.get(c)
            if o and o != BRIDGE:
                h[o] += 1
    return h


def child():
    own, edges, rows = load()
    lab = collections.Counter()
    for r in rows:
        seeds = [(r.get(k) or "").strip().upper() for k in ("begin", "poll", "result")]
        seeds = [s for s in seeds if s]
        if seeds:
            h = hits1(seeds, own, edges)
            if h:
                lab[h.most_common(1)[0][0]] += 1
    print(json.dumps(lab))


def parent():
    runs = {}
    for s in range(12):
        env = dict(os.environ, PYTHONHASHSEED=str(s))
        out = subprocess.run([sys.executable, "-B", __file__, "--child"], capture_output=True, text=True, env=env).stdout
        runs[s] = json.loads(out)
    env = dict(os.environ, PYTHONHASHSEED="7")
    again = json.loads(subprocess.run([sys.executable, "-B", __file__, "--child"], capture_output=True, text=True, env=env).stdout)
    own, edges, rows = load()
    alpha, tied = collections.Counter(), 0
    for r in rows:
        seeds = [(r.get(k) or "").strip().upper() for k in ("begin", "poll", "result")]
        seeds = [s for s in seeds if s]
        if seeds:
            h = hits1(seeds, own, edges)
            if h:
                top = max(h.values())
                best = sorted(o for o, v in h.items() if v == top)
                tied += len(best) > 1
                alpha[best[0]] += 1
    subs = sorted(set().union(*[set(v) for v in runs.values()]) | set(alpha), key=lambda k: -alpha.get(k, 0))
    print("depth-1 labels over PYTHONHASHSEED 0..11; alphabetical tie-break; tied verbs %d; total per seed %s"
          % (tied, sorted(set(sum(v.values()) for v in runs.values()))))
    moving = 0
    for k in subs:
        vals = [runs[s].get(k, 0) for s in runs]
        moving += min(vals) != max(vals)
        print("  %-32s alpha %4d   seeds %4d..%-4d %s" % (k, alpha.get(k, 0), min(vals), max(vals), "MOVES" if min(vals) != max(vals) else ""))
    print("rows that move across seeds: %d; alphabetical total %d" % (moving, sum(alpha.values())))
    print("CONTROL same seed twice gives the same labels: %s" % ("PASS" if again == runs[7] else "FAIL"))


if __name__ == "__main__":
    child() if "--child" in sys.argv else parent()
