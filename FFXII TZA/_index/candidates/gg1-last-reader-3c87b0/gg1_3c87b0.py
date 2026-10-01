"""gg1_3c87b0.py - GG-1's last reader, 003C87B0: where it runs relative to the arbiter's stores (FABLE, Claude Opus 5.5,
2026-09-28). Static.
  L1  003C87B0 reads 02F9736A at 003C889D and 003C88AD (bit tests 0x80 and 0x20)
  L2  its direct callers are the arbiter 00253C70 (00254044) and 00254B50; 00254B50's callers are the arbiter (002540D2,
      002541C7), the wrapper 00254B40 and 002E09A0 (002E0D0B)
  L3  inside the arbiter, every control-flow path into each of the three calls passes a store of di to 02F9736A first:
      00254044 after 00253FE9, 002540D2 after 002540C5, 002541C7 after 002541BC - so there it reads the value just stored
  L4  outside the arbiter it is reached through 00254B40 and 002E09A0, whose callers include widget procs' message-1, 12
      and 18 arms and non-proc roots; those paths are not placed here
  L5  in the world tick 00314020, the paths into its 002E09A0 call (0031427D) pass the arbiter call (00314137 or
      003141F2), or neither: on some ticks the reader runs with no arbiter in that tick
  C   control: the same backward walk from the arbiter's 002287D0 call (00253CCC) finds no store before it (entry), as
      ../gg1-helper-readers/ H2 established
"""
import os, re, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
body = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3: body[p[1]].append((int(p[0], 16), p[2]))
for f in body: body[f].sort()
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
reads = [a for a, s in body["003C87B0"] if "=>02F9736A" in s]
ok("L1", reads == [0x003C889D, 0x003C88AD], "reads %s" % ["%08X" % a for a in reads])
def callers(t): return sorted((f, a) for f, ins in body.items() for a, s in ins if re.match(r"(call|jmp) 0x%x$" % t, s))
c1 = callers(0x3C87B0); c2 = callers(0x254B50)
ok("L2", c1 == [("00253C70", 0x00254044), ("00254B50", 0x00254C0F)] and c2 == [("00253C70", 0x002540D2), ("00253C70", 0x002541C7), ("00254B40", 0x00254B45), ("002E09A0", 0x002E0D0B)],
   "003C87B0 <- %s; 00254B50 <- %s" % (["%s@%08X" % x for x in c1], ["%s@%08X" % x for x in c2]))
ins = body["00253C70"]; idx = {a: i for i, (a, s) in enumerate(ins)}
preds = collections.defaultdict(set)
for i, (a, s) in enumerate(ins):
    m = re.match(r"j\w+ 0x([0-9a-f]+)", s)
    if m and int(m.group(1), 16) in idx: preds[idx[int(m.group(1), 16)]].add(i)
    if not s.startswith(("jmp", "ret")) and i + 1 < len(ins): preds[i + 1].add(i)
def walk(site):
    seen = set(); st = list(preds[idx[site]]); out = set()
    while st:
        k = st.pop()
        if k in seen: continue
        seen.add(k); s = ins[k][1]
        if "=>02F9736A" in s and s.startswith("mov word ptr [rip") and s.split(";")[0].split(",")[1].strip() == "di": out.add("store@%08X" % ins[k][0]); continue
        if k == 0: out.add("entry"); continue
        st.extend(preds[k])
    return out
w = {s: walk(s) for s in (0x00254044, 0x002540D2, 0x002541C7)}
ok("L3", w == {0x00254044: {"store@00253FE9"}, 0x002540D2: {"store@002540C5"}, 0x002541C7: {"store@002541BC"}},
   "paths into the three arbiter calls: %s" % {"%08X" % k: sorted(v) for k, v in w.items()})
c3 = callers(0x254B40); c4 = callers(0x2E09A0)
ok("L4", len(c3) > 0 and ("00314020", 0x0031427D) in c4, "outside the arbiter: 00254B40 <- %d sites; 002E09A0 <- %s" % (len(c3), ["%s@%08X" % x for x in c4]))
tk = body["00314020"]; tidx = {a: i for i, (a, s) in enumerate(tk)}
tp = collections.defaultdict(set)
for i, (a, s) in enumerate(tk):
    m = re.match(r"j\w+ 0x([0-9a-f]+)", s)
    if m and int(m.group(1), 16) in tidx: tp[tidx[int(m.group(1), 16)]].add(i)
    if not s.startswith(("jmp", "ret")) and i + 1 < len(tk): tp[i + 1].add(i)
seen = set(); st = list(tp[tidx[0x0031427D]]); tout = set()
while st:
    k = st.pop()
    if k in seen: continue
    seen.add(k); s = tk[k][1]
    if s.startswith("call 0x2e0d90"): tout.add("arbiter-call@%08X" % tk[k][0]); continue
    if k == 0: tout.add("entry"); continue
    st.extend(tp[k])
ok("L5", tout == {"arbiter-call@00314137", "arbiter-call@003141F2", "entry"},
   "world tick: paths into 0031427D pass the arbiter call at 00314137 or 003141F2, or neither (%s)" % sorted(tout))
ok("C", walk(0x00253CCC) == {"entry"}, "control: no store precedes the arbiter's 002287D0 call at 00253CCC")
print("FAILS", fails); sys.exit(1 if fails else 0)
