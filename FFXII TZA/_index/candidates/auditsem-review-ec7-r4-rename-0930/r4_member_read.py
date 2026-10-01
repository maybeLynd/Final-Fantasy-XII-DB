"""SWE2-AUDIT-SEM: read member 00611A10 (44 B) and its constructor callee's first instructions."""
import re
import img
xs = img.dis(0x00611A10, 20)
for x in xs:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
calls = [int(x.op_str, 16) for x in xs if x.mnemonic in ("call", "jmp") and re.fullmatch(r"0x[0-9a-f]+", x.op_str)]
for c in calls[:1]:
    print(" callee %08X:" % c)
    for x in img.dis(c, 14):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
