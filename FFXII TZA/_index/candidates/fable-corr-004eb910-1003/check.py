"""check.py - executed regression for this correction: what 004EB910 finally stores to floats 02064C18 and 02064C28.
Expected: xmm0 is loaded from 01E02838, then 01E0283C is added (004EBD39 / 004EBD44), and that xmm0, untouched in
between, is stored to both cells (004EBDD6 / 004EBDDE); both source cells are in .data (mutable), with file values
0.0 and 1.0. Control (the defect corrected): the old reading "a constant 1.0 from 01E0283C" must FAIL here, both
because the stored value is a two-cell sum and because the cells are writable data, not .rdata. Prints FAILS N."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
img = Img.load(); img.cs.detail = True
F, N = 0x004EB910, 1387
ins = list(img.cs.disasm(img.read(F, N), F))
by = {i.address: i for i in ins}


def rip(i, k=1):
    op = i.operands[k]
    return i.address + i.size + op.mem.disp if op.type == 3 and op.mem.base == 41 else None


def section(va):
    r = va - img.base
    return next((s[0] for s in img.secs if s[1] <= r < s[1] + max(s[2], s[4])), "?")


fails = 0
def check(name, ok):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", name)); fails += not ok


ld, add = by.get(0x004EBD39), by.get(0x004EBD44)
check("004EBD39 movss xmm0, [01E02838]", ld is not None and ld.mnemonic == "movss" and ld.op_str.startswith("xmm0") and rip(ld) == 0x01E02838)
check("004EBD44 addss xmm0, [01E0283C]", add is not None and add.mnemonic == "addss" and add.op_str.startswith("xmm0") and rip(add) == 0x01E0283C)
st1, st2 = by.get(0x004EBDD6), by.get(0x004EBDDE)
check("004EBDD6 stores xmm0 to 02064C18", st1 is not None and st1.mnemonic == "movss" and rip(st1, 0) == 0x02064C18 and st1.op_str.endswith("xmm0"))
check("004EBDDE stores xmm0 to 02064C28", st2 is not None and st2.mnemonic == "movss" and rip(st2, 0) == 0x02064C28 and st2.op_str.endswith("xmm0"))
between = [i for i in ins if 0x004EBD44 < i.address < 0x004EBDD6]
writes_xmm0 = [i for i in between if i.op_str.split(",")[0].strip() == "xmm0" or i.mnemonic == "call"]
check("xmm0 not written and no call between the add and the stores", not writes_xmm0)
check("01E02838 and 01E0283C are in .data (mutable)", section(0x01E02838) == ".data" and section(0x01E0283C) == ".data")
v0, v1 = struct.unpack("<f", img.read(0x01E02838, 4))[0], struct.unpack("<f", img.read(0x01E0283C, 4))[0]
check("file values 0.0 and 1.0", (v0, v1) == (0.0, 1.0))
# control: the corrected reading must fail this instrument
old_reading_holds = (ld is not None and rip(ld) == 0x01E0283C and add is None) or section(0x01E0283C) == ".rdata"
check("control: 'a constant 1.0 loaded from 01E0283C' is refuted", not old_reading_holds)
print("FAILS %d" % fails)
