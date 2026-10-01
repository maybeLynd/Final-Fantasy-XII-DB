"""ctx.py START SITE [before] [after] - boundary-true decode from START, print the window around SITE."""
import sys
from img import dis

s, a = int(sys.argv[1], 16), int(sys.argv[2], 16)
b = int(sys.argv[3]) if len(sys.argv) > 3 else 25
f = int(sys.argv[4]) if len(sys.argv) > 4 else 6
ins = dis(s, a + 0x60)
k = [n for n, i in enumerate(ins) if i.address <= a < i.address + i.size]
k = k[0] if k else len(ins) - 1
for i in ins[max(0, k - b):k + f]:
    print("%s%08X %-7s %s" % ("> " if i.address == ins[k].address else "  ", i.address, i.mnemonic, i.op_str))
