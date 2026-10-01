"""alloc.py - OV-26, the allocation-failure half, at the owner setup (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  A  THE ALLOCATOR 0036A100 tries the current arena (0036BC60), then a fallback (0036BFE0), and returns NULL when both fail
  T  THE TAGGED WRAPPER 003AB8B0 selects arena 6 and, for mode 0, returns 0036A100's result unchanged
  C  THE COPY SETUP 0051F020 stores that pointer and the size into the entry buffer unconditionally, then calls 003AB880,
     which returns 0 for a NULL input (null-safe)
  S  THE SETUP 00409A60 (mode 0) skips the copy when the buffer pointer is NULL (00409BC7 test / je past the copy), then
     records the source size at entry +0x40 and returns normally: no failure is reported to the caller
  Not claimed: what a later parse does with the NULL buffer (not read); whether shipped play exhausts both arenas.
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
check("A", at(dis(0x36A100, 0x36A181), {0x36A11F: "call 0x36bc60", 0x36A129: "test rax, rax", 0x36A12C: "jne 0x36a156",
                                       0x36A149: "call 0x36bfe0", 0x36A151: "test rax, rax", 0x36A154: "je 0x36a171",
                                       0x36A16A: "mov rax, rbx"}), "allocator: arena, fallback, else NULL")
check("T", at(dis(0x3AB8B0, 0x3AB907), {0x3AB8C3: "mov edx, 6", 0x3AB8E7: "call 0x36a100", 0x3AB8EC: "mov rdi, rax", 0x3AB8F9: "mov rax, rdi"}),
      "wrapper: arena 6, mode 0 returns the allocator's result")
check("C", at(dis(0x51F020, 0x51F06B), {0x51F03C: "call 0x3ab8b0", 0x51F044: "mov qword ptr [rdi + 8], rax", 0x51F048: "mov dword ptr [rdi + 0x10], esi",
                                       0x51F04B: "call 0x3ab880"})
      and at(dis(0x3AB880, 0x3AB88B), {0x3AB883: "test rcx, rcx", 0x3AB886: "jne 0x3ab88b", 0x3AB888: "xor eax, eax"}),
      "copy setup stores the result unconditionally; the follow-up call is null-safe")
check("S", at(dis(0x409BA4, 0x409BFF), {0x409BB9: "call 0x51f020", 0x409BC2: "call 0x6b5c70", 0x409BC7: "test rax, rax",
                                       0x409BCA: "je 0x409bdc", 0x409BD7: "call 0x51ef90", 0x409BF1: "mov dword ptr [r14 + 0x40], eax",
                                       0x409BFE: "ret"})
      and dis(0x6B5C70, 0x6B5C75).get(0x6B5C70) == "mov rax, qword ptr [rcx + 8]",
      "setup: NULL buffer -> copy skipped, size recorded, normal return")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
