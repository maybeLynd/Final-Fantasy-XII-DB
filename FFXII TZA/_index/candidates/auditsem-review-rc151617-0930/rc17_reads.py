"""SWE2-AUDIT-SEM RC-17 re-read: the skipexec handler 0034ECF0, the skip begin 00360710's head, the manager-index
copy in ActorStorage_InitializeRecord (00266550.. 00266616/00266624), and every byte store at +0x15 in that function."""
import img
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("== 0034ECF0"); show(0x0034ECF0, 0x0034ED10)
print("== 00360710 head"); show(0x00360710, 0x00360770)
print("== 00266550..00266630 (rcx/manager flow and the +0x15 store)")
for x in img.md.disasm(img.rd(0x00266550, 0xF0), 0x00266550):
    if x.address > 0x00266630:
        break
    if "0x15" in x.op_str or "0x28" in x.op_str or x.address in (0x00266561,) or "rcx" in x.op_str.split(",")[-1]:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
