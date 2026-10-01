"""sr5_routes.py - the three routes out of SebController_PlayByBankBlock's bank walk (FABLE, Claude Opus 5.5, 2026-09-27;
on ASTRA-RETURN-FABLE-SR5-EXHAUSTION-TRIGGER). Static.

  R1 empty list: 0021B5F1 cmp rcx, rbx / 0021B5F4 je 0021B621 - straight to the epilogue, never at 0021B608.
  R2 non-empty miss: the loop's 0021B606 jne falls through to 0021B608 jmp 0021B621.
  R3 match: 0021B5FE je 0021B60A, callback 0021B61A, 0021B61F mov eax, esi.
  R4 between the receipt call 0021B5E2 and the epilogue, eax is written only at 0021B61F, so both miss routes return
     the receipt. Planted negative: the empty-route target must NOT be 0021B608.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
ins = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x21B5E2):off(0x21B621)], 0x21B5E2)]
m = {a: ("%s %s" % (mn, o)).strip() for a, mn, o in ins}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
check("R1 the empty list bypasses 0021B608", m.get(0x21B5F1) == "cmp rcx, rbx" and m.get(0x21B5F4) == "je 0x21b621"
      and m.get(0x21B5F4) != "je 0x21b608")
check("R2 the non-empty miss falls through to 0021B608", m.get(0x21B606) == "jne 0x21b5f6" and m.get(0x21B608) == "jmp 0x21b621")
check("R3 the match calls back and restores eax", m.get(0x21B5FE) == "je 0x21b60a" and m.get(0x21B61A) == "call 0x224540"
      and m.get(0x21B61F) == "mov eax, esi")
w = [a for a, mn, o in ins if a > 0x21B5E2 and o.split(",")[0].strip() in ("eax", "rax") and mn not in ("cmp", "test")]
check("R4 eax is written only at 0021B61F after the receipt call", w == [0x21B61F], str(["%08X" % a for a in w]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
