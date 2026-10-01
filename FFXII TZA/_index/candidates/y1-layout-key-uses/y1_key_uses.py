"""y1_key_uses.py - Y-1: what each UISize layout key positions (FABLE, Claude Opus 5.5, 2026-09-27). Static.

y1-layout-key-uses.tsv gives, per (key, reader) pair of the page's layout-key-readers.tsv, every read site and what the
value is used for. This control checks what the bytes decide:
  K1 the rows are exactly the 335 (key, reader) pairs of members/layout-key-readers.tsv (the join corrected 2026-09-27:
     226 keys bound, 213 with a reader).
  K2 per row, the site list equals every instruction in the reader that reads the key's global by rip (a mov whose
     destination is the global is a write and is not listed; 0028B24A is one).
  K3 per row, no invented address: every 8-hex address the use column cites (outside parentheses) is a function entry
     in functions.tsv, a real instruction start inside the listed function containing it, or a global some instruction
     in the image references by rip. Control: 00562C54 (WorldMapLineScale's read) passes and 00562C55, one byte into it
     (the address an earlier draft cited), fails.
  K4 the 13 keys with no reader have none by any route: no rip operand outside their slot's installer, no image-base-relative
     operand ([reg + global - 0x120000]) and no qword load of their pointer slot other than by the installer that stores it:
     settings +0x3B00 + slot for the 12 int keys (installer 001AF470), 001B5FB0()'s object + slot for FontShadowAlphaMuti
     (installer 001B44A0; that slot is looked for only in functions that call 001B5FB0 or load its singleton 01F81200, and
     001CA600's own load of it is the store of the key's value). Positive control: every one of the 213 read keys has a rip reader.
  K5 the 2026-09-27 correction of FABLE's 09-13 key -> global join holds in the bytes (223 int + 3 float reads; the float
     keys go through 001B5FB0()'s object, filled by 001B44A0; 01E0CDA8 is MessageWinMaskBottom's) and in the members table.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
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
DIS = {}
def ins(f):
    if f not in DIS:
        o = off(f); DIS[f] = list(cs.disasm(d[o:o + SIZES.get(f, 0x200)], f)) if o is not None and SIZES.get(f, 0) > 0 else []
    return DIS[f]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
def ript(x):
    m = RIP.search(x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
M = DB / "16-UI/Layout-Parameter-System/members"
pairs = [(r["key"], r["reader"].upper()) for r in csv.DictReader(open(M / "layout-key-readers.tsv", encoding="utf-8"), delimiter="\t")]
rows = list(csv.DictReader(open(HERE / "y1-layout-key-uses.tsv", encoding="utf-8"), delimiter="\t"))
got = [(r["key"], r["reader"].upper()) for r in rows]
check("K1 the rows are exactly the 335 key/reader pairs", sorted(got) == sorted(pairs) and len(got) == 335, "rows %d" % len(got))

import bisect
FS = sorted(SIZES)
def boundary(c):
    """c is a real instruction start inside the listed function that contains it"""
    i = bisect.bisect_right(FS, c) - 1
    return i >= 0 and FS[i] <= c < FS[i] + SIZES[FS[i]] and any(x.address == c for x in ins(FS[i]))
b2 = []; b3 = []
ALLRIP = set()
for f0 in SIZES:
    if 0x121000 <= f0 < 0x8C0000:
        for x in ins(f0):
            t0 = ript(x)
            if t0 is not None: ALLRIP.add(t0)
for r in rows:
    f = int(r["reader"], 16); g = int(r["global"], 16)
    L = ins(f); addrs = {x.address for x in L}
    # a read: the global is not the destination operand (0028B24A writes EXPLPNumOffsetX; the column lists reads)
    reads = [x.address for x in L if ript(x) == g and not (x.op_str.split(",")[0].endswith("]") and x.mnemonic.startswith("mov"))]
    listed = [int(s, 16) for s in re.findall(r"[0-9A-Fa-f]{8}", r["sites"])]
    if sorted(listed) != sorted(reads): b2.append(r["key"] + "@" + r["reader"])
    tg = {int(x.op_str, 16) for x in L if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")}
    tg2 = set()
    for t in tg:
        for y in ins(t):
            if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"): tg2.add(int(y.op_str, 16))
    rips = {ript(x) for x in L} - {None}
    cited = {int(m, 16) for m in re.findall(r"\b([0-9A-Fa-f]{8})\b", re.sub(r"\([^)]*\)", "", r["use"]))}
    if any(c not in tg | tg2 | addrs | rips and c not in SIZES and c not in ALLRIP and not boundary(c) for c in cited): b3.append(r["key"] + "@" + r["reader"])
check("K2 site lists equal the reader's reads of the key's global", not b2, str(b2[:5]))
check("K3 no invented address: every cited address is a function entry, an instruction start inside a listed function, or a global the image references",
      not b3 and boundary(0x562C54) and not boundary(0x562C55), "%s; control 00562C54 %s, 00562C55 %s" % (b3[:5], boundary(0x562C54), boundary(0x562C55)))

slots = {}
for l in open(M / "layout-key-slots.tsv", encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) > 3: slots[p[0]] = (int(p[1].lstrip("+"), 16), int(p[2], 16), int(p[3], 16))
readkeys = {k for k, _ in pairs}
dead = sorted(k for k in slots if k not in readkeys)
deadg = {slots[k][1]: k for k in dead}
deadslot = {0x3B00 + slots[k][0]: k for k in dead if slots[k][2] == 0x1AF470}
deadslotB = {slots[k][0]: k for k in dead if slots[k][2] == 0x1B44A0}
inst = {k: slots[k][2] for k in dead}
liveg = {slots[k][1] for k in readkeys if k in slots}
IBR = re.compile(r"\[(\w+)(?: \+ \w+(?:\*\d)?)? \+ (0x[0-9a-f]{5,})\]")
SLOT = re.compile(r"\[(\w+)(?: \+ \w+(?:\*\d)?)? \+ (0x[0-9a-f]+)\]")
BUSERS = {0x1B44A0} | {f for f in SIZES if 0x121000 <= f < 0x8C0000 and any(
    (x.mnemonic in ("call", "jmp") and x.op_str == "0x1b5fb0") or ript(x) == 0x1F81200 for x in ins(f))}
riphit = collections.defaultdict(list); ibrhit = []; slothit = collections.defaultdict(list); livehit = set()
for f in sorted(SIZES):
    if not (0x121000 <= f < 0x8C0000): continue
    for x in ins(f):
        t = ript(x)
        if t in deadg and f != inst[deadg[t]]: riphit[deadg[t]].append(x.address)
        if t in liveg: livehit.add(t)
        for m in IBR.finditer(x.op_str):
            v = int(m.group(2), 16)
            if BASE + v in deadg: ibrhit.append((deadg[BASE + v], x.address))
        for m in SLOT.finditer(x.op_str):
            v = int(m.group(2), 16)
            if v in deadslot and not (m.group(1) == "rsp"): slothit[deadslot[v]].append((f, x.address, x.op_str))
            if v in deadslotB and f in BUSERS and not (m.group(1) == "rsp"): slothit[deadslotB[v]].append((f, x.address, x.op_str))
def is_ptr_load(s):
    """a qword load of the slot into a register: 'rXX, qword ptr [...]'"""
    return bool(re.match(r"r\w+, qword ptr \[", s))
slot_readers = {k: ["%08X %s" % (a, s) for f, a, s in slothit.get(k, []) if f not in (inst[k], 0x1CA600) and is_ptr_load(s)] for k in dead}
check("K4 the 13 unread keys: no rip or image-base reader, and only their installer stores their pointer slot; control: all 213 read keys have a rip reader",
      len(dead) == 13 and not any(riphit.values()) and not ibrhit and all(not v for v in slot_readers.values())
      and all(any(f == inst[k] for f, a, s in slothit.get(k, [])) for k in dead) and len(livehit) == len(liveg) == 213,
      "dead %d; rip %s; ibr %s; slot readers %s; live with reader %d/%d" % (len(dead), dict(riphit), ibrhit, {k: v for k, v in slot_readers.items() if v}, len(livehit), len(liveg)))

# K5 the 2026-09-27 join correction, from the bytes: 001CA600 makes 223 Variant_ReadInt and 3 Variant_ReadFloat reads; the
# float keys' slot pointers are loaded from 001B5FB0()'s object (rbx reloaded at 001CC572), which 001B44A0 fills with
# 01E0CF90/01E0CF94/01DF6DE0; MessageWinMaskBottom's int slot +0x2F8 (001CB2CD) holds 01E0CDA8 (001AF9CC/001AF9D3); and
# members/layout-key-slots.tsv now agrees: 226 rows, MessageWinMaskBottom -> 01E0CDA8, FontItalicVal -> 01E0CF90.
LD = ins(0x1CA600)
nint = sum(1 for x in LD if x.mnemonic == "call" and x.op_str == "0x200b80")
nflt = sum(1 for x in LD if x.mnemonic == "call" and x.op_str == "0x200b50")
at = {x.address: x for x in LD}
def cstr(va):
    o = off(va); return d[o:d.index(b"\0", o)].decode("latin1")
reload_ok = at[0x1CC566].op_str == "0x1b5fb0" and at[0x1CC572].op_str == "rbx, rax" and at[0x1CC589].op_str == "rcx, qword ptr [rbx + 0x2f8]"
mwmb_ok = at[0x1CB2CD].op_str == "rcx, qword ptr [rbx + 0x2f8]" and cstr(ript(at[0x1CB2B0])) == "MessageWinMaskBottom"
IB = {x.address: x for x in ins(0x1B44A0)}
fill_ok = [ript(IB[a]) for a in (0x1B4551, 0x1B455F, 0x1B456D)] == [0x1E0CF90, 0x1E0CF94, 0x1DF6DE0]
IA = {x.address: x for x in ins(0x1AF470)}
inst_ok = ript(IA[0x1AF9CC]) == 0x1E0CDA8 and IA[0x1AF9D3].op_str == "qword ptr [rcx + 0x3df8], rax"
tsv_ok = len(slots) == 226 and slots.get("MessageWinMaskBottom", (0, 0))[1] == 0x1E0CDA8 and slots.get("FontItalicVal", (0, 0))[1] == 0x1E0CF90
check("K5 the join correction holds in the bytes and in layout-key-slots.tsv",
      nint == 223 and nflt == 3 and reload_ok and mwmb_ok and fill_ok and inst_ok and tsv_ok,
      "int %d float %d reload %s maskbottom %s fill %s install %s tsv %s" % (nint, nflt, reload_ok, mwmb_ok, fill_ok, inst_ok, tsv_ok))
print("FAILS", fails)
sys.exit(1 if fails else 0)
