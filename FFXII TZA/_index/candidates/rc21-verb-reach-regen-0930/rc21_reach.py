"""rc21_reach.py - RC-21: the script-verb reach census regenerated at the current census, with the counting rule and
tie-break stated and made deterministic. ORACLE, 2026-09-30. Static; reads only the ledger TSVs.

The method is the page's own (Tools/analysis-kit/gfz-scripts/census_verb_reach.py, the generator of
scriptvm-verb-reach.tsv), re-implemented here without its one nondeterminism:
  owner(f)  = the GFZ.V120.PrimaryOwner.<X> tag, else the first FFXII.<X> tag, else none   (as the generator)
  edges     = edges.tsv rows with callee_external == false                                   (as the generator)
  seeds     = the begin / poll / result columns of scriptvm-verb-table.tsv                   (as the generator)
  reach(d)  = breadth-first to depth d from the seeds; every newly seen callee counts once for its owner unless the
              owner is Script_VM_Native_Bridge; bridge callees are still walked through         (as the generator)
  label     = the owner with the most hits (the rule falsification pass 1 recovered: one verb, one subsystem)
  TIE-BREAK = the generator used Counter.most_common(1) over a set of address strings, so among tied owners it took
              the one whose callee the set iteration met first - which depends on Python's per-process string hash
              seed. That is why the page's rows cannot be reproduced to the unit. Here a tie is broken
              ALPHABETICALLY by owner name, and every tied verb is also reported, with each subsystem's range
              [strict wins, strict wins + ties it is part of].

Snapshots: `cur` = Tools/work/graph/functions.tsv + edges.tsv (the census on the certified GN162 parent);
`old` = functions_live.tsv + edges_live.tsv (2026-09-03, the GN160-era export) as the history control.
Controls:
  C1  1,960 verb rows.
  C2  the old snapshot reproduces the page's depth totals 616 / 851 / 944 exactly.
  C3  every one of the page's fourteen GN160 depth-1 rows lies inside the old snapshot's [strict, strict+ties] range
      (so the published table is one tie-break draw of this method on that snapshot).
  C4  the owner-tag control of section 8 at the current census: 1,890 of 1,922 handler rows read the bridge.
"""
import collections, csv, hashlib, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))              # Database/FFXII TZA
G = os.path.abspath(os.path.join(DB, "..", "Tools", "work", "graph"))
TSV = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
BRIDGE = "Script_VM_Native_Bridge"
PAGE_D1 = {"Movement": 182, "ActorEntity": 142, "Party": 51, "Presentation": 42, "Audio": 36, "Input": 35,
           "Spawn_Encounter_Lifecycle": 31, "WorldAreaField": 29, "Story_Event_Quest_Hunt": 21,
           "CoreRuntimeScheduling": 11, "UI": 8, "CombatFormula": 7, "Resource": 6,
           "Rewards_Progression_Economy": 4}
fails = 0


def check(ok, name):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    fails += not ok


def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def owner_of(tag):
    for part in tag.split(";"):
        if part.startswith("GFZ.V120.PrimaryOwner."):
            return part.split(".")[-1]
    for part in tag.split(";"):
        if part.startswith("FFXII."):
            return part[6:]
    return None


