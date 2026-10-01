"""gr1315_fwd.py - the message-26 forward hop (002D2DB0 -> procedure of [control + 0xC8]) for the shop's list control.

Prints: every store to +0xC8 / +0xD8 / +0x120 in the driver's bodies and in the helpers the driver calls on its
control (whole .pdata extents), and every store to +0xC8 image-wide whose instruction also sits in a function that
installs 002D2DB0 (002D14E0) - i.e. who sets a list control's forward target."""
import os, sys, struct, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import gr1315_q2 as Q  # noqa: E402  (decode(), root(), CHUNKS)
from capstone import CS_OP_MEM

FUNCS = [0x0056D370, 0x0056C490, 0x0056C850, 0x0056CA60, 0x0056D9D0, 0x0029FB50, 0x002D14E0, 0x002D2DB0, 0x002432B0]
for f in FUNCS:
    ins, order = Q.decode(f)
    print("== %08X (%d instructions)" % (f, len(order)))
    for a in order:
        i = ins[a]
        if i.operands and i.operands[0].type == CS_OP_MEM and i.operands[0].mem.disp in (0xC8, 0xD8, 0x120, 0xC0) \
                and i.mnemonic.startswith(("mov", "and", "or")):
            print("  %08X %s %s" % (a, i.mnemonic, i.op_str))
