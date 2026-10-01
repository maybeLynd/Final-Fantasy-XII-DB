"""SWE2-AUDIT-SEM BIT46 checks: the set, the guarded clear and the bit-30 arm in 00304850; the leader test in
0023B040; and the battle-unit slot pool's two whole-unit memsets (free 002342CE, allocate 002344D2), which clear the
flag qword (bit 46 included) at a slot's lifetime boundaries."""
import img
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("set"); show(0x00304EF3, 0x00304F00)
print("bit-30 arm and guarded clear"); show(0x00304F62, 0x00304FAD)
print("leader test"); show(0x0023B0D4, 0x0023B0ED)
print("slot free memset"); show(0x002342C3, 0x002342D6)
print("slot allocate memset"); show(0x002344C7, 0x002344DA)
