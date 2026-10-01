"""gg1_helpers.py - GG-1: nine more readers of 02F9736A placed through their callers (FABLE, Claude Opus 5.5, 2026-09-28).
Static; companion to ../gg1-static-order/ and ../gg1-message10-readers/ (whose jump-table decoder this imports).

  H1  seven readers that are not message procs are reached ONLY from call sites inside decoded message-10 arms (every
      direct caller path ends in a proc whose call site sits in its message-10 arm): 00240DE0, 002A5CC0, 002A5F40,
      0023F240, 00284EC0, 0029B870, 0055C740 - so they share the message-10 frame placement
  H2  002287D0's only caller is the arbiter itself, at 00253CCC, before every one of the arbiter's five clears
      (00253F70, 00253FE9, 002540C5, 0025415F, 002541BC) - so it reads the snapshot before the arbiter clears it
  H3  the arbiter 00253C70 reads the word itself (it is the consumer the question is about)
  N   002D3900 is NOT placed: one of its paths comes through 002BD680's message-9 (focus lost) arm, whose sender is the
      focus switch, not a frame position
  C   control: a reader known to be a message-10 proc (002778C0) is refused by H1's helper test (it has no direct callers)
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "../gg1-message10-readers/gg1_msg10_readers.py"), encoding="utf-8").read().split("def is_read")[0])
callers = collections.defaultdict(set)
for f, ins in body.items():
    for a, s in ins:
        m = re.match(r"(call|jmp) 0x([0-9a-f]+)$", s)
        if m: callers["%08X" % int(m.group(2), 16)].add((f, a))
def roots(h):
    seen = {h}; q = [h]; hits = []; dead = []
    while q:
        g = q.pop(0)
        cs = callers.get(g, ())
        if not cs and g != h: dead.append(g)
        for c, site in cs:
            arms = decode(c)
            if arms:
                starts = sorted(set(arms.values())); arm = max((t for t in starts if t <= site), default=None)
                dflt = collections.Counter(arms.values()).most_common(1)[0][0]
                hits.append((c, site, () if arm == dflt else tuple(sorted(m for m, t in arms.items() if t == arm))))
            elif c not in seen and len(seen) < 500:
                seen.add(c); q.append(c)
    return hits, dead, seen
H1 = ["00240DE0", "002A5CC0", "002A5F40", "0023F240", "00284EC0", "0029B870", "0055C740"]
res = {h: roots(h) for h in H1}
learef = {h for h in H1 if any("=>%s" % h in x for f, ins in body.items() for a, x in ins if x.startswith("lea"))}
ok("H1", not learef and all(res[h][0] and all(ids and 10 in ids and set(ids) <= {10, 11} for c, s, ids in res[h][0]) and not res[h][1] for h in H1),
   "none address-taken (%s); each reached only through message-10 arms: %s" % (sorted(learef), {h: sorted({(c, ids) for c, s, ids in res[h][0]}) for h in H1}))
arb = [s for a, s in body["00253C70"]]
clears = [a for a, s in body["00253C70"] if s.startswith("mov word ptr [rip") and "=>02F9736A" in s and s.split(";")[0].split(",")[1].strip() == "di"]
ok("H2", sorted(callers["002287D0"]) == [("00253C70", 0x00253CCC)] and clears and all(0x00253CCC < c for c in clears),
   "002287D0's only caller is the arbiter at 00253CCC; the arbiter's clears of 02F9736A: %s" % ["%08X" % c for c in clears])
ok("H3", any("=>02F9736A" in s and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0]) for s in arb), "the arbiter reads 02F9736A itself")
r = roots("002D3900")
ok("N", any(ids == (9,) for c, s, ids in r[0]) and any(10 in ids for c, s, ids in r[0]), "002D3900 is mixed: %s" % sorted({(c, ids) for c, s, ids in r[0]}))
ok("C", not callers.get("002778C0") and not roots("002778C0")[0], "control: the message-10 proc 002778C0 has no direct callers, so it is not a helper")
print("FAILS", fails); sys.exit(1 if fails else 0)
