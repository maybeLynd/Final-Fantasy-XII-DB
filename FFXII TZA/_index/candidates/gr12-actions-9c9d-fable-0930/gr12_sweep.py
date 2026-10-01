"""gr12_scan.py - image-wide: instructions whose immediate is 0x9C / 0x9D (cmp / mov / sub / lea disp), and byte reads
of +0x1E followed within 3 instructions by a compare with 0xD. Linear sweep of .text (capstone skips bad bytes)."""
import struct, sys, re
import capstone
import os
EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; o = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(n):
    s = pe + 24 + o + 40 * i
    if d[s:s + 5] == b".text":
        vsz, va, rsz, raw = struct.unpack_from("<IIII", d, s + 8)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.skipdata = True
hits_imm, hits_cat = [], []
win = []
for ins in md.disasm(d[raw:raw + rsz], BASE + va):
    t = ins.op_str
    m = ins.mnemonic
    if re.search(r"(?<![0-9a-fx])0x9[bcd](?![0-9a-f])", t) and "rsp" not in t and "rbp" not in t and "rip" not in t and m not in ("call","jmp") and not m.startswith("j"):
        hits_imm.append("%08X %s %s" % (ins.address, m, t))
    win.append(ins); win = win[-4:]
    if m == "cmp" and t.endswith(", 0xd"):
        for w in win[:-1]:
            if "+ 0x1e]" in w.op_str and "byte" in w.op_str:
                hits_cat.append("%08X %s %s  <- %08X %s %s" % (ins.address, m, t, w.address, w.mnemonic, w.op_str)); break
print("imm 0x9C/0x9D sites:", len(hits_imm))
for h in hits_imm: print("  " + h)
print("+0x1E == 0xD tests:", len(hits_cat))
for h in hits_cat: print("  " + h)
