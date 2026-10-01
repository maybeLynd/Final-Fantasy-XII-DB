"""SWE2-AUDIT-SPEC: is r13 zero at 0059CD14 on EVERY path through 0059C700, not only on the fall-through from 0059CC38?
Forward must-be-zero dataflow over the linear decode of 0059C700 (listed extent). Lattice ZERO / TOP.
xor r13d,r13d -> ZERO; any other instruction whose first operand is r13/r13d/r13w/r13b (mov/lea/pop/...) -> TOP;
direct calls and indirect calls preserve r13 (Win64 ABI: nonvolatile - a premise, not re-proved per callee).
Entry state TOP. A second run treats 0059CB1C->0059CC3B specially only by reporting the state on that edge.
Control (sensitivity): the same engine must report TOP at 0059CB2E (right after 0059CB2A mov r13d,[rax+0x10])."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\takebacks"))
import tk
ins = list(tk.fdis(0x0059C700))
addr = [x.address for x in ins]; idx = {a: i for i, a in enumerate(addr)}
R13 = ("r13", "r13d", "r13w", "r13b")
def transfer(x, s):
    first = x.op_str.split(",")[0].strip()
    if x.mnemonic == "xor" and x.op_str in ("r13d, r13d", "r13, r13"): return "ZERO"
    if first in R13 and x.mnemonic not in ("cmp", "test", "push"): return "TOP"
    return s
def succ(i):
    x = ins[i]; m = x.mnemonic
    if m == "ret" or (m == "jmp" and not x.op_str.startswith("0x")): return []
    if m == "int3": return []
    out = []
    if m.startswith("j") and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if t in idx: out.append(idx[t])
        else: out.append(("EXT", t))
        if m == "jmp": return out
    if i + 1 < len(ins): out.append(i + 1)
    return out
state = {0: "TOP"}; work = [0]; ext = set()
def join(a, b): return a if a == b else "TOP"
IN = {}
while work:
    i = work.pop()
    s = IN.get(i, "TOP") if i != 0 else "TOP"
    if i in IN: s = IN[i]
    o = transfer(ins[i], s)
    for j in succ(i):
        if isinstance(j, tuple): ext.add(j[1]); continue
        n = o if j not in IN else join(IN[j], o)
        if IN.get(j) != n: IN[j] = n; work.append(j)
IN[0] = "TOP"
for a in (0x0059CB2E, 0x0059CC38, 0x0059CC3B, 0x0059CD14, 0x0059CB1C):
    i = idx.get(a); print("state of r13 on entry to %08X: %s" % (a, IN.get(i, "unreached")))
x = ins[idx[0x0059CB1C]]
print("edge 0059CB1C->0059CC3B carries:", transfer(x, IN[idx[0x0059CB1C]]))
print("unreached instructions:", sum(1 for i in range(len(ins)) if i not in IN and i != 0), "of", len(ins))
print("branch targets outside the listed extent:", ["%08X" % t for t in sorted(ext)])
