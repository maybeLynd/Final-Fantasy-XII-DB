"""SWE2-AUDIT-SEM AB-8 check (own code): every route into the counter updater 00316A50.
T  every 5-byte `jmp 00316A50` thunk anywhere in .text (not only 00253770), and every qword / rip lea naming the updater
   or any thunk.
S  every direct call/jmp into the updater or a thunk, with the last write of ecx (counter id) and edx (amount) in the 16
   instructions before it (printed for reading).
C  the callers of 002E2380 and 00317090."""
import struct, re
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
T = 0x00316A50
def sites(t):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t:
            out.append((va0 + i, "call" if text[i] == 0xE8 else "jmp"))
    return out
thunks = []
for a, k in sites(T):
    x = next(img.md.disasm(img.rd(a - 16, 32), a - 16), None)
    prev = [y for y in img.md.disasm(img.rd(a - 1, 1), a - 1)]
    # a thunk: the jmp is preceded by int3/ret padding (a function start)
    before = img.rd(a - 1, 1)[0]
    if k == "jmp" and before in (0xCC, 0xC3, 0x90):
        thunks.append(a)
print("T jmp-thunks into 00316A50:", ["%08X" % a for a in thunks])
refs = {}
for tgt in [T] + thunks:
    q = img.raw.count(struct.pack("<Q", tgt))
    refs["%08X" % tgt] = q
print("T qwords naming the updater or a thunk:", refs)
def last(ins, regs):
    for x in reversed(ins):
        o = [s.strip() for s in x.op_str.split(",")]
        if o and o[0] in regs and x.mnemonic not in ("cmp", "test", "push"):
            return "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
        if x.mnemonic == "call":
            return "(call before: %s)" % x.op_str
    return "?"
for tgt in [T] + thunks:
    for a, k in sites(tgt):
        if a in thunks:
            continue
        for back in range(60, 10, -1):
            xs = list(img.md.disasm(img.rd(a - back, back + 5), a - back))
            if any(x.address == a for x in xs):
                break
        pre = [x for x in xs if x.address < a][-16:]
        print("S %08X %s -> %08X  ecx: %s | edx: %s" % (a, k, tgt, last(pre, ("ecx", "rcx")), last(pre, ("edx", "rdx"))))
for f in (0x002E2380, 0x00317090):
    print("C callers of %08X:" % f, ["%08X %s" % s for s in sites(f)])
print("D the three direct callers, read around the call")
for lo, hi in ((0x00254EE0, 0x00254F07), (0x00312470, 0x0031249B), (0x0056D4B0, 0x0056D4D7)):
    for back in range(40, 0, -1):
        xs = list(img.md.disasm(img.rd(lo - back, hi - lo + back + 16), lo - back))
        if any(x.address == lo for x in xs):
            break
    for x in xs:
        if lo <= x.address <= hi:
            print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    print("   --")
