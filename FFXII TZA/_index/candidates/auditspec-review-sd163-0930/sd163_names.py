"""sd163_names.py - SWE2-AUDIT-SPEC (SD-163 review, 2026-09-30). The action-name tables 00792B70 fetches handles for:
digital names at 01F40210 (16 qword pointers, handle -> 02EA9510 + 8k, loop bound 0x80) and analog names at
01F40290 (2 pointers, handle -> 02EA9590 + 8k, loop bound 0x10), both addressed image-base-relative (rbp = 0x120000).
Prints each handle cell, its name, and the device byte / dword 007A1CD0 stores that handle's state to
(pairs copied from sd163_indep.out section A, hard-coded below and re-checked by that script).
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402


def cstr(va):
    b = T.rd(va, 64)
    return b.split(b"\0", 1)[0].decode("latin-1")


# (handle cell -> device field) from sd163_indep.out section A
STORE = {0x02EA9548: 0x43F, 0x02EA9530: 0x43E, 0x02EA9538: 0x43D, 0x02EA9540: 0x43C, 0x02EA9550: 0x440,
         0x02EA9568: 0x441, 0x02EA9558: 0x442, 0x02EA9570: 0x443, 0x02EA9588: 0x444, 0x02EA9580: 0x445,
         0x02EA9560: 0x446, 0x02EA9578: 0x447, 0x02EA9510: 0x448, 0x02EA9528: 0x449, 0x02EA9518: 0x44A,
         0x02EA9520: 0x44B}
rows = []
for k in range(16):
    p = struct.unpack("<Q", T.rd(0x01F40210 + 8 * k, 8))[0]
    cell = 0x02EA9510 + 8 * k
    rows.append((STORE[cell], cell, p, cstr(p)))
    print("digital  %08X  name@%08X %-10s -> device +0x%03X" % (cell, p, cstr(p), STORE[cell]))
for k in range(2):
    p = struct.unpack("<Q", T.rd(0x01F40290 + 8 * k, 8))[0]
    print("analog   %08X  name@%08X %s" % (0x02EA9590 + 8 * k, p, cstr(p)))
print("device byte order +0x43C..+0x44B: %s" % " ".join(n for f, c, p, n in sorted(rows)))
