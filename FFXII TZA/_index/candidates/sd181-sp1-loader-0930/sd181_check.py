"""sd181_check.py - SD-181 closed: 02ADD060 is filled with slot 16 of the map's .mpk by the map_ctrl pack's completion
00378BC0, so the emitter base 022CBAF0 points into the SP1 section of ps2data/plan_master/map_ctrl/<area>/<map>/bin/<map>.mpk
(OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

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


# L1 - the map_ctrl pack request: 00378030 submits the load with completion 00378BC0 (the one reference to it)
check("L1", txt(0x003780B1).startswith("lea rax, [rip") and rip(0x003780B1) == 0x00378BC0
      and c["refs"].get(0x00378BC0) == {(0x00378030, 0x003780B1, "lea")} and not c["calls"].get(0x00378BC0),
      "00378030 registers 00378BC0 as the pack load's completion (its only reference)")
# L2 - the completion splits the loaded block into 32 slot pointers on its stack: 0036B970(block & ~3, rsp + 0x20, 0x20)
check("L2", txt(0x00378BDD) == "lea rdx, [rsp + 0x20]" and txt(0x00378BE7) == "mov r8d, 0x20" and txt(0x00378BED) == "and rcx, rax"
      and txt(0x00378BE2) == "mov eax, 0xfffffffc" and txt(0x00378BF3) == "call 0x36b970",
      "00378BC0: 0036B970(block & ~3, &slots[0] = rsp + 0x20, 32)")
# L3 - slot 16 -> 02ADD060: rsp + 0xA0 is slots[(0xA0 - 0x20) / 8] = slots[16], stored at 00378E9D
check("L3", txt(0x00378E95) == "mov rcx, qword ptr [rsp + 0xa0]" and rip(0x00378E9D) == 0x02ADD060
      and txt(0x00378E9D).startswith("mov qword ptr [rip") and (0xA0 - 0x20) // 8 == 16,
      "slots[16] (the SP1 section) is stored into 02ADD060")
# L4 - control on the arithmetic: the same function copies slots[24..27] (rsp + 0xE0 + 8 i) to 02ADD010 + 8 i, the map
#      pictures the map_ctrl page's slot table maps to 02ADD010+
check("L4", txt(0x00378C40) == "mov rcx, qword ptr [rsp + r9 + 0xe0]" and txt(0x00378C48) == "mov qword ptr [r9 + r11 + 0x29bd010], rcx"
      and txt(0x00378C06).startswith("lea r11, [rip") and rip(0x00378C06) == 0x00120000 and (0xE0 - 0x20) // 8 == 24,
      "control: slots[24] lands at 02ADD010, as the slot table says")
# L5 - the rest of the chain, from sd180-181-emitter-walk-0930 B1: 003775D0 reads [02ADD060] and 003635C0 stores it into
#      the emitter base 022CBAF0; the teardown 00378230 frees and zeroes 02ADD060
w = sorted(set((f, k) for f, s, k in c["refs"][0x02ADD060]))
check("L5", rip(0x003775EE) == 0x02ADD060 and [f for f, s in c["calls"].get(0x003635C0, ())] == [0x003775D0]
      and w == [(0x003775D0, "R"), (0x00378230, "R"), (0x00378230, "W"), (0x00378BC0, "W")],
      "02ADD060: written by 00378BC0 (slot 16) and the teardown 00378230; read by 003775D0 -> 003635C0 -> 022CBAF0")
print("FAILS %d" % fails)
