"""check.py : SWE2-EC7 control for the 002FEAD0 bit-20 polarity correction (record swe2ec7-corr-002fead0-bit20-1003).
Executes the original zero-path bytes 002FEB24..ret under Unicorn on a planted unit record, over mask / +0xEA9 / +0x6B6 cases,
and compares bit 20 of [unit+4] with two models:
  CORRECTED : set iff some set mask bit i (0..31) has i != byte[+0xEA9], or bit byte[+0xEA9] is set and byte[+0x6B6] == 0
  OLD (page): set iff the bit whose index equals byte[+0xEA9] is set and byte[+0x6B6] != 0; all other cases clear
Passes only if CORRECTED matches every case AND OLD mismatches at least one (the control is sensitive to the defect).
System python (unicorn, pefile). Certified image SHA256 73461D08...21F8 is asserted."""
import hashlib, struct, sys
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RBX, UC_X86_REG_RSP, UC_X86_REG_RCX

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash"
pe = pefile.PE(data=raw)
BASE = 0x120000
text = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"][0]
TVA = BASE + text.VirtualAddress
code = text.get_data()
START, RETS = 0x2FEB24, {0x2FEB23, 0x2FEB66, 0x2FEB7B}
UNIT, STACK = 0x10000000, 0x20000000


def run(mask, ea9, b6b6, pre4):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(TVA & ~0xFFF, (len(code) + 0x2000) & ~0xFFF)
    mu.mem_write(TVA, code)
    mu.mem_map(UNIT, 0x2000)
    mu.mem_map(STACK, 0x10000)
    mu.mem_write(UNIT + 4, struct.pack("<I", pre4))
    mu.mem_write(UNIT + 0xEA4, struct.pack("<I", mask))
    mu.mem_write(UNIT + 0xEA9, bytes([ea9]))
    mu.mem_write(UNIT + 0x6B6, bytes([b6b6]))
    mu.reg_write(UC_X86_REG_RBX, UNIT)
    mu.reg_write(UC_X86_REG_RCX, 0xDEAD)            # the body zeroes ecx itself (002FEB2B)
    mu.reg_write(UC_X86_REG_RSP, STACK + 0x8000)
    hit = []

    def hook(uc, addr, size, _):
        if addr in RETS:
            hit.append(addr); uc.emu_stop()
    mu.hook_add(UC_HOOK_CODE, hook)
    mu.emu_start(START, 0x2FEB7C, count=2000)
    assert hit, "no return reached"
    return (struct.unpack("<I", bytes(mu.mem_read(UNIT + 4, 4)))[0] >> 20) & 1, struct.unpack("<I", bytes(mu.mem_read(UNIT + 4, 4)))[0]


def corrected(mask, ea9, b6b6):
    if any(mask >> i & 1 and i != ea9 for i in range(32)):
        return 1
    return 1 if (ea9 < 32 and mask >> ea9 & 1 and b6b6 == 0) else 0


def old(mask, ea9, b6b6):
    return 1 if (ea9 < 32 and mask >> ea9 & 1 and b6b6 != 0) else 0


cases = []
for mask in (0, 1 << 5, 1 << 7, (1 << 5) | (1 << 7), 0xFFFFFFFF, 1 << 31):
    for ea9 in (5, 7, 31, 40):
        for b6b6 in (0, 1):
            for pre4 in (0, 0xFFFFFFFF):
                cases.append((mask, ea9, b6b6, pre4))
bad = oldmiss = 0
for mask, ea9, b6b6, pre4 in cases:
    got, word = run(mask, ea9, b6b6, pre4)
    assert word & ~(1 << 20) == pre4 & ~(1 << 20), "other bits of [unit+4] changed"
    if got != corrected(mask, ea9, b6b6):
        bad += 1; print("CORRECTED MISMATCH", hex(mask), ea9, b6b6, got)
    if got != old(mask, ea9, b6b6):
        oldmiss += 1
print("cases %d: corrected model mismatches %d; old page wording mismatches %d" % (len(cases), bad, oldmiss))
ok = bad == 0 and oldmiss > 0
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
