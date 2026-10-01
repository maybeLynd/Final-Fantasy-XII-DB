"""Widget-derived types carry the shared Widget header as one embedded row (OPUS, 2026-09-27). Control. Static.

Three types (GlyphRunWidget1498, ActiveLogWidget40C8, MapScreenPage) already carry `+0x0000 192 widgetBase0000 Widget`,
the base 002465F0 writes on every constructed widget. The other widget-derived types re-describe that header row by row
from their own per-type censuses. Three things go wrong with that:
- they leave "unobserved" gaps over header fields the Widget type names;
- they give +0x98 / +0x9C as dwords, where the base has four int16s and one packed initialising store;
- they give +0xA1 as a word, where the base has two bytes.
  H1 RECEIVER PROOF, per type: the site each type's own allocation record cites builds the object at its base -
     `mov ecx, <type size>` then `call/jmp 00244F50` (the widget allocator), or `mov edx, <type size>` then
     `call 00245000` (in place). Only verified types are normalised
  H2 the base's +0x98..+0x9E are four int16s: in the widget code (00240000-0024C000) each is accessed as a word, and
     every dword or qword access at +0x98 / +0x9C there is a packed store or an 8-byte copy (the initialiser's 00246711 /
     00246717 and 002445F3), never a dword field read
  H3 STORE REGRESSION: every verified type has exactly one row starting below +0xC0 - `widgetBase0000 Widget` at +0
  H4 the one width conflict a type recorded against the base: MessageWindowRecord +0x40 "flags040 uint8" is the base's
     dword flags - 002465F0 writes it as a dword (0024666D) and the registry probe byte-tests bit 0x10 of it (002A28F8)
Not claimed: the unverified candidates (records cite no single construction site); any meaning beyond the base's own.
Revised 2026-09-27 (OPUS, on review): H1 is split - H1a WHOLE-OBJECT (the site loads the type's own size; 69 types) and
H1b PREFIX ONLY (ManagerSub7FB0Record: a 0xF0 widget at the base of a 0x110 record - base identity, not extent), with N
(no `mov edx, 0x110` precedes its site) and R (the tracked verified-sites.json reproduces; it is written only with
--write, each entry carrying its kind).
"""
import os, re, json, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

