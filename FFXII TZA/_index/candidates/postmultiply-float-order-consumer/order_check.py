"""order_check.py - 003977B0's first output is f32(f32(f32(p1 + p0) + p2) + p3) (FABLE, Claude Opus 5.5, 2026-09-28).
Static: binds the products and the add chain from the listing.
  O1  p1 = x4 * [rdx+4] into xmm2 (00397821); p0 = x7 * [rdx] into xmm0 (00397829); p2 = x5 * [rdx+8] into xmm1 (0039783F);
      p3 = x6 * [rdx+0xC] into xmm0 (0039784B)
  O2  the chain into xmm2: + xmm0 (p0) at 00397844, + xmm1 (p2) at 00397850, + xmm0 (p3) at 00397857, stored at 0039785E,
      with no other write to xmm2 in between
  C   control: the same check on a copy with the 00397850 and 00397857 adds swapped fails
"""
import os, re, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
ins = []
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3 and p[1] == "003977B0": ins.append((int(p[0], 16), p[2].split(" ;")[0]))
ins.sort()
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def chain(seq):
    """walk 00397810..0039785E: track which product each xmm holds, and the add order into xmm2"""
    held = {}; adds = []; src = {"xmm4": "x4", "xmm7": "x7", "xmm5": "x5", "xmm6": "x6"}
    prod = {"[rdx]": "p0", "[rdx + 4]": "p1", "[rdx + 8]": "p2", "[rdx + 0xc]": "p3"}
    for a, s in seq:
        if not (0x00397810 <= a <= 0x0039785E): continue
        m = re.match(r"movaps (xmm\d), (xmm\d)$", s)
        if m: held[m.group(1)] = src.get(m.group(2), held.get(m.group(2))); continue
        m = re.match(r"mulss (xmm\d), dword ptr (\[rdx(?: \+ 0x[0-9a-f]+| \+ \d+)?\])$", s)
        if m: held[m.group(1)] = (held.get(m.group(1)), prod.get(m.group(2))); continue
        m = re.match(r"addss xmm2, (xmm\d)$", s)
        if m:
            if not adds: adds.append(held["xmm2"])
            adds.append(held.get(m.group(1))); continue
        if s == "movss dword ptr [rax - 0x20], xmm2": return adds, a
        if re.match(r"\w+ xmm2,", s): return None, a
    return adds, None
adds, store = chain(ins)
want = [("x4", "p1"), ("x7", "p0"), ("x5", "p2"), ("x6", "p3")]
ok("O1+O2", adds == want and store == 0x0039785E, "first output: %s, stored at %s" % (adds, hex(store or 0)))
sw = dict(ins); a1, a2 = sw[0x00397850], sw[0x00397857]
mut = [(a, a2 if a == 0x00397850 else a1 if a == 0x00397857 else s) for a, s in ins]
madds, mstore = chain(mut)
ok("C", madds != want, "control: with the two late adds swapped the chain reads %s" % madds)
print("FAILS", fails); sys.exit(1 if fails else 0)
