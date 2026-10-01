"""sd126_arms.py - SD-126: the message-dispatch arms of the battle-HUD widget procedures 002778C0, 00405310, 003FDFE0 and
003FF360 (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py. The id
sets agree with 16-UI/Widget-Object-Model/widget-message-handlers.tsv (resolve_switch_arms.py, 2026-09-20); this adds
the id -> arm map and each arm's direct callees. Message names are the-widget-message-protocol.md's.
"""
import csv, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def table(bound, shift, btab, dtab):
    out = {}
    for i in range(bound):
        a = R.at(btab + i, 1)[0] if btab else i
        out[i + shift] = struct.unpack("<I", R.at(dtab + 4 * a, 4))[0] + 0x00120000
    return out


def callees(t, n=10):
    cs = []
    for i in R.md.disasm(R.at(t, 0x400), t):
        if i.mnemonic == "call" and i.op_str.startswith("0x"):
            cs.append(int(i.op_str, 16))
        if i.mnemonic in ("jmp", "ret") or len(cs) >= n or i.address - t > 0x180:
            break
    return cs


MSG = {1: "CONSTRUCT", 2: "GENERATION RECONCILE", 4: "draw: after content", 8: "FOCUS GAINED", 10: "directional input",
       11: "input notice during a transition", 12: "enable/disable", 14: "opening transition started",
       15: "ABOUT TO BE DESTROYED", 18: "BEING DESTROYED", 19: "TRANSITION FINISHED, FORWARD", 30: "(30, narrowed)",
       31: "-", 32: "-", 35: "-", 44: "-", 45: "-", 285: "(285: the 0xA-based command range)"}
hand = {r["handler"]: r["ids"] for r in csv.DictReader(open(os.path.join(HERE, "..", "..", "..", "16-UI", "Widget-Object-Model",
                                                                          "widget-message-handlers.tsv"), encoding="utf-8"), delimiter="\t")}
# A1 - 002778C0: bound 45, id - 1 through the byte table 00279D98 into the dword table 00279D60 (dispatch 00277923)
t1 = table(45, 1, 0x00279D98, 0x00279D60)
default1 = 0x00279D2C
arms1 = {i: t for i, t in t1.items() if t != default1}
check("A1", txt(0x002778FF) == "cmp eax, 0x2c" and txt(0x00277911) == "movzx eax, byte ptr [rdx + rax + 0x159d98]"
      and txt(0x00277919) == "mov ecx, dword ptr [rdx + rax*4 + 0x159d60]" and sorted(arms1) == [int(x) for x in hand["002778C0"].split(",")]
      and arms1[10] == arms1[11] == 0x00277A64 and callees(default1)[0] == 0x005C5230,
      "002778C0: 14 ids with arms (10 and 11 share one), 31 to the base procedure 005C5230")
# A2 - 00405310: bound 19, dword table 00405724
t2 = table(19, 1, None, 0x00405724)
default2 = 0x004056FD
arms2 = {i: t for i, t in t2.items() if t != default2}
check("A2", txt(0x00405339) == "cmp eax, 0x12" and txt(0x0040534B) == "mov eax, dword ptr [r12 + rax*4 + 0x2e5724]"
      and sorted(arms2) == [int(x) for x in hand["00405310"].split(",")] and callees(default2)[0] == 0x005C5230,
      "00405310: ids 1, 2, 4, 14, 18, 19 have arms")
# A3 - 003FDFE0: a subtract chain on [rdx]: 1, 10, 12, 15, 18, else 005C5230
arms3 = {1: 0x003FE2EC, 10: 0x003FE2DF, 12: 0x003FE07E, 15: 0x003FE377, 18: 0x003FE035}
check("A3", txt(0x003FE003) == "sub ecx, 1" and txt(0x003FE006) == "je 0x3fe2ec" and txt(0x003FE00C) == "sub ecx, 9"
      and txt(0x003FE00F) == "je 0x3fe2df" and txt(0x003FE015) == "sub ecx, 2" and txt(0x003FE018) == "je 0x3fe07e"
      and txt(0x003FE01A) == "sub ecx, 3" and txt(0x003FE01D) == "je 0x3fe377" and txt(0x003FE023) == "cmp ecx, 3"
      and txt(0x003FE026) == "je 0x3fe035" and txt(0x003FE02B) == "call 0x5c5230"
      and sorted(arms3) == [int(x) for x in hand["003FDFE0"].split(",")],
      "003FDFE0: 1, 10, 12, 15, 18")
# A4 - 003FF360: a binary-search chain: 12 (pivot), 1, 8, 10 low; 18, 19, 285 high; else 005C5230
arms4 = {1: 0x003FF59D, 8: 0x003FF560, 10: 0x003FF3B1, 12: 0x003FF6EA, 18: 0x003FF8DD, 19: 0x003FF892, 285: 0x003FF7AB}
check("A4", txt(0x003FF387) == "cmp ecx, 0xc" and txt(0x003FF390) == "je 0x3ff6ea" and txt(0x003FF399) == "je 0x3ff59d"
      and txt(0x003FF3A2) == "je 0x3ff560" and txt(0x003FF3A8) == "cmp ecx, 2" and txt(0x003FF784) == "sub ecx, 0x12"
      and txt(0x003FF787) == "je 0x3ff8dd" and txt(0x003FF790) == "je 0x3ff892" and txt(0x003FF796) == "cmp ecx, 0x10a"
      and txt(0x003FF7A1) == "call 0x5c5230" and sorted(arms4) == [int(x) for x in hand["003FF360"].split(",")],
      "003FF360: 1, 8, 10, 12, 18, 19, 285")
for name, f, arms in (("002778C0", 0x002778C0, arms1), ("00405310", 0x00405310, arms2), ("003FDFE0", 0x003FDFE0, arms3),
                      ("003FF360", 0x003FF360, arms4)):
    for i in sorted(arms):
        print("      %s id %-4d %-36s arm %08X  callees %s" % (name, i, MSG.get(i, "-"), arms[i], " ".join("%08X" % x for x in callees(arms[i]))))
print("FAILS %d" % fails)
