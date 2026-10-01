"""sd22_rederive.py - SWE2-AUDIT-SPEC independent decode of the options node table (2026-09-30), not through retool.
Reads the qword pointers at 01E0BF60 until a non-pointer, decodes each node (type +0, id +1, count +2, 6-byte children
from +4), lists every parent of 0x13/0x14/0x15, checks each node's own id equals its table index, and prints the
0023EBE0 lines around the change call plus the head of 00240750."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
T = 0x01E0BF60
nodes = []
i = 0
while True:
    p = tk.u64(T + 8 * i)
    if p is None or not (0x00120000 <= p < 0x04000000) or tk.off(p) is None: break
    nodes.append(p); i += 1
print("table %08X: %d consecutive image pointers; qword after = %s" % (T, len(nodes), hex(tk.u64(T + 8 * len(nodes)) or 0)))
def node(p):
    o = tk.off(p); b = tk.d[o:o + 4 + 6 * 64]
    typ, nid, cnt = b[0], b[1], b[2]
    kids = [b[4 + 6 * k:10 + 6 * k] for k in range(cnt)]
    return typ, nid, cnt, kids
bad = []
parents = {0x13: [], 0x14: [], 0x15: []}
types = {}
for idx, p in enumerate(nodes):
    typ, nid, cnt, kids = node(p)
    types[idx] = typ
    if nid != idx: bad.append((idx, nid))
    for k, kb in enumerate(kids):
        if kb[0] in parents: parents[kb[0]].append((idx, k, kb.hex()))
print("nodes whose id byte != table index:", bad)
for c in (0x12, 0x13, 0x14, 0x15):
    print("node %#x type %d" % (c, types.get(c, -1)))
for c, ps in parents.items():
    print("parents of %#x: %s" % (c, ps))
for r in (0, 1, 2):
    typ, nid, cnt, kids = node(nodes[r])
    print("root %d type %d children ids %s" % (r, typ, [kb[0] for kb in kids]))
from collections import Counter
print("type histogram:", sorted(Counter(types.values()).items()))
print("--- 0023EBE0 around the change call")
for x in tk.dis(0x0023EC40, 0x0023EC80):
    print("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("--- 00240750 head")
for x in tk.dis(0x00240750, 0x002407A0):
    print("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
# the eight descriptors whose +1 byte is not their table index: their parents (who lists them as a child)
for idx in (0, 1, 2, 23, 39, 40, 41, 42, 43, 44):
    typ, nid, cnt, kids = node(nodes[idx])
    par = [(j, k) for j, p in enumerate(nodes) for k, kb in enumerate(node(p)[3]) if kb[0] == idx]
    print("desc %d: type %d, +1 = %d, count %d, listed as a child by %s" % (idx, typ, nid, cnt, par[:6]))
