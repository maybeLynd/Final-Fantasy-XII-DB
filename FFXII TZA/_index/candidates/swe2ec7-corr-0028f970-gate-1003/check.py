"""check.py : SWE2-EC7 control for the 0028F970 correction (record swe2ec7-corr-0028f970-gate-1003). Decodes 0028F970 from the
certified image and reports (1) what `bt ecx, 0xd` is followed by - `jb` to the epilogue means a SET bit 13 returns early, so the
body proceeds only when it is clear; (2) the rip target of the load that forms `rcx` for the `00273A20` call. Passes only if the
corrected reading holds (jb to the epilogue; rcx from [0209BE80]) AND the page's old reading ('requires bit 0x2000', i.e. a jae
early-out; and [0209BE78]) is refused."""
import hashlib, re, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8", "image hash"
pe = pefile.PE(data=raw)
md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = list(md.disasm(pe.get_data(0x28F970 - 0x120000, 0x70), 0x28F970))
ret_at = next(i.address for i in ins if i.mnemonic == "ret")
epilogue = ret_at - 4                                   # add rsp, 0x28 / ret
k = next(n for n, i in enumerate(ins) if i.mnemonic == "bt" and i.op_str == "ecx, 0xd")
after_bt = ins[k + 1]
call_i = next(n for n, i in enumerate(ins) if i.mnemonic == "call" and i.op_str == "0x273a20")
rcx_src = None
for i in reversed(ins[:call_i]):
    m = re.match(r"rcx, qword ptr \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
    if i.mnemonic == "mov" and m:
        rcx_src = i.address + i.size + int(m.group(1), 16); break
print("after bt ecx,0xd: %s %s (epilogue %08X); rcx for 00273A20 from [%08X]" % (after_bt.mnemonic, after_bt.op_str, epilogue, rcx_src or 0))


def accepts(early_out_mnemonic, cell):
    return after_bt.mnemonic == early_out_mnemonic and int(after_bt.op_str, 16) == epilogue and rcx_src == cell


ok = accepts("jb", 0x0209BE80) and not accepts("jae", 0x0209BE80) and not accepts("jb", 0x0209BE78)
print("corrected (set bit returns; [0209BE80]): %s; old 'requires the bit': %s; old cell [0209BE78]: %s"
      % (accepts("jb", 0x0209BE80), accepts("jae", 0x0209BE80), accepts("jb", 0x0209BE78)))
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
