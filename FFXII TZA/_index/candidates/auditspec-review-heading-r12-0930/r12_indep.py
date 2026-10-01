"""r12_indep.py - SWE2-AUDIT-SPEC independent re-derivation for heading-r12-restore-0930 (2026-09-30). Static, read-only.

Independent of the author's decoder (which reads through rc9_channels.at and walks only direct branches):
  A  extent: listed size vs .pdata range of 00533B20; count indirect jmp/call-through-register inside the reached set.
  B  every instruction in the reached set that writes any R12 width (capstone regs_access), incl. xchg/pop/cmov.
  C  path check with a DIFFERENT method: forward dataflow "R12 holds caller value" (bool lattice, AND at joins) from the
     entry; a write kills it, `mov r12,[rsp+0x390]` restores it only if slot 0x390 still holds the spill (tracked as a
     second bool: slot-valid, set by the spill, killed by any direct rsp-based store overlapping 0x390).
     Verdict = value at every RET.
  D  aliasing exposure: every `lea reg,[rsp+d]` in the body (a pointer into the frame that a callee could write through),
     with d, so the reader can see whether 0x390 lies above a passed buffer.
  E  caller side: 004607C0 zeroes r12d at 00460A5B, 00533B20 called at 00460A9A/00460AB6/00460AC5, compare at 00460ACA;
     and any R12 write between 00460A5B and 00460ACA other than the calls.
  K  sensitivity control: the same dataflow with the reload removed (treated as a nop) must end R12=clobbered at RET.
"""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
import capstone
from capstone import x86 as X

F = 0x00533B20
md = tk.md
R12 = {"r12", "r12d", "r12w", "r12b"}

def dec(a):
    o = tk.off(a)
    return next(md.disasm(tk.d[o:o + 16], a, 1), None)

def succ(i):
    n = i.address + i.size
    m = i.mnemonic
    if m.startswith("ret"): return []
    if m == "jmp":
        op = i.operands[0]
        return [op.imm] if op.type == X.X86_OP_IMM else ["IND"]
    if m.startswith("j") or m.startswith("loop"):
        op = i.operands[0]
        return [n, op.imm] if op.type == X.X86_OP_IMM else [n, "IND"]
    if m == "int3" : return []
    return [n]

ins = {}; work = [F]; ind = []; leave = []
own, how = tk.owner(F)
size = tk.fsize(F)
while work:
    a = work.pop()
    if a in ins: continue
    i = dec(a)
    if i is None: continue
    ins[a] = i
    for t in succ(i):
        if t == "IND": ind.append(a); continue
        if not (F <= t < F + size): leave.append((a, t)); continue
        work.append(t)
pd = [p for p in tk.pdata if p[0] <= F < p[1]]
print("A listed size %d; pdata %s; reached %d insns; indirect jmp/jcc %s; direct edges leaving body %s" % (
    size, ["%08X-%08X" % (p[0], p[1]) for p in pd], len(ins), ["%08X" % x for x in ind], [("%08X" % a, "%08X" % t) for a, t in leave]))
icall = [a for a, i in ins.items() if i.mnemonic == "call" and i.operands[0].type != X.X86_OP_IMM]
print("A indirect calls in body: %d" % len(icall))

def wr12(i):
    try: _, w = i.regs_access()
    except capstone.CsError: return False
    return any(md.reg_name(x) in R12 for x in w)
W = sorted(a for a, i in ins.items() if wr12(i))
print("B instructions writing an R12 width: %s" % ["%08X %s %s" % (a, ins[a].mnemonic, ins[a].op_str) for a in W])

def is_spill(i):
    return i.mnemonic == "mov" and i.op_str == "qword ptr [rsp + 0x390], r12"
def is_reload(i):
    return i.mnemonic == "mov" and i.op_str == "r12, qword ptr [rsp + 0x390]"
def slot_store(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and (op.access & capstone.CS_AC_WRITE) and md.reg_name(op.mem.base) == "rsp" and op.mem.index == 0:
            if op.mem.disp <= 0x390 < op.mem.disp + op.size or 0x390 <= op.mem.disp < 0x398: return True
    return False

def flow(skip_reload=False):
    # state: (r12_is_caller, slot_holds_caller); lattice AND at joins; start (True, False)
    st = {F: (True, False)}; work = [F]
    while work:
        a = work.pop(); i = ins[a]; r, s = st[a]
        if is_spill(i): s = r
        elif is_reload(i) and not skip_reload: r = s
        elif wr12(i): r = False
        if slot_store(i) and not is_spill(i): s = False
        for t in succ(i):
            if t == "IND" or t not in ins: continue
            new = (r, s) if t not in st else (st[t][0] and r, st[t][1] and s)
            if st.get(t) != new:
                st[t] = new; work.append(t)
    rets = [a for a, i in ins.items() if i.mnemonic.startswith("ret")]
    return {"%08X" % a: st.get(a) for a in rets}
print("C dataflow at RET (r12_is_caller, slot_holds_caller): %s" % flow())
print("K control, reload treated as nop: %s" % flow(True))
spills = ["%08X" % a for a, i in ins.items() if is_spill(i)]
reloads = ["%08X" % a for a, i in ins.items() if is_reload(i)]
others = ["%08X %s" % (a, i.op_str) for a, i in ins.items() if slot_store(i) and not is_spill(i)]
print("C spill %s reload %s other direct stores covering +0x390 %s" % (spills, reloads, others))
leas = sorted((i.operands[1].mem.disp, a) for a, i in ins.items() if i.mnemonic == "lea" and md.reg_name(i.operands[1].mem.base) == "rsp")
print("D lea reg,[rsp+d]: %d sites; displacements %s" % (len(leas), sorted(set("%#x" % d for d, _ in leas))))
print("D lea nearest below 0x390: %s" % [("%#x" % d, "%08X" % a) for d, a in leas if d <= 0x390][-3:])
rsp = ["%08X %s %s" % (a, i.mnemonic, i.op_str) for a, i in ins.items() if i.operands and i.operands[0].type == X.X86_OP_REG and md.reg_name(i.operands[0].reg) == "rsp" and i.mnemonic not in ("push", "pop", "call", "ret")]
print("C explicit RSP writes: %s" % rsp)
# E caller side
body = tk.dis(0x00460A40, 0x00460AE0)
for i in body:
    if 0x00460A5B <= i.address <= 0x00460ACA and (wr12(i) or i.mnemonic == "call" or "r12" in i.op_str):
        print("E %08X %s %s" % (i.address, i.mnemonic, i.op_str))
rc = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
print("E raw callers of 00533B20: %s" % rc.get("533B20"))
