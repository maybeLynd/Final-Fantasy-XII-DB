"""SWE2-AUDIT-SEM T5 check: what the manager's +0x1F0 points at. The allocator 002679F0 sets it after the pool memset
(00267A8B); 0046BAC0 fills it with one dword per qualifying record."""
import img
for x in img.md.disasm(img.rd(0x267A60, 0x60), 0x267A60):
    if x.address <= 0x267AC2:
        print('  %08X %s %s' % (x.address, x.mnemonic, x.op_str))
print('--- 0046BB50..0046BB82 and 0046BD10..0046BD45')
for x in img.md.disasm(img.rd(0x46BB4F, 0x40), 0x46BB4F):
    if x.address <= 0x46BB82:
        print('  %08X %s %s' % (x.address, x.mnemonic, x.op_str))
for x in img.md.disasm(img.rd(0x46BCF0, 0x60), 0x46BCF0):
    if x.address <= 0x46BD45:
        print('  %08X %s %s' % (x.address, x.mnemonic, x.op_str))
