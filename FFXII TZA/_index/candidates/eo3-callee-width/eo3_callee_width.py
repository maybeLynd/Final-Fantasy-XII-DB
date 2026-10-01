"""eo3_callee_width.py - EO-3 callee 0036C140: writes RAX (full, at 0036C17C) / EAX, RCX, RDX and globals, never RDI;
spins at 0036C150 when its depth is not positive (FABLE, Claude Opus 5.5, 2026-09-26). Static.
Sensitivity: a synthetic 'mov edi, eax' appended to the body is detected by the same RDI-family test."""
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
body = d[off(0x36C140):off(0x36C140) + 0x54]
ins = list(cs.disasm(body, 0x36C140))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
DI = ("rdi", "edi", "di", "dil")
def writes_rdi(L): return [x for x in L if x.op_str.split(",")[0].strip() in DI and x.mnemonic not in ("cmp", "test", "push")]
s = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in ins}
check("C1 0036C17C loads the full RAX", s.get(0x36C17C) == "mov rax, qword ptr [rdx + rcx*8 + 8]")
check("C2 no instruction writes RDI/EDI and there is no call", not writes_rdi(ins) and not any(x.mnemonic == "call" for x in ins))
check("C3 a non-positive depth spins at 0036C150", s.get(0x36C148) == "jg 0x36c152" and s.get(0x36C150) == "jmp 0x36c150")
mut = list(cs.disasm(body[:-1] + b"\x89\xc7\xc3", 0x36C140))
check("C4 sensitivity: a synthetic mov edi, eax is detected", bool(writes_rdi(mut)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
