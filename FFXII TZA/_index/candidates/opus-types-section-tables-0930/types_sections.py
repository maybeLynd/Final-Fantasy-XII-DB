"""types_sections.py - where OffsetIndexedStringTable (ActorManagerSlot +0x0A0 / +0x0A8) and CountedU32LookupTable
(+0x100) come from: sections +0x18 / +0x1C / +0x40 of the EBP primary payload, bound by 003304A0's section ladder, so
the tables are file-resident views into the loaded payload, not owned allocations (OPUS, 2026-09-30).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = ins(a)
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


SLOT, STRIDE = 0x02098E10, 0x288
# P1 - the EBP primary-payload dispatcher 003304A0 binds section +0x18 / +0x1C / +0x40 by passing
#      (payload + dword[payload + off]) | tag, truncated to 32 bits (mov ecx, eax), to 00330190 / 00330220 / 0032FB70
rungs = {0x18: (0x0033051F, 0x00330526, 0x0033052D, 0x0033052F, "0x330190"),
         0x1C: (0x0033053A, 0x00330541, 0x00330548, 0x0033054A, "0x330220"),
         0x40: (0x003305EA, 0x003305F1, 0x003305F8, 0x003305FA, "0x32fb70")}
ok = True
for off, (ld, add, mv, call, tgt) in rungs.items():
    ok &= txt(ld) == "mov eax, dword ptr [rdi + 0x%x]" % off and txt(add) == "add rax, rdi" and txt(mv) == "mov ecx, eax" \
        and txt(call) == "call " + tgt
check("P1", ok, "003304A0: section base = payload + dword[payload + off], for +0x18 / +0x1C / +0x40")
# P2 - each binder masks the tag off (& ~0xF), keeps the base in its per-tag table and calls its slot setter with it
binders = {0x003301B6: (0x003301BB, "0x26c880"), 0x00330246: (0x0033024B, "0x26c8a0"), 0x0032FB96: (0x0032FB9B, "0x26ce40")}
ok = True
for b, (st, setter) in binders.items():
    ok &= txt(b) == "and rdx, rax" and txt(st).startswith("mov qword ptr [r14 + rcx*8 +") \
        and txt(st + 8) == "call " + setter
check("P2", ok, "binders 00330190 / 00330220 / 0032FB70: base & ~0xF -> per-tag table, then the slot setter")
# P3 - the three setters store rdx at the 0x288-stride slot array 02098E10 + tag * 0x288 + field
ok = True
for s, field in ((0x0026C880, 0xA0), (0x0026C8A0, 0xA8), (0x0026CE40, 0x100)):
    ok &= txt(s + 3) == "imul rcx, rax, 0x288" and rip(s + 0xA) == SLOT + field and txt(s + 0x11) == "mov qword ptr [rcx + rax], rdx"
check("P3", ok, "0026C880 / 0026C8A0 / 0026CE40 write slot +0xA0 / +0xA8 / +0x100 (slot array 02098E10, stride 0x288)")
# P4 - the only other write of +0x100 is the teardown 0032ED80, which stores 0 (rbp, zeroed at 0032EDC2)
t0 = V.value_at(0x0032ED80, 0x0032F0F0, "rbp", 2)
check("P4", t0 == {("C", 0)} and txt(0x0032F0FA) == "call 0x26ce40" and txt(0x0032F0EE) == "xor edx, edx"
      and sorted(set(f for f, s in c["calls"].get(0x0026CE40, ()))) == [0x0032ED80, 0x0032FB70]
      and [f for f, s in c["calls"].get(0x0026C880, ())] == [0x00330190] and [f for f, s in c["calls"].get(0x0026C8A0, ())] == [0x00330220],
      "writers: +0xA0 only 00330190, +0xA8 only 00330220, +0x100 the bind 0032FB70 and the teardown 0032ED80 (0)")
print("FAILS %d" % fails)
