"""gg1_msg10_readers.py - GG-1 extended: which readers of 02F9736A read it in a widget focus-input (message 10/11) arm,
and that message 10/11 has one sender (FABLE, Claude Opus 5.5, 2026-09-28). Static; companion to ../gg1-static-order/.

  M1  a generic MSVC jump-table decode (message id = dword [rdx], minus the dec/sub bias, bounded by cmp, optional byte
      index table, dword offset table off the image base) for every reader: the arm that holds each read
  M2  the readers whose reads all sit in a message-10 or message-10/11 arm (the placement ../gg1-static-order/ derived
      for 002778C0 then applies to each of them)
  M3  message 10/11's only sender: the .rdata records 009150D8 {10} / 009150F0 {11} are referenced only by 002481C0,
      and the one stack-built {10} passed in rdx (0057F6B0 -> 00582540) goes into an event queue, not to a widget
      handler (00582540 copies a 0x58-byte record into an 8-slot array)
  C1  control: the decoder reproduces 002778C0's table (message 1 -> 00277925, messages 10 and 11 -> 00277A64)
  C2  control for M3's census: the same stack-record scan finds the one known stack {10} at 0057F72B
Undecoded readers (cmp chains, direct frame callees, other shapes) are listed, not placed.
"""
import os, re, struct, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, vs, ra, rs)); o += 40
def rd(va, n):
    r = va - 0x120000
    for sva, vs, ra, rs in secs:
        if sva <= r < sva + rs: return d[ra + r - sva: ra + r - sva + n]
body = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3: body[p[1]].append((int(p[0], 16), p[2]))
for f in body: body[f].sort()
def decode(f):
    ins = body[f]
    j = next((i for i, (a, s) in enumerate(ins) if re.match(r"jmp r\w+$", s)), None)
    if j is None or j > 60: return None
    win = [s for a, s in ins[:j + 1]]
    if not any(re.match(r"mov e\w+, dword ptr \[rdx\]$", s) for s in win): return None
    k = 0; bound = btab = dtab = None
    for s in win:
        m = re.match(r"(dec|inc) e\w+$", s)
        if m: k += 1 if m.group(1) == "dec" else -1
        m = re.match(r"(sub|add) e\w+, (-?0x[0-9a-f]+|\d+)$", s)
        if m and bound is None: k += int(m.group(2), 0) if m.group(1) == "sub" else -int(m.group(2), 0)
        m = re.match(r"cmp e\w+, (0x[0-9a-f]+|\d+)$", s)
        if m: bound = int(m.group(1), 0)
        m = re.match(r"movzx e\w+, byte ptr \[r\w+ \+ r\w+ \+ (0x[0-9a-f]+)\]$", s)
        if m: btab = int(m.group(1), 16)
        m = re.match(r"mov e\w+, dword ptr \[r\w+ \+ r\w+\*4 \+ (0x[0-9a-f]+)\]$", s)
        if m: dtab = int(m.group(1), 16)
    if bound is None or dtab is None or bound > 400: return None
    arms = {}
    for idx in range(bound + 1):
        b = rd(0x120000 + btab + idx, 1)[0] if btab is not None else idx
        arms[idx + k] = 0x120000 + struct.unpack_from("<I", rd(0x120000 + dtab + 4 * b, 4))[0]
    return arms
def is_read(s): return "=>02F9736A" in s and not (s.startswith("mov") and "ptr [rip" in s.split(",")[0])
readers = sorted(f for f, ins in body.items() if any(is_read(s) for a, s in ins))
placed, other_arm, undecoded = {}, {}, []
for f in readers:
    arms = decode(f)
    if not arms: undecoded.append(f); continue
    starts = sorted(set(arms.values()))
    ids_per_read = []
    for a, s in body[f]:
        if is_read(s):
            arm = max((t for t in starts if t <= a), default=None)
            ids_per_read.append(tuple(sorted(m for m, t in arms.items() if t == arm)) if arm else ())
    if ids_per_read and all(set(ids) <= {10, 11} and 10 in ids for ids in ids_per_read): placed[f] = sorted(set(ids_per_read))
    else: other_arm[f] = sorted(set(ids_per_read))
ok("M1", len(readers) >= 50 and len(placed) + len(other_arm) >= 15, "%d readers; %d decoded (%d undecoded)" % (len(readers), len(placed) + len(other_arm), len(undecoded)))
ok("M2", len(placed) >= 10, "%d readers read only in a message-10 (or 10/11) arm: %s" % (len(placed), sorted(placed)))
print("     other arms: %s" % {f: v for f, v in other_arm.items()})
refs10 = [(f, a) for f, ins in body.items() for a, s in ins if "=>009150D8" in s]
refs11 = [(f, a) for f, ins in body.items() for a, s in ins if "=>009150F0" in s]
stack10 = []
for f, ins in body.items():
    for i, (a, s) in enumerate(ins):
        m = re.match(r"mov dword ptr \[rsp \+ (0x[0-9a-f]+)\], 0xa$", s)
        if m and any(re.match(r"lea rdx, \[rsp \+ %s\]$" % m.group(1), s2) for a2, s2 in ins[i + 1:i + 14]): stack10.append((f, "%08X" % a))
q = [s for a, s in body["00582540"]]
ok("M3", [f for f, a in refs10] == ["002481C0"] and [f for f, a in refs11] == ["002481C0"] and stack10 == [("0057F6B0", "0057F72B")]
   and any("movups xmmword ptr [rcx + rbx + 0xd8], xmm0" == s for s in q),
   "{10}/{11} records referenced only by 002481C0; the one stack {10} in rdx (0057F6B0) goes to the event-queue copy 00582540")
a02 = decode("002778C0")
ok("C1", a02 and a02[1] == 0x00277925 and a02[10] == a02[11] == 0x00277A64, "control: 002778C0 decodes to message 1 -> 00277925, 10/11 -> 00277A64")
ok("C2", ("0057F6B0", "0057F72B") in stack10, "control: the stack scan finds the known stack {10} at 0057F72B")
print("undecoded (not placed): %s" % undecoded)
print("FAILS", fails); sys.exit(1 if fails else 0)
