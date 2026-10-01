"""gr17_ops.py - sample of the package's E6 for the opcodes c_all.efx actually carries, re-derived with this review's
graph (gr17_graph2 boundary-checked reach set R0 to 00312280).

  O1  opcode -> arm through the two tables of 003B8670 (byte index at image base + 0x29994C, dword offsets at + 0x299854;
      read at 003B8787 / 003B8790).
  O2  for every opcode 1..128: the direct call / tail targets reachable from its arm by a CFG walk inside 003B8670 that
      stops at the loop continuations (003B88F4 / 003B88F8 / 003B8740 / 003B97EE, as the package) - over-approximate:
      every jcc edge is followed; each target tested against R0. Also indirect calls met.
  O3  the event kind each 002EB740 caller passes ([rsp+0x30] immediate before the call), and 00319F50's kind jump table
      (image base + 0x1FA200, 9 arms): which arms reach 0030E360 in R0.
  C   control: opcode 3 (the hit) must come out reaching.
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr17_graph2 as G2
GG = G2.GG; T = G2.T; P = G2.P; G = GG.G
IB = T.IB
ed0, _, _ = G2.build(False)
R0 = P.reach(ed0)
R0K = P.reach(ed0, 0x0030E360)

F = 0x003B8670
ext = [(T.IB + b, T.IB + e) for b, e, u in G.PD if G.root(T.IB + b) == F]
lo, hi = min(a for a, b in ext), max(b for a, b in ext)
INS = {i.address: i for a, b in ext for i in T.dis(a, b)}
STOP = {0x003B88F4, 0x003B88F8, 0x003B8740, 0x003B97EE}


def walk(start, stops, ins, inside):
    seen, st, calls, ind = set(), [start], set(), []
    while st:
        a = st.pop()
        if a in seen or a in stops or a not in ins:
            continue
        seen.add(a)
        i = ins[a]
        nxt = a + i.size
        if i.mnemonic == "call":
            op = i.operands[0]
            if op.type == 2:
                calls.add(op.imm)
            else:
                ind.append("%08X %s" % (a, i.op_str))
            st.append(nxt)
        elif i.mnemonic == "ret":
            continue
        elif i.mnemonic == "jmp":
            op = i.operands[0]
            if op.type == 2:
                if inside(op.imm):
                    st.append(op.imm)
                else:
                    calls.add(op.imm)
            else:
                ind.append("%08X jmp %s" % (a, i.op_str))
        elif i.mnemonic.startswith("j"):
            st.append(nxt)
            if i.operands[0].type == 2:
                st.append(i.operands[0].imm)
        else:
            st.append(nxt)
    return calls, ind, seen


inside = lambda t: any(a <= t < b for a, b in ext)
arm = {}
for op in range(1, 129):
    k = T.rd(IB + 0x29994C + op - 1, 1)[0]
    arm[op] = IB + struct.unpack("<I", T.rd(IB + 0x299854 + 4 * k, 4))[0]
print("== O1/O2 opcode arms of 003B8670 (extent %08X-%08X)" % (lo, hi))
reach_ops = {}
for op in range(1, 129):
    calls, ind, seen = walk(arm[op], STOP, INS, inside)
    r = sorted("%08X" % c for c in calls if GG.tfn(c) in R0)
    if r or ind:
        reach_ops[op] = (r, ind)
for op in sorted(reach_ops):
    print("  op %3d arm %08X reaching callees %s indirect %s" % (op, arm[op], reach_ops[op][0], reach_ops[op][1]))
print("  opcodes with a reaching direct callee: %s" % sorted(op for op, v in reach_ops.items() if v[0]))
print("  opcodes with an indirect call/jmp: %s" % sorted(op for op, v in reach_ops.items() if v[1]))
for op in (5, 6, 9, 25, 26, 39, 41):
    calls, ind, seen = walk(arm[op], STOP, INS, inside)
    print("  c_all opcode %2d arm %08X: callees %s ; reaching %s ; indirect %s" % (
        op, arm[op], sorted("%08X" % c for c in calls), sorted("%08X" % c for c in calls if GG.tfn(c) in R0), ind))

print("== O3 event kinds passed to 002EB740, and 00319F50's kind arms")
for a in sorted(INS):
    i = INS[a]
    if i.mnemonic == "call" and i.operands[0].type == 2 and i.operands[0].imm == 0x002EB740:
        back = [INS[b] for b in sorted(INS) if a - 0x80 <= b < a]
        kv = [("%08X %s %s" % (x.address, x.mnemonic, x.op_str)) for x in back if "[rsp + 0x30]" in x.op_str]
        print("  call 002EB740 at %08X; last [rsp+0x30] writes before it: %s" % (a, kv[-2:]))
F9 = 0x00319F50
ext9 = [(T.IB + b, T.IB + e) for b, e, u in G.PD if G.root(T.IB + b) == F9]
INS9 = {i.address: i for a, b in ext9 for i in T.dis(a, b)}
in9 = lambda t: any(a <= t < b for a, b in ext9)
for k in range(9):
    t = IB + struct.unpack("<I", T.rd(IB + 0x1FA200 + 4 * k, 4))[0]
    calls, ind, seen = walk(t, {0x0031A1D7, 0x0031A1D5, 0x0031A1CE}, INS9, in9)
    print("  kind %d arm %08X: reaching 0030E360 via %s ; indirect %s" % (
        k, t, sorted("%08X" % c for c in calls if GG.tfn(c) in R0K), ind))
print("== C control: opcode 3's arm reaches: %s" % (3 in reach_ops and bool(reach_ops[3][0])))
print("== E5 sample: 0046EFD0's other launches against R0 (none may reach 00312280)")
for t in (0x003A8240, 0x003A8020, 0x003A8AE0, 0x004FF2C0, 0x005372D0, 0x0046EF10, 0x00314960, 0x001EDDA0, 0x0020E600):
    print("  %08X reaches 00312280: %s" % (t, GG.tfn(t) in R0))
print("  control 003B8670 reaches: %s" % (0x003B8670 in R0))
print("== E4 spot check: the c_all path string")
p = struct.unpack("<Q", T.rd(0x01E127B8, 8))[0]
print("  qword 01E127B8 -> %08X : %r" % (p, T.rd(p, 48).split(b"\0")[0]))
