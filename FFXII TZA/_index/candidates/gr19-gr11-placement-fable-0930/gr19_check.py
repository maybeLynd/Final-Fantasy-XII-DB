"""gr19_check.py - FABLE's controls for GR-19 (the defeat body's drop gate is the shared placement test) and GR-11's first
question (camera context 0 installs the outgoing leader's movement-body placement record). Capstone decodes of the
shipping image; PASS/FAIL per check, then FAILS n.

The load-bearing facts:
 R1  003377C0 calls 00314EB0 with rdx = the gathered actor: rdx is loaded at 0033790D and no instruction between it and
     the call at 00337956 writes rdx (the check walks every instruction in between, both paths, with capstone's
     register-write sets). Positive control: the same walk from 0033790D to 0033796F must see the explicit
     `mov rdx, ...` at 0033795F (so the walk does detect rdx writes).
 R2  after the loop, a nonzero esi AND a nonzero edi both return 0 (0033798D..0033799C).
 R3  00337700: LQUERY 00391410 must return 0, 00384130 must not return 0xFF, 00336390 must return nonzero.
 R4  00336390 calls the point query 0032A6A0 five times (centre + four corners).
 R5  0025A180 takes [[rcx+0xC0]+0x138] and copies from +0x30 into context +0x7A0.
"""
import os, struct, sys
import capstone
from capstone import x86

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000
data = open(EXE, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]; optsz = struct.unpack_from("<H", data, pe + 20)[0]
secs = [struct.unpack_from("<IIII", data, pe + 24 + optsz + 40 * i + 8) for i in range(nsec)]
def off(a):
    r = a - BASE
    for vsz, va, rsz, raw in secs:
        if va <= r < va + max(vsz, rsz): return raw + r - va
    raise ValueError(hex(a))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
def body(a, n): return list(md.disasm(data[off(a):off(a) + n], a))
def txt(i): return ("%s %s" % (i.mnemonic, i.op_str)).strip()
fails = 0
def check(name, ok, got=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, got)); fails += 0 if ok else 1

F = body(0x3377C0, 565)
at = {i.address: i for i in F}
RDX = {x86.X86_REG_RDX, x86.X86_REG_EDX, x86.X86_REG_DX, x86.X86_REG_DL, x86.X86_REG_DH}
def writes_rdx(i):
    _, w = i.regs_access()
    return bool(RDX & set(w)) or i.mnemonic == "call"   # a call clobbers rdx (Win64 volatile)
def rdx_writers(lo, hi):
    return ["%08X %s" % (i.address, txt(i)) for i in F if lo < i.address < hi and writes_rdx(i)]
check("R1 0033790D loads rdx from the gathered list", txt(at[0x33790D]).startswith("mov rdx, qword ptr [rsp + rbx*8 + 0x80]"), txt(at[0x33790D]))
check("R1 00337956 call 00314EB0", txt(at[0x337956]) == "call 0x314eb0")
w = rdx_writers(0x33790D, 0x337956)
check("R1 no rdx write between 0033790D and 00337956", w == [], str(w))
w2 = rdx_writers(0x33790D, 0x33796F)
check("R1 control: the walk sees the rdx writes before 0033796F", any(s.startswith("0033795F") for s in w2), str(w2))
seq = [txt(at[a]) for a in (0x33798D, 0x33798F, 0x337991, 0x337993, 0x337995, 0x337998, 0x33799A)]
check("R2 esi or edi nonzero -> return 0", seq == ["test esi, esi", "jne 0x33799a", "neg edi", "sbb eax, eax",
      "and eax, 2", "je 0x33799e", "xor eax, eax"], str(seq))
G = {i.address: txt(i) for i in body(0x337700, 184)}
check("R3 LQUERY 00391410 then jne refuse", G.get(0x33774C) == "call 0x391410" and G.get(0x337753) == "jne 0x337724")
check("R3 00384130 then 0xFF refuses", G.get(0x33776F) == "call 0x384130" and G.get(0x337774) == "cmp eax, 0xff" and G.get(0x337779) == "je 0x337724")
check("R3 00336390 with max(f0,f1) and unit +0x1F4", G.get(0x337784) == "maxss xmm1, dword ptr [rsp + 0x24]"
      and G.get(0x33778A) == "movzx r8d, byte ptr [rdi + 0x1f4]" and G.get(0x337792) == "call 0x336390")
Q = [i for i in body(0x336390, 315) if txt(i) == "call 0x32a6a0"]
check("R4 00336390 calls 0032A6A0 five times", len(Q) == 5, str(len(Q)))
C = {i.address: txt(i) for i in body(0x25A180, 0x70)}
check("R5 [rcx+0xC0]", C.get(0x25A1A2) == "mov rax, qword ptr [rcx + 0xc0]")
check("R5 [+0x138]", C.get(0x25A1B2) == "mov rax, qword ptr [rax + 0x138]")
check("R5 copy from +0x30 to context +0x7A0", C.get(0x25A1C2) == "movups xmm0, xmmword ptr [rax + 0x30]"
      and C.get(0x25A1C6) == "lea r8, [rbx + 0x7a0]" and C.get(0x25A1DC) == "movups xmmword ptr [r8], xmm0")
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
