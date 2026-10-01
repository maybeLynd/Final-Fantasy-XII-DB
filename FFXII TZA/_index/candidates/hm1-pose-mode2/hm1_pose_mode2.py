"""HM-1 narrowing control (OPUS, 2026-09-27): what 'pose mode 2' is and where the second skeleton comes from.

P1  003703A0 takes the mapped (second-skeleton) path only when [record+0x6C8] == 2 AND [record+0x6D0] != 0 AND
    [skeleton+0xB0] != -1 (00370634 / 0037063D / 00370647).
P2  [record+0x6C8] is the five-state pair-binding machine of 002EDF90 (the add-motion page, section 3): requests
    1/2 set states 1/2 from 0, request 0 releases 1 -> 3 and 2 -> 4; state 2 is the record that carries the binding.
P3  [record+0x6D0] is built in 003703A0 itself: a (joint count x 4)-byte buffer from 0019C580, memset to -1
    (00370592), then 0017EF60(this record's +0x6B8, other record's +0x6B8, buffer) (003705AC).
P4  the other record is the render record whose index is the u16 at +0xA8 of the object [skeleton+0xC] resolves to
    (00370524); -1 selects none (00370531) and an inactive record (+0x284 == 0) selects none (0037054F cmove).
Mutant M1: a reading that takes the mapped path on state 1 is rejected by P1's immediate.
"""
import hashlib, pathlib
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE.parents[3] / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, n): o = pe.get_offset_from_rva(a - IB); return {i.address: (i.mnemonic, i.op_str) for i in md.disasm(raw[o:o + n], a)}
S = ins(0x3703A0, 0x500)
assert S[0x370634] == ("cmp", "dword ptr [rsi + 0x6c8], 2")                                  # P1 (and M1: not 1)
assert S[0x37063D] == ("cmp", "qword ptr [rsi + 0x6d0], 0")
assert S[0x370647] == ("cmp", "dword ptr [r14 + 0xb0], -1")
assert S[0x370579] == ("mov", "qword ptr [rsi + 0x6d0], rax") and S[0x370592] == ("call", "0x861ec0")   # P3
assert S[0x370580] == ("or", "edx, 0xffffffff") and S[0x3705AC] == ("call", "0x17ef60")
assert S[0x37059E] == ("mov", "rdx, qword ptr [rbx + 0x6b8]") and S[0x3705A5] == ("mov", "rcx, qword ptr [rsi + 0x6b8]")
assert S[0x370524] == ("movzx", "ecx, word ptr [rax + 0xa8]") and S[0x370531] == ("mov", "rbx, rdi")   # P4
assert S[0x37054F] == ("cmove", "rbx, rdi") and S[0x370548] == ("cmp", "dword ptr [rbx + 0x284], 0")
B = ins(0x2EDF90, 179)                                                                         # P2
assert B[0x2EDFCE] == ("mov", "dword ptr [rcx + 0x6c8], edx") and B[0x2EDFD4] == ("cmp", "edx, 2")
assert B[0x2EDFF9] == ("mov", "dword ptr [rcx + 0x6c8], 3") and B[0x2EE00C] == ("mov", "dword ptr [rcx + 0x6c8], 4")
assert B[0x2EE025] == ("mov", "dword ptr [rcx + 0x6c8], 1") and B[0x2EE038] == ("mov", "dword ptr [rcx + 0x6c8], 2")
print("PASS")
