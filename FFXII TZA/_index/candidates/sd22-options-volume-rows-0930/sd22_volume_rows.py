"""sd22_volume_rows.py - which options-screen rows send settings commands 0x13 / 0x14 / 0x15? (OPUS, 2026-09-30; SD-22)

Asserts each fact over the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py and prints the
static menu tree it reads. PASS/FAIL per fact, `FAILS n` last.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0
NODES, N = 0x01E0BF60, 0x2D          # 0023EDB9: [00120000 + rax*8 + 0x1CEBF60], bounded by `cmp eax, 0x2d`
TYPES = 0x00120000 + 0x11EF54         # 0023EE78: type 1..10 -> arm


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def node(i):
    p = struct.unpack("<Q", R.at(NODES + 8 * i, 8))[0]
    if not p:
        return None
    t, own, cnt = R.at(p, 1)[0], R.at(p + 1, 1)[0], struct.unpack("<H", R.at(p + 2, 2))[0]
    kids = [R.at(p + 4 + 6 * k, 6) for k in range(cnt)]
    return {"type": t, "own": own, "kids": kids}


# F1 - the builder 0023ED80 indexes the node table by the row byte +0xC0, reads each child entry's id byte, and picks
#      the child's handler by the child node's type through the table at 0023EE78
f1 = [ins(a) for a in (0x0023EDA3, 0x0023EDB4, 0x0023EDB9, 0x0023EE44, 0x0023EE5F, 0x0023EE78)]
check("F1", f1[0].op_str == "eax, byte ptr [rcx + 0xc0]" and f1[1].op_str == "eax, 0x2d" and "0x1cebf60" in f1[2].op_str
      and f1[3].op_str == "eax, byte ptr [rdx]" and f1[4].op_str == "eax, byte ptr [rcx]" and "0x11ef54" in f1[5].op_str,
      "node table 01E0BF60 (%d entries), child id byte, child type -> arm table" % N)
arms = {t + 1: 0x00120000 + x for t, x in enumerate(struct.unpack("<10I", R.at(TYPES, 40)))}
# F2 - type 6 selects the arm 0023EEA2, which registers handler 0023EBE0
check("F2", arms[6] == 0x0023EEA2 and ins(0x0023EEAA).op_str.startswith("rdx, [rip")
      and ins(0x0023EEAA).address + ins(0x0023EEAA).size + ins(0x0023EEAA).operands[1].mem.disp == 0x0023EBE0,
      "type 6 -> arm 0023EEA2 -> handler 0023EBE0")
# F3 - nodes 0x13, 0x14, 0x15 are type 6, and each is a child of the three root menus 0x00, 0x01, 0x02 (and of no other)
tree = {i: node(i) for i in range(N)}
parents = {k: sorted(i for i, n in tree.items() if n and any(e[0] == k for e in n["kids"])) for k in (0x13, 0x14, 0x15)}
check("F3", all(tree[k]["type"] == 6 and tree[k]["own"] == k for k in (0x13, 0x14, 0x15))
      and parents == {0x13: [0, 1, 2], 0x14: [0, 1, 2], 0x15: [0, 1, 2]},
      "types %s; parents %s" % ({hex(k): tree[k]["type"] for k in (0x13, 0x14, 0x15)}, {hex(k): v for k, v in parents.items()}))
labels = {k: sorted(set(e[1:].hex() for n in (tree[0], tree[1], tree[2]) for e in n["kids"] if e[0] == k)) for k in (0x13, 0x14, 0x15)}
print("      child entry bytes after the id (label / help fields): %s" % labels)
# F4 - the child id travels as the creation payload's +8 (0023EEA2 loads it; 0023EEC2 [rsp+0x30]) and 0023EBE0 stores it
#      into the row byte (0023ECBD movzx edx, [rdx+8] -> 0023D4F0, which writes +0xC0 at 0023D504)
check("F4", ins(0x0023EEA2).op_str == "eax, byte ptr [rdx]" and ins(0x0023EEC2).op_str == "qword ptr [rsp + 0x30], rax"
      and ins(0x0023EEC7).op_str == "r8, [rsp + 0x28]" and ins(0x0023ECBD).op_str == "edx, byte ptr [rdx + 8]"
      and ins(0x0023ECC1).op_str == "0x23d4f0" and ins(0x0023D504).op_str == "byte ptr [rcx + 0xc0], dl",
      "payload +8 = child id -> row byte +0xC0")
# F5 - on a change, 0023EBE0 sends the settings command with that byte as the id (0023EC6E / 0023EC7A -> 00240750)
check("F5", ins(0x0023EC6E).op_str == "ecx, byte ptr [rbx + 0xc0]" and ins(0x0023EC7A).op_str == "0x240750",
      "00240750(row byte +0xC0, &value) when the value differs (0023EC66 / 0023EC68)")
print("FAILS %d" % fails)
