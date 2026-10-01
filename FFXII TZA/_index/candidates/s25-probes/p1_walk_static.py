"""P1 (static) - what the gambit walk 00305CC0 itself stores, and how often it reads the unit
fields a stubbed commit would write.

Question: can the commit stub's SKIPPED writes (0030F760 stores unit+0x708/+0x710/+0x714 at
0030F7F9/0030F800/0030F806) feed anything the walk decides after the commit call?
Method: capstone over the whole body (422 B, functions.tsv), list every memory WRITE with its base
register, every read of [r13+0x708] / [r13+0x714] (r13 = unit, 00305CC9), and every read of the
subgroup count byte through r12.
"""
import os, sys
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import reg_tracking as RT
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, read
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE, CS_AC_READ
from capstone.x86 import X86_OP_MEM

WALK, SIZE = 0x305CC0, 422
raw, secs = load()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
code = read(raw, secs, WALK, SIZE)
writes, reads708, reads714, count_reads, calls = [], [], [], [], []
for ins in md.disasm(code, WALK):
    for oi, op in enumerate(ins.operands):
        if op.type != X86_OP_MEM:
            continue
        kind = RT.op_kind(ins, op, oi)  # shared policy (OPUS 2026-09-28)
        base = ins.reg_name(op.mem.base) if op.mem.base else "-"
        idx = ins.reg_name(op.mem.index) if op.mem.index else "-"
        disp = op.mem.disp
        if kind in ("w", "rw"):
            writes.append((ins.address, ins.mnemonic, ins.op_str, base))
        if kind in ("r", "rw"):
            if base == "r13" and disp == 0x708:
                reads708.append((ins.address, ins.op_str))
            if base == "r13" and disp == 0x714:
                reads714.append((ins.address, ins.op_str))
            if base == "r12" and disp == 0 and idx == "-":
                count_reads.append((ins.address, ins.op_str))
    if ins.mnemonic == "call":
        calls.append((ins.address, ins.op_str))

print("walk 00305CC0, %d bytes" % SIZE)
print("memory WRITES (address, insn, base reg):")
for a, m, o, b in writes:
    print("  %08X  %-6s %-40s base=%s" % (a, m, o, b))
nonstack = [w for w in writes if w[3] != "rsp"]
print("non-stack writes: %d" % len(nonstack))
print("reads of [r13+0x708] (unit ctx): %d -> %s" % (len(reads708), ["%08X" % a for a, _ in reads708]))
print("reads of [r13+0x714] (latched word): %d -> %s" % (len(reads714), ["%08X" % a for a, _ in reads714]))
print("reads of count byte [r12]: %d -> %s" % (len(count_reads), ["%08X" % a for a, _ in count_reads]))
print("calls: %s" % ["%08X->%s" % (a, o) for a, o in calls])
first_call = min(a for a, _ in calls)
print("every +0x708/+0x714 read precedes the first call (%08X): %s" % (
    first_call, all(a < first_call for a, _ in reads708 + reads714)))
print("count-byte reads after the eval/commit calls (in-loop re-read): %s" % (
    ["%08X" % a for a, _ in count_reads if a > first_call]))