def load(fn, ed):
    own, rawown = {}, {}
    with io.open(fn, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 9:
                o = owner_of(p[8])
                if o:
                    own[p[0].upper()] = o
            if len(p) >= 4:
                rawown[p[0].upper()] = p[3]
    edges = collections.defaultdict(set)
    with io.open(ed, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 3 and p[2] == "false":
                edges[p[0].upper()].add(p[1].upper())
    return own, rawown, edges


def reach(own, edges, seeds, depth):
    seen, front, hits = set(seeds), set(seeds), collections.Counter()
    for _ in range(depth):
        nxt = set()
        for f in sorted(front):
            for c in sorted(edges.get(f, ())):
                if c in seen:
                    continue
                seen.add(c)
                nxt.add(c)
                o = own.get(c)
                if o and o != BRIDGE:
                    hits[o] += 1
        front = nxt
    return hits


rows = list(csv.DictReader(io.open(TSV, encoding="utf-8", errors="replace"), delimiter="\t"))
check(len(rows) == 1960, "C1 verb rows = %d (1,960)" % len(rows))


def census(tag, fn, ed, out):
    own, rawown, edges = load(fn, ed)
    out.write("# snapshot %s: %s sha256 %s ; %s sha256 %s\n" % (tag, os.path.basename(fn), sha(fn)[:16],
                                                                 os.path.basename(ed), sha(ed)[:16]))
    res = {}
    for depth in (1, 2, 3):
        strict, alpha, tied_in, anysub = collections.Counter(), collections.Counter(), collections.Counter(), \
            collections.Counter()
        named = nties = 0
        per_verb = []
        for r in rows:
            seeds = [(r.get(k) or "").strip().upper() for k in ("begin", "poll", "result")]
            seeds = [s for s in seeds if s]
            h = reach(own, edges, seeds, depth) if seeds else collections.Counter()
            if not h:
                per_verb.append((r["call_id"], r["verb"], "", ""))
                continue
            named += 1
            top = max(h.values())
            best = sorted(o for o, v in h.items() if v == top)
            alpha[best[0]] += 1
            for o in h:
                anysub[o] += 1
            if len(best) == 1:
                strict[best[0]] += 1
            else:
                nties += 1
                for o in best:
                    tied_in[o] += 1
            per_verb.append((r["call_id"], r["verb"], best[0], "/".join(best) if len(best) > 1 else ""))
        res[depth] = dict(named=named, strict=strict, alpha=alpha, tied=tied_in, anysub=anysub, nties=nties,
                          per_verb=per_verb)
    # the owner-tag control, under both definitions the page uses:
    #   S2  (section 2): verb rows whose arg_handler carries an owner, and how many read the bridge;
    #   P1  (section 8, falsification pass 1): verb rows where any begin/poll/result seed carries an owner, and how many
    #       have every carried owner = the bridge.
    a = [rawown.get((r.get("arg_handler") or "").upper(), "") for r in rows if r.get("arg_handler")]
    a = [t for t in a if t]
    n = b = 0
    for r in rows:
        os_ = [rawown.get((r.get(k) or "").upper(), "") for k in ("begin", "poll", "result") if r.get(k)]
        os_ = [o for o in os_ if o]
        if os_:
            n += 1
            b += all(o == BRIDGE for o in os_)
    res["ownertag"] = ((sum(1 for t in a if t == BRIDGE), len(a)), (b, n))
    return res


out = io.open(os.path.join(HERE, "rc21_reach.tsv"), "w", encoding="utf-8", newline="")
old = census("old", os.path.join(G, "functions_live.tsv"), os.path.join(G, "edges_live.tsv"), out)
cur = census("cur", os.path.join(G, "functions.tsv"), os.path.join(G, "edges.tsv"), out)

check(tuple(old[d]["named"] for d in (1, 2, 3)) == (616, 851, 944),
      "C2 old snapshot depth totals %s (page 616 / 851 / 944)" % [old[d]["named"] for d in (1, 2, 3)])
bad = []
for s, v in PAGE_D1.items():
    lo, hi = old[1]["strict"][s], old[1]["strict"][s] + old[1]["tied"][s]
    if not lo <= v <= hi:
        bad.append("%s %d not in [%d,%d]" % (s, v, lo, hi))
check(not bad, "C3 every GN160 depth-1 row lies in the old snapshot's tie range %s" % (bad or ""))
print("owner-tag control S2 (arg_handler rows): old %d of %d, cur %d of %d" % (old["ownertag"][0] + cur["ownertag"][0]))
print("owner-tag control P1 (begin/poll/result rows, all bridge): old %d of %d, cur %d of %d" %
      (old["ownertag"][1] + cur["ownertag"][1]))
check(cur["ownertag"][0] == (1857, 1888) and cur["ownertag"][1] == (1890, 1922),
      "C4 section 2's 1,857 of 1,888 and pass 1's 1,890 of 1,922 both reproduce at the current census")
check(old["ownertag"] == cur["ownertag"], "C4b the two readings are the same at the old and the current snapshot")



def joint_feasible(res, page=PAGE_D1):
    """C5: is there ONE assignment of the depth-1 tied verbs, each to one owner of its tie set, that yields all fourteen
    GN160 rows exactly and puts the remaining 11 labelled verbs in the six omitted subsystems? Bipartite b-matching by
    augmenting paths (every achievable assignment is a possible first-hit order of the generator's sets)."""
    need = {}
    for s, v in page.items():
        need[s] = v - res[1]["strict"][s]
    omitted = sorted(set(res[1]["anysub"]) - set(page))
    need["OMITTED"] = 616 - 605 - sum(res[1]["strict"][s] for s in omitted)
    if any(v < 0 for v in need.values()):
        return False, need
    ties = [pv[3].split("/") for pv in res[1]["per_verb"] if pv[3]]
    ties = [["OMITTED" if o not in page else o for o in t] for t in ties]
    cap = dict(need)
    match = {}                                         # verb index -> subsystem
    load = collections.Counter()

    def augment(v, seen):
        for s in set(ties[v]):
            if s in seen:
                continue
            seen.add(s)
            if load[s] < cap[s]:
                match[v] = s; load[s] += 1
                return True
            for u, su in list(match.items()):
                if su == s and augment(u, seen):
                    match[v] = s
                    return True
        return False
    for v in range(len(ties)):
        augment(v, set())
    ok = len(match) == len(ties) and all(load[s] == cap[s] for s in cap)
    return ok, dict((s, (load[s], cap[s])) for s in cap)


ok, detail = joint_feasible(old)
check(ok, "C5 one tie assignment on the old snapshot reproduces all fourteen GN160 rows and the omitted 11 %s" %
      ("" if ok else detail))
ok, detail = joint_feasible(cur)
check(ok, "C5b the same holds on the current census")
neg = dict(PAGE_D1, ActorEntity=160, Party=53)     # each inside its own range, jointly impossible if they share ties
ok_neg, _d = joint_feasible(cur, neg)
neg2 = dict(PAGE_D1, Movement=179)                 # below Movement's strict wins
ok_neg2, _d2 = joint_feasible(cur, neg2)
check(not ok_neg2, "C6 negative control: an out-of-range target (Movement 179) is rejected by the matcher")
print("info: ActorEntity 160 with Party 53 jointly feasible: %s" % ok_neg)

for d in (1, 2, 3):
    subs = sorted(set(cur[d]["anysub"]) | set(old[d]["anysub"]) | (set(PAGE_D1) if d == 1 else set()),
                  key=lambda s: (-cur[d]["alpha"][s], s))
    print("\n=== depth %d: labelled cur %d (old %d); tied verbs cur %d (old %d) ===" %
          (d, cur[d]["named"], old[d]["named"], cur[d]["nties"], old[d]["nties"]))
    print("%-32s %6s %6s %6s %8s %13s %13s" % ("subsystem", "page", "old", "cur", "cur-any", "old range", "cur range"))
    for s in subs:
        pg = PAGE_D1.get(s, "") if d == 1 else ""
        print("%-32s %6s %6d %6d %8d %13s %13s" % (
            s, pg, old[d]["alpha"][s], cur[d]["alpha"][s], cur[d]["anysub"][s],
            "[%d,%d]" % (old[d]["strict"][s], old[d]["strict"][s] + old[d]["tied"][s]),
            "[%d,%d]" % (cur[d]["strict"][s], cur[d]["strict"][s] + cur[d]["tied"][s])))
    print("%-32s %6s %6d %6d" % ("TOTAL (partition)", "605" if d == 1 else "", sum(old[d]["alpha"].values()),
                                 sum(cur[d]["alpha"].values())))

out.write("call_id\tverb\td1_cur\td1_cur_ties\td2_cur\td2_cur_ties\td3_cur\td3_cur_ties\td1_old\td1_old_ties\n")
for k in range(len(rows)):
    c1, c2, c3, o1 = cur[1]["per_verb"][k], cur[2]["per_verb"][k], cur[3]["per_verb"][k], old[1]["per_verb"][k]
    out.write("\t".join([c1[0], c1[1], c1[2], c1[3], c2[2], c2[3], c3[2], c3[3], o1[2], o1[3]]) + "\n")
out.close()
moved = [(cur[1]["per_verb"][k][0], cur[1]["per_verb"][k][1], old[1]["per_verb"][k][2], cur[1]["per_verb"][k][2])
         for k in range(len(rows)) if old[1]["per_verb"][k][2] != cur[1]["per_verb"][k][2]]
print("\ndepth-1 label changes old -> cur (alphabetical tie-break both sides): %d" % len(moved))
for m in moved:
    print("  %s %-28s %s -> %s" % m)
print("\nFAILS %d" % fails)
sys.exit(1 if fails else 0)
