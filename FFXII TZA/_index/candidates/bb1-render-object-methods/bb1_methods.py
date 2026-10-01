"""bb1_methods.py - BB-1: what CharacterRenderObject renders, per method (FABLE, Claude Opus 5.5, 2026-09-27). Static.

bb1-methods.tsv has one row per slot of the 31-slot vtable 00903B68. This control checks what the bytes decide:
  M1 the rows are the 31 slots of 00903B68, in order, with the image's addresses.
  M2 no invented address or edge: every 8-hex address cited in the rows or in findings.md is a function entry, an
     instruction start of the function containing it, or an address in a data section; every 'A -[S]-> B' names a
     real direct call, jmp or jcc at S inside A whose target is B. Control: a planted mid-instruction address, a
     planted wrong edge and an out-of-image address are all refused.
  M3 no method draws by itself: no slot's direct call/jmp/jcc closure (depth 4) reaches the Gi emitters or the draw
     list (0020E680, 0020E630, 0039D5A0, 0039D970, 0039D6C0, 003A3010, 003A34D0, 00540DB0, 00540F40). Control: the
     effect walk dispatcher 002F4020 reaches 0039D5A0 by the same walk.
  M4 the draw route, instruction by instruction:
     - the render record's update 0053AB50 calls slot 1 through 0017F0B0 on [r12+0x6B8] (0053AE1A, 0053AE2C);
     - slot 1 001F89B0 tail-jumps to 0018AFF0 with the list from 0018B4E0 and this+0x28, and 0018AFF0 is a push_back
       (the pointer is stored at the list's end, 0018B013);
     - the element class's vtable 00903940 has 00215320 at slot 1, which is `mov rcx, [rcx+8]; jmp 001F5D70`;
     - the list walk 0018B100 calls each element's slot 1 (`call [rax+8]`, 0018B187), and the render pass list
       00187950 calls 0018B100 (00187D05);
     - GameApplication's render slot 8 (0017D090) runs 00187950;
     - 001F5D70, a method of the class that is not in its vtable, calls Phyre's draw submit 0060B980 (001F5F38,
       001F61CC).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def in_image_data(v): return any(BASE + va <= v < BASE + va + vs for vs, va, rs, ro in secs)
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
        o = off(f); DIS[f] = list(cs.disasm(d[o:o + SIZES.get(f, 0)], f)) if o is not None and SIZES.get(f, 0) > 0 else []
    return DIS[f]
def owner(a):
    i = bisect.bisect_right(FS, a) - 1
    return FS[i] if i >= 0 and FS[i] <= a < FS[i] + max(SIZES[FS[i]], 1) else None
def at(a):
    f = owner(a)
    return next((x for x in ins(f) if x.address == a), None) if f is not None else None
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

rows = [l.rstrip("\n").split("\t") for l in open(HERE / "bb1-methods.tsv", encoding="utf-8")][1:]
vt = [q(0x903B68 + 8 * k) for k in range(31)]
check("M1 the rows are the 31 slots of 00903B68", len(rows) == 31 and [int(r[0]) for r in rows] == list(range(31))
      and [int(r[1], 16) for r in rows] == vt, "rows %d" % len(rows))

EDGE = re.compile(r"(?=([0-9A-F]{8}) -\[([0-9A-F]{8})\]-> ([0-9A-F]{8}))")
def problems(text):
    bad = []
    for h in sorted(set(re.findall(r"(?<![0-9A-Fa-fx])([0-9A-F]{8})(?![0-9A-Fa-f])", text))):
        a = int(h, 16)
        if 0x121000 <= a < 0x8C2000:
            if a not in SIZES and at(a) is None: bad.append("not an instruction " + h)
        elif not in_image_data(a): bad.append("outside the image " + h)
    for A, S, B in EDGE.findall(text):
        x = at(int(S, 16))
        if owner(int(S, 16)) != int(A, 16) or x is None or not (x.mnemonic == "call" or x.mnemonic.startswith("j")) \
                or not x.op_str.startswith("0x") or int(x.op_str, 16) != int(B, 16):
            bad.append("edge %s -[%s]-> %s" % (A, S, B))
    return bad
text = (HERE / "bb1-methods.tsv").read_text(encoding="utf-8") + (HERE / "findings.md").read_text(encoding="utf-8")
bad = problems(text)
ctl = problems("001F6D7B and 001F89B0 -[001F89BF]-> 0018AFF0 and 0FFFFFFF")
check("M2 every cited address and edge is real; the three planted defects are refused", not bad and len(ctl) == 3, "%s; control %s" % (bad[:4], ctl))

def edges(f):
    end = f + SIZES.get(f, 0); out = set()
    for x in ins(f):
        if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if x.mnemonic != "call" and f <= t < end: continue
            out.add(t)
    return out
def closure(roots, depth=4):
    seen = set(roots); fr = set(roots)
    for _ in range(depth):
        nx = set()
        for f in fr:
            for t in edges(f):
                if t not in seen: seen.add(t); nx.add(t)
        fr = nx
    return seen
RENDER = {0x20E680, 0x20E630, 0x39D5A0, 0x39D970, 0x39D6C0, 0x3A3010, 0x3A34D0, 0x540DB0, 0x540F40}
hit = {k: sorted("%08X" % a for a in closure({vt[k]}) & RENDER) for k in range(31)}
hit = {k: v for k, v in hit.items() if v}
ctl3 = 0x39D5A0 in closure({0x2F4020})
check("M3 no slot reaches a Gi emitter or the draw list within depth 4; control 002F4020 reaches 0039D5A0", not hit and ctl3, "%s; control %s" % (hit, ctl3))

def is_(a, mn, ops=None):
    x = at(a); return x is not None and x.mnemonic == mn and (ops is None or x.op_str == ops)
w = ins(0x17F0B0)
m4 = {
 "0053AB50 calls slot 1 via 0017F0B0 on [r12+0x6B8]": is_(0x53AE1A, "call", "0x17f0b0") and is_(0x53AE2C, "call", "0x17f0b0")
     and is_(0x53AE12, "mov", "rcx, qword ptr [r12 + 0x6b8]") and any(x.op_str == "qword ptr [rax + 8]" and x.mnemonic == "jmp" for x in w),
 "slot 1 tail-jumps 0018AFF0 with 0018B4E0's list and this+0x28": vt[1] == 0x1F89B0 and is_(0x1F89B6, "mov", "rbx, qword ptr [rcx + 0x28]")
     and is_(0x1F89BF, "call", "0x18b4e0") and is_(0x1F89CF, "jmp", "0x18aff0"),
 "0018AFF0 is a push_back": is_(0x18B00A, "mov", "qword ptr [rcx + 8], rax") and is_(0x18B013, "mov", "qword ptr [rdx], r8"),
 "00903940 slot 1 = 00215320 = mov rcx,[rcx+8]; jmp 001F5D70": q(0x903940 + 8) == 0x215320 and is_(0x215320, "mov", "rcx, qword ptr [rcx + 8]") and is_(0x215324, "jmp", "0x1f5d70"),
 "0018B100 calls each element's slot 1": is_(0x18B187, "call", "qword ptr [rax + 8]"),
 "00187950 calls 0018B100": is_(0x187D05, "call", "0x18b100"),
 "render slot 8 0017D090 runs 00187950": q(0x8C5760 + 64) == 0x17D090 and 0x187950 in edges(0x17D090),
 "001F5D70 calls 0060B980": is_(0x1F5F38, "call", "0x60b980") and is_(0x1F61CC, "call", "0x60b980"),
}
check("M4 the draw route holds instruction by instruction", all(m4.values()), str({k: v for k, v in m4.items() if not v}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
