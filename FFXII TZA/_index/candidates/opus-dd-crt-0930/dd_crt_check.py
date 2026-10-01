"""dd_crt_check.py - OPUS DD content work on the two ordered-container pages (2026-09-30): the MSVC std::_Tree node's
allocation and construction, read from the certified image, for the _types row MsvcTreeNodeHeader and the MSVC page.
Static, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def callers(a):
    return sorted(set(f for f, s in c["calls"].get(a, ())))


# A1 - the three node allocators (MSVC _Buynode0): each asks 00210EC0 (the image's jmp-malloc wrapper, r8d = -1, edx = 0,
#      tail jump 0085E730) for the node size, calls a throw import on null, and points _Left, _Parent and _Right at the
#      tree's head [rcx]; 00714860 / 00714920 allocate 0x30, 0071F180 allocates 0x60
ok = txt(0x00210EC0) == "or r8d, 0xffffffff" and txt(0x00210EC6) == "jmp 0x85e730"
for a, size in ((0x00714860, 0x30), (0x00714920, 0x30), (0x0071F180, 0x60)):
    ok &= SZ.get(a) == 93 and txt(a + 0x12) == "mov ecx, 0x%x" % size and txt(a + 0x17) == "call 0x210ec0" \
        and txt(a + 0x29).startswith("call qword ptr [rip") and txt(a + 0x33) == "mov qword ptr [rdx], rax" \
        and txt(a + 0x42) == "mov qword ptr [rcx], rax" and txt(a + 0x51) == "mov qword ptr [rcx], rax" \
        and txt(a + 0x36) == "lea rcx, [rdx + 8]" and txt(a + 0x45) == "lea rcx, [rdx + 0x10]"
check("A1", ok, "_Buynode0: 00714860 / 00714920 -> 0x30, 0071F180 -> 0x60 from 00210EC0; all three links = the head")
# A2 - the value constructors (MSVC _Buynode): 00712E60 (one caller, 006F1F60 = the +0xC8 cache's create path) calls
#      00714860, zeroes the word at +0x18 (_Color red and _Isnil 0) and copies a 16-byte key/value pair to +0x20 / +0x28;
#      0071E340 (one caller 0071F000) calls 0071F180, zeroes +0x18 and initialises two MSVC strings, filling +0x20 from the caller's key (001A4C90, [r8], 0071E39F) and leaving +0x40 empty
#      (narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's dd-crt review)
#      (capacity 15, size 0, buffer[0] = 0) - the pair<string, string> MT-1 names for instantiation B
check("A2", callers(0x00714860) == [0x00712E60] and callers(0x00712E60) == [0x006F1F60]
      and txt(0x00712E72) == "call 0x714860" and txt(0x00712E7C) == "mov word ptr [rax + 0x18], 0"
      and txt(0x00712E82) == "lea r8, [rax + 0x20]" and txt(0x00712E8E) == "mov qword ptr [r8], rcx" and txt(0x00712E95) == "mov qword ptr [r8 + 8], rcx"
      and callers(0x0071F180) == [0x0071E340, 0x0071E3E0] and callers(0x0071E340) == [0x0071F000]
      and txt(0x0071E360) == "call 0x71f180" and txt(0x0071E36D) == "mov word ptr [rax + 0x18], 0"
      and txt(0x0071E37F) == "mov qword ptr [rbx + 0x18], 0xf" and txt(0x0071E3A7) == "add rbx, 0x20" and txt(0x0071E3AB) == "mov qword ptr [rbx + 0x18], 0xf",
      "_Buynode: colour/_Isnil word zeroed, value built at +0x20 (a 16-byte pair; two strings for B)")
# A3 - the second 0x30 allocator 00714920 has its own single caller 00712F20, and the second 0x60 caller 0071E3E0 calls
#      0071F180 too: two value-constructor variants per node size
check("A3", callers(0x00714920) == [0x00712F20] and txt(0x00712F32) == "call 0x714920",
      "a second 0x30 constructor path 00712F20 -> 00714920")
print("FAILS %d" % fails)
