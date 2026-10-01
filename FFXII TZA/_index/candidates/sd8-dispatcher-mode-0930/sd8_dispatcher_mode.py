"""sd8_dispatcher_mode.py - which dispatcher mode (02064AD3) does the title run in? (OPUS, 2026-09-30; register SD-8)

Re-reads each fact from the certified image through the shared lookup tool
Database/Tools/analysis-kit/gfz-scripts/retool.py and asserts it. Prints PASS/FAIL per fact and `FAILS n` last.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c, MODE = T.R, T.scan(), 0x02064AD3
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def called(site):
    i = ins(site)
    return int(i.op_str, 16) if i.mnemonic == "call" else None


# F1 - the frame dispatcher 0022A580 switches on the mode through the table at 0022A754 (7 entries, `cmp eax, 6`)
tab = [0x00120000 + v for v in struct.unpack("<7I", R.at(0x0022A754, 28))]
handlers = {0: called(0x0022A6A5), 1: called(0x0022A6AC), 2: called(0x0022A6D9), 3: called(0x0022A6B3), 4: called(0x0022A6C6),
            5: called(0x0022A6BA), 6: called(0x0022A6D2)}
check("F1", tab == [0x0022A6A5, 0x0022A6AC, 0x0022A6D9, 0x0022A6B3, 0x0022A6C1, 0x0022A6BA, 0x0022A6CD]
      and handlers == {0: 0x0022B6E0, 1: 0x0022B7E0, 2: 0x0022A770, 3: 0x0022B8C0, 4: 0x0022AF50, 5: 0x0022BC20, 6: 0x0022B000},
      "mode -> handler: %s" % {k: "%08X" % v for k, v in handlers.items()})
# F2 - every store to the mode byte, and its value
W = sorted((f, a) for f, a, k in c["refs"].get(MODE, ()) if k == "W")
vals = {a: ins(a).op_str.split(", ")[-1] for f, a in W}
check("F2", [f for f, _ in W] == [0x00229F00, 0x0022A0B0, 0x0022AF50, 0x0022B000, 0x0022B6E0, 0x0022B7E0, 0x0022B8C0, 0x0022BC20],
      "writers: %s" % " ".join("%08X@%08X=%s" % (f, a, vals[a]) for f, a in W))
# F3 - the per-mode transitions: 0 -> 1 (0022B74E), 1 -> 2 once 0032E520(1) and 0037C2E0() are 0 (0022B837..0022B85B),
#      4 -> 3 (0022AFF2), 6 -> 5 (0022B097), 3 -> 2 (0022BB81), 5 -> 2 (0022BDC5), init 0 (0022A1A0)
t = {a: vals.get(a) for a in (0x0022B74E, 0x0022AFF2, 0x0022B097, 0x0022BB81, 0x0022BDC5, 0x0022A1A0)}
m1 = [ins(a) for a in (0x0022B83C, 0x0022B841, 0x0022B84A, 0x0022B858, 0x0022B85B)]
check("F3", t == {0x0022B74E: "1", 0x0022AFF2: "3", 0x0022B097: "5", 0x0022BB81: "2", 0x0022BDC5: "2", 0x0022A1A0: "0"}
      and m1[0].op_str == "0x32e520" and m1[1].op_str == "ebx, 2" and m1[2].op_str == "0x37c2e0" and m1[3].mnemonic == "cmove",
      "0->1, 1->2 (when both waits are 0), 4->3, 6->5, 3->2, 5->2, init 0")
# F4 - the one outside setter 00229F00 is called with 4 (002E09A0 @002E0D39), 6 or 2 (002E2240 @002E2257 / @002E2274)
cs = sorted(c["calls"].get(0x00229F00, ()))
args = {a: ins(a - 5).op_str for f, a in cs}
check("F4", [a for _, a in cs] == [0x002E0D39, 0x002E2257, 0x002E2274]
      and args == {0x002E0D39: "ecx, 4", 0x002E2257: "ecx, 6", 0x002E2274: "ecx, 2"},
      "outside requests: %s" % args)
# F5 - the keyboard poll gate (0022A600..0022A657): modes 4 and 6 clear ebx; otherwise ebx survives only for 2..5 minus 4
g = [ins(a) for a in (0x0022A607, 0x0022A60A, 0x0022A613, 0x0022A61C, 0x0022A623, 0x0022A638, 0x0022A655, 0x0022A659)]
check("F5", g[0].op_str == "eax, [rdx - 4]" and g[1].op_str == "eax, 0xfffffffd" and g[2].op_str == "eax, [rdx - 2]"
      and g[3].op_str == "eax, 0xfffffffc" and g[4].op_str == "edx, 4" and g[5].op_str == "ebx, ebx" and g[6].op_str == "ebx, ebx"
      and g[7].op_str == "0x35e6f0",
      "poll (0022A659 -> 0035E6F0) runs in modes 2, 3, 5 only")
print("FAILS %d" % fails)
