"""ao4_families.py - AO-4: what the script command families 3, 5 and 7 contain (FABLE, Claude Opus 5.5, 2026-09-27).
Static. Records are 0x20 bytes at table + 8 + 0x20*n: begin +0, poll +8, result +0x18 (the dispatch-table page).

  F1 family 7's 104 records join the authored catalogue one to one, and its names fall in five prefixes: fsmenu_ (55),
     fs_ (6: the stone and food windows, fs_setclanrank, fs_reloadmrp), fsroll_ (31), fsttl_ (11) and unkCall_7067.
  F2 each prefix runs on its own native cluster: every staff-roll (fsroll_) handler reaches only 0053D000-0053F800 and
     the inert stubs; every title (fsttl_) handler and 7067 only the title singleton's 00394000-00394700 and the stubs;
     no fsmenu_ / fs_ handler reaches either range. Positive controls: fsroll_start -> 0053F460, fsttl_newgamestart ->
     00394640, fsmenu_openmenu -> 002D75F0.
  F3 the staff roll is a list of typed lines: fifteen fsroll_ verbs, and nothing else (a raw rel32 sweep of .text finds
     exactly their 15 call sites), append through the one appender 0053F0D0, which
     reads the singleton 02CA8A80, accepts kinds 1-14 only, caps the list at 0x800 entries (+0xC8) of 0x20 bytes (+0xC0),
     and the fixed-kind verbs pass speed 1, linedisp 2, layout 3, blank 4, nameA/B/C 5 (column 0/1/2), data 6, stop 7,
     fontA/B/C 8/9/10, setend 11, moviewait 14; fsroll_setparam passes a popped kind.
  F4 the inert records: fs_setclanrank, fsroll_setcounternow and fsroll_setdouble pop their operands and jump to the
     ret-0 stub 0016D6A0; fsroll_getcounternow / getcountermax share 0050F100, which returns 005C5230's constant 0;
     fsroll_getdouble returns 0053DD10's constant 1; fs_reloadmrp's begin is the stub and its poll reports "done" at
     once (0053DD10 = 1, so sete -> 0).
  F5 family 5 is one record identical to family 7's record 0 (begin 003567F0, poll 005114F0, no result).
  F6 family 3's catalogue is the battle-actor set: of its 147 records, 140 are catalogued, 133 of them btl* names
     (btlAtel* 121, btlGet* 6, btlSet* 6) and 7 unkCall_*.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a): return list(cs.disasm(d[off(a):off(a) + SIZES.get(a, 0x60)], a))
def callees(a):
    return {int(x.op_str, 16) for x in ins(a) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")
            and not (a <= int(x.op_str, 16) < a + SIZES.get(a, 0x60))}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
CAT = {}
for l in open(ROOT / "Collaboration/tools/ffxii/ff12-script-master/ff12-script/CScriptContainerInitializers.cpp", encoding="utf-8", errors="replace"):
    m = re.search(r"\{ 0x([0-9a-f]{4}), \{ L\"(\w+)\"", l)
    if m: CAT[int(m.group(1), 16)] = m.group(2)
def recs(base, count): return [struct.unpack_from("<QQQQ", d, off(base) + 8 + 32 * i) for i in range(count)]
F7 = recs(0x1F29440, 104)
names7 = [CAT.get(0x7000 + i) for i in range(104)]
def pref(nm):
    for p in ("fsmenu_", "fsroll_", "fsttl_", "fs_", "unkCall_"):
        if nm.startswith(p): return p
cnt = {p: sum(pref(nm) == p for nm in names7) for p in ("fsmenu_", "fs_", "fsroll_", "fsttl_", "unkCall_")}
check("F1 family 7: 104 records, 104 catalogue names, prefixes fsmenu_ 55 / fs_ 6 / fsroll_ 31 / fsttl_ 11 / unkCall 1",
      None not in names7 and max(k for k in CAT if k >> 12 == 7) == 0x7067
      and cnt == {"fsmenu_": 55, "fs_": 6, "fsroll_": 31, "fsttl_": 11, "unkCall_": 1}, str(cnt))

HELP = {0x267DB0, 0x267E10, 0x26B4E0, 0x16D6A0, 0x5C5230, 0x53DD10, 0x280120}
ROLL = range(0x53D000, 0x53F800); TTL = range(0x394000, 0x394700)
bad = []; reach = {}
for i, (b, p, _u, r) in enumerate(F7):
    c = set()
    for h in (b, p, r):
        if not h: continue
        c |= callees(h)
        for t in list(callees(h)):
            if t not in HELP and t not in ROLL and t not in TTL and SIZES.get(t, 999) <= 8: c |= callees(t)
    c -= HELP; reach[i] = c
    k = pref(names7[i])
    if k == "fsroll_" and not all(t in ROLL for t in c): bad.append(names7[i])
    if (k == "fsttl_" or i == 0x67) and not all(t in TTL for t in c): bad.append(names7[i])
    if k in ("fsmenu_", "fs_") and any(t in ROLL or t in TTL for t in c): bad.append(names7[i])
check("F2 staff-roll handlers reach only 0053D000-0053F800, title handlers only 00394000-00394700, menu/window handlers neither",
      bad == [] and 0x53F460 in reach[0x3E] and 0x394640 in reach[0x5D] and 0x2D75F0 in reach[0x02], "violations %s" % bad)

ap = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in ins(0x53F0D0)}
kinds = {}
for i, (b, p, _u, r) in enumerate(F7):
    if not r: continue
    L = ins(r); e = None; edx = 0
    for x in L:
        s = "%s %s" % (x.mnemonic, x.op_str)
        mm = re.fullmatch(r"mov edx, (0x[0-9a-f]+|\d+)", s)
        if mm: edx = int(mm.group(1), 0)
        if s in ("xor edx, edx", "xor r8d, r8d"): edx = 0
        m = re.fullmatch(r"(?:mov ecx, (0x[0-9a-f]+|\d+)|lea ecx, \[(?:rdx|r8|rax) \+ (0x[0-9a-f]+|\d+)\])", s)
        if m: e = int(m.group(1) or m.group(2), 0) + (edx if "rdx" in s else 0)
        if s == "mov ecx, eax": e = "popped"
        if x.mnemonic in ("call", "jmp") and x.op_str == "0x53f0d0": kinds[names7[i]] = e
WANT = {"fsroll_setparam": "popped", "fsroll_speed": 1, "fsroll_linedisp": 2, "fsroll_layout": 3, "fsroll_blank": 4,
        "fsroll_nameA": 5, "fsroll_nameB": 5, "fsroll_nameC": 5, "fsroll_data": 6, "fsroll_stop": 7, "fsroll_fontA": 8,
        "fsroll_fontB": 9, "fsroll_fontC": 10, "fsroll_setend": 11, "fsroll_moviewait": 14}
cols = [struct.unpack_from("<i", d, off(a) + 1)[0] if d[off(a)] == 0xBA else 0 for a in (0x5119AC, 0x5119FC)]
text = [(BASE + va, ro, rs) for vs, va, rs, ro in secs if va == 0x1000][0]
tb = d[text[1]:text[1] + text[2]]
sites = [text[0] + i for i in range(len(tb) - 5) if tb[i] in (0xE8, 0xE9)
         and text[0] + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == 0x53F0D0]
roll_res = {F7[idx][3] for idx in range(104) if names7[idx] in WANT}
owners = {max(h for h in roll_res if h <= s) for s in sites}
check("F3 one appender: singleton 02CA8A80, kinds 1-14, 0x800 x 0x20-byte lines; the fixed-kind verbs' kinds; its only callers (raw rel32) are those 15 verbs",
      len(sites) == 15 and owners == roll_res and all(s - max(h for h in roll_res if h <= s) < 0x60 for s in sites) and
      ap.get(0x53F0D6) == "mov rbx, qword ptr [rip + 0x27699a3]" and 0x53F0DD + 0x27699A3 == 0x2CA8A80
      and ap.get(0x53F10D) == "lea eax, [rcx - 1]" and ap.get(0x53F110) == "cmp eax, 0xd"
      and ap.get(0x53F0FD) == "cmp r10d, 0x800" and ap.get(0x53F0F6) == "movsxd r10, dword ptr [rbx + 0xc8]"
      and ap.get(0x53F1BF) == "shl rcx, 5" and ap.get(0x53F1C6) == "add rcx, qword ptr [rbx + 0xc0]"
      and kinds == WANT and cols == [1, 2], "%s cols %s" % (kinds, cols))

stub = d[off(0x16D6A0):off(0x16D6A0) + 3] == b"\xc2\x00\x00"
zero = d[off(0x5C5230):off(0x5C5230) + 3] == b"\x33\xc0\xc3"
one = d[off(0x53DD10):off(0x53DD10) + 6] == b"\xb8\x01\x00\x00\x00\xc3"
def only(a, want): return callees(a) == want
idx = {nm: i for i, nm in enumerate(names7)}
R = lambda nm: F7[idx[nm]][3]
rl = F7[idx["fs_reloadmrp"]]
pl = {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in ins(rl[1])}
check("F4 the inert records: three setters end in the ret-0 stub, the counters read constant 0, getdouble constant 1, reloadmrp does nothing",
      stub and zero and one
      and only(R("fs_setclanrank"), {0x267E10, 0x16D6A0}) and R("fsroll_setcounternow") == R("fsroll_setdouble")
      and only(R("fsroll_setdouble"), {0x267E10, 0x16D6A0})
      and R("fsroll_getcounternow") == R("fsroll_getcountermax") == 0x50F100 and only(0x50F100, {0x5C5230, 0x26B4E0})
      and only(R("fsroll_getdouble"), {0x53DD10, 0x26B4E0})
      and rl[0] == 0x17E7D0 and d[off(0x17E7D0)] == 0xE9 and only(0x17E7D0, {0x16D6A0}) and rl[3] == 0
      and pl.get(0x512164) == "call 0x53dd10" and pl.get(0x51216D) == "sete cl")
F5 = recs(0x1F29418, 1)[0]
check("F5 family 5's one record is family 7's record 0",
      F5[:2] == F7[0][:2] == (0x3567F0, 0x5114F0) and F5[3] == F7[0][3] == 0)
names3 = [CAT.get(0x3000 + i) for i in range(147)]
got = [nm for nm in names3 if nm]
btl = [nm for nm in got if nm.startswith("btl")]
check("F6 family 3: 140 of 147 records catalogued, 133 btl* (btlAtel 121, btlGet 6, btlSet 6) and 7 unkCall",
      len(got) == 140 and len(btl) == 133 and sum(nm.startswith("btlAtel") for nm in btl) == 121
      and sum(nm.startswith("btlGet") for nm in btl) == 6 and sum(nm.startswith("btlSet") for nm in btl) == 6
      and sum(nm.startswith("unkCall_") for nm in got) == 7)
print("FAILS", fails)
sys.exit(1 if fails else 0)
