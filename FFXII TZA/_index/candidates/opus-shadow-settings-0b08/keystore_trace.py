"""Pair each key string (lea rdx, [rip+str]) with the next float/int store after a getter call, inside one function."""
import pefile, re, struct, sys
from capstone import *
pe = pefile.PE(r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"); img = pe.get_memory_mapped_image(); ib = 0x120000
md = Cs(CS_ARCH_X86, CS_MODE_64)
F, N = int(sys.argv[1], 16), int(sys.argv[2], 16)
def cstr(va):
    o = va - ib
    if not (0 <= o < len(img)): return None
    e = img.find(b"\0", o, o + 80); s = img[o:e]
    return s.decode("latin1") if e > o and all(32 <= c < 127 for c in s) else None
key = None; regsrc = {}; out = []
for i in md.disasm(img[F - ib:F - ib + N], F):
    m = re.search(r"rip \+ (0x[0-9a-f]+)", i.op_str)
    tgt = i.address + i.size + int(m.group(1), 16) if m else None
    if i.mnemonic == "lea" and i.op_str.startswith("rdx") and tgt and cstr(tgt) and cstr(tgt).startswith(("m", "E", "S", "m_")):
        key = cstr(tgt)
    if i.mnemonic in ("mov", "lea") and tgt and re.match(r"^(r\w+),", i.op_str) and not cstr(tgt):
        regsrc[i.op_str.split(",")[0]] = tgt
    if i.mnemonic in ("movss", "mov") and i.op_str.startswith("dword ptr [") and ("xmm" in i.op_str.split(",")[1] or "eax" in i.op_str.split(",")[1]):
        dst = i.op_str.split(",")[0]
        if tgt: where = "%08X" % tgt
        else:
            mm = re.match(r"dword ptr \[(\w+)(?: \+ (0x[0-9a-f]+))?\]", dst)
            if mm and mm.group(1) not in ("rsp", "rbp"):
                base = regsrc.get(mm.group(1)); off = int(mm.group(2) or "0", 16)
                where = ("[%s=%08X]+0x%X" % (mm.group(1), base, off)) if base else ("[%s]+0x%X" % (mm.group(1), off))
            else: where = None
        if where and key:
            out.append(("%08X" % i.address, key, where)); key = None
for r in out: print(*r)
