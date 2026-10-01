"""gg1_sim.py - every reader of 02F9736A, with the message ids whose dispatch arm holds each read (FABLE, Claude Opus 5.5,
2026-09-28). Uses dispatch_sim.py (self-tested on four procs of different shapes).
Prints one line per reader: its ids per read, or why it has none (no dispatch head: a helper, not a proc).
  A1  agreement: every reader earlier records placed through a message-10 arm (27 procs) gets exactly {10} or {10, 11}
  A2  the message-2 and message-31 readers come out as {2} and {31}
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dispatch_sim as ds
ds.load()
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def is_read(s): return "02F9736A" in s and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0])
raw = collections.defaultdict(list)
for line in open(ds.CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3 and "=>02F9736A" in p[2]: raw[p[1]].append((int(p[0], 16), p[2]))
readers = sorted(f for f, rr in raw.items() if any(is_read(s.split(" ;")[0] + " 02F9736A") and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0]) for a, s in rr))
IDS = range(0, 0x60)
res = {}
for f in readers:
    i0, R = ds.head(f)
    if i0 is None: res[f] = ("no-head", None); continue
    arms = ds.arms(f, IDS)
    if any(v is None for v in arms.values()): res[f] = ("sim-incomplete", None); continue
    dflt = collections.Counter(arms.values()).most_common(1)[0][0]
    starts = sorted(set(arms.values()))
    per = []
    for a, s in raw[f]:
        if s.startswith("mov") and "ptr [rip" in s.split(",")[0]: continue
        arm = max((t for t in starts if t <= a), default=None)
        per.append(("default" if arm == dflt else tuple(m for m in IDS if arms[m] == arm)) if arm else ("head",))
    res[f] = ("proc", sorted(set(per), key=str))
for f in readers: print(f, res[f][0], res[f][1])
M10 = ["00228C70", "0023BD40", "0023CE10", "00241D40", "002778C0", "00280DE0", "002A6190", "002D5EB0", "00552250", "005528C0", "005542D0",
       "00560910", "00571A50", "00572E10", "005742D0", "0057AC10", "0023B6F0", "0023C5C0", "0023D6B0", "0023DB40", "0027EA70", "002C59D0",
       "003C8B70", "003EF050", "003F4330", "00572600", "005789D0"]
bad = [f for f in M10 if not (res[f][0] == "proc" and res[f][1] and all(set(x) <= {10, 11} and 10 in x for x in res[f][1]))]
ok("A1", len(readers) == 51 and not bad, "%d readers; the 27 message-10 procs all agree except %s" % (len(readers), bad))
ok("A2", res["0027AA70"][1] == [(2,)] and res["005519E0"][1] == [(2,)] and res["003CAB00"][1] == [(31,)], "message-2 / message-31 readers: %s %s %s" % (res["0027AA70"][1], res["005519E0"][1], res["003CAB00"][1]))
# H: readers with no dispatch head are helpers. Walk their direct callers up to procs that have one, and give each call
# site the ids of the arm that holds it (the same contiguity rule as the reads).
callers = collections.defaultdict(set)
for f, ins in ds.body.items():
    for a, s in ins:
        m = re.match(r"(call|jmp) 0x([0-9a-f]+)$", s)
        if m: callers["%08X" % int(m.group(2), 16)].add((f, a))
lea_taken = collections.defaultdict(set)
for line in open(ds.CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3 and p[2].startswith("lea"):
        m = re.search(r"=>([0-9A-F]{8})", p[2])
        if m: lea_taken[m.group(1)].add(p[1])
ARMS = {}
def arm_ids(proc, site):
    if proc not in ARMS: ARMS[proc] = ds.arms(proc, IDS)
    arms = ARMS[proc]
    if any(v is None for v in arms.values()): return ("sim-incomplete",)
    dflt = collections.Counter(arms.values()).most_common(1)[0][0]
    arm = max((t for t in set(arms.values()) if t <= site), default=None)
    return ("default",) if arm == dflt else (tuple(m for m in IDS if arms[m] == arm) if arm else ("head",))
def helper(h):
    seen = {h}; q = [h]; hits = set(); loose = set()
    while q:
        g = q.pop(0)
        if not callers.get(g) and g != h: loose.add(g)
        if lea_taken.get(g) and g != h and ds.head(g)[0] is None: loose.add(g + "(address-taken)")
        for c, site in callers.get(g, ()):
            if ds.head(c)[0] is not None: hits.add((c, arm_ids(c, site)))
            elif c not in seen and len(seen) < 400: seen.add(c); q.append(c)
    if lea_taken.get(h): loose.add(h + "(address-taken)")
    return sorted(hits, key=str), sorted(loose)
for f in readers:
    if res[f][0] == "no-head":
        hits, loose = helper(f)
        print("H", f, "via procs:", hits, "| other roots:", loose[:6])
HELP10 = {}
for f in readers:
    if res[f][0] == "no-head":
        hits, loose = helper(f); HELP10[f] = (hits, loose)
only10 = lambda hits, loose: hits and not loose and all(ids and ids[0] != "default" and 10 in ids and set(ids) <= {10, 11} for c, ids in hits)
NEW_PROC10 = ["002C2320", "003FF360"]
NEW_HELP10 = ["002D3900", "003FDAD0", "00564D30", "00564E10", "0056CA60", "0056DED0"]
ok("P1", all(res[f] == ("proc", [(10,)]) for f in NEW_PROC10), "two more procs read only in a message-10 arm: %s" % NEW_PROC10)
ok("P2", all(only10(*HELP10[f]) for f in NEW_HELP10),
   "six helpers reached only from message-10 arms, with no other root: %s" % {f: len(HELP10[f][0]) for f in NEW_HELP10})
B = {a: s for a, s in ds.body["0027E9E0"]}
ok("P3", res["002878E0"][1] == [(10,), (2,)] and B.get(0x0027EA1F) == "call 0x244f50" and B.get(0x0027EA26, "").startswith("mov qword ptr [rip")
   and B.get(0x0027EA49, "").startswith("mov rdx, qword ptr [rip") and B.get(0x0027EA50, "").startswith("mov rcx, qword ptr [rip") and B.get(0x0027EA57) == "call 0x246ad0"
   and sorted(lea_taken["002878E0"]) == ["0027E9E0"],
   "002878E0 reads in its message-10 and message-2 arms; 0027E9E0 creates its window (0027EA1F), stores it at 0209AC18 and attaches it to [0208EA40] (0027EA57)")
t = {m: ds.run("002BD680", m) for m in (9, 10)}
ok("C1", t[10] == 0x002BD714 and t[9] == 0x002BD834 and all(0x002BD714 <= a < 0x002BD75F for a in (0x002BD71F, 0x002BD745)),
   "control: 002BD680 (lea eax, [rcx - 1] bias) - message 10 -> 002BD714, which holds both calls to 002D3900 (002BD71F, 002BD745); message 9 -> 002BD834")
# P4: 002A9980 has no caller and no lea; it is the first qword of kind-0 and kind-1 records of the 0x18-stride table
# 009164C0, which 002B3930 indexes by the object's type byte (+0xA3) and tail-jumps through. 002B3930 is called only
# from 002A5CC0 (a helper reached only from message-10 arms, above) and from 0057C480's message-10 arm.
import struct as _st
def q(v): return _st.unpack("<Q", ds.rd(v, 8))[0]
refs29 = [v for v in range(0x00916000, 0x00917000, 8) if q(v) == 0x002A9980]
b393 = [s for a, s in ds.body["002B3930"]]
c393 = sorted(callers.get("002B3930", set()))
arm57 = arm_ids("0057C480", 0x0057C9B7)
ok("P4", not callers.get("002A9980") and not lea_taken.get("002A9980") and refs29 == [0x009164C0, 0x009164D8]
   and b393[:6] == ["movsx rax, byte ptr [rcx + 0xa3]", "lea rdx, [rax + rax*2]", "lea rax, [rip + 0x662b7d]", "mov rax, qword ptr [rax + rdx*8]", "test rax, rax", "je 0x2b394f"]
   and "jmp rax" in b393 and not lea_taken.get("002B3930") and [c for c, a in c393] == ["002A5CC0", "0057C480"] and arm57 == (10,)
   and only10(*HELP10["002A5CC0"]),
   "002A9980 is reached only by 002B3930's table jump (kinds 0 and 1 of 009164C0); 002B3930's callers: %s; 0057C480's call is in its message-%s arm" % ([c for c, a in c393], arm57))
unplaced = [f for f in readers if f not in set(M10) | {"0027AA70", "005519E0", "003CAB00", "002878E0", "002287D0", "00253C70", "002A9980"} | set(NEW_PROC10) | set(NEW_HELP10)
            | {"0023F240", "00240DE0", "00284EC0", "0029B870", "002A5CC0", "002A5F40", "0055C740"}]
print("T   placed %d of %d; not placed: %s" % (len(readers) - len(unplaced), len(readers), unplaced))
print("FAILS", fails); sys.exit(1 if fails else 0)
