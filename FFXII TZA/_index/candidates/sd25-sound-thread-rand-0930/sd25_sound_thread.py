"""sd25_sound_thread.py - which thread runs the Sound selects, and does it share rand() with gameplay? (OPUS, 2026-09-30;
register SD-25). Asserts each fact over the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py.
Prints PASS/FAIL per fact and `FAILS n` last.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
calls = c["calls"]
fails = 0
RAND_IAT, BEGINTHREADEX_IAT = 0x008C3098, 0x008C2D70


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


fwd = {}
for callee, sites in calls.items():
    for f, _ in sites:
        fwd.setdefault(f, set()).add(callee)


def closure(root):
    seen, st = {root}, [root]
    while st:
        for y in fwd.get(st.pop(), ()):
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def ancestors(t):
    seen, st, roots = {t}, [t], set()
    while st:
        x = st.pop()
        cs = set(f for f, _ in calls.get(x, ()))
        if not cs:
            roots.add(x)
        for f in cs:
            if f not in seen:
                seen.add(f)
                st.append(f)
    return roots


# F1 - the stepper's callers climb (direct calls) to three roots: 007A5400 and two virtual methods
roots = ancestors(0x007BD120)
check("F1", roots == {0x007A5400, 0x007E6620, 0x007E9AE0},
      "roots above the stepper 007BD120: %s (007E6620 = CycleSound slot 42, 007E9AE0 = SoundTrack slot 13)" % sorted("%08X" % r for r in roots))
# F2 - 007A5400 runs on a thread: 007A4D50 stores it at [02EACF78] (the thread argument 02EACF70 + 8) and starts
#      _beginthreadex with start routine 007A5550, which calls [arg + 8]
seq = [ins(a) for a in (0x007A51EC, 0x007A51F7, 0x007A51FE, 0x007A5205, 0x007A5232)]
proc = [ins(a) for a in (0x007A5554, 0x007A5557, 0x007A555B)]
check("F2", seq[0].op_str.startswith("rax, [rip") and seq[1].op_str.startswith("r9, [rip") and seq[2].op_str.endswith("rax")
      and seq[3].op_str.startswith("r8, [rip") and seq[4].mnemonic == "call"
      and seq[4].address + seq[4].size + seq[4].operands[0].mem.disp == BEGINTHREADEX_IAT
      and proc[0].op_str == "rax, rcx" and proc[2].op_str == "qword ptr [rax + 8]",
      "_beginthreadex(start 007A5550, arg 02EACF70) at 007A5232; [02EACF78] = 007A5400; 007A5550 calls [arg + 8]")
# F3 - the stepper and its caller 007BDFA0 are in that thread's direct-call closure; the rand() callers in it are
#      audio-module functions only, none of the gameplay callers
thr = closure(0x007A5400)
rc = sorted(set(f for f, a, k in c["refs"].get(RAND_IAT, ())))
inside = [f for f in rc if f in thr]
check("F3", 0x007BD120 in thr and 0x007BDFA0 in thr and inside and all(0x007A0000 <= f < 0x00800000 for f in inside),
      "rand callers %d; inside the sound thread's closure (%d functions): %s; outside: %d"
      % (len(rc), len(thr), ["%08X" % f for f in inside], len(rc) - len(inside)))
print("FAILS %d" % fails)
