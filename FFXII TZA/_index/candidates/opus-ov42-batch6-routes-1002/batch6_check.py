"""batch6_check.py - the byte facts OPUS re-read before consuming FABLE's routed OV-42 batch-6 text (OPUS, 2026-10-02).
Rejecting regression over the shipping image through retool.py: every check names an instruction at fn + off and the
text it must hold; a patched image or a moved site fails it. Last line 'FAILS n'."""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool  # noqa: E402

R = retool.R
fails = 0


def ins(fn, off):
    a = fn + off
    i = next(R.md.disasm(R.at(a, 16), a), None)
    return "" if i is None else ("%s %s" % (i.mnemonic, i.op_str)).replace("  ", " ")


def check(fn, off, want, what):
    global fails
    got = ins(fn, off)
    ok = all(w in got for w in want)
    print("%s  %08X + 0x%X  %-44s %s" % ("PASS" if ok else "FAIL", fn, off, got, what))
    fails += 0 if ok else 1


# the section binder 003845F0 and its two width helpers
check(0x3845F0, 0x04, ["mov qword ptr [rcx], rdx"], "*slot = desc before the null test")
check(0x3845F0, 0x10, ["mov eax, dword ptr [rdx + 0xc]"], "+0x0C through RDX")
check(0x3845F0, 0x21, ["mov r8, qword ptr [rcx]"], "+0x10 through a reload of *slot")
check(0x3845F0, 0x62, ["add eax, edx"], "+0x14 rebased: M = low32(x + low32(desc))")
check(0x3845F0, 0x6B, ["mov ebp, eax"], "EBP = M")
check(0x3845F0, 0x6D, ["call 0x20e620"], "M encoded by 0020E620")
check(0x3845F0, 0x72, ["mov dword ptr [rdi + 0x14], eax"], "the ENCODED DWORD stored back")
check(0x3845F0, 0x75, ["test rbp, rbp"], "sub-directory only when M != 0")
check(0x3845F0, 0x90, ["call 0x20e600"], "sub-directory reached through the decoder")
check(0x3845F0, 0xB9, ["add edx, ebp"], "child argument entry + M")
check(0x3845F0, 0xC9, ["add dword ptr [rbx], ebp"], "last entry rebased in place by M")
check(0x20E620, 0x00, ["sub ecx, dword ptr [rip + 0x1d74f0a]"], "encoder: minus the low DWORD of 01F83530")
check(0x20E600, 0x00, ["mov eax, ecx"], "decoder: zero-extend")
check(0x20E600, 0x02, ["add rax, qword ptr [rip + 0x1d74f27]"], "decoder: plus the full QWORD 01F83530")
check(0x237FC0, 0x0F, ["movsxd rdx, ecx"], "caller: RDX = incoming ECX sign-extended")
check(0x237FC0, 0x15, ["lea rcx, [rip + 0x2c8715c]"], "caller: RCX = &02EBF138")
# forward readers (multiply)
check(0x304850, 0x3D, ["movzx r13d, word ptr [rsi + 0x64]"], "id latched (rsi = unit + 0x6B0, so unit + 0x714)")
check(0x304850, 0x58, ["mov ebx, 0x21e"], "the 542 bound")
check(0x304850, 0x8E, ["cmp r13w, bx"], "entry guard")
check(0x304850, 0x92, ["ja "], "unsigned: above 0x21E leaves")
check(0x304850, 0xB3, ["dword ptr [rax + 0xc]"], "+0x0C key")
check(0x304850, 0xC7, ["dword ptr [rax + 0xc]"], "+0x0C key, second lookup")
check(0x304850, 0xD9, ["movzx ecx, word ptr [rax + 8]"], "+0x08 stride")
check(0x304850, 0xE1, ["imul ecx, eax"], "id * stride")
check(0x304850, 0xE4, ["add r15d, ecx"], "32-bit add into the row register")
check(0x30D160, 0x27, ["movzx edi, dx"], "the word is the incoming DX")
check(0x30D160, 0x59, ["dword ptr [rax + 0xc]"], "+0x0C key")
check(0x30D160, 0x6D, ["dword ptr [rax + 0xc]"], "+0x0C key, second lookup")
check(0x30D160, 0x7F, ["movzx ecx, word ptr [rax + 8]"], "+0x08 stride")
check(0x30D160, 0x89, ["add esi, ecx"], "32-bit add into RSI")
check(0x305430, 0x16, ["mov eax, 0x115"], "bound 0x115")
check(0x305430, 0x23, ["cmp dx, ax"], "16-bit compare")
for o in (0x31, 0x46, 0x79, 0x8E, 0x162, 0x177):
    check(0x305430, o, ["dword ptr [", " + 0xc]"], "+0x0C key")
for o in (0x58, 0xA0, 0x186):
    check(0x305430, o, ["movzx", "word ptr [", " + 8]"], "+0x08 stride")
# inverse readers 4 and 5 (00305640) and the helper's widths
check(0x305640, 0x2E, ["dword ptr [rax + 0xc]"], "+0x0C key")
check(0x305640, 0x4B, ["movzx r10d, word ptr [r9 + 8]"], "+0x08 stride")
check(0x305640, 0x50, ["div r10d"], "unsigned 32-bit divide")
check(0x305640, 0x128, ["dword ptr [rax + 0xc]"], "+0x0C key")
check(0x305640, 0x13C, ["movzx ecx, word ptr [rax + 8]"], "+0x08 stride")
check(0x305640, 0x143, ["div ecx"], "unsigned 32-bit divide")
check(0x305640, 0x73, ["mov dword ptr [rbp + 0xe58], r15d"], "own write unit +0xE58")
check(0x305640, 0x7A, ["mov word ptr [rbp + 0xdc8], ax"], "own write unit +0xDC8")
check(0x305640, 0x81, ["movzx edx, di"], "q mod 65536 to the first comparator")
check(0x305640, 0x8C, ["movzx edx, di"], "q mod 65536 to the second comparator")
check(0x305640, 0x99, ["mov rcx, qword ptr [rbp + 0x698]"], "unit +0x698 read")
check(0x305640, 0xA3, ["test r12d, r12d"], "mode flag tested")
check(0x305640, 0xA8, ["setne sil"], "mode normalised to 0 / 1")
check(0x305640, 0xC4, ["movsx edx, word ptr [rcx + 0x28]"], "record WORD +0x28")
check(0x305640, 0x14A, ["mov edx, eax"], "full 32-bit q passed on")
# the eligibility masks' global half and the settings root
check(0x30B770, 0x0F, ["mov ecx, dword ptr [rip + 0x1d7dbbb]"], "global mask reads 02089340")
check(0x30B770, 0x15, ["mov dword ptr [rbp], 0"], "result DWORD zeroed")
check(0x30B770, 0x1C, ["test ecx, 0x3080"], "mask 0x3080")
check(0x17D470, 0x09, ["mov eax, dword ptr [rax + 0xc20]"], "setting getter reads +0xC20")
check(0x1D50D0, 0x0D, ["mov rax, qword ptr [rip + 0x1dac344]"], "accessor root 01F81428")
check(0x1D50D0, 0x19, ["mov ecx, 0x10e8"], "lazy allocation 0x10E8")
check(0x1D50D0, 0x30, ["call 0x1ccb20"], "constructor 001CCB20")
print("FAILS %d" % fails)