hdr = None; T = {}
for l in open(DB / "_types/types.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if hdr is None: hdr = c; continue
    T[c[0]] = dict(zip(hdr, c))
FIELDS = os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv"
rows = collections.defaultdict(list)
for l in open(FIELDS, encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9: rows[c[0]].append(c)

def site_of(d_):
    a = d_["allocation_site"] + " || " + d_["ctor"]
    m = (re.search(r"00244F50 at ([0-9A-F]{8})", a) or re.search(r"CONSTRUCTED IN PLACE at ([0-9A-F]{8})", a)
         or re.search(r"HEAP ([0-9A-F]{8}) - call 00244F50", a) or re.search(r"with ecx=0x[0-9A-F]+ at ([0-9A-F]{8})", a)
         or re.search(r"\((0[0-9A-F]{7}) / 0[0-9A-F]{7}\)", a) or re.search(r"construction entry at ([0-9A-F]{8}) with size", a)
         or re.search(r"00245000 at ([0-9A-F]{8})", a))
    return int(m.group(1), 16) if m else None
import bisect
KEYS = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(KEYS, v) - 1
    return KEYS[k] if k >= 0 and v < KEYS[k] + sizes[KEYS[k]] else None
def verify(t):
    """in the owning function: a call/jmp to 00244F50 (allocator) or 00245000 (in place) at the cited site, and within
    16 instructions before it `mov ecx|edx, <type size>` with no intervening write to that register"""
    sz = int(T[t]["size"], 16); s = site_of(T[t])
    f = owner(s) if s else None
    if f is None: return None
    xs = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    i = next((k for k, x in enumerate(xs) if x.address == s), None)
    if i is None or xs[i].mnemonic not in ("call", "jmp") or xs[i].op_str not in ("0x244f50", "0x245000"): return None
    reg = ("ecx", "rcx", "cx", "cl") if xs[i].op_str == "0x244f50" else ("edx", "rdx", "dx", "dl")
    for y in reversed(xs[max(0, i - 16):i]):
        first = y.op_str.split(",")[0].strip()
        if y.mnemonic == "mov" and first == reg[0] and re.match(r"%s, (0x[0-9a-f]+)$" % reg[0], y.op_str):
            return (s, xs[i].op_str, y.address) if int(y.op_str.split(", ")[1], 16) == sz else None
        if first in reg and y.mnemonic not in ("cmp", "test", "push"): return None
    return None
cands = [t for t in T if t != "Widget" and re.search(r"00244F50|00245000|widget construction entry", T[t]["allocation_site"] + T[t]["ctor"])]
V = {t: verify(t) for t in sorted(cands)}
# INTERIOR types whose records name no single site the pattern above can parse: the in-place construction is proved
# from the owning function's own instructions - call 00245000 at the site, `mov edx, <widget size>` just before it.
#   BattleMenuChildWidget1620 - its record's "CONSTRUCTED IN PLACE ... at 002779FA": rcx = parent + 0xF0, size 0x1620
#   ManagerSub7FB0Record      - the queue consumer 00296860 builds a 0xF0 widget at rbx - 0x104, and rbx is the record's
#                               +0x104 (the store's consumeCursor0104 row: `movsx rax, word ptr [rbx]` at 002968AC)
#   PaneSlotWidget0160        - 0029BB40 builds 0x160 widgets at r15 + 0x240 + rbp, the record's slot formula
INPLACE = {"BattleMenuChildWidget1620": (0x2779FA, 0x1620), "ManagerSub7FB0Record": (0x2968DE, 0xF0), "PaneSlotWidget0160": (0x29BBDA, 0x160)}
for t, (s, sz) in INPLACE.items():
    f = owner(s); xs = list(cs.disasm(d[off(f):off(f) + sizes[f]], f)) if f else []
    i = next((k for k, x in enumerate(xs) if x.address == s), None)
    good = i is not None and xs[i].op_str == "0x245000" and any(y.mnemonic == "mov" and y.op_str == "edx, %s" % hex(sz) for y in xs[max(0, i - 8):i])
    V[t] = (s, "0x245000", next(y.address for y in xs[max(0, i - 8):i] if y.op_str == "edx, %s" % hex(sz))) if good else None
ok = sorted(t for t, v in V.items() if v)
# WHOLE vs PREFIX (2026-09-27, OPUS, on review). A site that loads the type's OWN size proves the whole object is built
# by the widget constructor. A site that loads LESS proves only that the object's base is a widget of that size - a
# receiver / base-identity proof, NOT an extent proof. ManagerSub7FB0Record is the one such: its site loads 0xF0 and the
# record is 0x110; the 0x110 rests on the parent's stride arithmetic (types.tsv), never on this constructor.
def loaded(v):
    xs = {x.address: x for x in cs.disasm(d[off(v[2]):off(v[2]) + 8], v[2])}
    return int(xs[v[2]].op_str.split(", ")[1], 16)
KIND = {t: ("whole" if loaded(V[t]) == int(T[t]["size"], 16) else "prefix:%s" % hex(loaded(V[t]))) for t in ok}
REC = {t: [hex(V[t][0]), V[t][1], hex(V[t][2]), KIND[t]] for t in ok}
RECEIPT = HERE / "verified-sites.json"
if "--write" in sys.argv:          # the tracked receipt changes only on request (immutable otherwise)
    json.dump(REC, open(RECEIPT, "w"), indent=0); print("receipt written")
whole = [t for t in ok if KIND[t] == "whole"]; prefix = [t for t in ok if KIND[t] != "whole"]
check("H1a WHOLE-OBJECT: the cited site loads the type's own size and calls the widget allocator / in-place constructor",
      len(whole) == 77 and len(V) == 84,   # 77 / 84: BattleMenuChildBase4C0 (child_base_4c0.py B); 70 / 79 from 2026-09-28: Widget0720At0209BE80_AB30 (battle_menu_child_base.py X); 71 / 80: ManagerSubA0D0Record (a0d0_record.py S); 72 / 81: WidgetChild00D0At3CA530 (widget_singleton_nested.py N); 73 / 82: HelpMessageSlotRecord0100 (help_pane_audit.py H); 74 / 83: WidgetChild0650At298250 (widget0720_child.py N); 76 / 83: HelpMessageWidget0500 + WidgetConsumer02AEE4C8 (widget_header_more.py S)
      "%d whole of %d candidates; unverified: %s" % (len(whole), len(V), sorted(t for t, v in V.items() if not v)))
check("H1b PREFIX ONLY: ManagerSub7FB0Record's site builds a 0xF0 widget at the base of a 0x110 record - base identity, "
      "not extent", prefix == ["ManagerSub7FB0Record"] and KIND["ManagerSub7FB0Record"] == "prefix:0xf0"
      and int(T["ManagerSub7FB0Record"]["size"], 16) == 0x110, str({t: KIND[t] for t in prefix}))
f7 = owner(0x2968DE); x7 = list(cs.disasm(d[off(f7):off(f7) + sizes[f7]], f7))
i7 = next(k for k, x in enumerate(x7) if x.address == 0x2968DE)
check("N  the prefix cannot be promoted: no `mov edx, 0x110` precedes 002968DE", not any(y.op_str == "edx, 0x110" for y in x7[max(0, i7 - 16):i7]))
check("R  the tracked receipt reproduces", json.load(open(RECEIPT)) == REC)

acc = collections.Counter(); packed = []
for f in sorted(sizes):
    if not (0x240000 <= f < 0x24C000) or off(f) is None: continue
    for x in cs.disasm(d[off(f):off(f) + sizes[f]], f):
        m = re.search(r"(byte|word|dword|qword) ptr \[r(?!sp|ip)\w+ \+ 0x(98|9a|9c|9e)\]", x.op_str)
        if m:
            acc[(m.group(1), m.group(2))] += 1
            if m.group(1) in ("dword", "qword"): packed.append((x.address, x.mnemonic, x.op_str))
check("H2 the base's +0x98..+0x9E are word fields; the wider accesses are packed stores or 8-byte copies",
      acc[("word", "9a")] >= 9 and acc[("word", "9e")] >= 15 and all(p[2].startswith(("dword ptr", "qword ptr")) or p[2].startswith(("rax, qword", "rcx, qword", "rdx, qword")) for p in packed),
      "word 98/9a/9c/9e = %d/%d/%d/%d; wide: %s" % (acc[("word", "98")], acc[("word", "9a")], acc[("word", "9c")], acc[("word", "9e")], ["%08X %s %s" % p for p in packed][:6]))
def hdr_ok(t):
    below = [c for c in rows[t] if int(c[1], 16) < 0xC0]
    if [c[3] for c in below] == ["widgetBase0000"]: return True
    # the header inside an embedded widget base at +0 (BattleMenuChildWidget1620 -> BattleMenuChildBase4C0, child_base_4c0.py E)
    return len(below) == 1 and int(below[0][1], 16) == 0 and below[0][4] in rows and [c[3] for c in rows[below[0][4]] if int(c[1], 16) < 0xC0] == ["widgetBase0000"]
bad = [t for t in ok if not hdr_ok(t)]
check("H3 STORE REGRESSION: every verified type has one row below +0xC0, widgetBase0000 Widget",
      not bad, "%d of %d still re-describe the header: %s" % (len(bad), len(ok), bad[:5]))
K = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x2465F0):off(0x2465F0) + sizes[0x2465F0]], 0x2465F0)}
P = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x2A28E0):off(0x2A28E0) + 0x40], 0x2A28E0)}
check("H4 MessageWindowRecord +0x40 is the base's dword flags, byte-tested for bit 0x10",
      K.get(0x24666D) == "mov dword ptr [rdi + 0x40], eax" and K.get(0x2466F2) == "or dword ptr [rdi + 0x40], eax"
      and P.get(0x2A28F8) == "test byte ptr [rax + 0x40], 0x10" and "MessageWindowRecord" in ok)
print("FAILS", fails)
sys.exit(1 if fails else 0)
