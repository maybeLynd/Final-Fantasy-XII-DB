"""fbucket.py KIT DB [BASE_DB] - bucket check_dispositions' frontier by cause (SWE2-EC7, 2026-09-30).

Uses check_dispositions' own evaluate() from KIT, so the sets are the gate's.
Per body at DB:
  A-REFUSED-ROW   frontier only because its row is refused for A overlap (linkage drift: the row's
                  accounting is intact, the row is refused whole because another member became A)
  OTHER-REFUSED   frontier because its row is refused for a non-A reason
  UNDECLARED      declared by no row at all (genuine frontier)
With BASE_DB, each body that is frontier at DB but not at BASE is classified by what it was at BASE
and what changed (lost A = semantic loss of individual accounting; left an accepted row, etc.).
"""
import collections, io, json, os, re, sys

KIT, DB = sys.argv[1], sys.argv[2]
BASE = sys.argv[3] if len(sys.argv) > 3 else None
sys.path.insert(0, KIT)
import check_dispositions as CD  # noqa

sizes = CD.load_functions()


def state(db):
    r = CD.evaluate(db, sizes)
    a_set = CD.measure_a(db, sizes)[0]
    rows = CD.parse_families(db)
    refused = dict(r["refusals"])
    acc = {w for w, _l, _n in r["accepted"]}
    member_of = collections.defaultdict(list)   # body -> [(who, status, why)]
    rowinfo = {}
    for doc, parts in rows:
        if len(parts) < 5:
            continue
        who = "%s :: %s" % (os.path.basename(doc), parts[0])
        try:
            mem = CD.read_members(doc, parts[2])
        except Exception:
            continue
        st = "ACC" if who in acc else ("REF" if who in refused else "?")
        why = refused.get(who, "")
        kind = "A" if "already measured as A" in why else ("OTHER" if why else "")
        rowinfo[who] = (st, kind, len(mem), os.path.relpath(doc, db).replace("\\", "/"))
        for m in mem:
            member_of[m].append((who, st, kind))
    return r, a_set, member_of, rowinfo


r, a_set, mem, rows = state(DB)
fr = r["frontier_set"]
b = collections.Counter()
per_row = collections.Counter()
for f in fr:
    ms = mem.get(f, [])
    if not ms:
        b["UNDECLARED"] += 1
    elif any(k == "A" for _w, _s, k in ms):
        b["A-REFUSED-ROW"] += 1
        for w, s, k in ms:
            if k == "A":
                per_row[w] += 1
    else:
        b["OTHER-REFUSED"] += 1
        for w, s, k in ms:
            per_row[w] += 1
print("DB %s" % DB)
print("frontier %d  A %d  B %d  C %d  refused rows %d" % (r["frontier"], r["A"], r["B"], r["C"], r["families_refused"]))
for k in ("A-REFUSED-ROW", "OTHER-REFUSED", "UNDECLARED"):
    print("  %-14s %6d" % (k, b[k]))
uc1f = r["frontier_set"] & CD.uc1_band.frontier_starts()
print("  (of UNDECLARED+rest, UC-1 frontier bodies: %d)" % len(uc1f))
print("refused rows -> bodies they drop to frontier:")
for w, n in per_row.most_common():
    st, kind, size, doc = rows[w]
    na = sum(1 for m in a_set if any(x[0] == w for x in mem.get(m, [])))
    print("  %5d  [%s] %s (declared-file %d, A members %d)  %s" % (n, kind, w[:90], size, na, doc))

if BASE:
    r0, a0, mem0, rows0 = state(BASE)
    fr0 = r0["frontier_set"]
    print()
    print("BASE %s: frontier %d  A %d  refused rows %d" % (BASE, r0["frontier"], r0["A"], r0["families_refused"]))
    new = fr - fr0
    gone = fr0 - fr
    print("frontier at DB not at BASE: %d ; frontier at BASE not at DB: %d ; net %+d" % (len(new), len(gone), len(fr) - len(fr0)))
    c = collections.Counter()
    ex = collections.defaultdict(list)
    for f in new:
        was = "A" if f in a0 else ("ROW" if any(s == "ACC" for _w, s, _k in mem0.get(f, [])) else "?")
        ms = mem.get(f, [])
        if was == "A":
            if any(k == "A" for _w, _s, k in ms):
                cause = "was-A, lost A, row refused (A-drift) -> linkage"
            elif ms:
                cause = "was-A, lost A, in a non-A-refused row"
            else:
                cause = "SEMANTIC: was A, lost A (page demoted or cite moved), no row"
        elif was == "ROW":
            w0 = [w for w, s, _k in mem0.get(f, []) if s == "ACC"]
            if any(k == "A" for _w, _s, k in ms):
                cause = "LINKAGE: row refused for A overlap (A-drift)"
            elif ms and any(k == "OTHER" for _w, _s, k in ms):
                cause = "row refused for another reason"
            elif not ms:
                cause = "left its row's members file (removed / row retired)"
            else:
                cause = "other"
            ex[cause].append((f, w0[0] if w0 else ""))
        else:
            cause = "not in BASE census"
        c[cause] += 1
    for k, v in c.most_common():
        print("  %6d  %s" % (v, k))
    for k in ex:
        if not k.startswith("LINKAGE"):
            rowc = collections.Counter(w for _f, w in ex[k])
            print("   %s, by BASE row: %s" % (k, "; ".join("%s=%d" % (w[:70], n) for w, n in rowc.most_common(8))))
    # A gained/lost
    print("A gained %d, A lost %d" % (len(a_set - a0), len(a0 - a_set)))
    lostA = sorted(a0 - a_set)
    print("A lost, now frontier: %d ; now in accepted row: %d" % (
        sum(1 for f in lostA if f in fr), sum(1 for f in lostA if f not in fr)))
    json.dump({"lostA": ["%08X" % f for f in lostA], "new_frontier": ["%08X" % f for f in sorted(new)]},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fbucket_diff.json"), "w"))
