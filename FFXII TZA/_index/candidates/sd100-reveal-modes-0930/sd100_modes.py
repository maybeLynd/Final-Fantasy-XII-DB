"""sd100_modes.py - SD-100: the reveal stepper 002ABF70's modes - which writer sets each mode byte (+0xB0 low byte) and
what each mode does (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py
and the `pe` module of _index/candidates/rc22-34-resource-readers-0930/ (38,161 bodies).
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# M1 - the stepper dispatches on the low byte of +0xB0 (bound 7) through the image-relative table 002AC1B4
tab = [struct.unpack("<I", R.at(0x002AC1B4 + 4 * k, 4))[0] + 0x00120000 for k in range(8)]
check("M1", txt(0x002ABF79) == "mov ecx, dword ptr [rcx + 0xb0]" and txt(0x002ABF7F) == "movzx eax, cl" and txt(0x002ABF82) == "cmp eax, 7"
      and tab == [0x002AC06B, 0x002AC06B, 0x002AC04F, 0x002ABF9F, 0x002AC06B, 0x002ABFFC, 0x002AC1AB, 0x002AC18B],
      "modes 0/1/4 -> 002AC06B, 2 -> 002AC04F, 3 -> 002ABF9F, 5 -> 002ABFFC, 6 -> 002AC1AB (exit), 7 -> 002AC18B")
# M2 - mode 3 (002ABF9F) counts the tick word +0x88 down and steps the reveal target every tick (+0x92 = +0x90,
#      +0x90 += (s8)+0xA0 while below +0x8C); at zero it sets +0x9B = 30 and mode 0
check("M2", txt(0x002ABF9F) == "movzx eax, word ptr [rbx + 0x88]" and txt(0x002ABFAF) == "sub ax, 1"
      and txt(0x002ABFBC) == "mov byte ptr [rbx + 0x9b], 0x1e" and txt(0x002ABFC3) == "mov byte ptr [rbx + 0xb0], 0"
      and txt(0x002ABFDE) == "movsx eax, byte ptr [rbx + 0xa0]" and txt(0x002ABFEF) == "mov word ptr [rbx + 0x90], ax",
      "mode 3: timed hold that keeps typing; ends in mode 0")
# M3 - mode 5 (002ABFFC) never reads +0x88: it adds the speed +0x9C to the accumulator +0x9B and, each time that reaches
#      30, steps the target by +0xA0 - typing at an authored rate
check("M3", txt(0x002ABFFC) == "movzx eax, byte ptr [rbx + 0x9c]" and txt(0x002AC003) == "add byte ptr [rbx + 0x9b], al"
      and txt(0x002AC009) == "cmp byte ptr [rbx + 0x9b], 0x1e" and txt(0x002AC01D) == "mov byte ptr [rbx + 0x9b], 0"
      and not any("0x88]" in "%s %s" % (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(0x002ABFFC, 0x53), 0x002ABFFC)),
      "mode 5: rate stepping (+0x9C per tick, a step every 30), no +0x88")
# M4 - modes 0/1/4 (002AC06B) use the same accumulator and, when a line is full, advance the page through 002ABB20
#      (automatically when +0xA0 > 1, else only when 00248F20 answers 1) and restore the budget 0x7D00; mode 2 (002AC04F)
#      first counts the fade word +0x5A down (reset by bit 22), then falls into the same path
check("M4", txt(0x002AC06B) == "movzx eax, byte ptr [rbx + 0x9c]" and txt(0x002AC07C) == "cmp byte ptr [rbx + 0xa0], 1"
      and txt(0x002AC085) == "call 0x248f20" and txt(0x002AC0A7) == "call 0x2abb20" and txt(0x002AC0B3) == "mov ecx, 0x7d00"
      and txt(0x002AC04F) == "bt ecx, 0x16" and txt(0x002AC064) == "dec ax" and txt(0x002AC067) == "mov word ptr [rbx + 0x5a], ax",
      "modes 0/1/4: type and page; mode 2: count the fade word down, then the same")
# M6 - mode 7 (002AC18B) counts +0x88 down WITHOUT stepping, then mode 0: a frozen timed pause
check("M6", txt(0x002AC18B) == "movzx eax, word ptr [rbx + 0x88]" and txt(0x002AC197) == "sub ax, 1"
      and txt(0x002AC1A4) == "mov byte ptr [rbx + 0xb0], 0" and txt(0x002AC1AB) == "add rsp, 0x20",
      "mode 7: count +0x88 down with the text frozen, then mode 0")
# M5 - every byte store to +0xB0 in the image, by value (the 007Exxxx stores are the audio code's own structure)
W = collections.defaultdict(list)
for f in sorted(pe.funcs):
    for x in pe.dis(f):
        m = re.match(r"byte ptr \[(\w+) \+ 0xb0\], (.+)$", x.op_str)
        if x.mnemonic == "mov" and m and m.group(1) not in ("rsp", "rbp", "rip") and f < 0x00700000:
            W[m.group(2)].append((f, x.address))
for v in sorted(W):
    print("      mode %-4s %s" % (v, " ".join("%08X@%08X" % w for w in W[v])))
want = {"0": [(0x002A5CC0, 0x002A5E75), (0x002ABF70, 0x002ABFC3), (0x002ABF70, 0x002AC1A4), (0x002AC1E0, 0x002AC239), (0x002B3D50, 0x002B3D68)],
        "1": [(0x002A8C50, 0x002A8D2B), (0x002A8C50, 0x002A9923)], "2": [(0x002A8C50, 0x002A989E)], "3": [(0x002A8C50, 0x002A9428)],
        "4": [(0x002A8C50, 0x002A9193), (0x002B0280, 0x002B199A)], "5": [(0x002A8C50, 0x002A97EA), (0x002A8C50, 0x002A98B5), (0x002AC5F0, 0x002AD225)],
        "6": [(0x002A6190, 0x002A67DB), (0x002A9980, 0x002A9AA2), (0x002A9980, 0x002A9D1C)], "7": [(0x002A3250, 0x002A3556)],
        "dil": [(0x002A9980, 0x002A9A27)], "al": [(0x002B3950, 0x002B3963)]}
check("M5", dict(W) == want, "the writer census of the mode byte (text code below 00700000): 20 stores")
print("FAILS %d" % fails)
