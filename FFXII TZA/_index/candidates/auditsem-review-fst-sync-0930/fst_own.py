"""SWE2-AUDIT-SEM FST-SYNC check (own code): 001A0BB0's two arms, the r8 each constructor passes, and whether any
branch lands between the r8 write and the call (which would let another r8 value reach the call).
Discrimination test: the producer's C2 expectation ('mov r8b, 1') applied to 001D6D90, and C3's ('xor r8d, r8d')
applied to 001D6FB0, must both fail."""
import img

def body(lo, n):
    out = []
    for x in img.md.disasm(img.rd(lo, n), lo):
        out.append(x)
        if x.mnemonic == "ret":
            break
    return out

q = body(0x001A0BB0, 0x100)
for x in q[:18]:
    print("Q %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for f, n in ((0x001D6FB0, 0x100), (0x001D6D90, 0x100)):
    b = body(f, n)
    call = next(x for x in b if x.mnemonic == "call" and x.op_str == "0x1a0bb0")
    w = [x for x in b if x.address < call.address and x.op_str.split(",")[0].strip() in ("r8", "r8d", "r8b")][-1]
    landing = [x for x in b if x.mnemonic.startswith("j") and x.op_str.startswith("0x")
               and w.address < int(x.op_str, 16) <= call.address]
    print("F %08X: last r8 write %08X %s %s; call %08X; branches landing between: %s" % (
        f, w.address, w.mnemonic, w.op_str, call.address, [("%08X" % x.address) for x in landing] or "none"))
    for want in ("mov r8b, 1", "xor r8d, r8d"):
        print("   expectation %-14s -> %s" % (want, "MATCH" if "%s %s" % (w.mnemonic, w.op_str) == want else "no match"))
