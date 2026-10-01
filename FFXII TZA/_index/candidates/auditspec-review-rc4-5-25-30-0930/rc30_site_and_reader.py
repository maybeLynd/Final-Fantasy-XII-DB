"""SWE2-AUDIT-SPEC independent checks for RC-30 (rc30-cl2-request-bounds-0930), 2026-09-30. Image only.
R1  the 003C208D request: the instructions that form (kind, id) before it.
R2  003C26C0 and the section walker 0024A9E0: every memory operand with displacement in 0x10..0x24 (header fields),
    so an unread +0x22/+0x23 shows as absent. Control: the record's three reads 003C27B0/003C27B4/003C27B7 must appear.
R3  raw callers of 003C26C0 and of 003C1F00.
"""
import sys, json, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
print("R1 003C2040..003C2098:")
for x in tk.dis(0x3C2040, 0x3C2098): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for e in (0x3C26C0, 0x24A9E0):
    seen = []
    for x in tk.fdis(e):
        for k, op in enumerate(x.operands):
            if op.type == X86_OP_MEM and op.mem.base != 0 and 0x10 <= op.mem.disp <= 0x24 and x.reg_name(op.mem.base) not in ("rsp", "rbp"):
                seen.append((x.address, op.mem.disp, op.size, x.mnemonic + " " + x.op_str))
    print("R2 %08X header-range operands: %d" % (e, len(seen)))
    for a, dsp, sz, t in seen: print("  %08X +0x%X w%d | %s" % (a, dsp, sz, t))
    if e == 0x3C26C0:
        print("  CONTROL 003C27B0/003C27B4/003C27B7 present:", {0x3C27B0, 0x3C27B4, 0x3C27B7} <= {a for a, *_ in seen})
        print("  any +0x22/+0x23 operand:", any(dsp in (0x22, 0x23) for _, dsp, _, _ in seen))
for e in (0x3C26C0, 0x3C1F00, 0x24A9E0):
    cs = RAW.get("%X" % e, [])
    print("R3 raw callers of %08X: %d %s" % (e, len(cs), " ".join(cs[:12])))
