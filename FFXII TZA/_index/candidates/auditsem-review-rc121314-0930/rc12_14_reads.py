"""SWE2-AUDIT-SEM: the four spans read by hand for RC-12 (the wait resolver's slot read, the generic accessor 00263D40)
and RC-14 (the two promoter loops 003DB1F0 / 003DBBF0)."""
import img
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print('  %08X %s %s' % (x.address, x.mnemonic, x.op_str))
print('== 0025E150..0025E18C (wait resolver slot read)'); show(0x25E150, 0x25E18C)
print('== 00263D40 (generic accessor)'); show(0x263D40, 0x263DB0)
print('== 003DB1F0 promoter'); show(0x3DB1F0, 0x3DB265)
print('== 003DBC70 promoter'); show(0x3DBC70, 0x3DBCC0)
