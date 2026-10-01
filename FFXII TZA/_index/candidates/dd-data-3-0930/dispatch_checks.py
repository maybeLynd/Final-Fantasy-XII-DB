"""the-text-element-dispatch-table (DD batch 3, SWE2-DATA 2026-09-30), static.

D1 002B3400 stamps kind 2 at 002B3470 on every path; the 00254A10 test (002B342B..002B3432) gates only the branch that
   sets flag 0x800 and resolves +0x60 when byte +0xA6 is 7 (002B3434..002B3452).
D2 00254A10 returns 1 when bit (mode) of 0xD81 is set, mode = 00229E40() = the dword at 01E02814, whose .data initial
   value is 0x0A - bit 10 is set, so with that value the predicate is 1 and the +0xA6 == 7 branch is skipped.
D3 002DD680, which follows 002B3400 at two of the not-'ex' sites, calls the byte-charset renderer 002B0280 (002DD784).
C1 control: the handler table at 009164C0 (kind * 24 + column * 8) has kind 2's three slots null and kind 0's column 0
   = 002A9980, as the page's §3 table states.
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis, section  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


a = {x.address: x for x in dis(0x002B3400)}
check("D1 kind-2 stamp is unconditional; 00254A10 gates only the +0xA6 == 7 branch",
      a[0x002B342B].op_str == "0x254a10" and a[0x002B3432].op_str == "0x2b3456"
      and a[0x002B3434].op_str == "byte ptr [rdi + 0xa6], 7" and a[0x002B343D].op_str == "dword ptr [rdi + 0x44], 0x800"
      and a[0x002B3470].op_str == "byte ptr [rdi + 0xa3], 2"
      and all(x.address < 0x002B3456 for x in a.values() if x.op_str.startswith("0x2b3470")))
p = {x.address: x for x in dis(0x00254A10)}
g = dis(0x00229E40)[0]
m = re.search(r"\[rip \+ 0x([0-9a-f]+)\]", g.op_str)
cell = g.address + g.size + int(m.group(1), 16)
init = struct.unpack_from("<I", d, off(cell))[0]
check("D2 mode = dword 01E02814 (.data initial 0x0A); 0xD81 has bit 10 set, so the predicate is 1",
      cell == 0x01E02814 and section(cell) == ".data" and init == 0x0A and p[0x00254A1E].op_str == "ecx, 0xd81"
      and p[0x00254A23].op_str == "ecx, eax" and (0xD81 >> init) & 1 == 1, "%08X %s 0x%X" % (cell, section(cell), init))
c = [x.address for x in dis(0x002DD680) if x.mnemonic == "call" and x.op_str == "0x2b0280"]
check("D3 002DD680 calls 002B0280", c == [0x002DD784], str(["%08X" % v for v in c]))
T = 0x009164C0
row = lambda k: [struct.unpack_from("<Q", d, off(T + k * 24 + i * 8))[0] for i in range(3)]
check("C1 control: kind 2's row is null and kind 0's column 0 is 002A9980",
      row(2) == [0, 0, 0] and row(0)[0] == 0x002A9980, " ".join("%X" % v for v in row(0)))
print("RESULT the kind-2 stamp is unconditional (the region predicate gates a resource branch), and 002DD680 hands "
      "kind-2 text to 002B0280")
print("FAILS %d" % FAILS)
