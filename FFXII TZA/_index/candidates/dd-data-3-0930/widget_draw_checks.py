"""the-widget-tree-draw-pass (DD batch 3, SWE2-DATA 2026-09-30), static reads of 00245E60 and its two brackets.

W1 the handler's messages 3 and 4 run only when flag bit 24 equals the pass global 0208F564 and bit 28 is clear
   (0024623A..00246255; calls 002462D0, 0024635A); message 5 runs only when bit 24 matches and bit 12 is set
   (00246388..0024639F; call 002463BC); the child loop (0024635C..00246386) is outside both gates.
W2 the pass global is the bracket's pass index: 002450B0 stores 0 and 00245110 stores 1, each before calling 00245E60.
W3 the background drawers run only when flag bit 7 is set and bit 24 matches (002461BB..002461CE); bit 8 picks
   002455A0 (set) or 00245170 (clear) (002461D9..002461F0).
W4 003985B0 and 00398C50 are called only when their float is non-zero (ucomiss/je at 0024601F, 0024603F); 0039ADE0
   only when flag bit 21 is set (002460FA..00246100), scaling by node +0x8C.
W5 the typed-list draw 002435C0 runs on node +0x50 when that word's bit 0 is set (002462D2..002462E0).
C1 control: the three message records at 009151C0 / D8 / F0 carry ids 3, 4, 5, and the three lea targets are those
   records.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def rip(x):
    import re
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


m = {x.address: x for x in dis(0x00245E60)}
check("W1 messages 3/4: bit 24 == pass and bit 28 clear; message 5: bit 24 == pass and bit 12 set",
      m[0x0024623F].op_str == "eax, 0x18" and rip(m[0x00246245]) == 0x0208F564 and m[0x00246251].op_str == "ecx, 0x1c"
      and m[0x00246255].mnemonic == "jb" and m[0x002462D0].op_str == "rax" and m[0x0024635A].op_str == "rax"
      and rip(m[0x00246393]) == 0x0208F564 and m[0x0024639B].op_str == "ecx, 0xc" and m[0x0024639F].mnemonic == "jae"
      and m[0x002463BC].op_str == "rax" and m[0x0024637A].op_str == "0x245e60"
      and m[0x0024624B].op_str == "0x24635c")
b0 = {x.address: x for x in dis(0x002450B0)}
b1 = {x.address: x for x in dis(0x00245110)}
check("W2 002450B0 stores pass 0, 00245110 pass 1, then each walks the tree",
      rip(b0[0x002450B9]) == 0x0208F564 and b0[0x002450B9].op_str.endswith(", 0") and b0[0x002450D2].op_str == "0x245e60"
      and rip(b1[0x00245119]) == 0x0208F564 and b1[0x00245119].op_str.endswith(", 1") and b1[0x00245132].op_str == "0x245e60")
check("W3 background: bit 7 set and bit 24 == pass; bit 8 picks 002455A0 / 00245170",
      m[0x002461BE].op_str == "al, al" and m[0x002461C0].mnemonic == "jns" and rip(m[0x002461C8]) == 0x0208F564
      and m[0x002461D9].op_str == "dword ptr [rbx + 0x40], 0x100" and m[0x002461E9].op_str == "0x2455a0"
      and m[0x002461F0].op_str == "0x245170")
check("W4 rotations only on non-zero floats; 0039ADE0 on bit 21 with node +0x8C",
      m[0x0024601F].mnemonic == "ucomiss" and m[0x0024602C].mnemonic == "je" and m[0x00246035].op_str == "0x3985b0"
      and m[0x0024603F].mnemonic == "ucomiss" and m[0x0024604C].mnemonic == "je" and m[0x00246055].op_str == "0x398c50"
      and m[0x002460FA].op_str == "eax, 0x15" and m[0x00246100].mnemonic == "je"
      and m[0x00246102].op_str == "xmm0, dword ptr [rbx + 0x8c]" and m[0x00246131].op_str == "0x39ade0")
check("W5 002435C0 on node +0x50 when its bit 0 is set",
      m[0x002462D2].op_str == "byte ptr [rbx + 0x50], 1" and m[0x002462D6].op_str == "rcx, [rbx + 0x50]"
      and m[0x002462E0].op_str == "0x2435c0")
ids = [d[off(a)] for a in (0x009151C0, 0x009151D8, 0x009151F0)]
check("C1 control: message records 3/4/5 and the three lea targets",
      ids == [3, 4, 5] and rip(m[0x002462C6]) == 0x009151C0 and rip(m[0x00246350]) == 0x009151D8
      and rip(m[0x002463B2]) == 0x009151F0, str(ids))
print("RESULT the draw pass runs twice per bracket pass index (0208F564 = 0 or 1); a node draws its own background "
      "and messages in the pass matching its bit 24, and its children are visited in both")
print("FAILS %d" % FAILS)
