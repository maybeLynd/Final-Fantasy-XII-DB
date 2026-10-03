"""check.py : SWE2-EC7 control for the 00360C70 argument-order correction (record swe2ec7-corr-00360c70-args-1003).
Decodes 00360CA1..00360CA9 from the certified image and reports the immediates loaded into edx and ecx before the call to
0032E400, and decodes 0032E400's first instructions to show ecx indexes the 022C51F0 group table and edx the entry. Passes only
if the call is 0032E400(ecx=9, edx=6) AND the swapped reading (6, 9) - the page's old text - is refused."""
import hashlib, re, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8", "image hash"
pe = pefile.PE(data=raw)
md = Cs(CS_ARCH_X86, CS_MODE_64)


def code(va, n):
    return pe.get_data(va - 0x120000, n)


regs = {}
call = None
for i in md.disasm(code(0x360CA1, 0x10), 0x360CA1):
    m = re.match(r"(e\w\w), (0x[0-9a-f]+|\d+)$", i.op_str)
    if i.mnemonic == "mov" and m:
        regs[m.group(1)] = int(m.group(2), 0)
    m = re.match(r"(e\w\w), \[r(\w\w) \+ (0x[0-9a-f]+|\d+)\]$", i.op_str)
    if i.mnemonic == "lea" and m:
        regs[m.group(1)] = regs["e" + m.group(2)] + int(m.group(3), 0)
    if i.mnemonic == "call":
        call = int(i.op_str, 16); break
lead = [(i.mnemonic, i.op_str) for i in md.disasm(code(0x32E400, 0x30), 0x32E400)][:10]
print("call target %s, ecx=%s, edx=%s" % (hex(call or 0), regs.get("ecx"), regs.get("edx")))
print("0032E400 lead:", "; ".join("%s %s" % x for x in lead))
group_from_ecx = any(m == "movsxd" and "ecx" in o for m, o in lead) and any("0x400" in o and "rdx" in o for m, o in lead)


def accepts(ecx, edx):
    return call == 0x32E400 and regs.get("ecx") == ecx and regs.get("edx") == edx and group_from_ecx


ok = accepts(9, 6) and not accepts(6, 9)
print("corrected reading (ecx=9 group, edx=6 entry): %s; old reading (6, 9): %s" % (accepts(9, 6), accepts(6, 9)))
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
