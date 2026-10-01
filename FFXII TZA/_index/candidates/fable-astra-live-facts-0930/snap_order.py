# snap_order.py - place the readers of the newly-pressed snapshot word 02F9736A against the arbiter 00253C70, statically.
# Readers: every rip-relative operand that addresses 02F9736A (any width covering it: 02F97368..02F9736B word/dword, and
# qword/xmm loads from 02F97360..), found by scanning each listed function. For each reader function, a reverse BFS over
# DIRECT calls (E8/E9 raw index) up to the three frame bodies records which frame-body call site(s) reach it.
# Order per frame body is by call-site address (the bodies are straight-line at these sites per gg1-static-order O3/O4).
# Readers not reached from a frame body by direct calls are UNRESOLVED (indirect dispatch) - they stay for observation.
# Controls: the battle command menu reader 00277ACD (in 002778C0, reached only through a widget proc = indirect) must come
# out UNRESOLVED by direct calls; the arbiter 00253C70 itself must be reached from 00314020 (world tick).
import os, re, json, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False
TARGET = 0x02F9736A
FRAMES = {0x0022A770: "field", 0x0022B8C0: "full-menu", 0x0022BC20: "capture"}
TICK = 0x00314020
WIDTH = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}

readers = collections.defaultdict(list)
for fn, size in sorted(funcs.items()):
    o = off(fn)
    if o is None or size > 0x10000:
        continue
    for i in md.disasm(bytes(d[o:o + size]), fn):
        m = re.search(r"(byte|word|dword|qword|xmmword) ptr \[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
        if not m:
            continue
        disp = int(m.group(3), 16) * (1 if m.group(2) == "+" else -1)
        ea = i.address + i.size + disp
        w = WIDTH[m.group(1)]
        if ea <= TARGET < ea + w:
            dst = i.op_str.split(",")[0]
            if "rip" in dst and i.mnemonic.startswith("mov"):
                kind = "write"
            else:
                kind = "read"
            readers[fn].append((i.address, kind, i.mnemonic, i.op_str))

raw = json.load(open("tools/rawcalls.json"))
callers = collections.defaultdict(set)  # callee -> set of (site, owner)
fl = sorted(funcs)
import bisect
def owner(a):
    k = bisect.bisect_right(fl, a) - 1
    return fl[k] if k >= 0 and a < fl[k] + funcs[fl[k]] else None
for tgt, sites in raw.items():
    t = int(tgt, 16)
    for s in sites:
        s = int(s, 16)
        ow = owner(s)
        if ow is not None:
            callers[t].add((s, ow))

def frame_sites(fn, maxdepth=12):
    """(frame, site) pairs through which fn is reached by direct calls; and whether the path passes the world tick."""
    out = set()
    seen = {fn}
    q = collections.deque([(fn, 0, False)])
    while q:
        f, dpt, via_tick = q.popleft()
        if dpt > maxdepth:
            continue
        for s, ow in callers.get(f, ()):
            vt = via_tick or f == TICK
            if ow in FRAMES:
                out.add((FRAMES[ow], s, vt))
                continue
            if ow not in seen:
                seen.add(ow)
                q.append((ow, dpt + 1, vt))
    return out

nread = sum(1 for f in readers for r in readers[f] if r[1] == "read")
nwrite = sum(1 for f in readers for r in readers[f] if r[1] == "write")
print("reader sites %d, writer sites %d, functions %d" % (nread, nwrite, len(readers)))
tick_sites = {fr: sorted(s for s, ow in callers[TICK] if ow == f) for f, fr in FRAMES.items()}
print("world tick call sites per frame:", {k: ["%08X" % s for s in v] for k, v in tick_sites.items()})
print("CONTROL arbiter reached:", sorted(("%s %08X tick=%s" % (a, b, c)) for a, b, c in frame_sites(0x00253C70))[:6])
print("CONTROL 002778C0 (widget proc):", sorted(frame_sites(0x002778C0)) or "UNRESOLVED")
for fn in sorted(readers):
    rs = [r for r in readers[fn] if r[1] == "read"]
    if not rs:
        continue
    fsites = frame_sites(fn)
    pos = []
    for fr, s, vt in sorted(fsites):
        ts = tick_sites.get(fr, [])
        if vt:
            rel = "INSIDE-TICK"
        elif not ts:
            rel = "no-tick-in-frame"
        elif all(s < t for t in ts):
            rel = "before-tick"
        elif all(s > t for t in ts):
            rel = "after-tick"
        else:
            rel = "between-ticks"
        pos.append("%s@%08X:%s" % (fr, s, rel))
    print("%08X  reads %s  | %s" % (fn, ",".join("%08X" % r[0] for r in rs), "; ".join(pos) if pos else "UNRESOLVED (no direct path to a frame body)"))
