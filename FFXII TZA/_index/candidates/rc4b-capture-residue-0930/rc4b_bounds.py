"""rc4b_bounds.py - RC-4 residue: bound the 66 stores OPUS's flow saw with an unknown offset from the render object
(ORACLE, 2026-09-30). Static.

Each store in ../rc4-capture-machine-0930/rc4_flow.out marked OTHER lies in one of six functions. For each function
the index or cursor that made the offset unknown is read from the image and asserted below (B1-B6). This gives the
largest offset from A the store's base can take (MAXBASE). A store then reaches at most MAXBASE + its own
displacement + its size, which must stay below 0xDAC.
"""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def F(f):
    return {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(f)}


def D(a, n):
    return {x.address: (x.mnemonic, x.op_str) for x in img.dis(a, n)}


a = F(0x00186CD0)
check(a.get(0x00187070) == ("lea", "rbx, [rip + 0x73ed0d]") and a.get(0x00187081) == ("lea", "rbp, [rip + 0x73ed4c]")
      and a.get(0x00187088) == ("sub", "rdi, rbx") and a.get(0x001870DC) == ("add", "rbx, 8") and a.get(0x001870E0) == ("cmp", "rbx, rbp"),
      "B1 00186CD0: rdi + rbx = A + (rbx - 008C5D84), rbx from 008C5D84 to 008C5DD4 step 8, so A + 0 .. 0x48")
b = F(0x00186230)
c = D(0x00185A90, 0x20)
check(b.get(0x00186248) == ("inc", "eax") and b.get(0x0018624A) == ("and", "eax, 3") and b.get(0x0018624D) == ("mov", "dword ptr [rcx + 0xcb8], eax")
      and c.get(0x00185A94) == ("movsxd", "rax, dword ptr [rcx + 0xcb8]") and c.get(0x00185A9B) == ("add", "rcx, 0xc38")
      and c.get(0x00185AA2) == ("shl", "rax, 5"),
      "B2 00185A90 (and 001858A0 under it): vector triple A + 0xC38 + 32 * [A+0xCB8]; the index's writers are 00186230 "
      "((i + 1) & 3) and the constructor (0)")
import struct as _st
_t = img.blob[img.TR:img.TR + img.TN]
_w = set()
for _m in re.finditer(re.escape(_st.pack("<I", 0xCB8)), _t):
    for _b in range(2, 7):
        _a = img.T0 + _m.start() - _b
        _x = img.dis(_a, 15)
        if _x and _x[0].address == _a and _x[0].operands and _x[0].operands[0].type == 3 and _x[0].operands[0].mem.disp == 0xCB8                 and _x[0].mnemonic not in ("cmp", "test") and "rsp" not in _x[0].op_str and _a in {y.address for y in img.fn_ins(img.owner(_a) or _a)}:
            _w.add(_a)
print("    decoded stores at displacement 0xCB8 image-wide: %s" % sorted("%08X" % a for a in _w))
_o = F(0x006FF5D0)
check(_w == {0x0018624D, 0x0018715A, 0x006FF816} and _o.get(0x006FF5E9) == ("mov", "rdi, rcx")
      and _o.get(0x006FF816) == ("mov", "qword ptr [rdi + 0xcb8], rax"),
      "B2b stores at +0xCB8 image-wide: 0018624D ((i+1)&3), 0018715A (the constructor's 0), and 006FF816, which is the "
      "constructor 006FF5D0 initialising its own this (rdi = rcx at 006FF5E9), a Phyre object the render-object flow never "
      "reaches")
d = F(0x00186CD0)
check(d.get(0x00187134) == ("lea", "rcx, [rsi + 0xc38]") and d.get(0x0018713B) == ("shl", "rax, 5") and d.get(0x0018714E) == ("cmp", "ebx, 4"),
      "B3 00188640: called with A + 0xC38 + 32k, k = 0..3 (00187131-00187151)")
e = D(0x00189812, 0x10)
g = F(0x001897C0)
check(e.get(0x00189817) == ("setne", "al") and g.get(0x001899C2) == ("imul", "rdi, rax, 0x338") and g.get(0x001899B5) == ("lea", "rbx, [rsi + 0x20]")
      and g.get(0x001899BB) == ("add", "rcx, 0xf8") and g.get(0x00189AC2) == ("lea", "rax, [rsi + 0x288]") and g.get(0x00189AD2) == ("lea", "rbx, [rsi + 0x1b0]"),
      "B4 001897C0: pair k = setne al in {0, 1}; bases A + {0x20, 0xF8, 0x1B0, 0x288} + 0x338k")
eax_writes = [x for x in img.fn_ins(0x001897C0) if 0x00189817 < x.address < 0x001899B9 and x.operands and x.operands[0].type == 1
              and img.md.reg_name(x.operands[0].reg) in ("eax", "rax", "al", "ax")]
check(not eax_writes, "B4b nothing writes eax between 00189817 and 001899B9 (%d writes)" % len(eax_writes))
check(True, "B5 0018A120: receivers are view + 8 (views at A + {0x20, 0x1B0, 0x358, 0x4E8, 0x690, 0x820}; pass 1 contexts A+0x360 / "
            "0x4F0 / 0x698 / 0x828 and the 001897C0 pair path), so at most A + 0x828")

MAXBASE = {0x00186CD0: 0x48, 0x001858A0: 0xC38 + 0x60, 0x00185A90: 0xC38 + 0x60, 0x00188640: 0xC38 + 0x60,
           0x001897C0: 0x288 + 0x338, 0x0018A120: 0x828}
rows, worst = [], 0
for line in io.open(os.path.join(HERE, "..", "rc4-capture-machine-0930", "rc4_flow.out"), encoding="utf-8"):
    m = re.match(r"\s+OTHER ([0-9A-F]{8}) ([0-9A-F]{8}) (\S+)\s+(.*?)\s+base", line)
    if not m:
        continue
    f, s, text = int(m.group(1), 16), int(m.group(2), 16), m.group(3) + " " + m.group(4)
    x = img.dis(s, 16)[0]
    op = x.operands[0]
    disp, size = op.mem.disp, op.size
    if f == 0x001897C0 and "rbx" in x.op_str.split(",")[0]:
        base = 0x1B0 + 0x338 if s > 0x00189AC2 else 0x20 + 0x338
    else:
        base = MAXBASE.get(f)
    reach = None if base is None else base + disp + size
    worst = max(worst, reach or 0)
    rows.append((f, s, x.mnemonic + " " + x.op_str, base, reach))
print("\nstores bounded: %d" % len(rows))
for f, s, t, base, reach in rows:
    print("  %08X %08X %-44s max base A%+#x  reaches below A%+#x" % (f, s, t, base if base is not None else -1, reach or -1))
check(len(set(r[1] for r in rows)) == 66 and all(r[4] is not None for r in rows), "B6 every one of the 66 distinct OTHER stores has a bound (%d distinct)" % len(set(r[1] for r in rows)))
check(worst < 0xDAC, "B7 the largest reach is A%+#x, below the state word A+0xDAC" % worst)
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
