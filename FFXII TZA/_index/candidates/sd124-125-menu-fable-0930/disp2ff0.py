"""disp2ff0.py - SD-125: every instruction image-wide with displacement 0x2FF0..0x2FF3 (the command-menu widget's +0x2FF0
word), writers flagged. Control: the confirm arm 00276D30 must be found reading it. Also names the SD-124 walk owner."""
import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
d = tk.d; pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    s = pe + 24 + opt + 40 * i
    if d[s:s + 8].rstrip(b"\0") == b".text": vs, va, rs, ro = struct.unpack_from("<IIII", d, s + 8)
blob = d[ro:ro + rs]; BASE = 0x00120000
hits = {}
for disp in range(0x2FF0, 0x2FF4):
    pat = struct.pack("<i", disp); p = blob.find(pat)
    while p >= 0:
        for back in range(2, 12):
            st = p - back
            for x in md.disasm(blob[st:st + 16], BASE + va + st, 1):
                if x.address + x.size >= BASE + va + p + 4 and any(op.type == 3 and op.mem.disp == disp for op in x.operands):
                    hits[x.address] = x
        p = blob.find(pat, p + 1)
ctl = False
for a in sorted(hits):
    x = hits[a]; o, _ = tk.owner(a)
    w = x.operands[0].type == 3 and x.operands[0].mem.disp in range(0x2FF0, 0x2FF4) and x.mnemonic not in ("cmp", "test", "lea", "bt")
    if o == 0x00276D30: ctl = True
    print("%08X %-5s %-6s %-42s in %08X %s" % (a, "WRITE" if w else "", x.mnemonic, x.op_str, o, tk.fname(o)[:40]))
print("CONTROL 00276D30 reads it:", "PASS" if ctl else "FAIL")
print("SD-124 walk owner of 0035BDB0:", tk.fname(tk.owner(0x0035BDB0)[0]))
