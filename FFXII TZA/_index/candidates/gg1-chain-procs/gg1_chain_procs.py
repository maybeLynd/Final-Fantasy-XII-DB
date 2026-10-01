"""gg1_chain_procs.py - GG-1: extended dispatch decode (FABLE, Claude Opus 5.5, 2026-09-28) - - jump tables through any 32-bit register (r8d etc.) and sub/cmp je chains
(cumulative id). Maps each read of 02F9736A to the message ids of its arm (FABLE, 2026-09-28)."""
import re, struct, collections, sys, os
sys.argv = [sys.argv[0]]
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "../gg1-message10-readers/gg1_msg10_readers.py"), encoding="utf-8").read().split("def decode")[0])
FIRST = {}
exec(open(os.path.join(HERE, "../gg1-message10-readers/gg1_msg10_readers.py"), encoding="utf-8").read().split("def is_read")[0].split("for f in body: body[f].sort()")[1], FIRST)
R32 = r"(?:e\w+|r\d+d)"
def decode_table(ins, j):
    win = [s for a, s in ins[:j + 1]]
    k = 0; bound = btab = dtab = None
    for s in win:
        m = re.match(r"(dec|inc) %s$" % R32, s)
        if m: k += 1 if m.group(1) == "dec" else -1
        m = re.match(r"(sub|add) %s, (-?0x[0-9a-f]+|\d+)$" % R32, s)
        if m and bound is None: k += int(m.group(2), 0) if m.group(1) == "sub" else -int(m.group(2), 0)
        m = re.match(r"cmp %s, (0x[0-9a-f]+|\d+)$" % R32, s)
        if m: bound = int(m.group(1), 0)
        m = re.match(r"movzx %s, byte ptr \[r\w+ \+ r\w+ \+ (0x[0-9a-f]+)\]$" % R32, s)
        if m: btab = int(m.group(1), 16)
        m = re.match(r"mov %s, dword ptr \[r\w+ \+ r\w+\*4 \+ (0x[0-9a-f]+)\]$" % R32, s)
        if m: dtab = int(m.group(1), 16)
    if bound is None or dtab is None or bound > 400: return None
    arms = {}
    for idx in range(bound + 1):
        b = rd(0x120000 + btab + idx, 1)[0] if btab is not None else idx
        arms[idx + k] = 0x120000 + struct.unpack_from("<I", rd(0x120000 + dtab + 4 * b, 4))[0]
    return arms
def decode_chain(ins):
    # id register loaded from dword [rdx]; then sub/je and cmp/je|jne sequences
    i0 = next((i for i, (a, s) in enumerate(ins[:40]) if re.match(r"mov (%s), dword ptr \[rdx\]$" % R32, s)), None)
    if i0 is None: return None
    reg = re.match(r"mov (%s), dword ptr \[rdx\]$" % R32, ins[i0][1]).group(1)
    cum = 0; arms = {}; i = i0 + 1
    while i < len(ins) and i < i0 + 60:
        a, s = ins[i]
        m = re.match(r"sub %s, (0x[0-9a-f]+|\d+)$" % reg, s)
        if m:
            cum += int(m.group(1), 0); i += 1
            if i < len(ins):
                m2 = re.match(r"je 0x([0-9a-f]+)$", ins[i][1])
                if m2: arms[cum] = int(m2.group(1), 16); i += 1
            continue
        m = re.match(r"(?:dec) %s$" % reg, s)
        if m:
            cum += 1; i += 1
            if i < len(ins):
                m2 = re.match(r"je 0x([0-9a-f]+)$", ins[i][1])
                if m2: arms[cum] = int(m2.group(1), 16); i += 1
            continue
        m = re.match(r"cmp %s, (0x[0-9a-f]+|\d+)$" % reg, s)
        if m and i + 1 < len(ins):
            v = cum + int(m.group(1), 0); nxt = ins[i + 1][1]
            m2 = re.match(r"(je|jne) 0x([0-9a-f]+)$", nxt)
            if m2 and m2.group(1) == "je": arms[v] = int(m2.group(2), 16); i += 2; continue
            if m2 and m2.group(1) == "jne" and i + 2 < len(ins): arms[v] = ins[i + 2][0]; i += 2; break
            break
        if re.match(r"test %s, %s$" % (reg, reg), s) and i + 1 < len(ins):
            m2 = re.match(r"je 0x([0-9a-f]+)$", ins[i + 1][1])
            if m2: arms[cum] = int(m2.group(1), 16); i += 2; continue
        if s.startswith(("j", "call", "ret")) or re.match(r"mov %s," % reg, s): break
        i += 1
    return arms if len(arms) >= 2 else None
def arms_of(f):
    ins = body[f]
    j = next((i for i, (a, s) in enumerate(ins) if re.match(r"jmp r\w+$", s)), None)
    if j is not None and j <= 60 and any(re.match(r"mov %s, dword ptr \[rdx\]$" % R32, s) for a, s in ins[:j + 1]):
        t = decode_table(ins, j)
        if t: return "table", t
    c = decode_chain(ins)
    return ("chain", c) if c else (None, None)
def is_read(s): return "=>02F9736A" in s and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0])

readers = sorted(f for f, ins in body.items() if any(is_read(s) for a, s in ins))
place = {}
for f in readers:
    kind, arms = arms_of(f)
    if not arms: continue
    starts = sorted(set(arms.values())); ids = set()
    for a, s in body[f]:
        if is_read(s):
            arm = max((t for t in starts if t <= a), default=None)
            ids.add(tuple(sorted(m for m, t in arms.items() if t == arm)) if arm else ("pre",))
    place[f] = (kind, sorted(ids))
FIRST16 = ["00228C70", "0023BD40", "0023CE10", "00241D40", "002778C0", "00280DE0", "002A6190", "002D5EB0", "00552250", "005528C0", "005542D0", "00560910", "00571A50", "00572E10", "005742D0", "0057AC10"]
new10 = sorted(f for f, (k, ids) in place.items() if f not in FIRST16 and ids and all(10 in i and set(i) <= {10, 11} for i in ids))
msg2 = sorted(f for f, (k, ids) in place.items() if ids == [(2,)])
ok("D1", len(new10) >= 10, "%d more readers read only in a message-10 arm: %s" % (len(new10), new10))
snd2 = sorted({f for f, ins in body.items() for a, s in ins if s == "call 0x248030"})
ok("D2", msg2 and "002284F0" in snd2, "message-2 readers %s NOT placed: the reconcile sender 00248030 is also called by 002284F0, not a frame position (callers %s)" % (msg2, snd2))
ok("C1", all(place.get(f, (None, []))[1] and all(10 in i for i in place[f][1]) for f in FIRST16), "control: the extended decoder agrees with the first on its 16 message-10 readers")
k, a = arms_of("0023B6F0")
ok("C2", k == "chain" and a.get(1) == 0x0023BA11 and a.get(4) == 0x0023B8EA and a.get(10) == 0x0023B818 and a.get(12) == 0x0023B7E7 and a.get(13) == 0x0023B73E,
   "control: the chain decode of 0023B6F0 matches its head (1, 4, 10, 12 by sub/je; 13 by cmp/jne fall-through)")
print("FAILS", fails); sys.exit(1 if fails else 0)
