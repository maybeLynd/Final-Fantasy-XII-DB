"""save_order.py - Save (0036D930) writes each pointer record before it loads that target (FABLE, Claude Opus 5.5,
2026-09-28). Static, from the listing.
  S1  inside the loop: mov [r8], rax at 0036D969 precedes movups xmm0, [rax] at 0036D974, which precedes the value store
      movups [r9 - 0x10], xmm0 at 0036D977; r8 walks 02EC0A00 (pointer records), r9 walks 02EC0800 (values)
  C   control: the same order test on a copy with the record store moved after the load is refused
"""
import os, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
ins = sorted((int(p[0], 16), p[2]) for p in (l.rstrip("\n").split(None, 2) for l in open(CACHE, encoding="utf-8", errors="replace")) if len(p) == 3 and p[1] == "0036D930")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def order(seq):
    pos = {}
    for k, (a, s) in enumerate(seq):
        s = s.split(" ;")[0]
        if s == "mov qword ptr [r8], rax": pos["record"] = k
        if s == "movups xmm0, xmmword ptr [rax]": pos["load"] = k
        if s == "movups xmmword ptr [r9 - 0x10], xmm0": pos["save"] = k
    return len(pos) == 3 and pos["record"] < pos["load"] < pos["save"]
bases = [s for a, s in ins if "=>02EC0A00" in s or "=>02EC0800" in s]
ok("S1", order(ins) and dict(ins).get(0x0036D969, "").startswith("mov qword ptr [r8], rax") and len(bases) == 2,
   "record 0036D969 < load 0036D974 < value store 0036D977; bases %s" % [b.split("; ")[-1] for b in bases])
k1 = next(k for k, (a, s) in enumerate(ins) if s.startswith("mov qword ptr [r8], rax")); k2 = next(k for k, (a, s) in enumerate(ins) if s.startswith("movups xmm0"))
mut = ins[:k1] + ins[k1 + 1:k2 + 1] + [ins[k1]] + ins[k2 + 1:]
ok("C", not order(mut), "control: with the record store after the load, the order test refuses")
print("FAILS", fails); sys.exit(1 if fails else 0)
