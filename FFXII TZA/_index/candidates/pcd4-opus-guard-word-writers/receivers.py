import pefile, hashlib, re
from capstone import *
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
raw = open(EXE, "rb").read(); assert hashlib.sha256(raw).hexdigest().startswith("73461d08")
pe = pefile.PE(data=raw); img = pe.get_memory_mapped_image(); ib = 0x120000
md = Cs(CS_ARCH_X86, CS_MODE_64)
CASES = [(0x266530, 0x26668B, "rbx"), (0x3AAA50, 0x3AAB9D, "rbp"), (0x41B550, 0x41B585, "rcx"), (0x552250, 0x5526B9, "rax"),
         (0x5528C0, 0x552BB8, "rdi"), (0x269F40, 0x269F48, "rcx"), (0x639290, 0x6392F0, "rbx")]
for f, site, reg in CASES:
    ins = list(md.disasm(img[f - ib:site - ib + 16], f))
    upto = [i for i in ins if i.address < site]
    setters = [i for i in upto if re.match(r"^%s\b" % reg, i.op_str) and i.mnemonic in ("mov", "lea", "add", "sub", "movsxd", "movzx", "xor")]
    tail = setters[-3:]
    rip = []
    for i in upto:
        m = re.search(r"rip \+ (0x[0-9a-f]+)", i.op_str)
        if m and i.mnemonic in ("lea", "mov"):
            rip.append("%08X" % (i.address + i.size + int(m.group(1), 16)))
    print("%08X site %08X base %s | last setters: %s | rip refs: %s" % (f, site, reg, [("%08X %s %s" % (i.address, i.mnemonic, i.op_str)) for i in tail], sorted(set(rip))[:8]))
