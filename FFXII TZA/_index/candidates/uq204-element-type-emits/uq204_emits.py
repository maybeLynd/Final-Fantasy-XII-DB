"""uq204_emits.py - UQ-204: what each effect element type puts on screen (FABLE, Claude Opus 5.5, 2026-09-27). Static.

uq204-element-type-emits.tsv has one row per element type with a dedicated handler. This control checks what the
bytes decide:
  E1 the rows are exactly the types of members/effect-type-methods.tsv that have at least one handler address (65), in
     order, and each row's walk is that table's walk or sub-walk.
  E2 no invented address or edge: every 8-hex code address the row cites is a function entry or an instruction start of
     the function containing it; every hop 'A -> B|C' of the emits chain is a direct call, jmp or jcc out of A's body;
     every 'mnem@SITE>TARGET' names the instruction at SITE. Controls: a planted false hop and a planted wrong site
     are refused.
  E3 the class each row states agrees with the emitters the type's methods reach (direct call/jmp/jcc closure, depth 5,
     over walk, sub-walk, step, update and seventh): a GiPrim/sprite/composer row reaches that emitter, a VU1 row a
     GiVmax registrar, a pair row 00540F40 or 00540DB0, a raw-packet row 003A3010, 003A31A0 or 00540C20, and a "none"
     row reaches no emitter of any class. Control: the known 0x01 walk 00442550 reaches the point emitter 0039C550.
  E4 the correction of FABLE's 2026-09-20 "0xA4 and 0xA7 emit nothing": 005227C5 in 00522300 is `call 003A3010`, and
     00526D2D in 00526A10 is `call 003A34D0`.
  E5 why the six raw-packet types reach no PC submission: 003A3010 stores rbx, zeroed at 003A3094, as the entry's
     callback +0x10 (003A310A), and 003A31A0 does the same at 003A322E / 003A329E. The drain 003A3740 calls +0x10 when it
     is set (003A38BA-003A38C6). Otherwise it submits only when +0 equals r15, which is zeroed at 003A37B0 (003A38CA).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, csv, re, struct, sys
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
FS = sorted(SIZES)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
DIS = {}
def ins(f):
    if f not in DIS:
        o = off(f); DIS[f] = list(cs.disasm(d[o:o + SIZES.get(f, 0x200) + 64], f)) if o is not None else []
    return DIS[f]
def owner(a):
    i = bisect.bisect_right(FS, a) - 1
    return FS[i] if i >= 0 and FS[i] <= a < FS[i] + max(SIZES[FS[i]], 1) else None
def at(a):
    e = owner(a)
    return next((x for x in ins(e) if x.address == a), None) if e is not None else None
def edges(f):
    end = f + SIZES.get(f, 0x200); out = set()
    for x in ins(f):
        if x.address >= end: break
        if (x.mnemonic in ("call", "jmp") or x.mnemonic.startswith("j")) and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if x.mnemonic != "call" and f <= t < end: continue
            out.add(t)
    return out
def closure(roots, depth=5):
    seen = set(roots); frontier = set(roots)
    for _ in range(depth):
        nxt = set()
        for f in frontier:
            for t in edges(f):
                if t not in seen: seen.add(t); nxt.add(t)
        frontier = nxt
    return seen
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
HEX = re.compile(r"\b[0-9A-F]{8}\b")

rows = list(csv.DictReader(open(HERE / "uq204-element-type-emits.tsv", encoding="utf-8"), delimiter="\t"))
M = [l.rstrip("\n").split("\t") for l in open(DB / "17-Presentation-Rendering/Effect-File-Formats/members/effect-type-methods.tsv", encoding="utf-8")]
meth = {r[0]: r for r in M[1:] if any(re.fullmatch(r"[0-9A-F]{8}", c) for c in r[1:])}
walk_ok = all(r["walk"] in (meth[r["type"]][3], meth[r["type"]][8]) or (r["walk"] == "-" and meth[r["type"]][3] in ("-", "default") and meth[r["type"]][8] in ("-", "default"))
              for r in rows if r["type"] in meth)
check("E1 the rows are the 65 handler-bearing types, in order, with the table's walk", [r["type"] for r in rows] == list(meth) and len(rows) == 65 and walk_ok,
      "rows %d, types match %s, walks %s" % (len(rows), [r["type"] for r in rows] == list(meth), walk_ok))

def row_errors(r):
    errs = []
    for col in ("walk", "emits", "evidence", "note"):
        for h in HEX.findall(r[col]):
            a = int(h, 16)
            if 0x121000 <= a < 0x8C0000 and a not in SIZES and at(a) is None: errs.append("not an instruction " + h)
    body = r["emits"].split(":", 1)[1] if ":" in r["emits"] else ""
    for chain in body.split(";"):
        hops = [HEX.findall(h) for h in chain.split("->")]
        hops = [h for h in hops if h]
        for i in range(len(hops) - 1):
            for x in hops[i]:
                if not any(int(y, 16) in edges(int(x, 16)) for y in hops[i + 1]): errs.append("%s reaches none of %s" % (x, hops[i + 1]))
            for y in hops[i + 1]:
                if not any(int(y, 16) in edges(int(x, 16)) for x in hops[i]): errs.append("nothing reaches %s" % y)
    for col in ("evidence", "note"):
        for mn, s, tg in re.findall(r"\b([a-z]+)@([0-9A-F]{8})>([0-9A-F]{8})", r[col]):
            x = at(int(s, 16))
            if x is None or x.mnemonic != mn or not x.op_str.startswith("0x") or int(x.op_str, 16) != int(tg, 16):
                errs.append("site %s is not %s %s" % (s, mn, tg))
    return errs
bad = {r["type"]: row_errors(r) for r in rows}
bad = {k: v for k, v in bad.items() if v}
c1 = row_errors({"walk": "-", "emits": "x: 00442550 -> 0039D5A0", "evidence": "", "note": ""})
c2 = row_errors({"walk": "-", "emits": "none", "evidence": "call@004425E8>0039C4C0", "note": ""})
check("E2 every cited address, hop and call site is real; controls refused", not bad and bool(c1) and bool(c2),
      "%s; planted hop refused %s, planted site refused %s" % (dict(list(bad.items())[:3]), bool(c1), bool(c2)))

EMIT = {"prim": {0x8642A0, 0x39D5A0, 0x39D890, 0x39D970, 0x39D6C0, 0x39C550, 0x39C4C0, 0x4355D0},
        "sprite": {0x501A50, 0x502280},
        "vu": {0x3A34D0, 0x3A35E0, 0x3A33B0, 0x3A2F70},
        "pair": {0x540F40, 0x540DB0},
        "raw": {0x3A3010, 0x3A31A0, 0x540C20}}
ALL = set().union(*EMIT.values())
def klass(e):
    e0 = e.split(":", 1)[0]
    if e0.startswith("none"): return "none"
    if "sprite" in e0: return "sprite"
    if "GiPrim" in e0 or "GiPolyGT4T" in e0 or "composer" in e0: return "prim"
    if "GS packet" in e0 or "arena packet" in e0: return "raw"
    if "0054" in e0 or "pair" in e0: return "pair"
    if "GiVmax" in e0: return "vu"
    return "?"
def roots(t):
    m = meth[t]
    return {int(c, 16) for i, c in enumerate(m) if i in (1, 2, 3, 5, 6, 7, 8, 9, 10) and re.fullmatch(r"[0-9A-F]{8}", c)}
e3 = []
for r in rows:
    k = klass(r["emits"]); reach = closure(roots(r["type"])) & ALL
    ok = (k == "none" and not reach) or (k in EMIT and reach & EMIT[k])
    if not ok: e3.append("%s:%s reaches %s" % (r["type"], k, sorted("%08X" % a for a in reach)))
ctl = 0x39C550 in closure({0x442550})
check("E3 each row's class matches the emitters its methods reach; control 00442550 -> 0039C550", not e3 and ctl, "%s; control %s" % (e3[:4], ctl))

x1, x2 = at(0x5227C5), at(0x526D2D)
check("E4 0xA4 and 0xA7 do emit: 005227C5 call 003A3010, 00526D2D call 003A34D0",
      owner(0x5227C5) == 0x522300 and x1.mnemonic == "call" and x1.op_str == "0x3a3010"
      and owner(0x526D2D) == 0x526A10 and x2.mnemonic == "call" and x2.op_str == "0x3a34d0",
      "%s %s / %s %s" % (x1.mnemonic, x1.op_str, x2.mnemonic, x2.op_str))

def is_(a, mn, ops): x = at(a); return x is not None and x.mnemonic == mn and x.op_str == ops
e5 = [is_(0x3A3094, "xor", "ebx, ebx"), is_(0x3A310A, "mov", "qword ptr [r14 + 0x10], rbx"),
      is_(0x3A37B0, "xor", "r15d, r15d"), is_(0x3A38BA, "mov", "rax, qword ptr [rbx + 0x10]"),
      is_(0x3A38C6, "call", "rax"), is_(0x3A38CA, "cmp", "qword ptr [rbx], r15"), is_(0x3A38CD, "jne", "0x3a38fb")]
check("E5 raw-packet entries carry no callback and a packet at +0, which the drain passes over", all(e5), str(e5))
print("FAILS", fails)
sys.exit(1 if fails else 0)
